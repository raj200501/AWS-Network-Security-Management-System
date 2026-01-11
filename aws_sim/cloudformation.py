"""CloudFormation stack simulator.

Provides an in-memory representation of a stack with resources and outputs. The
simulator supports create/update/delete semantics, change sets, and basic drift
checks so local tests can verify IaC workflows without AWS access.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional


@dataclass(frozen=True)
class StackResource:
    logical_id: str
    resource_type: str
    properties: Dict[str, object]
    physical_id: str
    status: str
    created_at: datetime
    updated_at: datetime


@dataclass(frozen=True)
class StackOutput:
    key: str
    value: str
    description: str


@dataclass(frozen=True)
class ChangeSet:
    change_set_id: str
    stack_name: str
    changes: List[str]
    created_at: datetime
    status: str


class CloudFormationStack:
    """In-memory CloudFormation stack."""

    def __init__(self, name: str) -> None:
        self.name = name
        self.status = "CREATE_COMPLETE"
        self._resources: Dict[str, StackResource] = {}
        self._outputs: Dict[str, StackOutput] = {}
        self._change_sets: List[ChangeSet] = []
        self._counter = 0

    def add_resource(self, logical_id: str, resource_type: str, properties: Dict[str, object]) -> StackResource:
        if logical_id in self._resources:
            raise ValueError(f"Resource already exists: {logical_id}")
        self._counter += 1
        now = datetime.utcnow()
        resource = StackResource(
            logical_id=logical_id,
            resource_type=resource_type,
            properties=properties,
            physical_id=f"{self.name}-{logical_id}-{self._counter:04d}",
            status="CREATE_COMPLETE",
            created_at=now,
            updated_at=now,
        )
        self._resources[logical_id] = resource
        return resource

    def update_resource(self, logical_id: str, properties: Dict[str, object]) -> StackResource:
        resource = self._resources.get(logical_id)
        if resource is None:
            raise KeyError(f"Resource not found: {logical_id}")
        now = datetime.utcnow()
        updated = StackResource(
            logical_id=resource.logical_id,
            resource_type=resource.resource_type,
            properties=properties,
            physical_id=resource.physical_id,
            status="UPDATE_COMPLETE",
            created_at=resource.created_at,
            updated_at=now,
        )
        self._resources[logical_id] = updated
        self.status = "UPDATE_COMPLETE"
        return updated

    def remove_resource(self, logical_id: str) -> bool:
        if logical_id in self._resources:
            del self._resources[logical_id]
            self.status = "UPDATE_COMPLETE"
            return True
        return False

    def list_resources(self) -> List[StackResource]:
        return list(self._resources.values())

    def add_output(self, key: str, value: str, description: str = "") -> StackOutput:
        output = StackOutput(key=key, value=value, description=description)
        self._outputs[key] = output
        return output

    def list_outputs(self) -> List[StackOutput]:
        return list(self._outputs.values())

    def create_change_set(self, changes: List[str]) -> ChangeSet:
        self._counter += 1
        change_set = ChangeSet(
            change_set_id=f"cs-{self._counter:04d}",
            stack_name=self.name,
            changes=changes,
            created_at=datetime.utcnow(),
            status="CREATE_COMPLETE",
        )
        self._change_sets.append(change_set)
        return change_set

    def list_change_sets(self) -> List[ChangeSet]:
        return list(self._change_sets)

    def drift_detect(self) -> Dict[str, str]:
        """Simulate drift detection for resources."""

        drift_status = {}
        for resource in self._resources.values():
            drift_status[resource.logical_id] = "IN_SYNC"
        return drift_status


@dataclass
class StackTemplate:
    description: str
    resources: Dict[str, Dict[str, object]] = field(default_factory=dict)
    outputs: Dict[str, Dict[str, str]] = field(default_factory=dict)

    def add_resource(self, logical_id: str, resource_type: str, properties: Dict[str, object]) -> None:
        self.resources[logical_id] = {
            "Type": resource_type,
            "Properties": properties,
        }

    def add_output(self, key: str, value: str, description: str = "") -> None:
        self.outputs[key] = {"Value": value, "Description": description}


class CloudFormationService:
    """Service that manages multiple stacks."""

    def __init__(self) -> None:
        self._stacks: Dict[str, CloudFormationStack] = {}

    def create_stack(self, name: str, template: StackTemplate) -> CloudFormationStack:
        if name in self._stacks:
            raise ValueError(f"Stack already exists: {name}")
        stack = CloudFormationStack(name)
        for logical_id, resource in template.resources.items():
            stack.add_resource(
                logical_id,
                resource_type=resource["Type"],
                properties=resource.get("Properties", {}),
            )
        for key, output in template.outputs.items():
            stack.add_output(key, output["Value"], output.get("Description", ""))
        self._stacks[name] = stack
        return stack

    def update_stack(self, name: str, template: StackTemplate) -> CloudFormationStack:
        stack = self._stacks.get(name)
        if stack is None:
            raise KeyError(f"Stack not found: {name}")
        for logical_id, resource in template.resources.items():
            if any(res.logical_id == logical_id for res in stack.list_resources()):
                stack.update_resource(logical_id, resource.get("Properties", {}))
            else:
                stack.add_resource(
                    logical_id,
                    resource_type=resource["Type"],
                    properties=resource.get("Properties", {}),
                )
        return stack

    def delete_stack(self, name: str) -> None:
        if name in self._stacks:
            del self._stacks[name]

    def list_stacks(self) -> List[str]:
        return list(self._stacks.keys())
