from typing import Optional

from PyQt5.QtWidgets import QTableWidget, QTabWidget, QVBoxLayout, QWidget


class OutcomeWidget(QWidget):
    """Result or error of a run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._tabs = QTabWidget(self)
        self._layout.addWidget(self._tabs)
