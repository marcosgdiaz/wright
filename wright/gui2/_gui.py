import asyncio
import sys

from PyQt5.QtWidgets import QApplication
from qasync import QEventLoop

from .widgets import MainWidget


def gui() -> None:
    """Start the GUI."""
    print("hi there gui2")
    # set_logging_defaults()
    app = QApplication(sys.argv)
    event_loop = QEventLoop(app)
    asyncio.set_event_loop(event_loop)
    with event_loop:
        main_widget = MainWidget()
        main_widget.show()
        event_loop.run_forever()
