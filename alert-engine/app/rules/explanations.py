def explain_alert(rule_name: str, event_type: str, severity: str) -> tuple[str, str]:
    if rule_name == "credential_attack":
        return (
            "Multiple failed logins combined with elevated anomaly scores indicate possible credential stuffing behavior.",
            "Investigate authentication logs, enforce step-up authentication, and consider temporarily rate-limiting the entity.",
        )
    if rule_name == "api_abuse":
        return (
            "High API request volume with elevated risk score suggests automated abuse or bot activity.",
            "Review API tokens, inspect user-agent/source-IP patterns, and apply throttling if abuse is confirmed.",
        )
    if rule_name == "network_spike":
        return (
            "Network byte volume and risk signals suggest a potential data transfer spike or scanning behavior.",
            "Validate destination systems, inspect network flow records, and isolate the source if exfiltration is suspected.",
        )
    if rule_name == "high_anomaly":
        return (
            f"The ML detector classified this {event_type} signal as {severity} based on abnormal feature patterns.",
            "Review the related entity timeline and compare recent behavior against normal operating baselines.",
        )
    return (
        "Correlated telemetry and risk signals indicate activity outside the expected baseline.",
        "Review the incident timeline, validate business context, and escalate if the activity is unauthorized.",
    )

