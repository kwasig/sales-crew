# file: services/enhanced_news_service.py

import os
import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from collections import Counter
import sys

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from tools.exa_dev_tool import ExaDevTool

class EnhancedNewsService:
    """
    Enhanced news service with comprehensive categorization, sentiment analysis,
    and advanced news processing capabilities.
    """
    
    def __init__(self):
        self.search_tool = ExaDevTool()
        
        # Enhanced news categories with subcategories
        self.news_categories = {
            "financial": ["earnings", "stocks", "markets", "investing", "banking"],
            "business": ["corporate", "mergers", "leadership", "strategy"],
            "technology": ["innovation", "ai", "software", "hardware"],
            "economic": ["inflation", "gdp", "employment", "trade"],
            "regulatory": ["compliance", "legislation", "policy"],
            "industry_specific": ["sector_trends", "competition", "supply_chain"]
        }
        
        # News source credibility scoring
        self.source_credibility = {
            "reuters": 95, "bloomberg": 95, "wsj": 95, "financialtimes": 95,
            "cnbc": 90, "yahoo_finance": 85, "marketwatch": 85,
            "seekingalpha": 80, "investing": 80, "benzinga": 75
        }
        
        # Advanced sentiment indicators
        self.sentiment_indicators = {
            "positive": {
                "strong": ["surge", "record", "breakthrough", "dominant", "outperform"],
                "moderate": ["growth", "profit", "expansion", "opportunity", "strength"],
                "weak": ["stable", "steady", "maintain", "consistent"]
            },
            "negative": {
                "strong": ["collapse", "plummet", "crisis", "bankruptcy", "failure"],
                "moderate": ["decline", "loss", "challenge", "risk", "pressure"],
                "weak": ["volatile", "uncertain", "cautious", "modest"]
            }
        }
    
    def get_enhanced_news_analysis(self, 
                                 company_name: str = None,
                                 industry: str = None,
                                 product: str = None,
                                 max_results: int = 20) -> Dict:
        """
        Get comprehensive news analysis with enhanced features
        """
        
        # Build comprehensive search queries
        queries = self._build_enhanced_queries(company_name, industry, product)
        
        # Fetch news with enhanced parameters
        all_news = []
        for query in queries:
            news_results = self._get_enhanced_news(query, max_results=8)
            all_news.extend(news_results)
        
        # Advanced processing
        processed_news = self._process_news_articles(all_news)
        
        # Generate comprehensive analysis
        analysis = self._generate_enhanced_analysis(
            company_name, industry, product, processed_news
        )
        
        return analysis
    
    def _build_enhanced_queries(self, company_name: str, industry: str, product: str) -> List[str]:
        """Build comprehensive search queries for enhanced news analysis"""
        queries = []
        
        if company_name:
            queries.extend([
                f"{company_name} Q4 2024 earnings financial results",
                f"{company_name} stock performance market analysis",
                f"{company_name} business strategy news updates",
                f"{company_name} recent developments innovations",
                f"{company_name} industry position competitive analysis",
                f"{company_name} regulatory compliance news"
            ])
        
        if industry:
            queries.extend([
                f"{industry} market trends 2024 outlook",
                f"{industry} financial performance analysis",
                f"{industry} investment opportunities risks",
                f"{industry} technological innovations developments",
                f"{industry} regulatory changes impact"
            ])
        
        if product:
            queries.extend([
                f"{product} market adoption growth trends",
                f"{product} competitive landscape analysis",
                f"{product} innovation developments news",
                f"{product} investment potential analysis"
            ])
        
        return queries if queries else ["financial markets economic news analysis"]
    
    def _get_enhanced_news(self, query: str, max_results: int = 8) -> List[Dict]:
        """Get enhanced news with better categorization and metadata"""
        try:
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
                enhanced_news = []
                for result in exa_results["results"]:
                    news_item = self._enhance_news_item(result)
                    enhanced_news.append(news_item)
                return enhanced_news
        except Exception as e:
            print(f"Error fetching enhanced news: {e}")
        
        return []
    
    def _enhance_news_item(self, result: Dict) -> Dict:
        """Enhance news item with additional metadata and analysis"""
        title = result.get("title", "")
        url = result.get("url", "")
        summary = result.get("summary", "")
        text = result.get("text", "")[:1000]  # Increased text limit
        
        # Extract source and credibility
        source = self._extract_source(url)
        credibility_score = self._calculate_credibility(source)
        
        # Enhanced categorization
        categories = self._categorize_news(title + " " + summary)
        
        # Advanced sentiment analysis
        sentiment_score, sentiment_magnitude = self._analyze_sentiment(title + " " + summary)
        
        # Impact scoring
        impact_score = self._calculate_impact(title, summary, source)
        
        return {
            "title": title,
            "url": url,
            "summary": summary,
            "text": text,
            "published_date": self._extract_enhanced_date(result),
            "source": source,
            "credibility_score": credibility_score,
            "categories": categories,
            "sentiment": {
                "score": sentiment_score,
                "magnitude": sentiment_magnitude,
                "label": self._get_sentiment_label(sentiment_score)
            },
            "impact_score": impact_score,
            "key_topics": self._extract_key_topics(title + " " + summary),
            "relevance_score": self._calculate_relevance(title, summary)
        }
    
    def _extract_source(self, url: str) -> str:
        """Extract news source from URL"""
        if not url:
            return "unknown"
        
        # Extract domain name
        domain_match = re.search(r'https?://([^/]+)', url)
        if domain_match:
            domain = domain_match.group(1)
            # Remove www and extract main domain
            domain = domain.replace('www.', '')
            return domain.split('.')[0]  # Get main domain name
        
        return "unknown"
    
    def _calculate_credibility(self, source: str) -> int:
        """Calculate source credibility score"""
        return self.source_credibility.get(source.lower(), 50)  # Default 50 for unknown sources
    
    def _categorize_news(self, text: str) -> List[str]:
        """Categorize news into multiple categories"""
        text_lower = text.lower()
        categories = []
        
        for main_category, subcategories in self.news_categories.items():
            # Check main category keywords
            category_keywords = [main_category] + subcategories
            if any(keyword in text_lower for keyword in category_keywords):
                categories.append(main_category)
        
        return categories if categories else ["general"]
    
    def _analyze_sentiment(self, text: str) -> Tuple[float, float]:
        """Advanced sentiment analysis with magnitude scoring"""
        text_lower = text.lower()
        
        positive_score = 0
        negative_score = 0
        
        # Calculate sentiment scores
        for sentiment_type, strength_levels in self.sentiment_indicators.items():
            for strength, keywords in strength_levels.items():
                weight = {"strong": 3, "moderate": 2, "weak": 1}[strength]
                for keyword in keywords:
                    if keyword in text_lower:
                        if sentiment_type == "positive":
                            positive_score += weight
                        else:
                            negative_score += weight
        
        # Calculate net sentiment score (-1 to 1)
        total_keywords = positive_score + negative_score
        if total_keywords > 0:
            sentiment_score = (positive_score - negative_score) / total_keywords
        else:
            sentiment_score = 0
        
        # Calculate magnitude (0 to 1)
        magnitude = min(1.0, total_keywords / 10)
        
        return sentiment_score, magnitude
    
    def _get_sentiment_label(self, score: float) -> str:
        """Convert sentiment score to label"""
        if score > 0.3:
            return "strongly_positive"
        elif score > 0.1:
            return "positive"
        elif score > -0.1:
            return "neutral"
        elif score > -0.3:
            return "negative"
        else:
            return "strongly_negative"
    
    def _calculate_impact(self, title: str, summary: str, source: str) -> int:
        """Calculate news impact score (0-100)"""
        impact_score = 50  # Base score
        
        # Title impact indicators
        title_lower = title.lower()
        impact_indicators = ["breaking", "exclusive", "major", "significant", "critical"]
        for indicator in impact_indicators:
            if indicator in title_lower:
                impact_score += 10
        
        # Source credibility impact
        credibility = self._calculate_credibility(source)
        impact_score += (credibility - 50) / 5  # Scale credibility impact
        
        # Length impact
        content_length = len(title + summary)
        if content_length > 500:
            impact_score += 5
        
        return max(0, min(100, impact_score))
    
    def _extract_key_topics(self, text: str) -> List[str]:
        """Extract key topics from news text"""
        # Simple topic extraction based on frequency
        words = re.findall(r'\b\w{4,}\b', text.lower())
        
        # Filter common words and count frequency
        common_words = {"company", "market", "news", "report", "analysis", "financial"}
        filtered_words = [word for word in words if word not in common_words]
        
        word_counts = Counter(filtered_words)
        return [word for word, count in word_counts.most_common(5)]
    
    def _calculate_relevance(self, title: str, summary: str) -> int:
        """Calculate relevance score for the news"""
        # Simple relevance scoring based on financial/business keywords
        financial_keywords = ["earnings", "revenue", "profit", "stock", "market", 
                            "investment", "financial", "business", "corporate"]
        
        content = (title + " " + summary).lower()
        relevance_count = sum(1 for keyword in financial_keywords if keyword in content)
        
        return min(100, relevance_count * 20)  # Scale to 100
    
    def _extract_enhanced_date(self, result: Dict) -> str:
        """Extract publication date with better parsing"""
        # Try to extract from metadata if available
        if "published_date" in result:
            return result["published_date"]
        
        # Fallback to current date
        return datetime.now().strftime("%Y-%m-%d")
    
    def _process_news_articles(self, news_items: List[Dict]) -> List[Dict]:
        """Process news articles with advanced deduplication and clustering"""
        if not news_items:
            return []
        
        # Advanced deduplication
        unique_news = self._advanced_deduplication(news_items)
        
        # Sort by impact and relevance
        sorted_news = sorted(unique_news, 
                           key=lambda x: (x["impact_score"], x["relevance_score"]), 
                           reverse=True)
        
        return sorted_news
    
    def _advanced_deduplication(self, news_items: List[Dict]) -> List[Dict]:
        """Advanced deduplication using title similarity and content analysis"""
        unique_items = []
        seen_titles = set()
        
        for item in news_items:
            title = item["title"].lower().strip()
            
            # Check for similar titles using fuzzy matching
            is_duplicate = False
            for seen_title in seen_titles:
                similarity = self._calculate_title_similarity(title, seen_title)
                if similarity > 0.8:  # 80% similarity threshold
                    is_duplicate = True
                    break
            
            if not is_duplicate:
                seen_titles.add(title)
                unique_items.append(item)
        
        return unique_items
    
    def _calculate_title_similarity(self, title1: str, title2: str) -> float:
        """Calculate similarity between two titles"""
        words1 = set(title1.split())
        words2 = set(title2.split())
        
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union)
    
    def _generate_enhanced_analysis(self, 
                                  company_name: str, 
                                  industry: str, 
                                  product: str,
                                  news_items: List[Dict]) -> Dict:
        """Generate comprehensive enhanced analysis"""
        
        # Advanced insights extraction
        key_insights = self._extract_enhanced_insights(news_items)
        
        # Market outlook with confidence scoring
        market_outlook = self._generate_enhanced_market_outlook(news_items)
        
        # Risk assessment with probability scoring
        risk_assessment = self._assess_enhanced_risks(news_items)
        
        # Opportunity identification with potential scoring
        opportunities = self._identify_enhanced_opportunities(news_items)
        
        # News trends and patterns
        news_trends = self._analyze_news_trends(news_items)
        
        analysis = {
            "company_name": company_name or "",
            "industry": industry or "",
            "product_focus": product or "",
            "analysis_date": datetime.now().isoformat(),
            "news_analysis": {
                "total_articles": len(news_items),
                "articles": news_items[:15],  # Top 15 articles
                "summary_statistics": self._generate_news_statistics(news_items)
            },
            "key_insights": key_insights,
            "market_outlook": market_outlook,
            "risk_assessment": risk_assessment,
            "opportunities": opportunities,
            "news_trends": news_trends,
            "recommendations": self._generate_enhanced_recommendations(news_items)
        }
        
        return analysis
    
    def _extract_enhanced_insights(self, news_items: List[Dict]) -> List[Dict]:
        """Extract enhanced insights with confidence scoring"""
        insights = []
        
        for item in news_items:
            # Extract insights based on sentiment and impact
            if item["sentiment"]["score"] > 0.2 and item["impact_score"] > 70:
                insights.append({
                    "insight": f"Positive development: {item['title']}",
                    "confidence": min(95, item["impact_score"]),
                    "source": item["source"],
                    "category": item["categories"][0] if item["categories"] else "general"
                })
            elif item["sentiment"]["score"] < -0.2 and item["impact_score"] > 70:
                insights.append({
                    "insight": f"Potential concern: {item['title']}",
                    "confidence": min(95, item["impact_score"]),
                    "source": item["source"],
                    "category": item["categories"][0] if item["categories"] else "general"
                })
        
        return insights[:8]  # Return top 8 insights
    
    def _generate_enhanced_market_outlook(self, news_items: List[Dict]) -> Dict:
        """Generate enhanced market outlook with detailed analysis"""
        if not news_items:
            return {
                "sentiment": "neutral",
                "confidence": 50,
                "key_drivers": [],
                "time_horizon": "6-12 months",
                "trend_direction": "stable"
            }
        
        # Calculate weighted sentiment
        total_impact = sum(item["impact_score"] for item in news_items)
        weighted_sentiment = sum(item["sentiment"]["score"] * item["impact_score"] 
                               for item in news_items) / total_impact
        
        # Determine outlook based on weighted sentiment
        if weighted_sentiment > 0.15:
            outlook = "positive"
        elif weighted_sentiment > -0.15:
            outlook = "neutral"
        else:
            outlook = "cautious"
        
        # Calculate confidence based on source credibility and impact
        avg_credibility = sum(item["credibility_score"] for item in news_items) / len(news_items)
        confidence = min(95, (avg_credibility + total_impact / len(news_items)) / 2)
        
        return {
            "sentiment": outlook,
            "confidence": confidence,
            "key_drivers": self._extract_market_drivers(news_items),
            "time_horizon": "6-12 months",
            "trend_direction": "upward" if weighted_sentiment > 0 else "downward" if weighted_sentiment < 0 else "stable",
            "weighted_sentiment": weighted_sentiment
        }
    
    def _extract_market_drivers(self, news_items: List[Dict]) -> List[str]:
        """Extract key market drivers from news"""
        drivers = []
        
        for item in news_items:
            if item["impact_score"] > 70:
                # Extract potential drivers from high-impact news
                text = item["title"] + " " + item["summary"]
                if any(driver in text.lower() for driver in ["earnings", "revenue"]):
                    drivers.append("Financial Performance")
                elif any(driver in text.lower() for driver in ["innovation", "technology"]):
                    drivers.append("Technological Developments")
                elif any(driver in text.lower() for driver in ["regulation", "policy"]):
                    drivers.append("Regulatory Changes")
        
        return list(set(drivers))[:5]
    
    def _assess_enhanced_risks(self, news_items: List[Dict]) -> List[Dict]:
        """Assess enhanced risks with probability scoring"""
        risks = []
        
        risk_patterns = {
            "market_volatility": ["volatile", "uncertain", "fluctuation"],
            "regulatory_risk": ["regulation", "compliance", "legislation"],
            "competitive_threat": ["competition", "rival", "market share"],
            "economic_risk": ["recession", "inflation", "economic"],
            "supply_chain_risk": ["supply chain", "logistics", "production"]
        }
        
        for risk_type, keywords in risk_patterns.items():
            risk_articles = [item for item in news_items 
                           if any(keyword in (item["title"] + " " + item["summary"]).lower() 
                                for keyword in keywords)]
            
            if risk_articles:
                # Calculate risk probability based on article impact and sentiment
                total_impact = sum(item["impact_score"] for item in risk_articles)
                avg_sentiment = sum(item["sentiment"]["score"] for item in risk_articles) / len(risk_articles)
                
                probability = min(90, total_impact / len(risk_articles) * (1 - avg_sentiment))
                
                risks.append({
                    "risk_type": risk_type.replace("_", " ").title(),
                    "probability": probability,
                    "severity": "high" if probability > 70 else "medium" if probability > 40 else "low",
                    "sources": [item["source"] for item in risk_articles[:3]]
                })
        
        return sorted(risks, key=lambda x: x["probability"], reverse=True)[:5]
    
    def _identify_enhanced_opportunities(self, news_items: List[Dict]) -> List[Dict]:
        """Identify enhanced opportunities with potential scoring"""
        opportunities = []
        
        opportunity_patterns = {
            "market_expansion": ["growth", "expansion", "new market"],
            "innovation_opportunity": ["innovation", "breakthrough", "new technology"],
            "strategic_partnership": ["partnership", "collaboration", "joint venture"],
            "investment_opportunity": ["investment", "funding", "capital"],
            "competitive_advantage": ["advantage", "leadership", "dominant"]
        }
        
        for opp_type, keywords in opportunity_patterns.items():
            opp_articles = [item for item in news_items 
                          if any(keyword in (item["title"] + " " + item["summary"]).lower() 
                               for keyword in keywords) 
                          and item["sentiment"]["score"] > 0]
            
            if opp_articles:
                # Calculate opportunity potential based on sentiment and impact
                total_impact = sum(item["impact_score"] for item in opp_articles)
                avg_sentiment = sum(item["sentiment"]["score"] for item in opp_articles) / len(opp_articles)
                
                potential = min(90, total_impact / len(opp_articles) * avg_sentiment)
                
                opportunities.append({
                    "opportunity_type": opp_type.replace("_", " ").title(),
                    "potential": potential,
                    "timeframe": "short_term" if potential > 70 else "medium_term" if potential > 40 else "long_term",
                    "sources": [item["source"] for item in opp_articles[:3]]
                })
        
        return sorted(opportunities, key=lambda x: x["potential"], reverse=True)[:5]
    
    def _analyze_news_trends(self, news_items: List[Dict]) -> Dict:
        """Analyze news trends and patterns"""
        if not news_items:
            return {"trends": [], "pattern_analysis": "Insufficient data"}
        
        # Analyze category distribution
        category_counts = {}
        for item in news_items:
            for category in item["categories"]:
                category_counts[category] = category_counts.get(category, 0) + 1
        
        # Analyze sentiment trends
        sentiment_distribution = {"positive": 0, "neutral": 0, "negative": 0}
        for item in news_items:
            sentiment_label = item["sentiment"]["label"]
            if "positive" in sentiment_label:
                sentiment_distribution["positive"] += 1
            elif "negative" in sentiment_label:
                sentiment_distribution["negative"] += 1
            else:
                sentiment_distribution["neutral"] += 1
        
        return {
            "category_distribution": category_counts,
            "sentiment_distribution": sentiment_distribution,
            "top_sources": Counter([item["source"] for item in news_items]).most_common(5),
            "average_impact": sum(item["impact_score"] for item in news_items) / len(news_items)
        }
    
    def _generate_news_statistics(self, news_items: List[Dict]) -> Dict:
        """Generate comprehensive news statistics"""
        if not news_items:
            return {}
        
        return {
            "total_articles": len(news_items),
            "average_credibility": sum(item["credibility_score"] for item in news_items) / len(news_items),
            "average_sentiment": sum(item["sentiment"]["score"] for item in news_items) / len(news_items),
            "high_impact_articles": len([item for item in news_items if item["impact_score"] > 70]),
            "top_categories": Counter([cat for item in news_items for cat in item["categories"]]).most_common(3)
        }
    
    def _generate_enhanced_recommendations(self, news_items: List[Dict]) -> List[Dict]:
        """Generate enhanced investment recommendations"""
        recommendations = []
        
        # Base recommendations on news analysis
        if news_items:
            avg_sentiment = sum(item["sentiment"]["score"] for item in news_items) / len(news_items)
            
            if avg_sentiment > 0.2:
                recommendations.append({
                    "type": "Investment",
                    "action": "Consider strategic investments",
                    "rationale": "Positive market sentiment indicates growth opportunities",
                    "priority": "High",
                    "confidence": min(85, avg_sentiment * 100)
                })
            elif avg_sentiment < -0.2:
                recommendations.append({
                    "type": "Risk Management",
                    "action": "Implement defensive strategies",
                    "rationale": "Negative sentiment suggests increased market risks",
                    "priority": "High",
                    "confidence": min(85, abs(avg_sentiment) * 100)
                })
        
        # Add monitoring recommendations
        recommendations.append({
            "type": "Monitoring",
            "action": "Track key market indicators",
            "rationale": "Continuous monitoring essential for timely decision-making",
            "priority": "Medium",
            "confidence": 75
        })
        
        return recommendations


def main():
    """Test the enhanced news service"""
    service = EnhancedNewsService()
    
    # Test with sample parameters
    analysis = service.get_enhanced_news_analysis(
        company_name="Microsoft",
        industry="technology",
        product="cloud computing",
        max_results=15
    )
    
    print("Enhanced News Analysis Results:")
    print(json.dumps(analysis, indent=2))

if __name__ == "__main__":
    main()