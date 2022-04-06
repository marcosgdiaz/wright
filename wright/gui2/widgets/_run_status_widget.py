from typing import Optional

from PyQt5.QtWidgets import QTabWidget, QVBoxLayout, QWidget


class RunStatusWidget(QWidget):
    """Status of a run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._tabs = QTabWidget(self)
        self._layout.addWidget(self._tabs)
