#!/usr/bin/env bash
set -euo pipefail

echo "Starting full Streaming Analytics AI SOC platform..."
docker compose up --build -d
python3 scripts/health_check.py
