# Langfuse Integration Guide

This document describes the Langfuse logging integration for the Sales Crew AI agents, providing comprehensive observability and monitoring capabilities.

## Overview

Langfuse is an open-source LLM observability platform that helps you monitor, debug, and improve your AI applications. This integration adds tracing, metrics, and logging to the CrewAI agents in the sales-crew repository.

## Features

- **End-to-end tracing** - Track requests through the entire pipeline
- **Agent-level observability** - Monitor individual agent performance
- **Tool execution tracking** - Log external API calls (Exa, SambaNova)
- **Error tracking** - Capture and analyze failures
- **Performance metrics** - Measure execution times and bottlenecks
- **Token usage monitoring** - Track LLM costs

## Setup

### 1. Install Dependencies

The Langfuse package has been added to `requirements.txt`:

```bash
pip install -r backend/requirements.txt
```

### 2. Configure Environment Variables

Copy the template and add your API keys:

```bash
cp backend/.env.template backend/.env
```

Edit `backend/.env` with your credentials:

```env
# Required API Keys
SAMBANOVA_API_KEY=your_sambanova_key_here
EXA_API_KEY=your_exa_key_here

# Langfuse Configuration (Optional but Recommended)
LANGFUSE_PUBLIC_KEY=pk-lf-your-public-key
LANGFUSE_SECRET_KEY=sk-lf-your-secret-key
LANGFUSE_HOST=https://cloud.langfuse.com
LANGFUSE_ENABLED=true
```

### 3. Get Langfuse API Keys

1. Sign up at [cloud.langfuse.com](https://cloud.langfuse.com)
2. Create a new project
3. Go to Project Settings > API Keys
4. Copy your Public Key and Secret Key

## Architecture

### Integration Layers

The Langfuse integration is implemented across 4 layers:

```
┌─────────────────────────────────────────────┐
│  Layer 1: API Entry Points                  │
│  - Request/response tracking                │
│  - User identification                      │
│  - Error capture                            │
└─────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────┐
│  Layer 2: Crew Execution                    │
│  - Pipeline orchestration                   │
│  - Input/output logging                     │
│  - Execution metrics                        │
└─────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────┐
│  Layer 3: Agent/Task Level                  │
│  - Individual agent spans                   │
│  - Task execution tracking                  │
│  - Tool usage monitoring                    │
└─────────────────────────────────────────────┘
                         │
┌─────────────────────────────────────────────┐
│  Layer 4: Tool/Service Level                │
│  - External API calls                       │
│  - LLM interactions                         │
│  - Performance metrics                      │
└─────────────────────────────────────────────┘
```

### Key Components

#### 1. LangfuseManager (`utils/langfuse_utils.py`)

Singleton manager for Langfuse client initialization:

```python
from utils.langfuse_utils import langfuse_manager

# Check if Langfuse is enabled
if langfuse_manager.is_enabled:
    client = langfuse_manager.client
    # Use client...
```

#### 2. Decorators

The `@observe` decorator from Langfuse is used to automatically trace functions:

```python
from langfuse.decorators import observe

@observe(as_type="span")
def my_function():
    # This function will be automatically traced
    pass
```

#### 3. Manual Instrumentation

For more control, use the Langfuse client directly:

```python
from utils.langfuse_utils import get_langfuse_client

langfuse = get_langfuse_client()
if langfuse:
    trace = langfuse.trace(
        name="my_operation",
        metadata={"key": "value"}
    )
```

## Usage

### Running with Langfuse

1. Start the API server:

```bash
cd backend
python api/lead_generation_api.py
```

2. Make a request:

```bash
curl -X POST http://localhost:8000/generate-leads \
  -H "Content-Type: application/json" \
  -H "x-sambanova-key: your_key" \
  -H "x-exa-key: your_key" \
  -d '{"prompt": "Find AI hardware startups in Silicon Valley"}'
```

3. View traces in Langfuse dashboard

### Health Check

Check if Langfuse is enabled:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "langfuse_enabled": true
}
```

## Trace Structure

Each request creates a trace with the following structure:

```
Trace: lead_generation_request
├── Span: prompt_extraction (50ms)
├── Span: crew_execution (2.3s)
│   ├── Span: aggregator_search (800ms)
│   │   └── Span: exa_api_call (600ms)
│   ├── Span: data_extraction (400ms)
│   ├── Span: data_enrichment (300ms)
│   ├── Span: market_trends (500ms)
│   │   └── Span: exa_api_call (400ms)
│   ├── Span: financial_analysis (600ms)
│   │   └── Span: exa_api_call (500ms)
│   └── Span: outreach_generation (200ms)
└── Span: response_formatting (20ms)
```

## Metrics Tracked

### Performance Metrics
- Execution time for each agent/task
- API response times (Exa, SambaNova)
- Total pipeline duration
- Token usage per agent

### Quality Metrics
- Number of companies found
- Data completeness score
- Email generation success rate
- Prompt extraction accuracy

### Error Tracking
- API failures (Exa, SambaNova)
- Crew execution failures
- Tool execution errors
- Validation errors

## Configuration Options

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGFUSE_PUBLIC_KEY` | Public API key from Langfuse | Required |
| `LANGFUSE_SECRET_KEY` | Secret API key from Langfuse | Required |
| `LANGFUSE_HOST` | Langfuse server URL | `https://cloud.langfuse.com` |
| `LANGFUSE_ENABLED` | Enable/disable Langfuse | `true` |

### Disabling Langfuse

To run without Langfuse:

```env
LANGFUSE_ENABLED=false
```

Or simply don't set the Langfuse API keys.

## Troubleshooting

### Langfuse not initializing

**Problem**: "Warning: Langfuse credentials not found. Tracing disabled."

**Solution**: 
- Check that `.env` file exists in `backend/` directory
- Verify `LANGFUSE_PUBLIC_KEY` and `LANGFUSE_SECRET_KEY` are set
- Ensure keys are correct (no extra spaces)

### Traces not appearing in dashboard

**Problem**: Requests are processed but no traces appear

**Solution**:
1. Check Langfuse initialization message on startup
2. Verify internet connectivity to Langfuse host
3. Check Langfuse API key permissions
4. Look for error messages in console output
5. Ensure `langfuse_manager.flush()` is called

### Performance impact

**Problem**: Noticeable slowdown with Langfuse enabled

**Solution**:
- Langfuse has minimal overhead (<5% typically)
- Check network latency to Langfuse host
- Consider batching or async flushing
- Use Langfuse cloud for better performance

## Best Practices

### 1. Sensitive Data

The integration automatically excludes API keys from traces. No sensitive data is logged.

### 2. Error Handling

Always use try/except blocks and log errors to Langfuse:

```python
try:
    result = crew.execute_research(inputs)
except Exception as e:
    if langfuse_client:
        langfuse_client.event(
            name="error",
            status="error",
            metadata={"error": str(e)}
        )
    raise
```

### 3. Flushing Events

Events are automatically flushed at the end of each request using FastAPI's `BackgroundTasks`.

### 4. Trace Context

Use `langfuse_context` to add metadata to current observation:

```python
from langfuse.decorators import langfuse_context

langfuse_context.update_current_observation(
    metadata={"key": "value"},
    input={"data": "..."},
    output={"result": "..."}
)
```

## Monitoring and Alerting

### Key Metrics to Monitor

1. **Success Rate**: Percentage of successful crew executions
2. **Latency**: P95 and P99 execution times
3. **Error Rate**: Failures by agent and error type
4. **Token Usage**: Daily/weekly token consumption
5. **API Health**: Exa and SambaNova availability

### Setting Up Alerts

In Langfuse dashboard:

1. Go to Project Settings > Alerts
2. Create alerts for:
   - High error rates (>5%)
   - Slow execution times (>30s)
   - API failures
   - Token usage spikes

## Cost Considerations

### Langfuse Pricing

- **Free Tier**: 100k events/month
- **Pro Tier**: $29/month for 1M events
- **Team Tier**: $99/month for 5M events

The sales-crew integration typically generates:
- 1 trace per API request
- 6-8 spans per trace (agents + tools)
- 10-15 events per trace (LLM calls, API calls)

**Estimated usage**: ~25 events per lead generation request

### Optimization Tips

1. **Sampling**: For high-volume deployments, implement trace sampling
2. **Filtering**: Exclude health check endpoints
3. **Batching**: Group related events when possible
4. **Retention**: Configure data retention in Langfuse settings

## Security

### Data Privacy

- No API keys or credentials are logged
- Prompts and responses are captured for debugging
- Consider data retention policies for your use case
- Langfuse is GDPR compliant

### Self-Hosting Option

For enhanced privacy, you can self-host Langfuse:

```env
LANGFUSE_HOST=http://your-langfuse-instance.com
```

See [Langfuse self-hosting guide](https://langfuse.com/docs/deployment/self-host) for details.

## Support

### Resources

- [Langfuse Documentation](https://langfuse.com/docs)
- [Langfuse GitHub](https://github.com/langfuse/langfuse)
- [CrewAI Documentation](https://docs.crewai.com)

### Getting Help

1. Check Langfuse logs for error messages
2. Verify API keys and network connectivity
3. Review trace structure in dashboard
4. Open an issue on the sales-crew repository

## Contributing

To extend the Langfuse integration:

1. Add new spans using `@observe` decorator
2. Use `langfuse_context` for metadata
3. Follow existing patterns for consistency
4. Test with and without Langfuse enabled
5. Update this documentation

## License

This integration follows the same license as the sales-crew repository.