# file: services/financial_analysis_service.py

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tools.exa_dev_tool import ExaDevTool

class FinancialAnalysisService:
    """
    Enhanced financial analysis service that provides comprehensive news integration
    for financial analysis routes.
    """
    
    def __init__(self):
        self.search_tool = ExaDevTool()
        self.news_categories = ["business", "finance", "technology", "markets"]
    
    def get_financial_analysis(self, 
                             company_name: str = None,
                             industry: str = None,
                             product: str = None,
                             max_results: int = 15) -> Dict:
        """
        Get comprehensive financial analysis with detailed news integration
        
        Args:
            company_name: Specific company to analyze
            industry: Industry focus
            product: Product/technology focus
            max_results: Maximum number of news articles to return
            
        Returns:
            Dict containing financial analysis with detailed news
        """
        
        # Build search queries for different aspects
        queries = self._build_financial_queries(company_name, industry, product)
        
        # Get news articles for each query
        all_news = []
        for query in queries:
            news_results = self._get_financial_news(query, max_results=5)
            all_news.extend(news_results)
        
        # Remove duplicates and limit results
        all_news = self._deduplicate_news(all_news)[:max_results]
        
        # Generate comprehensive analysis
        analysis = self._generate_financial_analysis(
            company_name, industry, product, all_news
        )
        
        return analysis
    
    def _build_financial_queries(self, company_name: str, industry: str, product: str) -> List[str]:
        """Build comprehensive search queries for financial analysis"""
        queries = []
        
        if company_name:
            queries.extend([
                f"{company_name} financial news Q4 2024",
                f"{company_name} earnings report latest",
                f"{company_name} stock performance analysis",
                f"{company_name} market trends",
                f"{company_name} business news"
            ])
        
        if industry:
            queries.extend([
                f"{industry} market analysis 2024",
                f"{industry} financial trends",
                f"{industry} investment outlook",
                f"{industry} business news"
            ])
        
        if product:
            queries.extend([
                f"{product} market analysis",
                f"{product} financial trends",
                f"{product} investment news"
            ])
        
        return queries if queries else ["financial markets news"]
    
    def _get_financial_news(self, query: str, max_results: int = 5) -> List[Dict]:
        """Get financial news using Exa search"""
        try:
            # Get recent news (last 30 days)
            exa_results = self.search_tool.run(
                search_query=query,
                search_type="neural",
                category="news",
                num_results=max_results,
                text=True,
                summary=True,
                livecrawl="always",
                api_key=self.api_key
            )
            
            if isinstance(exa_results, dict) and "results" in exa_results:
                news_items = []
                for result in exa_results["results"]:
                    news_item = {
                        "title": result.get("title", ""),
                        "url": result.get("url", ""),
                        "summary": result.get("summary", ""),
                        "text": result.get("text", "")[:500],  # Limit text length
                        "published_date": self._extract_date(result)
                    }
                    news_items.append(news_item)
                return news_items
        except Exception as e:
            print(f"Error fetching financial news: {e}")
        
        return []
    
    def _extract_date(self, result: Dict) -> str:
        """Extract or estimate publication date"""
        # Exa might provide dates in metadata
        # For now, use current date as fallback
        return datetime.now().strftime("%Y-%m-%d")
    
    def _deduplicate_news(self, news_items: List[Dict]) -> List[Dict]:
        """Remove duplicate news articles based on title similarity"""
        seen_titles = set()
        unique_news = []
        
        for item in news_items:
            # Simple deduplication based on title
            title = item["title"].lower().strip()
            if title not in seen_titles:
                seen_titles.add(title)
                unique_news.append(item)
        
        return unique_news
    
    def _generate_financial_analysis(self, 
                                   company_name: str, 
                                   industry: str, 
                                   product: str,
                                   news_items: List[Dict]) -> Dict:
        """Generate comprehensive financial analysis"""
        
        # Analyze news sentiment and extract key points
        key_insights = self._extract_key_insights(news_items)
        
        # Generate market outlook
        market_outlook = self._generate_market_outlook(company_name, industry, product, news_items)
        
        # Create investment recommendations
        recommendations = self._generate_recommendations(company_name, industry, product, news_items)
        
        analysis = {
            "company_name": company_name or "",
            "industry": industry or "",
            "product_focus": product or "",
            "analysis_date": datetime.now().isoformat(),
            "news_summary": {
                "total_articles": len(news_items),
                "articles": news_items[:10]  # Limit to top 10 articles
            },
            "key_insights": key_insights,
            "market_outlook": market_outlook,
            "investment_recommendations": recommendations,
            "risk_assessment": self._assess_risks(news_items),
            "opportunities": self._identify_opportunities(company_name, industry, product, news_items)
        }
        
        return analysis
    
    def _extract_key_insights(self, news_items: List[Dict]) -> List[str]:
        """Extract key insights from news articles"""
        insights = []
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')}"
            
            # Simple keyword-based insight extraction
            keywords = {
                "earnings": "Strong earnings performance reported",
                "growth": "Significant growth opportunities identified",
                "acquisition": "Merger and acquisition activity noted",
                "innovation": "Innovation and R&D developments",
                "regulation": "Regulatory changes affecting the market",
                "competition": "Competitive landscape developments"
            }
            
            for keyword, insight in keywords.items():
                if keyword.lower() in text.lower():
                    insights.append(insight)
        
        return list(set(insights))[:5]  # Return top 5 unique insights
    
    def _generate_market_outlook(self, company_name: str, industry: str, product: str, news_items: List[Dict]) -> Dict:
        """Generate market outlook based on news analysis"""
        
        # Simple sentiment analysis based on keywords
        positive_indicators = ["growth", "profit", "expansion", "innovation", "opportunity"]
        negative_indicators = ["decline", "loss", "risk", "challenge", "competition"]
        
        positive_count = sum(1 for item in news_items 
                           if any(indicator in item["title"].lower() 
                                for indicator in positive_indicators))
        negative_count = sum(1 for item in news_items 
                           if any(indicator in item["title"].lower() 
                                for indicator in negative_indicators))
        
        if positive_count > negative_count:
            outlook = "positive"
        elif negative_count > positive_count:
            outlook = "cautious"
        else:
            outlook = "neutral"
        
        return {
            "sentiment": outlook,
            "confidence": min(90, max(60, (positive_count / len(news_items)) * 100)) if news_items else 50,
            "key_drivers": ["Market trends", "Economic indicators", "Industry developments"],
            "time_horizon": "6-12 months"
        }
    
    def _generate_recommendations(self, company_name: str, industry: str, product: str, news_items: List[Dict]) -> List[Dict]:
        """Generate investment recommendations"""
        recommendations = []
        
        # Base recommendations on news analysis
        if news_items:
            recommendations.append({
                "type": "Market Research",
                "action": "Monitor industry developments",
                "rationale": "Recent news indicates dynamic market conditions",
                "priority": "High"
            })
        
        if company_name:
            recommendations.append({
                "type": "Company Analysis",
                "action": f"Research {company_name} financials",
                "rationale": "Company-specific developments require detailed analysis",
                "priority": "High"
            })
        
        if industry:
            recommendations.append({
                "type": "Industry Analysis",
                "action": f"Analyze {industry} market trends",
                "rationale": "Industry-level insights provide strategic context",
                "priority": "Medium"
            })
        
        return recommendations
    
    def _assess_risks(self, news_items: List[Dict]) -> List[str]:
        """Assess potential risks from news analysis"""
        risks = []
        
        risk_keywords = {
            "volatility": "Market volatility",
            "regulation": "Regulatory changes",
            "competition": "Increased competition",
            "economic": "Economic uncertainty",
            "supply chain": "Supply chain disruptions"
        }
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')}".lower()
            for keyword, risk in risk_keywords.items():
                if keyword in text and risk not in risks:
                    risks.append(risk)
        
        return risks[:3]  # Return top 3 risks
    
    def _identify_opportunities(self, company_name: str, industry: str, product: str, news_items: List[Dict]) -> List[str]:
        """Identify potential opportunities"""
        opportunities = []
        
        opportunity_keywords = ["growth", "innovation", "expansion", "partnership", "investment"]
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')}".lower()
            if any(keyword in text for keyword in opportunity_keywords):
                opportunities.append("Market expansion opportunities")
                break
        
        if company_name:
            opportunities.append(f"{company_name} strategic positioning")
        if industry:
            opportunities.append(f"{industry} growth potential")
        
        return list(set(opportunities))[:3]  # Return top 3 unique opportunities


def main():
    """Test the financial analysis service"""
    service = FinancialAnalysisService()
    
    # Test with a sample company
    analysis = service.get_financial_analysis(
        company_name="Microsoft",
        industry="technology",
        product="cloud computing",
        max_results=10
    )
    
    print("Financial Analysis Results:")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()