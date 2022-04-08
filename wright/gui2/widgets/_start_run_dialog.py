from typing import Optional

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QDialog, QPlainTextEdit, QPushButton, QVBoxLayout, QWidget

from ..models import RunPlan
from ._run_plan_widget import RunPlanWidget


class StartRunDialog(QDialog):
    """Form dialog to start a run."""

    def __init__(self, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.setWindowTitle("Start run")
        self._layout = QVBoxLayout()
        self.setLayout(self._layout)

        self._run_plan_widget = RunPlanWidget(self)
        self._layout.addWidget(self._run_plan_widget)

        ### Messages
        self._messages = QPlainTextEdit(self)
        self._messages.setStyleSheet("color: red")
        self._messages.setReadOnly(True)
        self._layout.addWidget(self._messages)

        ### Buttons
        self._cancel_button = QPushButton(self)
        self._cancel_button.setText("Cancel")
        self._layout.addWidget(self._cancel_button)

        self._start_run_button = QPushButton(self)
        self._start_run_button.setMinimumHeight(50)
        self._start_run_button.setText("Start run")
        self._start_run_button.setStyleSheet("background: blue;")
        self._layout.addWidget(self._start_run_button)

        ### Connections
        self._start_run_button.clicked.connect(self.accept)
        self._cancel_button.clicked.connect(self.reject)

        ### Validation timer
        self._validation_timer = QTimer(self)
        self._validation_timer.setInterval(1000)
        self._validation_timer.timeout.connect(self._validate)
        self._validation_timer.start()
        # Initial validation (to avoid 1 second delay before the timer kicks in)
        self._validate()

    def model(self) -> RunPlan:
        return self._run_plan_widget.model()

    def _validate(self) -> None:
        try:
            self.model()
        except ValueError as exc:
            message = str(exc)
            # Only update on changes. This avoids selection reset.
            if self._messages.toPlainText() != message:
                self._messages.setPlainText(message)
            self._messages.setEnabled(True)
            self._start_run_button.setEnabled(False)
        else:
            self._messages.setPlainText("")
            self._messages.setEnabled(False)
            self._start_run_button.setEnabled(True)

    def setRunPlan(self, run_plan: RunPlan) -> None:
        self._run_plan_widget.setRunPlan(run_plan)
        self._validate()
