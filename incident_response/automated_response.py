"""Simulated automated response actions."""

from nsms.incident import create_incident


def respond_to_incident(incident_id: str, severity: str) -> list[str]:
    incident = create_incident(
        incident_id=incident_id,
        severity=severity,
        description="Automated response triggered",
    )
    return incident.remediation_steps


if __name__ == "__main__":
    steps = respond_to_incident("INC-0001", "high")
    for step in steps:
        print(step)
