from __future__ import annotations

from ...commands import ResetDeviceSettings, StepSettings
from ...model import FrozenModel


class RunSteps(FrozenModel):
    reset_firmware: bool = True
    reset_operating_system: bool = True
    reset_config: bool = True
    reset_data: bool = True
    check_electronics: bool = True

    @property
    def reset_device_settings(self) -> ResetDeviceSettings:
        return ResetDeviceSettings(
            StepSettings(self.reset_firmware, 10),
            StepSettings(self.reset_operating_system, 10),
            StepSettings(self.reset_config, 10),
            StepSettings(self.reset_data, 10),
        )
