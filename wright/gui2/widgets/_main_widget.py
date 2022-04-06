from pathlib import Path
from typing import Optional

from PyQt5.QtWidgets import QGridLayout, QPushButton, QSizePolicy, QWidget

from ...config.branding import Branding
from ...device import DeviceType
from ..models import StepSettings
from ._history_widget import HistoryWidget
from ._outcome_widget import OutcomeWidget
from ._run_settings_widget import RunSettingsWidget
from ._run_status_widget import RunStatusWidget
from ._start_run_dialog import StartRunDialog


class MainWidget(QWidget):
    """Root widget that contains all other widgets."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QGridLayout()
        self.setLayout(self._layout)

        self._history_widget = HistoryWidget(self)
        self._history_widget.setSizePolicy(
            QSizePolicy.Policy.Maximum,  # Do not grow beyond the size hint
            QSizePolicy.Policy.MinimumExpanding,
        )
        self._layout.addWidget(self._history_widget, 0, 0)

        self._run_settings_widget = RunSettingsWidget(self)
        self._run_settings_widget.setEnabled(False)
        self._layout.addWidget(self._run_settings_widget, 0, 1)

        self._outcome_widget = OutcomeWidget(self)
        self._layout.addWidget(self._outcome_widget, 0, 2)

        self._start_run_button = QPushButton(self)
        self._start_run_button.setText("Start run...")
        self._start_run_button.setMinimumHeight(100)
        self._layout.addWidget(self._start_run_button, 1, 0)

        self._run_status_widget = RunStatusWidget(self)
        self._layout.addWidget(self._run_status_widget, 1, 1, 1, 2)  # Span two columns

        ### Connections
        self._start_run_button.clicked.connect(self._create_run)

    def _create_run(self) -> None:
        # Get all `last_` settings from the run history
        last_step_setting = StepSettings(
            device_type=DeviceType.BACTOBOX,
            hostname="bb2201001",
            swu_file=Path("/media/data/fw-3.2.0-and-sw-1.0.1-hwdev.swu"),
            branding=Branding.SBT,
        )
        dialog = StartRunDialog(self)
        dialog.setStepSettings(last_step_setting)
        dialog.exec()
