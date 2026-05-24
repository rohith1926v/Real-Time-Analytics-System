Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose up --build -d frontend
docker logs --tail 80 streaming-analytics-frontend
