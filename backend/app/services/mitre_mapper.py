from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class MitreMapping:
    tactic: str
    technique: str
    mitre_id: str
    confidence: float
    kill_chain_stage: str
    severity_weight: float


class MitreMapper:
    _mappings: tuple[tuple[set[str], MitreMapping], ...] = (
        ({"failed_login", "login_failure", "brute_force", "credential"}, MitreMapping("Credential Access", "Brute Force", "T1110", 0.88, "credential-access", 82)),
        ({"impossible_travel", "high_risk_geo", "geo"}, MitreMapping("Initial Access", "Valid Accounts", "T1078", 0.76, "initial-access", 70)),
        ({"lateral", "rdp", "smb", "admin_share"}, MitreMapping("Lateral Movement", "Remote Services", "T1021", 0.84, "lateral-movement", 86)),
        ({"privilege", "escalation", "admin", "sudo"}, MitreMapping("Privilege Escalation", "Valid Accounts", "T1078", 0.78, "privilege-escalation", 84)),
        ({"beacon", "periodic", "dns", "c2"}, MitreMapping("Command and Control", "Application Layer Protocol", "T1071", 0.72, "command-and-control", 78)),
        ({"exfiltration", "bytes_sent", "upload"}, MitreMapping("Exfiltration", "Exfiltration Over Web Service", "T1567", 0.74, "exfiltration", 88)),
        ({"process", "execution", "powershell"}, MitreMapping("Execution", "Command and Scripting Interpreter", "T1059", 0.80, "execution", 80)),
        ({"scan", "discovery", "port"}, MitreMapping("Discovery", "Network Service Discovery", "T1046", 0.68, "discovery", 62)),
    )

    tactics = [
        "Initial Access",
        "Execution",
        "Persistence",
        "Privilege Escalation",
        "Defense Evasion",
        "Credential Access",
        "Discovery",
        "Lateral Movement",
        "Collection",
        "Command and Control",
        "Exfiltration",
        "Impact",
    ]

    def map_event(self, text: str, risk_score: float = 0.0) -> MitreMapping:
        normalized = text.lower()
        for keywords, mapping in self._mappings:
            if any(keyword in normalized for keyword in keywords):
                return mapping
        if risk_score >= 85:
            return MitreMapping("Impact", "Data Manipulation", "T1565", 0.58, "impact", 76)
        return MitreMapping("Discovery", "Security Software Discovery", "T1518.001", 0.42, "discovery", 45)

    def techniques(self) -> list[dict]:
        return [
            {
                "tactic": mapping.tactic,
                "technique": mapping.technique,
                "mitre_id": mapping.mitre_id,
                "kill_chain_stage": mapping.kill_chain_stage,
                "confidence": mapping.confidence,
            }
            for _, mapping in self._mappings
        ]
