# Sales Crew - AI-Powered Sales Lead Generation

## Overview
Sales Crew is an AI-powered platform that generates targeted sales leads using advanced AI agents and real-time financial analysis.

## New Features (PR #31)

### Usage Dashboard and Financial Analysis Service Enhancements
- **Real-time Usage Dashboard**: Comprehensive analytics and metrics tracking
- **Enhanced Financial Analysis**: Improved service with additional insights
- **User Activity Monitoring**: Session tracking and search analytics
- **Interactive Visualizations**: Charts and graphs for data presentation

## Technology Stack

### Backend
- FastAPI with uvicorn server
- CrewAI, LangChain, OpenAI integration
- Exa search API for news and company intelligence
- Pydantic for data validation

### Frontend
- Vue.js 3 with Vue Router
- Tailwind CSS for styling
- Axios for API communication

## API Endpoints

### Lead Generation
- `POST /generate-leads` - Main lead generation endpoint

### Financial Analysis
- `POST /financial-analysis` - Standalone financial analysis
- `GET /health` - Service health check

### Dashboard (New)
- `GET /dashboard/metrics` - Comprehensive dashboard metrics
- `GET /dashboard/analytics/{days}` - Usage analytics for specified days
- `GET /dashboard/financial-insights` - Financial insights summary
- `POST /dashboard/session/start` - Start user session for tracking
- `POST /dashboard/search/track` - Track search operations

## Quick Start

1. **Clone the repository**
   ```bash
   git clone https://github.com/kwasig/sales-crew.git
   cd sales-crew
   ```

2. **Setup backend**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

3. **Setup frontend**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

4. **Access the application**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - Dashboard: http://localhost:3000/dashboard

## Dashboard Features

The new dashboard provides:
- **Overview Metrics**: Total sessions, searches, success rates
- **Activity Tracking**: Hourly and daily usage patterns
- **Top Companies**: Most searched companies
- **Recent Activity**: Latest search operations
- **Financial Insights**: Analysis summary and sentiment tracking

## Development

This enhancement adds comprehensive usage tracking and analytics capabilities to help users monitor system performance and gain insights into their sales lead generation activities.