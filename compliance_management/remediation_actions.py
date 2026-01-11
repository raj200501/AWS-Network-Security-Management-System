"""Example remediation actions for compliance violations."""

from nsms.incident import create_incident


if __name__ == "__main__":
    incident = create_incident(
        incident_id="INC-EXAMPLE",
        severity="medium",
        description="Example compliance violation",
    )
    print("Remediation steps:")
    for step in incident.remediation_steps:
        print(f"- {step}")
