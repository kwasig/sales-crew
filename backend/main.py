"""
Main FastAPI application for Sales Crew
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Import routers
from api.lead_generation_api import router as lead_generation_router
from api.financial_analysis_api import router as financial_analysis_router
from api.dashboard_api import router as dashboard_router

app = FastAPI(
    title="Sales Crew API",
    description="AI-powered sales lead generation and financial analysis platform",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(lead_generation_router)
app.include_router(financial_analysis_router)
app.include_router(dashboard_router)

@app.get("/")
async def root():
    return {
        "message": "Sales Crew API is running",
        "version": "1.0.0",
        "endpoints": {
            "lead_generation": "/generate-leads",
            "financial_analysis": "/financial-analysis",
            "dashboard": "/dashboard"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "Sales Crew API"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )