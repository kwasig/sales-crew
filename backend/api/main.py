# file: api/main.py

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import API routers
from .financial_analysis_api import FinancialAnalysisAPI
from .lead_generation_api import LeadGenerationAPI
from .usage_dashboard_api import router as usage_router

# Create main FastAPI app
app = FastAPI(title="Sales Crew API", version="1.0.0")

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*", "x-sambanova-key", "x-exa-key"],
)

# Create and mount API instances
financial_api = FinancialAnalysisAPI()
lead_api = LeadGenerationAPI()

# Mount the apps
app.mount("/financial", financial_api.app)
app.mount("/leads", lead_api.app)
app.include_router(usage_router, prefix="/api")

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy", 
        "service": "Sales Crew API",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Sales Crew API",
        "endpoints": {
            "financial_analysis": "/financial/",
            "lead_generation": "/leads/",
            "usage_dashboard": "/api/usage/",
            "health": "/health"
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)