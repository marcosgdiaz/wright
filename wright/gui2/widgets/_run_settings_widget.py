from typing import Optional

from PyQt5.QtWidgets import QVBoxLayout, QWidget

from ..models import RunSettings, StepSettings
from ._steps_settings_widget import StepsSettingsWidget


class RunSettingsWidget(QWidget):
    """Setting of a particular run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._steps_settings = StepsSettingsWidget(self)
        self._layout.addWidget(self._steps_settings)

    def model(self) -> RunSettings:
        return RunSettings(reset_params=self._steps_settings.model().reset_params)

    def setStepSettings(self, step_settings: StepSettings) -> None:
        self._steps_settings.setModel(step_settings)
