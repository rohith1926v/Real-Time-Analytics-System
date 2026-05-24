# Backend API

The backend is the FastAPI service layer for the Real-Time Streaming Analytics System. It exposes health checks and Phase 5 query APIs over locally persisted PostgreSQL and Elasticsearch data.

## Query APIs

- `GET /api/v1/analytics/summary`
- `GET /api/v1/events/recent`
- `GET /api/v1/predictions/recent`
- `GET /api/v1/predictions/{entity_id}`
- `GET /api/v1/risks/high`
- `GET /api/v1/search/events?q=...`
- `GET /api/v1/dashboard/overview`
- `GET /api/v1/dashboard/system-health`
- `GET /api/v1/dashboard/risk-trends`
- `GET /api/v1/dashboard/event-volume`
- `GET /api/v1/dashboard/severity-distribution`
- `GET /api/v1/dashboard/top-entities`
- `WS /api/v1/ws/dashboard`
- `GET /api/v1/alerts/recent`
- `GET /api/v1/alerts/high`
- `GET /api/v1/alerts/critical`
- `GET /api/v1/incidents/recent`
- `GET /api/v1/incidents/{incident_id}`
- `GET /api/v1/incidents/open`
- `GET /api/v1/alerts/stats`
- `GET /api/v1/alerts/search?q=...`
- `PATCH /api/v1/alerts/{alert_id}/status`
- `PATCH /api/v1/incidents/{incident_id}/status`
- `WS /api/v1/ws/alerts`
- `GET /api/v1/monitoring/overview`
- `GET /api/v1/monitoring/services`
- `GET /api/v1/monitoring/pipeline`
- `GET /api/v1/monitoring/errors`
- `GET /api/v1/monitoring/metrics-summary`
- `GET /metrics`

## Data Sources

- PostgreSQL stores structured telemetry, metrics, features, predictions, and dead letters.
- Elasticsearch backs search queries and is optional-safe.
- Prometheus backs monitoring summaries when available.
- Existing health endpoint remains available at `GET /api/v1/health`.

## Local Development

```bash
uvicorn app.main:app --reload
```

When running through Docker Compose, the backend uses:

```text
DATABASE_URL=postgresql+psycopg://streaming_user:streaming_password@streaming-analytics-postgres:5432/streaming_analytics
ELASTICSEARCH_HOST=http://streaming-analytics-elasticsearch:9200
PROMETHEUS_URL=http://streaming-analytics-prometheus:9090
```
