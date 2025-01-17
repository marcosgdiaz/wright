import logging


def set_logging_defaults() -> None:
    """Set global settings for logging."""
    # Log everything per default
    logging.basicConfig(level=logging.DEBUG)
    # Silence tftpy a bit
    logging.getLogger("tftpy").setLevel(level=logging.INFO)
    # Matplotlib is very spammy in debug mode
    logging.getLogger("matplotlib").setLevel(level=logging.INFO)
