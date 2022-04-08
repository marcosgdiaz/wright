from html import escape as escape_html
from logging import Formatter, Handler, LogRecord
from typing import Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtWidgets import QTextEdit, QVBoxLayout, QWidget


class LogWidget(QWidget):
    """Log (messages) of a run."""

    htmlAppended = pyqtSignal(str)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._log = QTextEdit(self)
        self._log.setReadOnly(True)
        self._log_style = self._log.style()
        self._layout.addWidget(self._log)

        # We use the `messageAppended` signal as a thread-safe layer of indirection.
        # This way, we can append to the log from non-GUI threads.
        self.htmlAppended.connect(self._append)

    def _append(self, html: str) -> None:
        self._log.append(html)


class GuiHandler(Handler):
    """Log handler that outputs to a `LogWidget`."""

    def __init__(self, log_widget: LogWidget) -> None:
        super().__init__()
        self._log_widget = log_widget

    def emit(self, record: LogRecord) -> None:
        """Emit the given record to the GUI element."""
        if record.name == "root":
            text_color = "white"
            background_color = "black"
        else:
            text_color = "auto"
            background_color = "auto"
        style = f"font-family: monospace; margin: 0; color: {text_color}; background: {background_color};"
        message = self.format(record)
        html = f'<span style="{style}">{escape_html(message)}</span>'
        self._log_widget.htmlAppended.emit(html)


class GuiFormatter(Formatter):
    """Log formatter for the GUI."""

    def __init__(self) -> None:
        super().__init__("%(levelname)s [%(name)s] %(message)s")
