Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

python -m compileall backend/app ml-models/app alert-engine/app storage-sink/app kafka-producers/app threat-intelligence-engine/app
Push-Location frontend
npm run build
Pop-Location
docker compose config --quiet
python scripts/health_check.py --json
