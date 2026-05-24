Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Starting full Streaming Analytics AI SOC platform..."
docker compose up --build -d
python scripts/health_check.py
