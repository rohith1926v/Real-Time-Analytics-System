# Real-Time Streaming Analytics System

An enterprise-grade streaming analytics platform foundation for cybersecurity and operational telemetry. The system now includes a React analytics console, FastAPI service layer, Kafka telemetry streaming infrastructure, and a Spark Structured Streaming analytics engine.

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
    -> future APIs, storage, search, and dashboards
```

Current platform components:

- `frontend`: React, Vite, TypeScript, Tailwind CSS dashboard shell.
- `backend`: FastAPI application with versioned APIs, settings management, CORS, logging, and health checks.
- `kafka-producers`: Synthetic telemetry producer and validating Kafka consumer.
- `spark-jobs`: Spark Structured Streaming analytics pipeline.
- `ml-models`: Isolation Forest training pipeline and real-time ML inference worker.
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
| Infrastructure | Docker, Docker Compose |
| Future Platform | PostgreSQL, Elasticsearch, Redis, observability stack, CI/CD, cloud deployment |

## Folder Structure

```text
streaming-analytics-system/
  frontend/
  backend/
  kafka-producers/
  spark-jobs/
  ml-models/
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
- Phase 5: PostgreSQL, Redis, persistent domain models, migrations, and service contracts.
- Phase 6: Elasticsearch indexing, analytics APIs, and dashboard modules.
- Phase 7: Monitoring, alerting, tracing, CI/CD, and cloud deployment.

## Current Scope

The implemented platform currently covers the enterprise foundation, Kafka streaming infrastructure, Spark Structured Streaming analytics pipeline, and ML anomaly detection inference. Database storage, Elasticsearch, dashboard ML visualizations, MLflow, and Kubernetes are intentionally reserved for later phases.
