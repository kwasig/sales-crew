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
        """Get financial news using Exa search with enhanced content quality"""
        try:
            # Get recent news with enhanced search parameters for better quality
            exa_results = self.search_tool.run(
                search_query=query,
                search_type="neural",
                category="news",
                num_results=max_results,
                text=True,
                summary=True,
                livecrawl="always",
                use_autoprompt=True,  # Enhanced: Use autoprompt for better query understanding
                include_domains=["reuters.com", "bloomberg.com", "wsj.com", "ft.com", "cnbc.com"],  # Enhanced: Focus on reputable sources
                exclude_domains=["blogspot.com", "wordpress.com"],  # Enhanced: Exclude low-quality sources
                api_key=self.api_key
            )
            
            if isinstance(exa_results, dict) and "results" in exa_results:
                news_items = []
                for result in exa_results["results"]:
                    # Enhanced: Filter for higher quality content
                    if self._is_high_quality_news(result):
                        news_item = {
                            "title": result.get("title", ""),
                            "url": result.get("url", ""),
                            "summary": result.get("summary", ""),
                            "text": result.get("text", "")[:1000],  # Enhanced: Increased text length for more context
                            "published_date": self._extract_date(result),
                            "source": self._extract_source(result.get("url", "")),  # Enhanced: Track source
                            "relevance_score": self._calculate_relevance(result, query)  # Enhanced: Add relevance scoring
                        }
                        news_items.append(news_item)
                
                # Enhanced: Sort by relevance and recency
                news_items.sort(key=lambda x: (x["relevance_score"], x["published_date"]), reverse=True)
                return news_items
        except Exception as e:
            print(f"Error fetching financial news: {e}")
        
        return []
    
    def _extract_date(self, result: Dict) -> str:
        """Extract or estimate publication date with enhanced accuracy"""
        # Enhanced: Try to extract actual publication date from metadata
        if result.get("published_date"):
            return result["published_date"]
        elif result.get("date"):
            return result["date"]
        # Fallback: Use current date but mark as estimated
        return datetime.now().strftime("%Y-%m-%d") + " (estimated)"
    
    def _extract_source(self, url: str) -> str:
        """Extract source domain from URL"""
        import re
        match = re.search(r'https?://([^/]+)', url)
        return match.group(1) if match else "unknown"
    
    def _calculate_relevance(self, result: Dict, query: str) -> float:
        """Calculate relevance score for news article"""
        score = 0.0
        
        # Score based on title match
        title = result.get("title", "").lower()
        query_terms = query.lower().split()
        
        for term in query_terms:
            if term in title:
                score += 0.3
        
        # Score based on source quality
        source = self._extract_source(result.get("url", ""))
        high_quality_sources = ["reuters", "bloomberg", "wsj", "ft", "cnbc", "forbes"]
        if any(quality_source in source for quality_source in high_quality_sources):
            score += 0.4
        
        # Score based on summary length (proxy for content quality)
        summary = result.get("summary", "")
        if len(summary) > 100:
            score += 0.2
        
        return min(1.0, score)
    
    def _is_high_quality_news(self, result: Dict) -> bool:
        """Filter for high-quality news articles"""
        title = result.get("title", "").lower()
        
        # Filter out low-quality indicators
        low_quality_indicators = ["sponsored", "advertisement", "press release", "blog", "opinion"]
        if any(indicator in title for indicator in low_quality_indicators):
            return False
        
        # Require minimum content quality
        summary = result.get("summary", "")
        if len(summary) < 50:  # Too short summary
            return False
        
        return True
    
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
        """Generate comprehensive financial analysis with enhanced detail"""
        
        # Enhanced: Filter for highest quality news first
        high_quality_news = [item for item in news_items if item.get("relevance_score", 0) > 0.6]
        
        # Enhanced: Analyze news sentiment and extract key points with more depth
        key_insights = self._extract_key_insights(high_quality_news if high_quality_news else news_items)
        
        # Enhanced: Generate market outlook with more sophisticated analysis
        market_outlook = self._generate_market_outlook(company_name, industry, product, news_items)
        
        # Enhanced: Create investment recommendations with detailed rationale
        recommendations = self._generate_recommendations(company_name, industry, product, news_items)
        
        # Enhanced: Add comprehensive news analysis section
        news_analysis = self._analyze_news_trends(news_items)
        
        analysis = {
            "company_name": company_name or "",
            "industry": industry or "",
            "product_focus": product or "",
            "analysis_date": datetime.now().isoformat(),
            "news_summary": {
                "total_articles": len(news_items),
                "high_quality_articles": len(high_quality_news),
                "articles": news_items[:15],  # Enhanced: Increased to top 15 articles
                "analysis": news_analysis
            },
            "key_insights": key_insights,
            "market_outlook": market_outlook,
            "investment_recommendations": recommendations,
            "risk_assessment": self._assess_risks(news_items),
            "opportunities": self._identify_opportunities(company_name, industry, product, news_items),
            "analysis_quality": {
                "confidence_score": self._calculate_confidence_score(news_items),
                "data_sources": list(set([item.get("source", "unknown") for item in news_items])),
                "time_coverage": self._get_time_coverage(news_items)
            }
        }
        
        return analysis
    
    def _extract_key_insights(self, news_items: List[Dict]) -> List[str]:
        """Extract key insights from news articles with enhanced analysis"""
        insights = []
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')} {item.get('text', '')}"
            
            # Enhanced: More sophisticated keyword-based insight extraction
            keyword_patterns = {
                "earnings": ["earnings", "profit", "revenue"],
                "growth": ["growth", "expansion", "increased", "surged"],
                "acquisition": ["acquisition", "merger", "takeover", "buyout"],
                "innovation": ["innovation", "technology", "breakthrough", "development"],
                "regulation": ["regulation", "policy", "compliance", "legal"],
                "competition": ["competition", "rival", "market share", "competitive"],
                "investment": ["investment", "funding", "capital", "venture"],
                "partnership": ["partnership", "collaboration", "alliance", "joint venture"]
            }
            
            for category, patterns in keyword_patterns.items():
                if any(pattern in text.lower() for pattern in patterns):
                    # Enhanced: More specific insights based on context
                    if category == "earnings" and "beat" in text.lower():
                        insights.append("Strong earnings beat expectations indicating robust performance")
                    elif category == "growth" and "accelerat" in text.lower():
                        insights.append("Accelerating growth trajectory observed")
                    elif category == "acquisition" and "strategic" in text.lower():
                        insights.append("Strategic acquisition activity suggests market consolidation")
                    else:
                        insights.append(f"{category.title()} developments indicate market movement")
        
        # Enhanced: Remove duplicates and prioritize by frequency
        insight_counts = {}
        for insight in insights:
            insight_counts[insight] = insight_counts.get(insight, 0) + 1
        
        # Return top 7 unique insights (increased from 5)
        return [insight for insight, count in sorted(insight_counts.items(), key=lambda x: x[1], reverse=True)][:7]
    
    def _generate_market_outlook(self, company_name: str, industry: str, product: str, news_items: List[Dict]) -> Dict:
        """Generate market outlook based on enhanced news analysis"""
        
        # Enhanced: More sophisticated sentiment analysis
        positive_indicators = ["growth", "profit", "expansion", "innovation", "opportunity", "strong", "beat", "surge", "gain", "positive"]
        negative_indicators = ["decline", "loss", "risk", "challenge", "competition", "weak", "miss", "fall", "drop", "negative"]
        neutral_indicators = ["stable", "maintain", "steady", "consistent", "unchanged"]
        
        positive_score = 0
        negative_score = 0
        neutral_score = 0
        
        for item in news_items:
            title = item["title"].lower()
            summary = item.get("summary", "").lower()
            text = title + " " + summary
            
            # Weighted scoring based on position and frequency
            positive_score += sum(0.5 if indicator in title else 0.3 for indicator in positive_indicators if indicator in text)
            negative_score += sum(0.5 if indicator in title else 0.3 for indicator in negative_indicators if indicator in text)
            neutral_score += sum(0.3 if indicator in title else 0.2 for indicator in neutral_indicators if indicator in text)
        
        # Enhanced: Determine outlook with more granularity
        total_score = positive_score + negative_score + neutral_score
        if total_score > 0:
            positive_pct = (positive_score / total_score) * 100
            negative_pct = (negative_score / total_score) * 100
            neutral_pct = (neutral_score / total_score) * 100
            
            if positive_pct > 60:
                outlook = "strongly positive"
            elif positive_pct > 40:
                outlook = "positive"
            elif negative_pct > 60:
                outlook = "strongly cautious"
            elif negative_pct > 40:
                outlook = "cautious"
            elif neutral_pct > 50:
                outlook = "stable"
            else:
                outlook = "mixed"
        else:
            outlook = "neutral"
        
        # Enhanced: More specific key drivers based on content
        key_drivers = self._identify_key_drivers(news_items)
        
        return {
            "sentiment": outlook,
            "confidence_score": self._calculate_sentiment_confidence(positive_score, negative_score, neutral_score, len(news_items)),
            "sentiment_breakdown": {
                "positive": round(positive_score, 1),
                "negative": round(negative_score, 1),
                "neutral": round(neutral_score, 1)
            },
            "key_drivers": key_drivers,
            "time_horizon": "6-12 months",
            "analysis_basis": f"Based on analysis of {len(news_items)} news articles"
        }
    
    def _generate_recommendations(self, company_name: str, industry: str, product: str, news_items: List[Dict]) -> List[Dict]:
        """Generate enhanced investment recommendations with detailed rationale"""
        recommendations = []
        
        # Enhanced: More specific recommendations based on news content
        if news_items:
            # Analyze news sentiment for more targeted recommendations
            sentiment_analysis = self._analyze_news_sentiment(news_items)
            
            if sentiment_analysis["positive"] > sentiment_analysis["negative"]:
                recommendations.append({
                    "type": "Investment Opportunity",
                    "action": "Consider strategic investment positions",
                    "rationale": "Positive news flow suggests favorable market conditions",
                    "priority": "High",
                    "timeframe": "Short-term (1-3 months)"
                })
            else:
                recommendations.append({
                    "type": "Risk Management",
                    "action": "Review portfolio exposure",
                    "rationale": "Mixed market signals suggest cautious approach",
                    "priority": "Medium",
                    "timeframe": "Immediate"
                })
        
        if company_name:
            recommendations.append({
                "type": "Company Analysis",
                "action": f"Conduct in-depth analysis of {company_name}",
                "rationale": "Company-specific developments require comprehensive assessment",
                "priority": "High",
                "timeframe": "2-4 weeks"
            })
        
        if industry:
            recommendations.append({
                "type": "Industry Research",
                "action": f"Investigate {industry} sector trends",
                "rationale": "Industry dynamics provide critical context for investment decisions",
                "priority": "Medium",
                "timeframe": "1-2 months"
            })
        
        # Enhanced: Add specific recommendations based on product focus
        if product:
            recommendations.append({
                "type": "Product Analysis",
                "action": f"Evaluate {product} market positioning",
                "rationale": "Product-level analysis reveals competitive advantages",
                "priority": "Medium",
                "timeframe": "3-6 months"
            })
        
        # Enhanced: Add general market monitoring recommendation
        recommendations.append({
            "type": "Market Monitoring",
            "action": "Establish regular market intelligence review",
            "rationale": "Continuous monitoring ensures timely response to market changes",
            "priority": "Medium",
            "timeframe": "Ongoing"
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
    
    def _analyze_news_trends(self, news_items: List[Dict]) -> Dict:
        """Analyze trends across news articles"""
        if not news_items:
            return {"trends": [], "summary": "Insufficient data for trend analysis"}
        
        trends = []
        
        # Analyze frequency of key topics
        topics = ["earnings", "acquisition", "regulation", "innovation", "market", "growth"]
        topic_counts = {topic: 0 for topic in topics}
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')}".lower()
            for topic in topics:
                if topic in text:
                    topic_counts[topic] += 1
        
        # Identify dominant trends
        dominant_topics = [topic for topic, count in topic_counts.items() if count > len(news_items) * 0.2]
        
        if dominant_topics:
            trends.append(f"Dominant themes: {', '.join(dominant_topics)}")
        
        # Analyze source distribution
        sources = [item.get("source", "unknown") for item in news_items]
        source_counts = {}
        for source in sources:
            source_counts[source] = source_counts.get(source, 0) + 1
        
        if source_counts:
            primary_source = max(source_counts.items(), key=lambda x: x[1])
            trends.append(f"Primary news source: {primary_source[0]} ({primary_source[1]} articles)")
        
        return {
            "trends": trends,
            "summary": f"Analysis based on {len(news_items)} articles from {len(set(sources))} sources"
        }
    
    def _calculate_confidence_score(self, news_items: List[Dict]) -> float:
        """Calculate confidence score for the analysis"""
        if not news_items:
            return 0.0
        
        score = 0.0
        
        # Score based on number of articles
        article_score = min(0.4, len(news_items) * 0.05)
        score += article_score
        
        # Score based on source quality
        high_quality_sources = ["reuters", "bloomberg", "wsj", "ft", "cnbc"]
        quality_count = sum(1 for item in news_items 
                          if any(source in item.get("source", "") for source in high_quality_sources))
        source_score = min(0.3, (quality_count / len(news_items)) * 0.3)
        score += source_score
        
        # Score based on recency (placeholder - would need actual dates)
        recency_score = 0.2  # Assume recent for now
        score += recency_score
        
        return min(1.0, score)
    
    def _get_time_coverage(self, news_items: List[Dict]) -> str:
        """Estimate time coverage of news articles"""
        if not news_items:
            return "No data"
        
        # Simple estimation based on article count
        if len(news_items) > 10:
            return "Comprehensive (30+ days)"
        elif len(news_items) > 5:
            return "Moderate (15-30 days)"
        else:
            return "Limited (7-15 days)"
    
    def _identify_key_drivers(self, news_items: List[Dict]) -> List[str]:
        """Identify key market drivers from news analysis"""
        drivers = []
        
        for item in news_items:
            title = item["title"].lower()
            
            if any(word in title for word in ["earnings", "profit", "revenue"]):
                drivers.append("Corporate earnings performance")
            if any(word in title for word in ["regulation", "policy", "compliance"]):
                drivers.append("Regulatory environment")
            if any(word in title for word in ["innovation", "technology", "digital"]):
                drivers.append("Technological innovation")
            if any(word in title for word in ["market", "economy", "economic"]):
                drivers.append("Macroeconomic factors")
            if any(word in title for word in ["competition", "rival", "market share"]):
                drivers.append("Competitive dynamics")
        
        return list(set(drivers))[:5]  # Return top 5 unique drivers
    
    def _analyze_news_sentiment(self, news_items: List[Dict]) -> Dict[str, int]:
        """Analyze sentiment distribution across news articles"""
        positive_count = 0
        negative_count = 0
        neutral_count = 0
        
        positive_words = ["growth", "profit", "strong", "beat", "surge", "gain", "positive", "success"]
        negative_words = ["decline", "loss", "weak", "miss", "fall", "drop", "negative", "challenge"]
        
        for item in news_items:
            text = f"{item['title']} {item.get('summary', '')}".lower()
            
            positive_matches = sum(1 for word in positive_words if word in text)
            negative_matches = sum(1 for word in negative_words if word in text)
            
            if positive_matches > negative_matches:
                positive_count += 1
            elif negative_matches > positive_matches:
                negative_count += 1
            else:
                neutral_count += 1
        
        return {
            "positive": positive_count,
            "negative": negative_count,
            "neutral": neutral_count
        }
    
    def _calculate_sentiment_confidence(self, positive_score: float, negative_score: float, neutral_score: float, article_count: int) -> int:
        """Calculate confidence score for sentiment analysis"""
        if article_count == 0:
            return 0
        
        total_score = positive_score + negative_score + neutral_score
        if total_score == 0:
            return 0
        
        # Confidence increases with more articles and clearer sentiment
        clarity = max(positive_score, negative_score, neutral_score) / total_score
        volume_factor = min(1.0, article_count / 10)  # Normalize by expected volume
        
        confidence = int((clarity * 0.7 + volume_factor * 0.3) * 100)
        return min(95, max(50, confidence))  # Keep between 50-95%


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