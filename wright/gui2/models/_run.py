from __future__ import annotations

from datetime import datetime
from pathlib import Path

from pydantic import Field

from ...model import FrozenModel
from ._run_plan import RunPlan
from ._run_status import RunStatus

_STATUS_FILE_NAME = "status.json"
_PLAN_FILE_NAME = "plan.json"
_LOG_FILE_NAME = "log.html"


class PartialRun(FrozenModel):
    directory: Path
    status: RunStatus

    @property
    def done_at(self) -> datetime:
        try:
            return datetime.fromisoformat(self.directory.name.replace("_", ":"))
        except ValueError as exc:
            raise ValueError("Could not deconde done time from directory name") from exc

    @classmethod
    def from_dir(cls, run_dir: Path) -> PartialRun:
        # Status map
        status_file = run_dir / _STATUS_FILE_NAME
        status = RunStatus.parse_file(status_file)
        return cls(directory=run_dir, status=status)


class Run(FrozenModel):
    status: RunStatus
    plan: RunPlan
    log: str  # HTML
    done_at: datetime = Field(default_factory=datetime.now)

    @classmethod
    def from_partial_run(cls, partial_run: PartialRun) -> Run:
        # Plan
        plan_file = partial_run.directory / _PLAN_FILE_NAME
        plan = RunPlan.parse_file(plan_file)
        # Log
        log_file = partial_run.directory / _LOG_FILE_NAME
        log = log_file.read_text()
        return cls(
            status=partial_run.status,
            plan=plan,
            log=log,
            done_at=partial_run.done_at,
        )

    def to_dir(self, parent_dir: Path) -> None:
        run_dir = parent_dir / self.done_at.isoformat().replace(":", "_")
        run_dir.mkdir()
        # Status map
        status_file = run_dir / _STATUS_FILE_NAME
        status_file.write_text(self.status.json())
        # Plan
        plan_file = run_dir / _PLAN_FILE_NAME
        plan_file.write_text(self.plan.json())
        # Log
        log_file = run_dir / _LOG_FILE_NAME
        log_file.write_text(self.log)
