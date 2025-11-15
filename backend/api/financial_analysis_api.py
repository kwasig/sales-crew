# file: api/financial_analysis_api.py

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

from services.financial_analysis_service import FinancialAnalysisService

# Create a global ThreadPoolExecutor for CPU-heavy tasks
executor = ThreadPoolExecutor(max_workers=2)

class FinancialAnalysisRequest(BaseModel):
    company_name: str = None
    industry: str = None
    product: str = None
    max_results: int = 15

class FinancialAnalysisAPI:
    def __init__(self):
        self.app = FastAPI()
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
            allow_headers=["*", "x-exa-key"],
        )
        

    def setup_routes(self):
        @self.app.post("/financial-analysis")
        async def financial_analysis(request: Request, background_tasks: BackgroundTasks):
            # Extract API key from headers
            exa_key = request.headers.get("x-exa-key")

            if not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required Exa API key"}
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
                    content={"error": str(e)}
                )

        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "Financial Analysis API"}

def create_app():
    api = FinancialAnalysisAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8001)