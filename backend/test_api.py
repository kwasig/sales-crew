#!/usr/bin/env python3
"""
Test script for the unified Sales Crew API
"""

import requests
import json
import sys

def test_health_endpoint():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✓ Health endpoint is working")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Health endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Health endpoint error: {e}")
        return False

def test_root_endpoint():
    """Test the root endpoint"""
    print("\nTesting root endpoint...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✓ Root endpoint is working")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Root endpoint failed with status {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Root endpoint error: {e}")
        return False

def test_lead_generation_missing_keys():
    """Test lead generation endpoint without API keys"""
    print("\nTesting lead generation endpoint (missing API keys)...")
    try:
        response = requests.post(
            "http://localhost:8000/generate-leads",
            json={"prompt": "AI chip startups in Silicon Valley"}
        )
        if response.status_code == 401:
            print("✓ Lead generation endpoint correctly requires API keys")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Lead generation endpoint error: {e}")
        return False

def test_financial_analysis_missing_keys():
    """Test financial analysis endpoint without API keys"""
    print("\nTesting financial analysis endpoint (missing API keys)...")
    try:
        response = requests.post(
            "http://localhost:8000/financial-analysis",
            json={"company_name": "Test Company"}
        )
        if response.status_code == 401:
            print("✓ Financial analysis endpoint correctly requires API keys")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        else:
            print(f"✗ Expected 401, got {response.status_code}")
            return False
    except Exception as e:
        print(f"✗ Financial analysis endpoint error: {e}")
        return False

def main():
    print("Sales Crew API Test Suite")
    print("=" * 50)
    
    tests = [
        test_health_endpoint,
        test_root_endpoint,
        test_lead_generation_missing_keys,
        test_financial_analysis_missing_keys
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("✓ All tests passed! The API is working correctly.")
        sys.exit(0)
    else:
        print("✗ Some tests failed. Please check the API implementation.")
        sys.exit(1)

if __name__ == "__main__":
    main()