from typing import Optional

from PyQt5.QtWidgets import QFormLayout, QHBoxLayout, QLineEdit, QProgressBar, QWidget

from ..models import OverallStatus, RunStatus, StepStatus


class RunStatusWidget(QWidget):
    """Status of a run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QFormLayout()
        self._overall = OverallStatus.IDLE
        self.setLayout(self._layout)

        self._prepare_status = StatusWidget(self)
        self._layout.addRow("Prepare", self._prepare_status)

        self._reset_firmware_status = StatusWidget(self)
        self._layout.addRow("Reset firmware", self._reset_firmware_status)

        self._reset_operating_system_status = StatusWidget(self)
        self._layout.addRow("Reset OS", self._reset_operating_system_status)

        self._reset_config_status = StatusWidget(self)
        self._layout.addRow("Reset config", self._reset_config_status)

        self._reset_data_status = StatusWidget(self)
        self._layout.addRow("Reset data", self._reset_data_status)

        self._check_electronics_status = StatusWidget(self)
        self._layout.addRow("Check electronics", self._check_electronics_status)

        self._status_widgets: dict[str, StatusWidget] = {
            "prepare": self._prepare_status,
            "reset_firmware": self._reset_firmware_status,
            "reset_operating_system": self._reset_operating_system_status,
            "reset_config": self._reset_config_status,
            "reset_data": self._reset_data_status,
        }

    def statusMap(self) -> RunStatus:
        steps = {name: w.status() for name, w in self._status_widgets.items()}
        return RunStatus(overall=self._overall, steps=steps)

    def setStatusMap(self, status_map: RunStatus) -> None:
        self._overall = status_map.overall
        for name, status in status_map.steps.items():
            try:
                status_widget = self._status_widgets[name]
            except KeyError:
                continue
            status_widget.setStatus(status)


class StatusWidget(QWidget):
    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self._layout)

        self._progress = QProgressBar(self)
        self._progress.setMaximum(100)
        self._layout.addWidget(self._progress, 2)

        self._description = QLineEdit(self)
        self._description.setReadOnly(True)
        self._description.setMinimumWidth(200)
        self._layout.addWidget(self._description)

    def status(self) -> StepStatus:
        return StepStatus(
            progress=self._progress.value(),
            description=self._description.text(),
        )

    def setStatus(self, status: StepStatus) -> None:
        self._progress.setValue(status.progress)
        self._description.setText(status.description)
