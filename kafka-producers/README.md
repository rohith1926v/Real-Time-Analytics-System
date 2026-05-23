# Kafka Telemetry Runtime

Python runtime for Phase 2 synthetic telemetry production and validation.

## Responsibilities

- Generate realistic cybersecurity and platform telemetry events.
- Validate all outbound events with Pydantic schemas.
- Publish events to Kafka topics with retry-safe producer configuration.
- Consume telemetry topics and validate received payloads.
- Route malformed or unprocessable messages to `telemetry.deadletter.events`.

## Runtime Modes

```bash
python -m app.main producer
python -m app.main consumer
```

## Environment Variables

| Variable | Default | Purpose |
| --- | --- | --- |
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker list. |
| `EVENT_RATE_PER_SECOND` | `5` | Producer event generation rate. |
| `ANOMALY_RATE` | `0.05` | Probability of generating anomaly events. |
| `PRODUCER_LOG_LEVEL` | `INFO` | Producer logging level. |
| `KAFKA_CONSUMER_GROUP` | `streaming-analytics-telemetry-consumers` | Consumer group id. |
| `CONSUMER_LOG_LEVEL` | `INFO` | Consumer logging level. |

## Topics

- `telemetry.login.events`
- `telemetry.api.events`
- `telemetry.network.events`
- `telemetry.anomaly.events`
- `telemetry.deadletter.events`
