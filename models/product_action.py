from dataclasses import dataclass, field
from typing import Any
import uuid


@dataclass
class ProductAction:

    id: str = field(default_factory=lambda: str(uuid.uuid4()))

    action_id: str = ""

    values: dict[str, Any] = field(default_factory=dict)

    enabled: bool = True
    
    children: list["ProductAction"] = field(default_factory=list)

    else_children: list["ProductAction"] = field(default_factory=list)

    def to_dict(self):
        return {
            "id": self.id,
            "action_id": self.action_id,
            "values": self.values,
            "enabled": self.enabled,
            "children": [child.to_dict() for child in self.children],
            "else_children": [child.to_dict() for child in self.else_children],
        }

    @staticmethod
    def from_dict(data):
        pa = ProductAction(
            action_id=data.get("action_id", ""),
        )

        pa.id = data.get("id", pa.id)
        pa.values = data.get("values", {})
        pa.enabled = data.get("enabled", True)

        pa.children = [
            ProductAction.from_dict(child)
            for child in data.get("children", [])
        ]

        pa.else_children = [
            ProductAction.from_dict(child)
            for child in data.get("else_children", [])
        ]

        return pa