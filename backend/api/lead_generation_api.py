# lead_generation_api.py

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
import json
import uvicorn
import sys
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import uuid


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Services, Tools, etc.
from services.user_prompt_extractor_service import UserPromptExtractor
from agent.lead_generation_crew import ResearchCrew
from utils.langfuse_integration import LangfuseIntegration

# Create a global ThreadPoolExecutor if you want concurrency in a single worker
# for CPU-heavy tasks (Pick a reasonable max_workers based on your environment).
executor = ThreadPoolExecutor(max_workers=2)

class QueryRequest(BaseModel):
    prompt: str

class LeadGenerationAPI:
    def __init__(self):
        self.app = FastAPI()
        self.langfuse = LangfuseIntegration()
        self.setup_cors()
        self.setup_routes()

    def setup_cors(self):
        # Get allowed origins from environment variable or use default
        allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
        
        # If no specific origins are set, default to allowing all
        if not allowed_origins or (len(allowed_origins) == 1 and allowed_origins[0] == '*'):
            allowed_origins = ["*"]
        else:
            # Add localhost for development
            allowed_origins.extend(["http://localhost:5173", "http://localhost:5174"])

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*", "x-sambanova-key", "x-exa-key"],
        )
        

    def setup_routes(self):
        @self.app.post("/generate-leads")
        async def generate_leads(request: Request, background_tasks: BackgroundTasks):
            # Extract API keys from headers
            sambanova_key = request.headers.get("x-sambanova-key")
            exa_key = request.headers.get("x-exa-key")
            user_id = request.headers.get("x-user-id", str(uuid.uuid4()))

            if not sambanova_key or not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required API keys"}
                )

            # Create Langfuse trace for API request
            trace_id = self.langfuse.create_trace(
                name="api_generate_leads",
                user_id=user_id,
                metadata={
                    "endpoint": "/generate-leads",
                    "method": "POST",
                    "timestamp": time.time()
                }
            )

            try:
                # Get request body
                body = await request.json()
                prompt = body.get("prompt", "")

                if not prompt:
                    # Log error to Langfuse
                    if trace_id:
                        self.langfuse.log_error(
                            trace_id=trace_id,
                            error_message="Missing prompt in request body",
                            context={"status_code": 400}
                        )
                        self.langfuse.flush()
                    
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Missing prompt in request body"}
                    )

                # Log API request start
                if trace_id:
                    self.langfuse.log_task_execution(
                        trace_id=trace_id,
                        task_name="api_request_start",
                        input_data={"prompt": prompt},
                        output_data=None,
                        metadata={"status": "started"}
                    )

                # Initialize services with API keys
                extractor = UserPromptExtractor(sambanova_key)
                extracted_info = extractor.extract_lead_info(prompt)

                # Initialize crew with API keys and user ID for Langfuse tracking
                crew = ResearchCrew(sambanova_key=sambanova_key, exa_key=exa_key, user_id=user_id)

                # Offload CPU-bound or time-consuming "execute_research" call 
                # to a separate thread so it doesn't block the async event loop.
                loop = asyncio.get_running_loop()
                future = executor.submit(crew.execute_research, extracted_info)
                result = await loop.run_in_executor(None, future.result)
                # Alternatively:
                # result = await loop.run_in_executor(executor, crew.execute_research, extracted_info)

                # Parse result and return
                parsed_result = json.loads(result)
                outreach_list = parsed_result.get("outreach_list", [])

                # Log successful API completion
                if trace_id:
                    self.langfuse.log_task_execution(
                        trace_id=trace_id,
                        task_name="api_request_complete",
                        input_data={"prompt": prompt},
                        output_data={"results_count": len(outreach_list)},
                        metadata={"status": "completed", "results_count": len(outreach_list)}
                    )
                    self.langfuse.flush()

                return JSONResponse(content=outreach_list)

            except json.JSONDecodeError as e:
                # Log JSON error to Langfuse
                if trace_id:
                    self.langfuse.log_error(
                        trace_id=trace_id,
                        error_message="Invalid JSON response from research crew",
                        context={"error": str(e), "status_code": 500}
                    )
                    self.langfuse.flush()
                
                return JSONResponse(
                    status_code=500,
                    content={"error": "Invalid JSON response from research crew"}
                )
            except Exception as e:
                # Log general error to Langfuse
                if trace_id:
                    self.langfuse.log_error(
                        trace_id=trace_id,
                        error_message=str(e),
                        context={
                            "error_type": type(e).__name__,
                            "status_code": 500,
                            "timestamp": time.time()
                        }
                    )
                    self.langfuse.flush()
                
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

def create_app():
    api = LeadGenerationAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)
