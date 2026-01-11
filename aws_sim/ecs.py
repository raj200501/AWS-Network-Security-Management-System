"""ECS simulator.

Models clusters, task definitions, and services to emulate container
orchestration behavior for tests and local demos.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List


@dataclass(frozen=True)
class ContainerDefinition:
    name: str
    image: str
    cpu: int
    memory: int
    port_mappings: List[int]


@dataclass(frozen=True)
class TaskDefinition:
    task_definition_arn: str
    family: str
    containers: List[ContainerDefinition]
    created_at: datetime


@dataclass(frozen=True)
class Task:
    task_arn: str
    task_definition_arn: str
    status: str
    started_at: datetime


@dataclass
class Service:
    service_arn: str
    name: str
    task_definition_arn: str
    desired_count: int
    running_tasks: List[Task] = field(default_factory=list)

    def scale(self, desired_count: int) -> None:
        self.desired_count = desired_count


@dataclass
class Cluster:
    cluster_arn: str
    name: str
    services: Dict[str, Service] = field(default_factory=dict)
    tasks: Dict[str, Task] = field(default_factory=dict)


class EcsService:
    def __init__(self) -> None:
        self._clusters: Dict[str, Cluster] = {}
        self._task_definitions: Dict[str, TaskDefinition] = {}
        self._counter = 0

    def create_cluster(self, name: str) -> Cluster:
        self._counter += 1
        cluster = Cluster(cluster_arn=f"arn:aws:ecs::cluster/{self._counter:04d}", name=name)
        self._clusters[cluster.cluster_arn] = cluster
        return cluster

    def register_task_definition(self, family: str, containers: List[ContainerDefinition]) -> TaskDefinition:
        self._counter += 1
        arn = f"arn:aws:ecs::task-definition/{family}:{self._counter}"
        task_def = TaskDefinition(task_definition_arn=arn, family=family, containers=containers, created_at=datetime.utcnow())
        self._task_definitions[arn] = task_def
        return task_def

    def create_service(self, cluster_arn: str, name: str, task_definition_arn: str, desired_count: int) -> Service:
        cluster = self._clusters.get(cluster_arn)
        if cluster is None:
            raise KeyError("Cluster not found")
        self._counter += 1
        service_arn = f"arn:aws:ecs::service/{self._counter:04d}"
        service = Service(service_arn=service_arn, name=name, task_definition_arn=task_definition_arn, desired_count=desired_count)
        cluster.services[service_arn] = service
        return service

    def run_task(self, cluster_arn: str, task_definition_arn: str) -> Task:
        cluster = self._clusters.get(cluster_arn)
        if cluster is None:
            raise KeyError("Cluster not found")
        self._counter += 1
        task = Task(task_arn=f"arn:aws:ecs::task/{self._counter:04d}", task_definition_arn=task_definition_arn, status="RUNNING", started_at=datetime.utcnow())
        cluster.tasks[task.task_arn] = task
        return task

    def list_clusters(self) -> List[Cluster]:
        return list(self._clusters.values())
