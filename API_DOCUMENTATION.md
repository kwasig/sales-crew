# Sales Crew API Documentation

## Overview

The Sales Crew API provides a unified endpoint for lead generation and financial analysis. This API allows users to trigger AI agents and receive responses as JSON objects.

## Base URL

- Local Development: `http://localhost:8000`
- Production: `https://yourdomain.com/api`

## Authentication

The API requires API keys to be passed in the request headers:

- `x-sambanova-key`: Your SambaNova API key (required for lead generation)
- `x-exa-key`: Your Exa API key (required for both endpoints)

## Endpoints

### 1. Root Endpoint

**GET /**

Returns information about available endpoints.

**Response:**
```json
{
  "message": "Sales Crew Unified API",
  "endpoints": {
    "lead_generation": "/generate-leads",
    "financial_analysis": "/financial-analysis",
    "health": "/health"
  }
}
```

### 2. Health Check

**GET /health**

Returns the health status of the API and its endpoints.

**Response:**
```json
{
  "status": "healthy",
  "service": "Sales Crew Unified API",
  "endpoints": {
    "lead_generation": "active",
    "financial_analysis": "active"
  }
}
```

### 3. Lead Generation

**POST /generate-leads**

Generates leads based on a user prompt and returns personalized outreach emails.

**Headers:**
- `x-sambanova-key`: Your SambaNova API key
- `x-exa-key`: Your Exa API key
- `Content-Type`: application/json

**Request Body:**
```json
{
  "prompt": "AI chip startups in Silicon Valley"
}
```

**Response:**
```json
[
  {
    "company_name": "Example Company",
    "website": "https://example.com",
    "headquarters": "San Francisco, CA",
    "key_contacts": "John Doe, CEO",
    "funding_status": "Series A",
    "funding_amount": "$10M",
    "product": "AI Chip Design Platform",
    "relevant_trends": "Growing demand for AI hardware",
    "opportunities": "Expansion into edge computing",
    "challenges": "Competition from established players",
    "email_subject": "Partnership Opportunity for AI Chip Innovation",
    "email_body": "Dear Example Company, ..."
  }
]
```

**Error Responses:**
- `401 Unauthorized`: Missing required API keys
- `400 Bad Request`: Missing prompt in request body
- `500 Internal Server Error`: Server error or invalid response from research crew

### 4. Financial Analysis

**POST /financial-analysis**

Performs financial analysis on companies and returns detailed insights.

**Headers:**
- `x-exa-key`: Your Exa API key
- `Content-Type`: application/json

**Request Body:**
```json
{
  "company_name": "Example Company",
  "industry": "AI Hardware",
  "product": "AI Chip Design Platform",
  "max_results": 15
}
```

**Response:**
```json
{
  "company_analysis": {
    "company_name": "Example Company",
    "latest_news": [...],
    "market_position": "Leading in AI chip design"
  },
  "market_outlook": {
    "sentiment": "Positive",
    "trends": [...]
  },
  "investment_recommendations": [...],
  "risk_assessment": [...],
  "key_insights": [...]
}
```

**Error Responses:**
- `401 Unauthorized`: Missing required Exa API key
- `500 Internal Server Error`: Server error or invalid JSON in request body

## Usage Examples

### cURL Examples

#### Lead Generation
```bash
curl -X POST http://localhost:8000/generate-leads \
  -H "x-sambanova-key: your_sambanova_key" \
  -H "x-exa-key: your_exa_key" \
  -H "Content-Type: application/json" \
  -d '{"prompt": "AI chip startups in Silicon Valley"}'
```

#### Financial Analysis
```bash
curl -X POST http://localhost:8000/financial-analysis \
  -H "x-exa-key: your_exa_key" \
  -H "Content-Type: application/json" \
  -d '{
    "company_name": "Example Company",
    "industry": "AI Hardware",
    "product": "AI Chip Design Platform"
  }'
```

### Python Example

```python
import requests
import json

# Lead Generation
response = requests.post(
    "http://localhost:8000/generate-leads",
    headers={
        "x-sambanova-key": "your_sambanova_key",
        "x-exa-key": "your_exa_key",
        "Content-Type": "application/json"
    },
    json={"prompt": "AI chip startups in Silicon Valley"}
)

leads = response.json()
print(json.dumps(leads, indent=2))

# Financial Analysis
response = requests.post(
    "http://localhost:8000/financial-analysis",
    headers={
        "x-exa-key": "your_exa_key",
        "Content-Type": "application/json"
    },
    json={
        "company_name": "Example Company",
        "industry": "AI Hardware",
        "product": "AI Chip Design Platform"
    }
)

analysis = response.json()
print(json.dumps(analysis, indent=2))
```

### JavaScript Example

```javascript
// Lead Generation
const leadResponse = await fetch('http://localhost:8000/generate-leads', {
  method: 'POST',
  headers: {
    'x-sambanova-key': 'your_sambanova_key',
    'x-exa-key': 'your_exa_key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ prompt: 'AI chip startups in Silicon Valley' })
});

const leads = await leadResponse.json();
console.log(leads);

// Financial Analysis
const analysisResponse = await fetch('http://localhost:8000/financial-analysis', {
  method: 'POST',
  headers: {
    'x-exa-key': 'your_exa_key',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    company_name: 'Example Company',
    industry: 'AI Hardware',
    product: 'AI Chip Design Platform'
  })
});

const analysis = await analysisResponse.json();
console.log(analysis);
```

## Running the API

### Local Development

1. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Set up environment variables (optional):
```bash
export ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

3. Run the API:
```bash
python api/main_api.py
```

Or with uvicorn:
```bash
uvicorn api.main_api:create_app --reload --host 0.0.0.0 --port 8000
```

### Docker

1. Build and run with Docker Compose:
```bash
docker-compose up --build
```

2. The API will be available at `http://localhost:8000`

## Testing

Run the test script to verify the API is working:

```bash
cd backend
python test_api.py
```

## Error Handling

The API uses standard HTTP status codes:

- `200 OK`: Request successful
- `400 Bad Request`: Invalid request data
- `401 Unauthorized`: Missing or invalid API keys
- `500 Internal Server Error`: Server error

All error responses include a JSON body with an `error` field describing the issue.

## Rate Limiting

Currently, there are no rate limits implemented. However, please be mindful of the API usage limits of the underlying services (SambaNova and Exa).

## Support

For issues or questions, please open an issue on the GitHub repository: https://github.com/kwasig/sales-crew/issues