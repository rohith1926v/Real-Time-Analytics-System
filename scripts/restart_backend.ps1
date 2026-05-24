Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

docker compose up --build -d backend
docker logs --tail 80 streaming-analytics-backend
