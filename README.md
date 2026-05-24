# Real-Time Streaming Analytics System

An enterprise-grade streaming analytics platform foundation for cybersecurity and operational telemetry. The system now includes a React analytics console, FastAPI service layer, Kafka telemetry streaming infrastructure, Spark Structured Streaming analytics engine, ML anomaly detection, SOC alerting, local persistence, and a free local observability stack.

This repository is structured as a production-oriented monorepo with clear service boundaries, environment-driven configuration, Dockerized local workflows, typed frontend code, modular backend services, resilient Kafka producers and consumers, and Spark jobs organized for maintainable distributed processing.

## Architecture

```text
Synthetic Telemetry Generator
    -> Kafka telemetry topics
    -> Spark Structured Streaming
    -> real-time transformations and window aggregations
    -> analytics Kafka topics
    -> ML anomaly detection
    -> prediction Kafka topics
    -> PostgreSQL, Elasticsearch, and Redis
    -> Alert engine and incident intelligence
    -> Threat intelligence and detection engineering
    -> FastAPI query APIs
    -> React real-time enterprise dashboard
    -> Prometheus and Grafana observability
```

Current platform components:

- `frontend`: React, Vite, TypeScript, Tailwind CSS dashboard shell.
- `backend`: FastAPI application with versioned APIs, settings management, CORS, logging, and health checks.
- `kafka-producers`: Synthetic telemetry producer and validating Kafka consumer.
- `spark-jobs`: Spark Structured Streaming analytics pipeline.
- `ml-models`: Isolation Forest training pipeline and real-time ML inference worker.
- `storage-sink`: Kafka persistence worker for PostgreSQL, Elasticsearch, and Redis.
- `alert-engine`: Real-time SOC alert generation, deduplication, and incident correlation.
- `threat-intelligence-engine`: IOC enrichment, detection rules, MITRE mapping, threat scoring, entity profiling, and attack timelines.
- `detections`: Local Sigma-like YAML detection rules.
- `monitoring`: Prometheus configuration and provisioned Grafana dashboards.
- `docs`: Phase documentation and operational runbooks.
- `infrastructure`, `monitoring`, `architecture`, `datasets`, `ml-models`: reserved platform areas for upcoming phases.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Frontend | React, Vite, TypeScript, Tailwind CSS, React Router, Axios |
| Backend | FastAPI, Python 3.11, Uvicorn, Pydantic, SQLAlchemy |
| Streaming | Apache Kafka, Zookeeper, Kafka UI, Python telemetry services |
| Processing | Apache Spark 3.5, PySpark, Structured Streaming, Spark Kafka connector |
| ML | scikit-learn, pandas, NumPy, joblib, Pydantic |
| Persistence/Search | PostgreSQL, Elasticsearch, Redis, SQLAlchemy |
| Dashboard | React, TypeScript, Tailwind CSS, Recharts, WebSocket API |
| Infrastructure | Docker, Docker Compose |
| Observability | Prometheus, Grafana, Python prometheus-client |
| Threat Intelligence | Local IOC feeds, YAML detection rules, MITRE ATT&CK mapping, D3, React Flow, Framer Motion |
| Future Platform | CI/CD, cloud deployment, Kubernetes, authentication/RBAC |

## Folder Structure

```text
streaming-analytics-system/
  frontend/
  backend/
  kafka-producers/
  spark-jobs/
  ml-models/
  storage-sink/
  infrastructure/
  monitoring/
  datasets/
  docs/
  architecture/
  .env.example
  .gitignore
  docker-compose.yml
  README.md
  LICENSE
```

## Local Setup

Prerequisites:

- Docker Desktop
- Node.js 20+
- Python 3.11+
- Git

Create local environment files from examples when developing outside Compose:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Docker Development

Start the full stack:

```bash
docker compose up --build -d
```

Verify containers:

```bash
docker ps --filter "name=streaming-analytics"
```

Service endpoints:

| Service | URL |
| --- | --- |
| Frontend | `http://localhost:5173` |
| Backend API | `http://localhost:8000` |
| Backend health | `http://localhost:8000/api/v1/health` |
| OpenAPI docs | `http://localhost:8000/docs` |
| Kafka UI | `http://localhost:8080` |
| Spark Master UI | `http://localhost:8081` |
| Spark Worker UI | `http://localhost:8082` |
| Spark Driver UI | `http://localhost:4040` |
| Prometheus | `http://localhost:9090` |
| Grafana | `http://localhost:3000` |
| Threat Intel metrics | `http://localhost:9106/metrics` |

Grafana default login is `admin / admin`.

## Kafka Streaming Foundation

Phase 2 provides the Kafka telemetry backbone:

```text
Synthetic Event Generator -> Kafka Producer -> Kafka Topics -> Kafka Consumer -> Validated Telemetry
```

Telemetry topics:

- `telemetry.login.events`
- `telemetry.api.events`
- `telemetry.network.events`
- `telemetry.anomaly.events`
- `telemetry.deadletter.events`

Kafka verification:

```bash
docker logs streaming-analytics-producer --tail 100
docker logs streaming-analytics-consumer --tail 100
docker exec streaming-analytics-kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Detailed Phase 2 documentation is available in `docs/phase-2-kafka-streaming.md`.

## Spark Structured Streaming

Phase 3 provides real-time distributed analytics processing:

```text
telemetry.* Kafka topics
    -> Spark Structured Streaming
    -> event normalization
    -> risk enrichment
    -> event-time window metrics
    -> streaming feature engineering
    -> analytics.* Kafka topics
```

Analytics output topics:

- `analytics.enriched.events`
- `analytics.window.metrics`
- `analytics.risk.metrics`
- `analytics.feature.engineering`

Spark verification:

```bash
docker logs streaming-analytics-spark-streaming --tail 200
docker exec streaming-analytics-kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic analytics.enriched.events --from-beginning --max-messages 3 --timeout-ms 30000
```

Windowed aggregate topics are event-time and watermark based, so they can take a few minutes to emit after startup. Enriched events should appear first.

Detailed Phase 3 documentation is available in `docs/phase-3-spark-streaming.md`.

## ML Anomaly Detection

Phase 4 adds real-time ML inference over Spark analytics streams:

```text
analytics.* Kafka topics
    -> ML feature parser
    -> Isolation Forest model
    -> anomaly scoring and severity classification
    -> ml.anomaly.predictions
```

Train model artifacts manually:

```bash
docker compose run --rm ml-inference python -m app.training.train_model
```

Run inference:

```bash
docker compose up --build -d ml-inference
docker logs -f streaming-analytics-ml-inference
```

Sample predictions:

```bash
docker exec streaming-analytics-kafka kafka-console-consumer --bootstrap-server localhost:9092 --topic ml.anomaly.predictions --from-beginning --max-messages 3 --timeout-ms 30000
```

Detailed Phase 4 documentation is available in `docs/phase-4-ml-anomaly-detection.md`.

## Database, Search, And Cache

Phase 5 persists and queries the streaming platform with local free services:

```text
Kafka topics
    -> storage sink consumer
    -> PostgreSQL structured tables
    -> Elasticsearch searchable indexes
    -> Redis latest-value and counter cache
    -> FastAPI query APIs
```

Local services:

- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`
- Elasticsearch: `http://localhost:9200`

Query APIs:

- `GET /api/v1/analytics/summary`
- `GET /api/v1/events/recent`
- `GET /api/v1/predictions/recent`
- `GET /api/v1/predictions/{entity_id}`
- `GET /api/v1/risks/high`
- `GET /api/v1/search/events?q=login`

Detailed Phase 5 documentation is available in `docs/phase-5-database-search.md`.

## Enterprise Real-Time Dashboard

Phase 6 adds a multi-page AI/security analytics dashboard:

- Overview: streaming KPIs, risk posture, charts, and recent events.
- Live Stream: real-time telemetry and prediction feed.
- Risk Analytics: trend, volume, severity, and top entity visualizations.
- ML Predictions: anomaly score, confidence, severity, explanations, and feature payloads.
- Search: Elasticsearch-backed event search.
- System Health: local service status for backend, database, cache, search, Kafka, Spark, and ML.

Frontend routes:

- `/`
- `/live`
- `/risk`
- `/predictions`
- `/search`
- `/health`

Dashboard APIs:

- `GET /api/v1/dashboard/overview`
- `GET /api/v1/dashboard/system-health`
- `GET /api/v1/dashboard/risk-trends`
- `GET /api/v1/dashboard/event-volume`
- `GET /api/v1/dashboard/severity-distribution`
- `GET /api/v1/dashboard/top-entities`
- `WS /api/v1/ws/dashboard` (`ws://localhost:8000/api/v1/ws/dashboard` locally)

Screenshots:

- Add overview screenshot after running the local dashboard.
- Add risk analytics screenshot after storage sink has persisted live records.

Detailed Phase 6 documentation is available in `docs/phase-6-enterprise-dashboard.md`.

## Real-Time Alert Engine And Incident Intelligence

Phase 7 adds a local SOC-style alert and incident layer:

```text
ML predictions + Spark analytics
    -> alert rules
    -> Redis deduplication
    -> incident correlation
    -> PostgreSQL + Elasticsearch
    -> FastAPI APIs + WebSocket
    -> Alerts and Incidents dashboard pages
```

Alert APIs:

- `GET /api/v1/alerts/recent`
- `GET /api/v1/alerts/high`
- `GET /api/v1/alerts/critical`
- `GET /api/v1/incidents/recent`
- `GET /api/v1/incidents/open`
- `GET /api/v1/alerts/stats`
- `GET /api/v1/alerts/search?q=...`
- `WS /api/v1/ws/alerts`

Dashboard routes:

- `/alerts`
- `/incidents`

Screenshots:

- Add alerts page screenshot after alert-engine has consumed live ML predictions.
- Add incidents page screenshot after correlated incidents are created.

Detailed Phase 7 documentation is available in `docs/phase-7-alert-engine.md`.

## Observability, Monitoring, And System Health

Phase 8 adds local Prometheus and Grafana monitoring for the platform:

```text
Service metrics endpoints
    -> Prometheus scrape targets
    -> provisioned Grafana dashboards
    -> FastAPI monitoring APIs
    -> React observability page
```

Metrics endpoints:

- Backend: `http://localhost:8000/metrics`
- ML inference: `http://localhost:9101/metrics`
- Storage sink: `http://localhost:9102/metrics`
- Alert engine: `http://localhost:9103/metrics`
- Telemetry producer: `http://localhost:9104/metrics`
- Telemetry consumer: `http://localhost:9105/metrics`

Monitoring APIs:

- `GET /api/v1/monitoring/overview`
- `GET /api/v1/monitoring/services`
- `GET /api/v1/monitoring/pipeline`
- `GET /api/v1/monitoring/errors`
- `GET /api/v1/monitoring/metrics-summary`

Dashboard route:

- `/observability`

Provisioned Grafana dashboards:

- System Overview
- Streaming Pipeline
- ML Inference
- SOC Alert Engine

Verification:

```bash
docker compose up --build -d
docker ps --filter "name=streaming-analytics"
```

Open:

- `http://localhost:9090/targets`
- `http://localhost:3000`
- `http://localhost:5173/observability`

Detailed Phase 8 documentation is available in `docs/phase-8-observability-monitoring.md`.

## Threat Intelligence And Detection Engineering

Phase 9 adds a local XDR-style detection layer:

```text
Kafka + Spark + ML predictions
    -> threat-intelligence-engine
    -> IOC enrichment
    -> YAML detection rules
    -> MITRE ATT&CK mapping
    -> threat scoring
    -> entity profiles and attack timelines
    -> React XDR investigation pages
```

Threat intelligence APIs:

- `GET /api/v1/threat-intel/overview`
- `GET /api/v1/threat-intel/iocs`
- `GET /api/v1/threat-intel/entities`
- `GET /api/v1/threat-intel/mitre`
- `GET /api/v1/threat-intel/attack-timeline`
- `GET /api/v1/threat-intel/risk-heatmap`
- `GET /api/v1/threat-intel/threat-graph`
- `GET /api/v1/threat-intel/search?q=...`
- `WS /api/v1/ws/threat-intel`

Detection and entity APIs:

- `GET /api/v1/detections/rules`
- `GET /api/v1/detections/rules/{rule_id}`
- `GET /api/v1/detections/rule-stats`
- `GET /api/v1/entities/{entity_id}`
- `GET /api/v1/entities/high-risk`
- `GET /api/v1/entities/search?q=...`
- `GET /api/v1/mitre/tactics`
- `GET /api/v1/mitre/techniques`

Dashboard routes:

- `/threat-intelligence`
- `/detection-engineering`
- `/threat-hunting`
- `/mitre-attack`
- `/entities`
- `/attack-timeline`

Detailed Phase 9 documentation is available in `docs/phase-9-threat-intelligence.md`.

## Backend Development

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

The backend uses environment-driven settings, centralized logging, CORS middleware, and versioned API routing under `/api/v1`.

## Frontend Development

```bash
cd frontend
npm install
npm run dev
```

The frontend includes a responsive dashboard shell, sidebar navigation, typed API client, environment configuration, and modular folder organization for future analytics modules.

## Development Workflow

1. Create a feature branch from `main`.
2. Keep backend changes inside API, schema, service, and data-access boundaries.
3. Keep frontend changes modular by colocating reusable UI in `components`, page surfaces in `pages`, and integration code in `api` or `services`.
4. Keep streaming code organized by schemas, producers, consumers, transformations, aggregations, sinks, and configuration.
5. Run integration checks through Docker Compose before pushing changes.
6. Update docs when introducing or changing platform subsystems.

## Phase Roadmap

- Phase 1: Monorepo foundation, FastAPI shell, React shell, Docker development workflow.
- Phase 2: Kafka broker, topic initialization, synthetic telemetry producer, validating consumer, dead-letter support.
- Phase 3: Spark Structured Streaming ingestion, transformations, window metrics, feature engineering, and analytics Kafka sinks.
- Phase 4: ML anomaly detection training pipeline, streaming inference worker, and prediction Kafka topic.
- Phase 5: Local PostgreSQL, Elasticsearch, Redis, storage sink persistence, and FastAPI query APIs.
- Phase 6: Enterprise real-time React dashboard, dashboard APIs, charts, tables, search, and WebSocket updates.
- Phase 7: Real-time alert engine, incident intelligence, deduplication, SOC APIs, and dashboard integration.
- Phase 8: Local/free Prometheus metrics, Grafana dashboards, monitoring APIs, and observability UI.
- Phase 9: Local threat intelligence, detection engineering, MITRE mapping, entity intelligence, and attack timeline visualization.
- Future: Tracing, CI/CD, cloud deployment, Kubernetes, authentication/RBAC.

## Current Scope

The implemented platform currently covers the enterprise foundation, Kafka streaming infrastructure, Spark Structured Streaming analytics pipeline, ML anomaly detection inference, local persistence/search/cache, dashboard visualization, SOC alert/incident intelligence, and local observability. MLflow, Kubernetes, external alert delivery, authentication/RBAC, distributed tracing, and cloud deployment are intentionally reserved for later phases.
