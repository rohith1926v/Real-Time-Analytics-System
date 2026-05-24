#!/usr/bin/env bash
set -euo pipefail

base_services=(
  zookeeper
  kafka
  kafka-init
  postgres
  redis
  backend
  frontend
  telemetry-producer
  telemetry-consumer
)

intelligence_services=(
  ml-inference
  alert-engine
  threat-intelligence-engine
)

echo "Starting laptop-friendly platform mode..."
docker compose up --build -d "${base_services[@]}"
docker compose up --build -d --no-deps "${intelligence_services[@]}"
python3 scripts/health_check.py
