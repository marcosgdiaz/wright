import logging
from pathlib import Path

import anyio

from .. import execution_context
from .._green_mango import GreenMango

_LOGGER = logging.getLogger(__name__)


async def reset_firmware(device: GreenMango, firmware_image: Path) -> None:
    """Remove any existing firmware and write the given image to the device."""
    with anyio.fail_after(110):
        async with execution_context.StorkUboot.enter_context(device) as uboot:
            # First, erase the entire FLASH memory
            await uboot.erase_flash()
            # Second, write the firmware image to FLASH memory.
            await uboot.write_image_to_flash(firmware_image)


async def reset_software(device: GreenMango, software_image: Path) -> None:
    """Remove any existing software and write the given images to the device."""
    with anyio.fail_after(70):
        async with execution_context.Uboot.enter_context(device) as uboot:
            await uboot.partition_mmc()
            # We must power-cycle the device so that U-boot recognizes the
            # new partitioning.
            await device.hard_power_off()

        async with execution_context.Uboot.enter_context(device) as uboot:
            # Write to both "system" partitions so that we have a working fall-back
            # in case of a broken (interrupted) software update. This is part of the
            # dual boot strategy.
            await uboot.write_image_to_mmc(
                software_image, uboot.mmc.system0, uboot.mmc.system1
            )


async def reset_config(device: GreenMango, config_image: Path) -> None:
    """Remove any existing config and write the given images to the device."""
    with anyio.fail_after(40):
        async with execution_context.Uboot.enter_context(device) as uboot:
            # There is a single copy of the config image
            await uboot.write_image_to_mmc(config_image, uboot.mmc.config)


async def reset_data(device: GreenMango) -> None:
    """Remove all data on the device."""
    with anyio.fail_after(60):
        async with execution_context.QuietLinux.enter_context(device) as linux:
            await linux.reset_data()
