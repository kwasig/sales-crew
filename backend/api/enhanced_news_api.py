# file: api/enhanced_news_api.py

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

from services.enhanced_news_service import EnhancedNewsService

# Create a global ThreadPoolExecutor for CPU-heavy tasks
executor = ThreadPoolExecutor(max_workers=2)

class EnhancedNewsRequest(BaseModel):
    company_name: str = None
    industry: str = None
    product: str = None
    max_results: int = 20
    analysis_type: str = "comprehensive"  # comprehensive, sentiment, trends, risks

class NewsSearchRequest(BaseModel):
    query: str
    category: str = "news"
    max_results: int = 10
    time_range: str = "30d"  # 7d, 30d, 90d, 1y

class NewsTrendsRequest(BaseModel):
    company_name: str = None
    industry: str = None
    time_period: str = "30d"  # 7d, 30d, 90d
    trend_type: str = "sentiment"  # sentiment, topics, sources

class EnhancedNewsAPI:
    def __init__(self):
        self.app = FastAPI(title="Enhanced News Analysis API",
                          description="Comprehensive news analysis with advanced categorization, sentiment analysis, and trend detection")
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
        @self.app.post("/enhanced-news-analysis")
        async def enhanced_news_analysis(request: Request, background_tasks: BackgroundTasks):
            """
            Comprehensive enhanced news analysis endpoint
            Returns detailed analysis with categorization, sentiment, and trends
            """
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
                max_results = body.get("max_results", 20)
                analysis_type = body.get("analysis_type", "comprehensive")

                # Initialize service with API key
                service = EnhancedNewsService()
                service.api_key = exa_key

                # Offload CPU-bound analysis to a separate thread
                loop = asyncio.get_running_loop()
                future = executor.submit(
                    service.get_enhanced_news_analysis,
                    company_name=company_name,
                    industry=industry,
                    product=product,
                    max_results=max_results
                )
                result = await loop.run_in_executor(None, future.result)

                # Add analysis type metadata
                result["analysis_type"] = analysis_type
                result["api_version"] = "2.0"

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

        @self.app.post("/news-search")
        async def news_search(request: Request):
            """
            Direct news search endpoint with enhanced filtering
            """
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
                query = body.get("query")
                category = body.get("category", "news")
                max_results = body.get("max_results", 10)
                time_range = body.get("time_range", "30d")

                if not query:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Query parameter is required"}
                    )

                # Initialize service
                service = EnhancedNewsService()
                service.api_key = exa_key

                # Perform search
                news_results = service._get_enhanced_news(query, max_results=max_results)
                
                # Process results
                processed_news = service._process_news_articles(news_results)

                response = {
                    "query": query,
                    "category": category,
                    "time_range": time_range,
                    "total_results": len(processed_news),
                    "results": processed_news[:max_results]
                }

                return JSONResponse(content=response)

            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.post("/news-sentiment-analysis")
        async def news_sentiment_analysis(request: Request):
            """
            Focused sentiment analysis endpoint
            """
            # Extract API key from headers
            exa_key = request.headers.get("x-exa-key")

            if not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required Exa API key"}
                )

            try:
                body = await request.json()
                company_name = body.get("company_name")
                industry = body.get("industry")
                product = body.get("product")
                max_results = body.get("max_results", 15)

                service = EnhancedNewsService()
                service.api_key = exa_key

                # Get news analysis
                analysis = service.get_enhanced_news_analysis(
                    company_name=company_name,
                    industry=industry,
                    product=product,
                    max_results=max_results
                )

                # Extract sentiment-focused data
                sentiment_analysis = {
                    "overall_sentiment": analysis.get("market_outlook", {}).get("sentiment", "neutral"),
                    "sentiment_score": analysis.get("market_outlook", {}).get("weighted_sentiment", 0),
                    "confidence": analysis.get("market_outlook", {}).get("confidence", 50),
                    "sentiment_distribution": analysis.get("news_trends", {}).get("sentiment_distribution", {}),
                    "key_positive_articles": [article for article in analysis.get("news_analysis", {}).get("articles", []) 
                                            if article.get("sentiment", {}).get("label", "").startswith("positive")][:5],
                    "key_negative_articles": [article for article in analysis.get("news_analysis", {}).get("articles", []) 
                                            if article.get("sentiment", {}).get("label", "").startswith("negative")][:5],
                    "sentiment_trend": analysis.get("market_outlook", {}).get("trend_direction", "stable")
                }

                return JSONResponse(content=sentiment_analysis)

            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.post("/news-risk-assessment")
        async def news_risk_assessment(request: Request):
            """
            Focused risk assessment endpoint
            """
            # Extract API key from headers
            exa_key = request.headers.get("x-exa-key")

            if not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required Exa API key"}
                )

            try:
                body = await request.json()
                company_name = body.get("company_name")
                industry = body.get("industry")
                product = body.get("product")
                max_results = body.get("max_results", 15)

                service = EnhancedNewsService()
                service.api_key = exa_key

                # Get news analysis
                analysis = service.get_enhanced_news_analysis(
                    company_name=company_name,
                    industry=industry,
                    product=product,
                    max_results=max_results
                )

                # Extract risk-focused data
                risk_analysis = {
                    "risk_assessment": analysis.get("risk_assessment", []),
                    "high_risk_articles": [article for article in analysis.get("news_analysis", {}).get("articles", []) 
                                          if article.get("impact_score", 0) > 70 
                                          and article.get("sentiment", {}).get("score", 0) < -0.1][:5],
                    "risk_summary": {
                        "total_risks": len(analysis.get("risk_assessment", [])),
                        "high_priority_risks": len([risk for risk in analysis.get("risk_assessment", []) 
                                                   if risk.get("severity") == "high"]),
                        "average_risk_probability": sum(risk.get("probability", 0) for risk in analysis.get("risk_assessment", [])) / 
                                                   max(1, len(analysis.get("risk_assessment", [])))
                    }
                }

                return JSONResponse(content=risk_analysis)

            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.post("/news-trends")
        async def news_trends_analysis(request: Request):
            """
            News trends and pattern analysis endpoint
            """
            # Extract API key from headers
            exa_key = request.headers.get("x-exa-key")

            if not exa_key:
                return JSONResponse(
                    status_code=401,
                    content={"error": "Missing required Exa API key"}
                )

            try:
                body = await request.json()
                company_name = body.get("company_name")
                industry = body.get("industry")
                time_period = body.get("time_period", "30d")
                trend_type = body.get("trend_type", "sentiment")
                max_results = body.get("max_results", 20)

                service = EnhancedNewsService()
                service.api_key = exa_key

                # Get news analysis
                analysis = service.get_enhanced_news_analysis(
                    company_name=company_name,
                    industry=industry,
                    max_results=max_results
                )

                # Extract trend-focused data
                trends_analysis = {
                    "time_period": time_period,
                    "trend_type": trend_type,
                    "news_trends": analysis.get("news_trends", {}),
                    "category_trends": analysis.get("news_trends", {}).get("category_distribution", {}),
                    "source_trends": analysis.get("news_trends", {}).get("top_sources", []),
                    "impact_trend": analysis.get("news_trends", {}).get("average_impact", 0),
                    "key_trend_insights": self._generate_trend_insights(analysis.get("news_trends", {}))
                }

                return JSONResponse(content=trends_analysis)

            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.get("/news-categories")
        async def get_news_categories():
            """
            Get available news categories and subcategories
            """
            service = EnhancedNewsService()
            return JSONResponse(content={
                "categories": service.news_categories,
                "source_credibility": service.source_credibility
            })

        @self.app.get("/health")
        async def health_check():
            return {
                "status": "healthy", 
                "service": "Enhanced News Analysis API",
                "version": "2.0",
                "features": [
                    "comprehensive_news_analysis",
                    "sentiment_analysis", 
                    "risk_assessment",
                    "trend_detection",
                    "categorization",
                    "source_credibility_scoring"
                ]
            }

    def _generate_trend_insights(self, trends_data: Dict) -> List[str]:
        """Generate insights from trend data"""
        insights = []
        
        if not trends_data:
            return ["Insufficient data for trend analysis"]
        
        # Analyze sentiment distribution
        sentiment_dist = trends_data.get("sentiment_distribution", {})
        total = sum(sentiment_dist.values())
        if total > 0:
            positive_pct = (sentiment_dist.get("positive", 0) / total) * 100
            negative_pct = (sentiment_dist.get("negative", 0) / total) * 100
            
            if positive_pct > 60:
                insights.append("Strong positive sentiment trend detected")
            elif negative_pct > 60:
                insights.append("Strong negative sentiment trend detected")
            else:
                insights.append("Balanced sentiment distribution observed")
        
        # Analyze category distribution
        category_dist = trends_data.get("category_distribution", {})
        if category_dist:
            top_category = max(category_dist.items(), key=lambda x: x[1])[0]
            insights.append(f"Dominant news category: {top_category}")
        
        # Analyze impact trends
        avg_impact = trends_data.get("average_impact", 0)
        if avg_impact > 70:
            insights.append("High-impact news dominating current coverage")
        elif avg_impact < 40:
            insights.append("Low-impact news prevalent in current coverage")
        
        return insights

def create_app():
    api = EnhancedNewsAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8002)