import json
from pathlib import Path

from models.product import Product
from models.product_action import ProductAction


class ProductSerializer:

    def __init__(self, directory="products"):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def save(self, product: Product):

        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "version": product.version,
            "actions": [
                {
                    "id": action.id,
                    "action_id": action.action_id,
                    "values": action.values,
                    "enabled": action.enabled
                }
                for action in product.actions
            ]
        }

        filename = self.directory / f"{product.name}.json"

        with open(filename, "w", encoding="utf-8") as f:
            print("========== SAVE ==========")

            for action in product.actions:
                print(action.action_id, action.values)
            json.dump(data, f, indent=4)

    def load(self, name: str) -> Product:

        filename = self.directory / f"{name}.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        product = Product(
            id=data["id"],
            name=data["name"],
            description=data["description"],
            version=data["version"]
        )

        for item in data["actions"]:

            product.actions.append(
                ProductAction(
                    id=item["id"],
                    action_id=item["action_id"],
                    values=item["values"],
                    enabled=item["enabled"]
                )

            )
            print("LOAD:", item["values"])

        return product

    def list_products(self) -> list[str]:

        return sorted(
            file.stem
            for file in self.directory.glob("*.json")
        )

    def delete(self, name: str):

        filename = self.directory / f"{name}.json"

        if filename.exists():
            filename.unlink()