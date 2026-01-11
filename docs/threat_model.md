# Threat Model (Local Simulator)

This threat model documents the attack scenarios simulated by NSMS. While this
repo does not connect to AWS, it mirrors common network security workflows to
support repeatable testing and demonstration.

## Assets

- **Log data** (`data/sample_logs.csv`) representing network events.
- **Threat intelligence feed** (`data/threat_intel.json`).
- **Compliance policies** (`data/compliance_rules.json`).
- **Output artifacts** in `outputs/`.

## Actors

- **Benign user**: Normal traffic with OK status.
- **Suspicious user**: Denied or high-volume traffic.
- **Admin user**: Elevated access attempts.
- **Threat actor**: IPs in the threat intelligence feed.

## Attack Scenarios Simulated

### Credential Stuffing

- IP address listed in threat intel feed.
- Repeated denied login attempts (ROOT_LOGIN actions).
- Expected outcome: threat intel hit + anomaly detection → critical incident.

### Data Exfiltration

- Large byte transfers from sensitive resources.
- Admin user context.
- Expected outcome: anomaly detection → medium or high incident.

### Region Violation

- Traffic from unapproved regions.
- Expected outcome: compliance violation → high incident.

### Protocol Violation

- High-risk actions over non-approved protocols.
- Expected outcome: compliance violation → high incident.

## Defensive Controls

- **Anomaly detection**: Statistical outlier detection on bytes transferred.
- **Threat intel matching**: Known bad IP detection.
- **Compliance enforcement**: Policy-based rule checks.
- **Incident response**: Severity-based remediation steps.

## Assumptions

- Log data is reliable and complete.
- Threat intelligence feed is static for deterministic runs.
- Compliance rules reflect current policy and are version-controlled.

## Limitations

- The simulator does not implement real-time streaming.
- Network-based controls (WAF, firewall, IAM) are not executed.
- Threat intelligence is not automatically updated.

## Future Work

- Add signatures for specific exploits.
- Introduce rate-based anomaly detection.
- Integrate optional real-time streaming for demo purposes.

