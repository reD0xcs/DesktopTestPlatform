from dataclasses import dataclass, field

from models.parameter import Parameter


@dataclass
class Action:

    id: str

    name: str

    device: str

    category: str

    description: str = ""

    parameters: list[Parameter] = field(default_factory=list)