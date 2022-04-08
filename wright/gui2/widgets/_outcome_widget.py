from typing import Optional

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget

from ._log_widget import LogWidget


class OutcomeWidget(QWidget):
    """Data and log (messages) of a run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._tabs = QTabWidget(self)
        self._layout.addWidget(self._tabs)

        self._log = LogWidget(self)
        self._tabs.addTab(self._log, "Log")

    def setLogHtml(self, html: str) -> None:
        self._log._log.setHtml(html)
        self._scrollLogToBottom()

    def _scrollLogToBottom(self) -> None:
        log_scrollbar = self._log._log.verticalScrollBar()
        log_scrollbar.setValue(log_scrollbar.maximum())

    def appendLogHtml(self, html: str) -> None:
        """Append given HTML to the log.

        Thread-safe. You may call this in a non-GUI thread.
        """
        self._log.htmlAppended.emit(html)

    def getLogHtml(self) -> str:
        return self._log._log.toHtml()
