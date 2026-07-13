from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class ProductAction:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    action_id: str = ""

    values: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True