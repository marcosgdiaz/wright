from __future__ import annotations

from pydantic import FilePath

from ...device.models import Branding
from ...device import DeviceDescription
from ...model import FrozenModel


class ResetParams(FrozenModel):
    device_description: DeviceDescription
    swu_file: FilePath
    branding: Branding
