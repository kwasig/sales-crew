import os
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
from uuid import uuid4
from langfuse import Langfuse
from utils.envutils import EnvUtils


class LangfuseIntegration:
    """
    Langfuse integration for CrewAI agents to track and log agent executions
    """
    _instance = None
    _langfuse_client = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LangfuseIntegration, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._langfuse_client is None:
            self._initialize_langfuse()
    
    def _initialize_langfuse(self) -> None:
        """Initialize Langfuse client with environment variables"""
        env_utils = EnvUtils()
        
        langfuse_public_key = env_utils.get_env('LANGFUSE_PUBLIC_KEY')
        langfuse_secret_key = env_utils.get_env('LANGFUSE_SECRET_KEY')
        langfuse_host = env_utils.get_env('LANGFUSE_HOST', 'https://cloud.langfuse.com')
        
        if langfuse_public_key and langfuse_secret_key:
            try:
                self._langfuse_client = Langfuse(
                    public_key=langfuse_public_key,
                    secret_key=langfuse_secret_key,
                    host=langfuse_host
                )
                print("Langfuse client initialized successfully")
            except Exception as e:
                print(f"Failed to initialize Langfuse client: {e}")
                self._langfuse_client = None
        else:
            print("Langfuse credentials not found, running without Langfuse tracking")
            self._langfuse_client = None
    
    def is_enabled(self) -> bool:
        """Check if Langfuse tracking is enabled"""
        return self._langfuse_client is not None
    
    def create_trace(self, 
                    name: str, 
                    user_id: Optional[str] = None, 
                    metadata: Optional[Dict[str, Any]] = None) -> Optional[str]:
        """Create a new trace for a complete research execution"""
        if not self.is_enabled():
            return None
        
        try:
            trace_id = str(uuid4())
            trace = self._langfuse_client.trace(
                id=trace_id,
                name=name,
                userId=user_id,
                metadata=metadata or {}
            )
            return trace_id
        except Exception as e:
            print(f"Failed to create Langfuse trace: {e}")
            return None
    
    def log_agent_execution(self, 
                          trace_id: str, 
                          agent_name: str, 
                          input_data: Dict[str, Any], 
                          output_data: Any, 
                          metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log an agent execution as a generation"""
        if not self.is_enabled() or not trace_id:
            return
        
        try:
            generation = self._langfuse_client.generation(
                trace_id=trace_id,
                name=f"agent_{agent_name}",
                input=input_data,
                output=output_data,
                metadata={
                    'agent_name': agent_name,
                    'timestamp': datetime.now().isoformat(),
                    **(metadata or {})
                }
            )
            generation.end()
        except Exception as e:
            print(f"Failed to log agent execution to Langfuse: {e}")
    
    def log_task_execution(self, 
                         trace_id: str, 
                         task_name: str, 
                         input_data: Dict[str, Any], 
                         output_data: Any, 
                         metadata: Optional[Dict[str, Any]] = None) -> None:
        """Log a task execution as a span"""
        if not self.is_enabled() or not trace_id:
            return
        
        try:
            span = self._langfuse_client.span(
                trace_id=trace_id,
                name=f"task_{task_name}",
                input=input_data,
                output=output_data,
                metadata={
                    'task_name': task_name,
                    'timestamp': datetime.now().isoformat(),
                    **(metadata or {})
                }
            )
            span.end()
        except Exception as e:
            print(f"Failed to log task execution to Langfuse: {e}")
    
    def log_error(self, 
                 trace_id: str, 
                 error_message: str, 
                 context: Optional[Dict[str, Any]] = None) -> None:
        """Log an error to Langfuse"""
        if not self.is_enabled() or not trace_id:
            return
        
        try:
            self._langfuse_client.score(
                trace_id=trace_id,
                name="error_occurred",
                value=1,
                comment=error_message,
                metadata=context or {}
            )
        except Exception as e:
            print(f"Failed to log error to Langfuse: {e}")
    
    def flush(self) -> None:
        """Flush any pending Langfuse events"""
        if self.is_enabled():
            try:
                self._langfuse_client.flush()
            except Exception as e:
                print(f"Failed to flush Langfuse events: {e}")


def main():
    """Test the Langfuse integration"""
    langfuse = LangfuseIntegration()
    
    if langfuse.is_enabled():
        print("Langfuse integration is enabled")
        
        # Create a test trace
        trace_id = langfuse.create_trace(
            name="test_research_execution",
            user_id="test_user",
            metadata={"environment": "test"}
        )
        
        if trace_id:
            # Log a test agent execution
            langfuse.log_agent_execution(
                trace_id=trace_id,
                agent_name="test_agent",
                input_data={"query": "test query"},
                output_data={"result": "test result"}
            )
            
            # Log a test task execution
            langfuse.log_task_execution(
                trace_id=trace_id,
                task_name="test_task",
                input_data={"input": "test input"},
                output_data={"output": "test output"}
            )
            
            langfuse.flush()
            print(f"Test trace created with ID: {trace_id}")
        else:
            print("Failed to create test trace")
    else:
        print("Langfuse integration is not enabled (missing credentials)")


if __name__ == "__main__":
    main()