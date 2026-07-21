import json
from pathlib import Path

from models.product import Product
from models.product_action import ProductAction


class ProductSerializer:

    def __init__(self, directory="products"):
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    # ============================================================
    # SAVE PRODUCT
    # ============================================================
    def save(self, product: Product):

        data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "version": product.version,
            "actions": [action.to_dict() for action in product.actions]
        }

        filename = self.directory / f"{product.name}.json"

        with open(filename, "w", encoding="utf-8") as f:
            print("========== SAVE ==========")
            for action in product.actions:
                print(action.action_id, action.values)
            json.dump(data, f, indent=4)

    # ============================================================
    # LOAD PRODUCT
    # ============================================================
    def load(self, name: str) -> Product:

        filename = self.directory / f"{name}.json"

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)

        product = Product(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            version=data.get("version", "1.0")
        )

        # Load actions recursively
        product.actions = [
            ProductAction.from_dict(item)
            for item in data.get("actions", [])
        ]

        return product

    # ============================================================
    # LIST PRODUCTS
    # ============================================================
    def list_products(self) -> list[str]:
        return sorted(
            file.stem
            for file in self.directory.glob("*.json")
        )

    # ============================================================
    # DELETE PRODUCT
    # ============================================================
    def delete(self, name: str):

        filename = self.directory / f"{name}.json"

        if filename.exists():
            filename.unlink()
