# NSMS Data Dictionary

This file documents the fields used in NSMS log data, threat intelligence, and
compliance rules. It is intended to keep the data model explicit and stable.

## Log Record (`data/sample_logs.csv`)

| Field | Type | Description |
| --- | --- | --- |
| `timestamp` | ISO-8601 string | Event timestamp in UTC. |
| `source_ip` | string | Source IP address of the request. |
| `destination_ip` | string | Destination IP address of the request. |
| `protocol` | string | Network protocol (e.g., HTTPS, SSH, DNS). |
| `bytes` | integer | Bytes transferred in the request. |
| `action` | string | Action performed (READ, WRITE, LIST, DELETE, ROOT_LOGIN). |
| `region` | string | Region identifier (e.g., `us-east-1`). |
| `user` | string | Actor that initiated the request. |
| `resource` | string | Resource path being accessed. |
| `status` | string | Result of the request (`OK`, `DENIED`, or `ERROR`). |

### Notes

- `bytes` is used in the statistical anomaly detector.
- `action` and `status` are used for compliance and anomaly heuristics.
- `resource` is used to identify sensitive access patterns.

## Threat Intelligence (`data/threat_intel.json`)

The threat intelligence feed is a JSON object with the following structure:

```json
{
  "source": "local",
  "indicators": [
    {
      "ip_address": "198.51.100.99",
      "severity": "high",
      "description": "Known credential stuffing source"
    }
  ]
}
```

| Field | Type | Description |
| --- | --- | --- |
| `source` | string | Label for the feed origin (local, vendor, etc.). |
| `indicators[].ip_address` | string | Source IP address. |
| `indicators[].severity` | string | `low`, `medium`, `high`, or `critical`. |
| `indicators[].description` | string | Human-readable reason for the indicator. |

### Notes

- Severity labels are informational; enforcement is handled in the pipeline.
- Indicators are matched by exact IP address.

## Compliance Rules (`data/compliance_rules.json`)

Each compliance rule is defined as:

```json
{
  "rule_id": "CMP-001",
  "description": "Traffic must originate from approved regions",
  "allowed_regions": ["us-east-1", "us-west-2", "eu-west-1"],
  "allowed_protocols": ["HTTPS", "SSH", "DNS"],
  "high_risk_actions": ["DELETE", "ROOT_LOGIN"]
}
```

| Field | Type | Description |
| --- | --- | --- |
| `rule_id` | string | Unique identifier for the rule. |
| `description` | string | Human-readable rule description. |
| `allowed_regions` | list | Region allowlist. |
| `allowed_protocols` | list | Protocol allowlist. |
| `high_risk_actions` | list | Actions that should always flag a violation. |

### Notes

- A violation occurs when a record falls outside the allowed region or protocol,
  or when it performs a high-risk action.
- Multiple rules may be violated by a single record.

## Output Artifacts

### Alerts (`outputs/alerts.jsonl`)

Each line contains:

- `record_index` — index in the source log file
- `timestamp` — ISO timestamp from the log
- `source_ip` — source IP address
- `destination_ip` — destination IP address
- `anomaly` — boolean anomaly flag
- `threat_intel_hit` — boolean threat intel hit
- `compliance_violations` — list of violated rule IDs

### Incidents (`outputs/incidents.jsonl`)

Each line contains:

- `incident_id` — generated incident identifier
- `severity` — critical/high/medium/low
- `description` — summary of the triggering record
- `created_at` — UTC timestamp
- `remediation_steps` — list of prescribed steps

### Metrics (`outputs/metrics.json`)

- `total_records`
- `anomalous_records`
- `threat_intel_hits`
- `compliance_violations`

### Run Summary (`outputs/run_summary.json`)

Quick summary used for CI validation.

### Summary Report (`outputs/summary.md`)

A human-readable report that includes:

- A run summary
- Threat intelligence hits
- Compliance totals
- Sample log entries

