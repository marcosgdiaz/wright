from __future__ import annotations

from ...model import FrozenModel
from ._run_parameters import RunParameters
from ._run_steps import RunSteps


class RunPlan(FrozenModel):
    parameters: RunParameters
    steps: RunSteps
