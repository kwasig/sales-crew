# Usage Dashboard Implementation

## Overview

This implementation adds a comprehensive usage dashboard to the Sales Agent Crew application, addressing **Issue #27: "We need a new usage component for the agents"**. The dashboard provides real-time metrics and analytics for agent usage tracking.

## Features

### Frontend Dashboard Component
- **Real-time Metrics**: Display of total searches, today's usage, and performance statistics
- **Agent Usage Tracking**: Separate tracking for lead generation and financial analysis agents
- **Performance Analytics**: Average response time and success rate monitoring
- **Recent Activity Feed**: Live feed of user actions with timestamps
- **Auto-refresh**: Updates every 30 seconds for live data

### Backend Metrics API
- **Usage Tracking**: RESTful API for tracking user actions and agent usage
- **Performance Metrics**: Automatic calculation of response times and success rates
- **In-memory Storage**: Lightweight storage with persistence capabilities
- **CORS Support**: Cross-origin support for frontend integration

## Implementation Details

### Files Added

1. **`/backend/api/metrics_api.py`**
   - FastAPI-based metrics tracking service
   - Endpoints: `/track-usage` (POST), `/usage-metrics` (GET)
   - In-memory storage with automatic cleanup

2. **`/frontend/sales-agent-crew/src/components/UsageDashboard.vue`**
   - Vue.js component for displaying usage metrics
   - Responsive design with Tailwind CSS
   - Real-time data fetching and auto-refresh

3. **`/backend/main.py`**
   - Unified API entry point combining all services
   - Multi-port configuration for individual services

### Integration Points

- **MainLayout.vue**: Dashboard integrated into the main application layout
- **Usage Tracking**: Automatic tracking of lead generation and financial analysis actions
- **User Context**: User-specific metrics using Clerk authentication

## API Endpoints

### Track Usage
```
POST http://localhost:8001/track-usage
Content-Type: application/json

{
  "user_id": "user_123",
  "action": "lead_generation",
  "duration": 2.5,
  "success": true
}
```

### Get Usage Metrics
```
GET http://localhost:8001/usage-metrics

Response:
{
  "total_searches": 15,
  "today_usage": 3,
  "recent_activity": [...],
  "performance_stats": {
    "average_response_time": 1.2,
    "success_rate": 95.0,
    "total_errors": 1
  },
  "agent_usage": {
    "lead_generation": 10,
    "financial_analysis": 5
  }
}
```

## Setup and Running

### Backend Services
```bash
cd backend

# Option 1: Run individual services
python -m api.metrics_api
python -m api.financial_analysis_api  
python -m api.lead_generation_api

# Option 2: Run unified server
python main.py
```

### Frontend
```bash
cd frontend/sales-agent-crew
npm run dev
```

## Configuration

### Environment Variables
```bash
# CORS settings
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174

# API Keys (already configured in existing services)
PERPLEXITY_API_KEY=your_key
OPENAI_API_KEY=your_key
```

## Data Storage

Currently uses in-memory storage for simplicity. For production use:
- Replace with database (PostgreSQL recommended)
- Add data persistence
- Implement backup and recovery

## Future Enhancements

1. **Database Integration**: Persistent storage for historical data
2. **Advanced Analytics**: Trend analysis and predictive insights
3. **User Management**: Role-based access to metrics
4. **Export Functionality**: CSV/PDF reports
5. **Real-time Updates**: WebSocket connections for live dashboards

## Testing

### Manual Testing
1. Start the backend services
2. Launch the frontend application
3. Perform searches and financial analysis
4. Verify metrics update in real-time

### Automated Testing
- Unit tests for metrics calculation
- Integration tests for API endpoints
- E2E tests for dashboard functionality

## Dependencies

- FastAPI (backend)
- Vue.js 3 (frontend)
- Tailwind CSS (styling)
- Clerk (authentication)

## Performance Considerations

- In-memory storage suitable for development
- Consider Redis for production caching
- Implement rate limiting for API endpoints
- Add pagination for activity logs

## Security

- CORS configured for frontend domains
- User authentication via Clerk
- Input validation on API endpoints
- Rate limiting recommended for production

---

This implementation provides a solid foundation for agent usage tracking and can be extended based on specific business requirements.