import uuid
from dataclasses import dataclass, field

from models.product_action import ProductAction


@dataclass
class Product:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    name: str = ""

    description: str = ""

    version: str = "1.0"

    actions: list[ProductAction] = field(default_factory=list)