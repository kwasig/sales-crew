import os
from typing import Optional, Dict, Any
from dotenv import load_dotenv
from langfuse import Langfuse

class LangfuseManager:
    """
    Singleton manager for Langfuse client to ensure proper initialization
    and avoid multiple client instances.
    """
    _instance = None
    _langfuse = None
    _env_loaded = False
    
    def __new__(cls):
        """Singleton implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Langfuse client from environment variables"""
        if not self._env_loaded:
            load_dotenv()
            self._env_loaded = True
        
        public_key = os.getenv("LANGFUSE_PUBLIC_KEY")
        secret_key = os.getenv("LANGFUSE_SECRET_KEY")
        host = os.getenv("LANGFUSE_HOST", "https://cloud.langfuse.com")
        enabled = os.getenv("LANGFUSE_ENABLED", "true").lower() == "true"
        
        if not enabled:
            print("Info: Langfuse is disabled via LANGFUSE_ENABLED=false")
            self._langfuse = None
            return
        
        if not public_key or not secret_key:
            print("Warning: Langfuse credentials not found. Tracing disabled.")
            print("Set LANGFUSE_PUBLIC_KEY and LANGFUSE_SECRET_KEY to enable tracing.")
            self._langfuse = None
            return
        
        try:
            self._langfuse = Langfuse(
                public_key=public_key,
                secret_key=secret_key,
                host=host
            )
            print(f"Info: Langfuse initialized successfully (host: {host})")
        except Exception as e:
            print(f"Warning: Failed to initialize Langfuse: {e}")
            self._langfuse = None
    
    @property
    def client(self) -> Optional[Langfuse]:
        """Get the Langfuse client instance"""
        return self._langfuse
    
    @property
    def is_enabled(self) -> bool:
        """Check if Langfuse is enabled and initialized"""
        return self._langfuse is not None
    
    def flush(self):
        """Flush events to Langfuse"""
        if self._langfuse:
            try:
                self._langfuse.flush()
            except Exception as e:
                print(f"Warning: Failed to flush Langfuse events: {e}")
    
    def shutdown(self):
        """Shutdown Langfuse client"""
        if self._langfuse:
            try:
                self._langfuse.flush()
                self._langfuse.shutdown()
            except Exception as e:
                print(f"Warning: Error during Langfuse shutdown: {e}")

# Global instance
langfuse_manager = LangfuseManager()

# Convenience function for getting the client
def get_langfuse_client() -> Optional[Langfuse]:
    """Get the global Langfuse client instance"""
    return langfuse_manager.client

# Decorator for easy function tracing
def trace_function(name: str, as_type: str = "span"):
    """
    Decorator to trace a function with Langfuse
    
    Args:
        name: Name of the trace/span
        as_type: Type of observation ("span", "generation", "event")
    """
    def decorator(func):
        if not langfuse_manager.is_enabled:
            return func
        
        from langfuse.decorators import observe
        return observe(name=name, as_type=as_type)(func)
    
    return decorator