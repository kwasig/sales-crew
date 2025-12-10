# Unified API for Sales Crew - combines lead generation and financial analysis

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

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Import services
from services.user_prompt_extractor_service import UserPromptExtractor
from services.financial_analysis_service import FinancialAnalysisService
from agent.lead_generation_crew import ResearchCrew

# Create a global ThreadPoolExecutor for CPU-heavy tasks
executor = ThreadPoolExecutor(max_workers=2)

class QueryRequest(BaseModel):
    prompt: str

class FinancialAnalysisRequest(BaseModel):
    company_name: str = None
    industry: str = None
    product: str = None
    max_results: int = 15

class UnifiedAPI:
    def __init__(self):
        self.app = FastAPI(
            title="Sales Crew Unified API",
            description="Unified API for lead generation and financial analysis",
            version="1.0.0"
        )
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
        @self.app.get("/")
        async def root():
            return {
                "message": "Sales Crew Unified API",
                "endpoints": {
                    "lead_generation": "/generate-leads",
                    "financial_analysis": "/financial-analysis",
                    "health": "/health"
                }
            }

        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy", 
                "service": "Sales Crew Unified API",
                "endpoints": {
                    "lead_generation": "active",
                    "financial_analysis": "active"
                }
            }

        @self.app.post("/generate-leads")
        async def generate_leads(request: Request, background_tasks: BackgroundTasks):
            # Extract API keys from headers
            sambanova_key = request.headers.get("x-sambanova-key")
            exa_key = request.headers.get("x-exa-key")

            if not sambanova_key or not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required API keys. Please provide both x-sambanova-key and x-exa-key headers."}
                )

            try:
                # Get request body
                body = await request.json()
                prompt = body.get("prompt", "")

                if not prompt:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Missing prompt in request body"}
                    )

                # Initialize services with API keys
                extractor = UserPromptExtractor(sambanova_key)
                extracted_info = extractor.extract_lead_info(prompt)

                # Initialize crew with API keys
                crew = ResearchCrew(sambanova_key=sambanova_key, exa_key=exa_key)

                # Offload CPU-bound or time-consuming "execute_research" call 
                # to a separate thread so it doesn't block the async event loop.
                loop = asyncio.get_running_loop()
                future = executor.submit(crew.execute_research, extracted_info)
                result = await loop.run_in_executor(None, future.result)

                # Parse result and return
                parsed_result = json.loads(result)
                outreach_list = parsed_result.get("outreach_list", [])
                return JSONResponse(content=outreach_list)

            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Invalid JSON response from research crew"}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Lead generation failed: {str(e)}"}
                )

        @self.app.post("/financial-analysis")
        async def financial_analysis(request: Request, background_tasks: BackgroundTasks):
            # Extract API key from headers
            exa_key = request.headers.get("x-exa-key")

            if not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required Exa API key. Please provide x-exa-key header."}
                )

            try:
                # Get request body
                body = await request.json()
                company_name = body.get("company_name")
                industry = body.get("industry")
                product = body.get("product")
                max_results = body.get("max_results", 15)

                # Initialize service with API key
                service = FinancialAnalysisService()
                service.api_key = exa_key

                # Offload CPU-bound analysis to a separate thread
                loop = asyncio.get_running_loop()
                future = executor.submit(
                    service.get_financial_analysis,
                    company_name=company_name,
                    industry=industry,
                    product=product,
                    max_results=max_results
                )
                result = await loop.run_in_executor(None, future.result)

                return JSONResponse(content=result)

            except json.JSONDecodeError:
                return JSONResponse(
                    status_code=500,
                    content={"error": "Invalid JSON in request body"}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Financial analysis failed: {str(e)}"}
                )

def create_app():
    api = UnifiedAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8000)