from dataclasses import dataclass
from typing import Any


@dataclass
class Parameter:

    id: str
    name: str

    type: str

    default: Any = None

    required: bool = True

    description: str = ""

    unit: str = ""

    minimum: float | None = None
    maximum: float | None = None

    options: list[Any] | None = None