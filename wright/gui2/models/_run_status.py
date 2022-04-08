from __future__ import annotations

from datetime import datetime
from enum import Enum, unique
from typing import Mapping

from pydantic import Field, conint

from ...model import FrozenModel
from ...progress import Cancelled, Completed, Failed, Idle, Skipped, Status, StatusMap


@unique
class OverallStatus(Enum):
    IDLE = "idle"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

    @staticmethod
    def from_progress_status_map(status_map: StatusMap) -> OverallStatus:
        if any(isinstance(s, Cancelled) for s in status_map.values()):
            return OverallStatus.CANCELLED
        if any(isinstance(s, Failed) for s in status_map.values()):
            return OverallStatus.FAILED
        if all(isinstance(s, Completed) for s in status_map.values()):
            return OverallStatus.COMPLETED
        if all(isinstance(s, Idle) for s in status_map.values()):
            return OverallStatus.IDLE
        return OverallStatus.RUNNING


class StepStatus(FrozenModel):
    progress: conint(ge=0, le=100) = 0
    description: str

    @classmethod
    def from_progress_status(cls, status: Status) -> StepStatus:
        if isinstance(status, Idle):
            return cls(description="Pending")
        if isinstance(status, Skipped):
            return cls(description="Skipped")
        if isinstance(status, Completed):
            description = "Completed"
            if status.tries > 1:
                description += f" (tries: {status.tries})"
            return cls(progress=100, description=description)
        if isinstance(status, Failed):
            return cls(description="Failed")
        if isinstance(status, Cancelled):
            return cls(description="Cancelled")
        now = datetime.now()
        elapsed = now - status.begin_at
        remaining = status.expected_duration - elapsed
        progress = int(elapsed / status.expected_duration * 100)
        description = f"Max {int(remaining.total_seconds())} seconds left"
        if status.tries > 1:
            description += f" (tries: {status.tries})"
        return cls(progress=progress, description=description)


class RunStatus(FrozenModel):
    overall: OverallStatus = OverallStatus.IDLE
    steps: Mapping[str, StepStatus] = Field(default_factory=dict)

    @classmethod
    def from_progress_status_map(cls, status_map: StatusMap) -> RunStatus:
        return cls(
            overall=OverallStatus.from_progress_status_map(status_map),
            steps={
                key: StepStatus.from_progress_status(s) for key, s in status_map.items()
            },
        )
