"""In-memory AWS Lambda runtime simulator.

This module provides a lightweight executor for Lambda-like functions. It
captures invocation metadata, records durations, and can route events from
simulated sources like Kinesis or SNS.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional


LambdaHandler = Callable[[dict, dict], dict]


@dataclass(frozen=True)
class LambdaFunction:
    name: str
    handler: LambdaHandler
    timeout_seconds: int = 3
    memory_mb: int = 128
    environment: Optional[dict] = None


@dataclass(frozen=True)
class InvocationRecord:
    function_name: str
    request_id: str
    invoked_at: datetime
    duration_ms: float
    status: str
    result: dict


class LambdaRuntime:
    """Simple executor for Lambda-like functions."""

    def __init__(self) -> None:
        self._functions: Dict[str, LambdaFunction] = {}
        self._invocations: List[InvocationRecord] = []
        self._request_counter = 0

    def register(self, function: LambdaFunction) -> None:
        if function.name in self._functions:
            raise ValueError(f"Lambda function already registered: {function.name}")
        self._functions[function.name] = function

    def invoke(self, function_name: str, event: dict) -> dict:
        function = self._functions.get(function_name)
        if function is None:
            raise KeyError(f"Lambda function not found: {function_name}")
        start = datetime.utcnow()
        context = {
            "function_name": function.name,
            "timeout": function.timeout_seconds,
            "memory": function.memory_mb,
            "request_id": self._next_request_id(),
        }
        result = function.handler(event, context)
        duration_ms = (datetime.utcnow() - start).total_seconds() * 1000
        record = InvocationRecord(
            function_name=function.name,
            request_id=context["request_id"],
            invoked_at=start,
            duration_ms=duration_ms,
            status="success",
            result=result,
        )
        self._invocations.append(record)
        return result

    def list_functions(self) -> List[str]:
        return list(self._functions.keys())

    def invocations(self) -> List[InvocationRecord]:
        return list(self._invocations)

    def _next_request_id(self) -> str:
        self._request_counter += 1
        return f"req-{self._request_counter:06d}"
