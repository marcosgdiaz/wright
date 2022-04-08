import logging
from typing import Iterable, Optional

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QHeaderView,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ..globals import _STORAGE_DIR
from ..models import OverallStatus, PartialRun

_LOGGER = logging.getLogger(__name__)


class HistoryWidget(QWidget):
    """Show previous runs."""

    runSelected = pyqtSignal(PartialRun)

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._table = QTableWidget(self)
        self._table.setColumnCount(1)
        self._table.setHorizontalHeaderLabels(("Done at",))
        self._table.horizontalHeader().setStretchLastSection(True)
        self._table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeMode.Fixed
        )
        self._table.verticalHeader().hide()
        self._table.setShowGrid(False)
        self._table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self._table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self._layout.addWidget(self._table)

        self._table.currentItemChanged.connect(self._onSelection)

        self.refresh()

    def _onSelection(self, current: QTableWidgetItem) -> None:
        partial_run = current.data(Qt.ItemDataRole.UserRole)
        self.runSelected.emit(partial_run)

    def refresh(self) -> None:
        partial_runs = list(self._partial_runs())
        self._table.setRowCount(len(partial_runs))
        for row, partial_run in enumerate(partial_runs):
            item = _partial_run_to_item(partial_run)
            self._table.setItem(row, 0, item)

    def _partial_runs(self) -> Iterable[PartialRun]:
        directories = (d for d in _STORAGE_DIR.iterdir() if d.is_dir())
        for directory in directories:
            try:
                yield PartialRun.from_dir(directory)
            except ValueError as exc:
                _LOGGER.warning(
                    f"Could not parse run directory {directory} due to: {exc}"
                )


def _partial_run_to_item(partial_run: PartialRun) -> QTableWidgetItem:
    item = QTableWidgetItem(f"{partial_run.done_at}")
    item.setFlags(Qt.ItemFlag.ItemIsEnabled)
    item.setData(Qt.ItemDataRole.UserRole, partial_run)
    # Set background color
    background_color: Optional[Qt.GlobalColor] = None
    if partial_run.status.overall is OverallStatus.COMPLETED:
        background_color = Qt.GlobalColor.green
    elif partial_run.status.overall is OverallStatus.FAILED:
        background_color = Qt.GlobalColor.red
    if background_color is not None:
        item.setBackground(background_color)
    return item
