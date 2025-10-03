# API Documentation Standards

This document outlines the standards for API documentation in RJW-IDD projects.

## OpenAPI Specification

All APIs must include OpenAPI 3.0+ specifications:

```yaml
openapi: 3.0.3
info:
  title: RJW-IDD API
  version: 1.0.0
  description: API for RJW-IDD functionality
servers:
  - url: https://api.example.com/v1
    description: Production server
paths:
  /health:
    get:
      summary: Health check endpoint
      responses:
        '200':
          description: Service is healthy
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    enum: [healthy, unhealthy]
                  timestamp:
                    type: string
                    format: date-time
```

## API Documentation Structure

### 1. Endpoint Documentation
Each endpoint must document:

- **Purpose**: What the endpoint does
- **Method**: HTTP method (GET, POST, PUT, DELETE, etc.)
- **Path**: URL path with parameters
- **Authentication**: Required auth method
- **Request Body**: Schema and examples
- **Response**: Success and error responses
- **Rate Limits**: Applicable limits
- **Examples**: Code examples in multiple languages

### 2. Schema Documentation
All data schemas must include:

- **Type definitions**: Clear type specifications
- **Validation rules**: Required fields, constraints
- **Examples**: Valid and invalid examples
- **Deprecation notices**: For deprecated fields

### 3. Error Documentation
Standard error responses:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input parameters",
    "details": {
      "field": "email",
      "reason": "Invalid email format"
    },
    "timestamp": "2025-10-03T10:00:00Z",
    "request_id": "req-12345"
  }
}
```

## Documentation Tools

### Recommended Tools
- **OpenAPI Generator**: Generate client SDKs
- **Swagger UI**: Interactive API documentation
- **Redoc**: Clean API documentation
- **Spectral**: OpenAPI linting

### CI Integration
```yaml
- name: Validate OpenAPI specs
  run: |
    npm install -g @stoplight/spectral
    spectral lint api/openapi.yaml
```

## Code Examples

### Python Client
```python
import requests

class RJWIDDClient:
    def __init__(self, base_url: str, api_key: str):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        })

    def get_health(self) -> dict:
        """Get service health status."""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
```

### JavaScript Client
```javascript
class RJWIDDClient {
  constructor(baseURL, apiKey) {
    this.baseURL = baseURL;
    this.apiKey = apiKey;
  }

  async getHealth() {
    const response = await fetch(`${this.baseURL}/health`, {
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    return response.json();
  }
}
```

## Testing API Documentation

### Contract Testing
```python
import pytest
from openapi_spec_validator import validate_spec
from openapi_core import create_spec

def test_openapi_spec_valid():
    """Validate OpenAPI specification."""
    with open('api/openapi.yaml') as f:
        spec = yaml.safe_load(f)

    validate_spec(spec)

def test_api_contract(client, spec):
    """Test API against OpenAPI contract."""
    # Use openapi-core for contract testing
    spec = create_spec(spec)

    response = client.get('/health')
    result = spec.validate_response(response)

    assert result.errors == []
```

## Versioning

### API Versioning Strategy
- **URL Path**: `/v1/resource`
- **Header**: `Accept: application/vnd.rjw-idd.v1+json`
- **Query Parameter**: `?version=1`

### Deprecation Policy
1. **Announce**: Deprecation notice in documentation
2. **Grace Period**: 6 months minimum
3. **Sunset**: Remove deprecated endpoints
4. **Communication**: Email/API changelog notifications

## Security Documentation

### Authentication
```yaml
components:
  securitySchemes:
    bearerAuth:
      type: http
      scheme: bearer
      bearerFormat: JWT
    apiKey:
      type: apiKey
      in: header
      name: X-API-Key
```

### Rate Limiting
Document rate limits in API responses:
```json
{
  "error": "rate_limit_exceeded",
  "retry_after": 60,
  "limit": 100,
  "remaining": 0,
  "reset_time": "2025-10-03T11:00:00Z"
}
```

## Monitoring and Observability

### Metrics to Track
- Response time percentiles (p50, p95, p99)
- Error rates by endpoint
- Rate limit hits
- Payload sizes
- Geographic distribution

### Logging Standards
```json
{
  "timestamp": "2025-10-03T10:00:00Z",
  "level": "INFO",
  "service": "rjw-idd-api",
  "request_id": "req-12345",
  "method": "GET",
  "path": "/health",
  "status_code": 200,
  "response_time_ms": 45,
  "user_agent": "RJWIDDClient/1.0",
  "ip": "192.168.1.1"
}
```