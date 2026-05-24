from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from pydantic import BaseModel, Field


class IOCFinding(BaseModel):
    value: str
    ioc_type: str
    feed_name: str
    confidence: float
    severity: str
    description: str


class RuleHit(BaseModel):
    rule_id: str
    rule_name: str
    severity: str
    tactic: str
    technique: str
    mitre_id: str
    score: float


class ThreatEnrichment(BaseModel):
    event_id: str = Field(default_factory=lambda: str(uuid4()))
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    source_topic: str
    source_event_id: str | None = None
    entity_id: str | None = None
    entity_type: str = "unknown"
    event_type: str | None = None
    tactic: str | None = None
    technique: str | None = None
    mitre_id: str | None = None
    kill_chain_stage: str | None = None
    mitre_confidence: float = 0.0
    iocs: list[IOCFinding] = Field(default_factory=list)
    rule_hits: list[RuleHit] = Field(default_factory=list)
    geo_country: str | None = None
    asn: str | None = None
    threat_score: float
    confidence: float
    severity: str
    raw_payload: dict[str, Any]
