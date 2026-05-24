from app.schemas.threat import IOCFinding, RuleHit


class ThreatScorer:
    def score(self, base_risk: float, iocs: list[IOCFinding], rule_hits: list[RuleHit], mitre_weight: float) -> tuple[float, float, str]:
        ioc_score = max((self._severity_weight(ioc.severity) * ioc.confidence for ioc in iocs), default=0.0)
        rule_score = max((hit.score for hit in rule_hits), default=0.0)
        composite = min(100.0, base_risk * 0.38 + ioc_score * 0.24 + rule_score * 0.24 + mitre_weight * 0.14)
        confidence = min(1.0, 0.35 + len(iocs) * 0.12 + len(rule_hits) * 0.16 + (base_risk / 100) * 0.25)
        return round(composite, 2), round(confidence, 3), self._severity(composite)

    @staticmethod
    def _severity(score: float) -> str:
        if score >= 90:
            return "critical"
        if score >= 75:
            return "high"
        if score >= 50:
            return "medium"
        if score >= 25:
            return "low"
        return "info"

    @staticmethod
    def _severity_weight(severity: str) -> float:
        return {"critical": 100, "high": 82, "medium": 58, "low": 30, "info": 12}.get(severity, 20)
