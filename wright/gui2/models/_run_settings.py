from __future__ import annotations

from ...model import FrozenModel
from ._reset_params import ResetParams


class RunSettings(FrozenModel):
    reset_params: ResetParams
