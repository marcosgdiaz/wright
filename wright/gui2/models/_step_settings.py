from __future__ import annotations

from pydantic import FilePath

from ...config.branding import Branding
from ...device import DeviceDescription, DeviceType
from ...model import FrozenModel
from ._low_level_config import LowLevelConfig
from ._reset_params import ResetParams


class StepSettings(FrozenModel):
    device_type: DeviceType
    hostname: str
    swu_file: FilePath
    branding: Branding

    @property
    def reset_params(self) -> ResetParams:
        return ResetParams(
            device_description=self.device_description,
            swu_file=self.swu_file,
            branding=self.branding,
        )

    @property
    def device_description(self) -> DeviceDescription:
        low_level_config = LowLevelConfig.try_from_config_file()
        return DeviceDescription.from_raw_args(
            device_type=self.device_type,
            hostname=self.hostname,
            tty=low_level_config.tty,
            jtag_usb_serial=low_level_config.jtag_usb_serial,
            power_relay=low_level_config.power_relay,
            boot_mode_gpio=low_level_config.boot_mode_gpio,
        )
