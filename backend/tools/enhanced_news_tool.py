# file: tools/enhanced_news_tool.py

from crewai.tools import BaseTool
from typing import Optional
from pydantic import Field, ConfigDict
import sys
import os

# Ensure parent directory is in the path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.enhanced_news_service import EnhancedNewsService

class EnhancedNewsTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "Enhanced News Intelligence"
    description: str = (
        "Advanced news analysis tool with comprehensive categorization, sentiment analysis, "
        "risk assessment, and trend detection. Provides detailed financial and market insights "
        "based on the latest news coverage with source credibility scoring and impact analysis."
    )

    service: EnhancedNewsService = Field(default_factory=EnhancedNewsService)
    api_key: str = Field(default="")

    def _run(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        product: Optional[str] = None,
        max_results: int = 20,
        analysis_type: str = "comprehensive"
    ) -> str:
        """
        Execute enhanced news analysis with advanced features.
        
        Args:
            company_name (str, optional): Specific company to analyze
            industry (str, optional): Industry focus for analysis
            product (str, optional): Product/technology focus
            max_results (int): Maximum number of news articles to analyze (default: 20)
            analysis_type (str): Type of analysis - comprehensive, sentiment, risks, trends
        
        Returns:
            str: JSON string containing enhanced news analysis
        """
        
        # Set API key for the service
        self.service.api_key = self.api_key
        
        # Get comprehensive enhanced news analysis
        analysis = self.service.get_enhanced_news_analysis(
            company_name=company_name,
            industry=industry,
            product=product,
            max_results=max_results
        )
        
        # Add analysis type metadata
        analysis["tool_analysis_type"] = analysis_type
        analysis["tool_version"] = "2.0"
        
        # Convert to JSON string for crewai compatibility
        import json
        return json.dumps(analysis, indent=2)

class NewsSentimentTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "News Sentiment Analyzer"
    description: str = (
        "Specialized tool for analyzing news sentiment with advanced scoring. "
        "Provides sentiment distribution, confidence levels, and trend analysis "
        "based on comprehensive news coverage."
    )

    service: EnhancedNewsService = Field(default_factory=EnhancedNewsService)
    api_key: str = Field(default="")

    def _run(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        product: Optional[str] = None,
        max_results: int = 15
    ) -> str:
        """
        Execute focused sentiment analysis on news coverage.
        
        Args:
            company_name (str, optional): Specific company to analyze
            industry (str, optional): Industry focus for analysis
            product (str, optional): Product/technology focus
            max_results (int): Maximum number of news articles to analyze
        
        Returns:
            str: JSON string containing sentiment analysis results
        """
        
        # Set API key for the service
        self.service.api_key = self.api_key
        
        # Get comprehensive analysis
        analysis = self.service.get_enhanced_news_analysis(
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
            "sentiment_trend": analysis.get("market_outlook", {}).get("trend_direction", "stable"),
            "analysis_summary": self._generate_sentiment_summary(analysis)
        }
        
        # Convert to JSON string
        import json
        return json.dumps(sentiment_analysis, indent=2)
    
    def _generate_sentiment_summary(self, analysis: dict) -> str:
        """Generate a human-readable sentiment summary"""
        outlook = analysis.get("market_outlook", {})
        sentiment = outlook.get("sentiment", "neutral")
        confidence = outlook.get("confidence", 50)
        trend = outlook.get("trend_direction", "stable")
        
        summary = f"Market sentiment is {sentiment} with {confidence}% confidence. "
        summary += f"The trend direction is {trend}. "
        
        if sentiment == "positive" and confidence > 70:
            summary += "This indicates strong positive market conditions."
        elif sentiment == "negative" and confidence > 70:
            summary += "This suggests significant market concerns."
        else:
            summary += "Market conditions appear balanced with mixed signals."
        
        return summary

class NewsRiskAssessmentTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "News Risk Assessor"
    description: str = (
        "Advanced risk assessment tool that analyzes news coverage for potential risks. "
        "Identifies market volatility, regulatory risks, competitive threats, and economic "
        "uncertainties with probability scoring and severity assessment."
    )

    service: EnhancedNewsService = Field(default_factory=EnhancedNewsService)
    api_key: str = Field(default="")

    def _run(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        product: Optional[str] = None,
        max_results: int = 15
    ) -> str:
        """
        Execute comprehensive risk assessment based on news analysis.
        
        Args:
            company_name (str, optional): Specific company to analyze
            industry (str, optional): Industry focus for analysis
            product (str, optional): Product/technology focus
            max_results (int): Maximum number of news articles to analyze
        
        Returns:
            str: JSON string containing risk assessment results
        """
        
        # Set API key for the service
        self.service.api_key = self.api_key
        
        # Get comprehensive analysis
        analysis = self.service.get_enhanced_news_analysis(
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
            },
            "risk_mitigation_recommendations": self._generate_risk_recommendations(analysis.get("risk_assessment", []))
        }
        
        # Convert to JSON string
        import json
        return json.dumps(risk_analysis, indent=2)
    
    def _generate_risk_recommendations(self, risks: list) -> list:
        """Generate risk mitigation recommendations"""
        recommendations = []
        
        for risk in risks:
            risk_type = risk.get("risk_type", "")
            probability = risk.get("probability", 0)
            severity = risk.get("severity", "medium")
            
            if probability > 70 and severity == "high":
                recommendations.append({
                    "action": f"Immediate monitoring required for {risk_type}",
                    "priority": "critical",
                    "rationale": f"High probability ({probability}%) and severity combination"
                })
            elif probability > 50:
                recommendations.append({
                    "action": f"Develop contingency plan for {risk_type}",
                    "priority": "high",
                    "rationale": f"Moderate to high probability ({probability}%)"
                })
        
        return recommendations[:3]  # Return top 3 recommendations

class NewsTrendsTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "News Trends Analyzer"
    description: str = (
        "Trend analysis tool that identifies patterns and developments in news coverage. "
        "Analyzes category distribution, source patterns, impact trends, and emerging topics "
        "for strategic insights."
    )

    service: EnhancedNewsService = Field(default_factory=EnhancedNewsService)
    api_key: str = Field(default="")

    def _run(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        time_period: str = "30d",
        trend_type: str = "sentiment",
        max_results: int = 20
    ) -> str:
        """
        Execute trend analysis on news coverage.
        
        Args:
            company_name (str, optional): Specific company to analyze
            industry (str, optional): Industry focus for analysis
            time_period (str): Analysis time period - 7d, 30d, 90d
            trend_type (str): Type of trend analysis - sentiment, topics, sources
            max_results (int): Maximum number of news articles to analyze
        
        Returns:
            str: JSON string containing trend analysis results
        """
        
        # Set API key for the service
        self.service.api_key = self.api_key
        
        # Get comprehensive analysis
        analysis = self.service.get_enhanced_news_analysis(
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
            "key_trend_insights": self._generate_trend_insights(analysis.get("news_trends", {})),
            "emerging_topics": self._identify_emerging_topics(analysis.get("news_analysis", {}).get("articles", []))
        }
        
        # Convert to JSON string
        import json
        return json.dumps(trends_analysis, indent=2)
    
    def _generate_trend_insights(self, trends_data: dict) -> list:
        """Generate insights from trend data"""
        insights = []
        
        if not trends_data:
            return ["Insufficient data for trend analysis"]
        
        # Analyze sentiment distribution
        sentiment_dist = trends_data.get("sentiment_distribution", {})
        total = sum(sentiment_dist.values())
        if total > 0:
            positive_pct = (sentiment_dist.get("positive", 0) / total) * 100
            if positive_pct > 60:
                insights.append("Strong positive sentiment trend dominating coverage")
            elif positive_pct < 30:
                insights.append("Limited positive sentiment in current coverage")
        
        # Analyze category distribution
        category_dist = trends_data.get("category_distribution", {})
        if category_dist:
            top_category = max(category_dist.items(), key=lambda x: x[1])[0]
            insights.append(f"{top_category.replace('_', ' ').title()} category shows strongest presence")
        
        return insights
    
    def _identify_emerging_topics(self, articles: list) -> list:
        """Identify emerging topics from news articles"""
        if not articles:
            return []
        
        # Extract topics from high-impact articles
        topics = []
        for article in articles[:10]:  # Analyze top 10 articles
            if article.get("impact_score", 0) > 70:
                key_topics = article.get("key_topics", [])
                topics.extend(key_topics)
        
        # Count frequency and return top emerging topics
        from collections import Counter
        topic_counts = Counter(topics)
        return [topic for topic, count in topic_counts.most_common(5)]


if __name__ == "__main__":
    # Test the enhanced news tool
    tool = EnhancedNewsTool(api_key="your_api_key_here")
    
    test_cases = [
        {
            "company_name": "Microsoft",
            "industry": "technology",
            "product": "cloud computing",
            "max_results": 10,
            "analysis_type": "comprehensive"
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting Enhanced News Tool with parameters: {case}")
        result = tool._run(**case)
        print("Enhanced News Analysis Results:")
        print(result)
    
    # Test sentiment tool
    sentiment_tool = NewsSentimentTool(api_key="your_api_key_here")
    sentiment_result = sentiment_tool._run(company_name="Microsoft")
    print("\nSentiment Analysis Results:")
    print(sentiment_result)
    
    # Test risk assessment tool
    risk_tool = NewsRiskAssessmentTool(api_key="your_api_key_here")
    risk_result = risk_tool._run(company_name="Microsoft")
    print("\nRisk Assessment Results:")
    print(risk_result)