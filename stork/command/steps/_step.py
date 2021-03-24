from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Instruction:
    text: Optional[str] = None


@dataclass(frozen=True)
class RequestConfirmation:
    text: Optional[str] = None


StatusUpdate = str
