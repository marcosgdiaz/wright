from typing import Optional

from PyQt5.QtWidgets import QTableWidget, QVBoxLayout, QWidget


class HistoryWidget(QWidget):
    """Show previous runs."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._table = QTableWidget(self)
        self._layout.addWidget(self._table)
