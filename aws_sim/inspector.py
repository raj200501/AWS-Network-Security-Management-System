"""Amazon Inspector simulator.

Creates assessment runs and findings for EC2-like resources.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class AssessmentTemplate:
    template_id: str
    name: str
    rules_packages: List[str]


@dataclass(frozen=True)
class AssessmentRun:
    run_id: str
    template_id: str
    started_at: datetime
    status: str


@dataclass(frozen=True)
class InspectorFinding:
    finding_id: str
    run_id: str
    severity: str
    description: str
    resource_id: str
    created_at: datetime


class InspectorService:
    def __init__(self) -> None:
        self._templates: Dict[str, AssessmentTemplate] = {}
        self._runs: Dict[str, AssessmentRun] = {}
        self._findings: Dict[str, InspectorFinding] = {}
        self._counter = 0

    def create_template(self, name: str, rules_packages: List[str]) -> AssessmentTemplate:
        self._counter += 1
        template_id = f"tmpl-{self._counter:04d}"
        template = AssessmentTemplate(template_id=template_id, name=name, rules_packages=rules_packages)
        self._templates[template_id] = template
        return template

    def start_run(self, template_id: str) -> AssessmentRun:
        if template_id not in self._templates:
            raise KeyError("Template not found")
        self._counter += 1
        run_id = f"run-{self._counter:04d}"
        run = AssessmentRun(run_id=run_id, template_id=template_id, started_at=datetime.utcnow(), status="COMPLETED")
        self._runs[run_id] = run
        return run

    def create_finding(self, run_id: str, severity: str, description: str, resource_id: str) -> InspectorFinding:
        if run_id not in self._runs:
            raise KeyError("Run not found")
        self._counter += 1
        finding_id = f"finding-{self._counter:04d}"
        finding = InspectorFinding(
            finding_id=finding_id,
            run_id=run_id,
            severity=severity,
            description=description,
            resource_id=resource_id,
            created_at=datetime.utcnow(),
        )
        self._findings[finding_id] = finding
        return finding

    def list_findings(self) -> List[InspectorFinding]:
        return list(self._findings.values())
