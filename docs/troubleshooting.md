# Troubleshooting Guide

## Docker Desktop Engine Errors

Symptoms:

```text
failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine
500 Internal Server Error for dockerDesktopLinuxEngine
```

Fix:

1. Restart Docker Desktop.
2. Wait until the engine reports running.
3. Run:

```bash
docker compose config --quiet
docker compose up --build -d
```

## Empty Dashboards

The platform is streaming and multi-stage. Let it run for several minutes so data can move through:

```text
producer -> Kafka -> Spark -> ML -> alert engine -> threat intelligence -> storage -> APIs
```

Then refresh the dashboard.

## Laptop Resource Pressure

Use light mode:

```bash
./scripts/start_light.sh
```

Windows:

```powershell
.\scripts\start_light.ps1
```

Light mode avoids the heaviest optional visualization/observability services by default.

## Phase 10 Verification In Light Mode

Phase 10 can be verified without running the full heavy stack. Light mode is valid as long as the repository structure, scripts, docs, Docker Compose config, frontend files, backend app, and core service folders are present.

Run:

```bash
python scripts/verify_phase_10.py
```

The verifier treats frontend, backend health, and backend docs HTTP checks as optional runtime probes. If those services are not running, the script prints `[WARN]` but still exits successfully when core files and Compose configuration are valid.

## Prometheus Target Down

Open:

```text
http://localhost:9090/targets
```

If a target is down:

- confirm the container is running with `docker ps`
- check its logs with `docker logs <container-name>`
- verify the metrics port from `scripts/health_check.py`

## Elasticsearch Slow Startup

Elasticsearch can take longer than the Python services. If search APIs are empty, wait and check:

```text
http://localhost:9200/_cluster/health
```

PostgreSQL-backed APIs should continue to work even when Elasticsearch is temporarily unavailable.

## Pytest Not Installed Locally

Install service dependencies before running tests:

```bash
pip install -r backend/requirements.txt
pip install -r ml-models/requirements.txt
pip install -r alert-engine/requirements.txt
pip install -r threat-intelligence-engine/requirements.txt
python -m pytest
```

## Frontend Build Warning

The Vite build may warn about a large chunk because the dashboard includes charts, graph visualization, and animation libraries. This is acceptable for the local portfolio build. Future production work can code-split routes.
