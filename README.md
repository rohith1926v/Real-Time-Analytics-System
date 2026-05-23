# Real-Time Streaming Analytics Platform

An enterprise-grade foundation for a real-time streaming analytics platform. Phase 1 establishes the monorepo, development environment, service boundaries, API shell, UI shell, and Docker workflow that later phases will extend with Kafka, Spark Structured Streaming, anomaly detection, operational storage, observability, and cloud deployment.

This repository is intentionally structured like a production engineering codebase: clear ownership boundaries, environment-driven configuration, containerized local workflows, typed frontend code, modular backend services, and documentation-first architecture decisions.

## Architecture

The platform is organized as a monorepo with independently deployable application surfaces and dedicated folders for future streaming, processing, machine learning, infrastructure, and observability work.

- `frontend` contains the React analytics console built with Vite, TypeScript, Tailwind CSS, React Router, and Axios.
- `backend` contains the FastAPI service layer with versioned APIs, settings management, logging, CORS configuration, schemas, services, and database placeholders.
- `kafka-producers`, `spark-jobs`, and `ml-models` are reserved for later platform capabilities.
- `infrastructure`, `monitoring`, `docs`, and `architecture` hold operational assets and engineering documentation.

## Tech Stack

| Layer | Technologies |
| --- | --- |
| Frontend | React, Vite, TypeScript, Tailwind CSS, React Router, Axios |
| Backend | FastAPI, Python 3.11, Uvicorn, Pydantic, SQLAlchemy |
| Infrastructure | Docker, Docker Compose |
| Future Platform | Kafka, Spark Structured Streaming, PostgreSQL, Elasticsearch, Redis, ML services, observability stack |

## Folder Structure

```text
streaming-analytics-system/
├── frontend/
├── backend/
├── kafka-producers/
├── spark-jobs/
├── ml-models/
├── infrastructure/
├── monitoring/
├── datasets/
├── docs/
├── architecture/
├── .env.example
├── .gitignore
├── docker-compose.yml
├── README.md
└── LICENSE
```

## Local Setup

### Prerequisites

- Docker Desktop
- Node.js 20+
- Python 3.11+
- Git

### Environment Configuration

Create local environment files from the examples:

```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

## Docker Development

Start the full Phase 1 development environment:

```bash
docker compose up --build
```

Services:

- Frontend: `http://localhost:5173`
- Backend API: `http://localhost:8000`
- API health check: `http://localhost:8000/api/v1/health`
- OpenAPI docs: `http://localhost:8000/docs`
- Kafka UI: `http://localhost:8080`

The Compose setup mounts source directories for hot reload and runs application and streaming services on a shared Docker network.

## Kafka Streaming Foundation

Phase 2 adds a local Kafka telemetry pipeline:

```text
Synthetic Event Generator -> Kafka Producer -> Kafka Topics -> Kafka Consumer -> Validated Telemetry
```

Kafka services:

- `streaming-analytics-zookeeper`
- `streaming-analytics-kafka`
- `streaming-analytics-kafka-ui`
- `streaming-analytics-producer`
- `streaming-analytics-consumer`

Topics:

- `telemetry.login.events`
- `telemetry.api.events`
- `telemetry.network.events`
- `telemetry.anomaly.events`
- `telemetry.deadletter.events`

Verification commands:

```bash
docker ps
docker logs streaming-analytics-producer --tail 100
docker logs streaming-analytics-consumer --tail 100
docker exec streaming-analytics-kafka kafka-topics --bootstrap-server localhost:9092 --list
```

Detailed Phase 2 documentation is available in `docs/phase-2-kafka-streaming.md`.

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

The frontend includes a professional dashboard shell, responsive sidebar layout, top navigation, typed API client, environment configuration, and a scalable folder structure for future product modules.

## Development Workflow

1. Create a feature branch from `main`.
2. Keep backend changes inside versioned API, schema, service, and data-access boundaries.
3. Keep frontend changes modular by colocating reusable UI in `components`, page surfaces in `pages`, and integration code in `api` or `services`.
4. Run services through Docker Compose for integration checks.
5. Add documentation or architecture notes when introducing new subsystems.

## Phase Roadmap

- Phase 1: Monorepo foundation, FastAPI shell, React shell, Docker development workflow.
- Phase 2: Kafka broker, topic initialization, synthetic telemetry producer, validating consumer, dead-letter support.
- Phase 3: PostgreSQL, Redis, persistent domain models, migrations, service contracts.
- Phase 4: Spark Structured Streaming jobs and batch replay strategy.
- Phase 5: ML anomaly detection service and model lifecycle foundations.
- Phase 6: Elasticsearch indexing, analytics APIs, and dashboard modules.
- Phase 7: Monitoring, alerting, tracing, CI/CD, and cloud deployment.

## Current Scope

Phase 2 implements Kafka streaming infrastructure only. Spark, ML pipelines, dashboard integration, and production data stores remain future phases.
