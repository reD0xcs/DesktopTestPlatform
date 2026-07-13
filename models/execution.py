from dataclasses import dataclass, field
from datetime import datetime
import uuid

from models.action_result import ActionResult


@dataclass
class Execution:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    product_name: str = ""

    serial_number: str = ""

    operator: str = ""

    started_at: datetime = field(default_factory=datetime.now)

    finished_at: datetime | None = None

    success: bool = False

    results: list[ActionResult] = field(default_factory=list)

    @property
    def duration(self) -> float:
        if self.finished_at is None:
            return 0.0

        return (self.finished_at - self.started_at).total_seconds()

    def add_result(self, result: ActionResult) -> None:
        self.results.append(result)