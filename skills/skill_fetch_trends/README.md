# Skill: fetch_trends

## Overview

Retrieve trending topics from social media platforms for campaign targeting and content optimization.

**SRS Reference**: §4.2 Perception (FR2.2 Campaign Context Enrichment)  
**Spec Reference**: `specs/functional.md`, FR2.2 (lines 67-82)

## Purpose

This skill enables Chimera agents to:
1. Query real-time trending topics from social platforms
2. Filter trends by category and geographic region
3. Analyze trend sentiment for campaign alignment
4. Enrich campaign context with market intelligence

## Input Schema

### Parameters

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `platform` | string | **Yes** | - | Social platform identifier |
| `category` | string | No | null | Topic category filter |
| `region` | string | No | "GLOBAL" | Geographic region |
| `limit` | integer | No | 10 | Maximum trends to return (1-50) |

### Valid Values

**platform**:
- `twitter` - Twitter/X trending topics
- `instagram` - Instagram trending hashtags
- `tiktok` - TikTok trending sounds/hashtags
- `reddit` - Reddit trending subreddits

**category**:
- `tech` - Technology and innovation
- `fashion` - Fashion and style
- `sports` - Sports and athletics
- `entertainment` - Movies, TV, music
- `politics` - Political topics
- `business` - Business and finance

**region**:
- `US` - United States
- `EU` - European Union
- `ASIA` - Asia-Pacific
- `GLOBAL` - Worldwide trends

### Input Example

```json
{
  "platform": "twitter",
  "category": "tech",
  "region": "US",
  "limit": 5
}
```

### Input JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FetchTrendsInput",
  "type": "object",
  "required": ["platform"],
  "properties": {
    "platform": {
      "type": "string",
      "enum": ["twitter", "instagram", "tiktok", "reddit"]
    },
    "category": {
      "type": "string",
      "enum": ["tech", "fashion", "sports", "entertainment", "politics", "business"]
    },
    "region": {
      "type": "string",
      "enum": ["US", "EU", "ASIA", "GLOBAL"],
      "default": "GLOBAL"
    },
    "limit": {
      "type": "integer",
      "minimum": 1,
      "maximum": 50,
      "default": 10
    }
  }
}
```

---

## Output Schema

### Response Fields

| Field | Type | Description |
|-------|------|-------------|
| `trends` | array | List of trending topics |
| `trends[].topic` | string | Trending topic or hashtag |
| `trends[].volume` | integer | Post/mention volume (24h) |
| `trends[].sentiment` | number | Sentiment score (-1.0 to 1.0) |
| `trends[].growth_rate` | number | Growth rate percentage |
| `trends[].retrieved_at` | string | ISO 8601 timestamp |
| `metadata` | object | Request metadata |
| `metadata.platform` | string | Platform queried |
| `metadata.total_trends` | integer | Total trends available |
| `metadata.cache_hit` | boolean | Whether result was cached |

### Output Example

```json
{
  "trends": [
    {
      "topic": "#AI2026",
      "volume": 125000,
      "sentiment": 0.72,
      "growth_rate": 45.3,
      "retrieved_at": "2026-02-06T16:50:00Z"
    },
    {
      "topic": "#TechInnovation",
      "volume": 98000,
      "sentiment": 0.85,
      "growth_rate": 32.1,
      "retrieved_at": "2026-02-06T16:50:00Z"
    },
    {
      "topic": "#FutureOfWork",
      "volume": 87500,
      "sentiment": 0.61,
      "growth_rate": 28.7,
      "retrieved_at": "2026-02-06T16:50:00Z"
    }
  ],
  "metadata": {
    "platform": "twitter",
    "total_trends": 50,
    "cache_hit": false
  }
}
```

### Output JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "FetchTrendsOutput",
  "type": "object",
  "required": ["trends", "metadata"],
  "properties": {
    "trends": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["topic", "volume", "sentiment", "retrieved_at"],
        "properties": {
          "topic": { "type": "string" },
          "volume": { "type": "integer", "minimum": 0 },
          "sentiment": { "type": "number", "minimum": -1.0, "maximum": 1.0 },
          "growth_rate": { "type": "number" },
          "retrieved_at": { "type": "string", "format": "date-time" }
        }
      }
    },
    "metadata": {
      "type": "object",
      "properties": {
        "platform": { "type": "string" },
        "total_trends": { "type": "integer" },
        "cache_hit": { "type": "boolean" }
      }
    }
  }
}
```

---

## Dependencies

### External APIs
- **Twitter API v2**: Trending topics endpoint
- **Instagram Graph API**: Trending hashtags
- **TikTok API**: Trending sounds/hashtags
- **Reddit API**: Trending subreddits

### Internal Services
- **MCP Gateway**: Capability token validation and billing
- **Redis**: Trend caching (5-minute TTL)
- **Tenx MCP Sense**: Telemetry logging

### Python Packages
```
requests>=2.31.0
redis>=5.0.0
jsonschema>=4.20.0
```

---

## Usage Example

### From Worker Agent

```python
from mcp_client import MCPGateway

# Initialize MCP Gateway
gateway = MCPGateway()

# Request capability token
token = gateway.request_capability(
    capability_name="fetch_trends",
    soul_id="chimera:agent:uuid-123",
    max_spend=1.00
)

# Call skill
result = gateway.call_skill(
    token=token,
    skill_name="fetch_trends",
    input_data={
        "platform": "twitter",
        "category": "tech",
        "region": "US",
        "limit": 5
    }
)

# Use trends for content generation
trends = result["trends"]
top_trend = trends[0]["topic"]
print(f"Top trending topic: {top_trend}")
```

### From Planner (Campaign Context)

```python
# Enrich campaign manifest with trending topics
trends = fetch_trends_skill.execute({
    "platform": "twitter",
    "category": campaign.category,
    "region": campaign.target_region,
    "limit": 10
})

# Store trends in campaign context
campaign_manifest["context"]["trending_topics"] = trends["trends"]
```

---

## Error Handling

### Error Response Format

```json
{
  "status": "FAILED",
  "error": {
    "error_code": "API_RATE_LIMIT",
    "error_message": "Twitter API rate limit exceeded",
    "retry_after": 900
  }
}
```

### Error Codes

| Code | Description | Retry Strategy |
|------|-------------|----------------|
| `API_RATE_LIMIT` | Platform API rate limit exceeded | Wait `retry_after` seconds |
| `INVALID_PLATFORM` | Unsupported platform | Fix input, no retry |
| `AUTHENTICATION_FAILED` | API credentials invalid | Check MCP config |
| `NETWORK_ERROR` | Network connectivity issue | Exponential backoff |
| `CAPABILITY_DENIED` | Insufficient capability token | Request new token |

---

## Performance Characteristics

### Latency
- **Cache Hit**: < 50ms
- **Cache Miss**: 500-2000ms (depends on platform API)

### Cost
- **Per Call**: $0.10 USD
- **Rate Limit**: 100 calls/hour per agent

### Caching
- **TTL**: 5 minutes
- **Cache Key**: `trends:{platform}:{category}:{region}`

---

## Testing

### Unit Tests

```python
# tests/test_fetch_trends.py

def test_fetch_trends_twitter_success():
    input_data = {
        "platform": "twitter",
        "category": "tech",
        "limit": 5
    }
    
    result = fetch_trends.execute_skill(input_data)
    
    assert "trends" in result
    assert len(result["trends"]) <= 5
    assert all("topic" in t for t in result["trends"])
    assert all("sentiment" in t for t in result["trends"])

def test_fetch_trends_invalid_platform():
    input_data = {
        "platform": "invalid_platform"
    }
    
    with pytest.raises(jsonschema.ValidationError):
        fetch_trends.execute_skill(input_data)

def test_fetch_trends_cache_hit():
    # First call (cache miss)
    result1 = fetch_trends.execute_skill({"platform": "twitter"})
    assert result1["metadata"]["cache_hit"] is False
    
    # Second call (cache hit)
    result2 = fetch_trends.execute_skill({"platform": "twitter"})
    assert result2["metadata"]["cache_hit"] is True
```

---

## Security Considerations

1. **API Key Protection**: Twitter/Instagram API keys stored in MCP Gateway secrets
2. **Rate Limiting**: Enforced at MCP Gateway level
3. **Input Validation**: All inputs validated against JSON schema
4. **Output Sanitization**: Trend topics sanitized to prevent XSS
5. **Capability Tokens**: Required for all skill calls

---

## Future Enhancements

- [ ] Support for LinkedIn trending topics
- [ ] Historical trend analysis (7-day, 30-day)
- [ ] Trend prediction using ML models
- [ ] Multi-platform trend correlation
- [ ] Real-time trend streaming (WebSocket)

---

**Skill Version**: 1.0.0  
**Last Updated**: 2026-02-06  
**Owner**: Skills Team  
**Status**: Specification Complete (Implementation Pending)
