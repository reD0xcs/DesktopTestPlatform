from dataclasses import dataclass, field
from typing import Any
import time


@dataclass
class ActionResult:

    action_id: str

    success: bool

    message: str = ""

    outputs: dict[str, Any] = field(default_factory=dict)

    duration: float = 0.0

    timestamp: float = field(default_factory=time.time)