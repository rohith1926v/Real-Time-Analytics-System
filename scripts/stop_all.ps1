Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

Write-Host "Stopping Streaming Analytics platform..."
docker compose down
