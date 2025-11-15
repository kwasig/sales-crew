# file: tools/financial_analysis_tool.py

from crewai.tools import BaseTool
from typing import Optional
from pydantic import Field, ConfigDict
import sys
import os

# Ensure parent directory is in the path
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.financial_analysis_service import FinancialAnalysisService

class FinancialAnalysisTool(BaseTool):
    model_config = ConfigDict(arbitrary_types_allowed=True)
    
    name: str = "Financial Analysis Intelligence"
    description: str = (
        "Enhanced financial analysis tool that provides comprehensive news integration "
        "for detailed financial analysis. Returns structured financial insights with "
        "market trends, investment recommendations, and risk assessment."
    )

    service: FinancialAnalysisService = Field(default_factory=FinancialAnalysisService)
    api_key: str = Field(default="")

    def _run(
        self,
        company_name: Optional[str] = None,
        industry: Optional[str] = None,
        product: Optional[str] = None,
        max_results: int = 15
    ) -> str:
        """
        Execute comprehensive financial analysis with detailed news integration.
        
        Args:
            company_name (str, optional): Specific company to analyze
            industry (str, optional): Industry focus for analysis
            product (str, optional): Product/technology focus
            max_results (int): Maximum number of news articles to analyze (default: 15)
        
        Returns:
            str: JSON string containing comprehensive financial analysis
        """
        
        # Set API key for the service
        self.service.api_key = self.api_key
        
        # Get comprehensive financial analysis
        analysis = self.service.get_financial_analysis(
            company_name=company_name,
            industry=industry,
            product=product,
            max_results=max_results
        )
        
        # Convert to JSON string for crewai compatibility
        import json
        return json.dumps(analysis, indent=2)

if __name__ == "__main__":
    # Test the tool
    tool = FinancialAnalysisTool(api_key="your_api_key_here")
    
    test_cases = [
        {
            "company_name": "Microsoft",
            "industry": "technology",
            "product": "cloud computing",
            "max_results": 10
        }
    ]
    
    for case in test_cases:
        print(f"\nTesting with parameters: {case}")
        result = tool._run(**case)
        print("Financial Analysis Results:")
        print(result)