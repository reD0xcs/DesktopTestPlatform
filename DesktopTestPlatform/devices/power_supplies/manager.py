import importlib
import inspect
import pkgutil

import devices.power_supplies
from devices.power_supplies.base import PowerSupplyBase


class PowerSupplyManager:

    def __init__(self):
        self.power_supplies = {}
        self._load_power_supplies()

    def _load_power_supplies(self):

        for _, module_name, _ in pkgutil.iter_modules(devices.power_supplies.__path__):

            if module_name == "base":
                continue

            module = importlib.import_module(
                f"devices.power_supplies.{module_name}"
            )

            for _, obj in inspect.getmembers(module, inspect.isclass):

                if issubclass(obj, PowerSupplyBase) and obj is not PowerSupplyBase:

                    instance = obj()

                    self.power_supplies[instance.id] = instance

                    print(f"✓ Loaded Power Supply: {instance.name}")

    def get_available(self):

        return [
            {
                "id": ps.id,
                "name": ps.name
            }
            for ps in self.power_supplies.values()
        ]

    def get(self, id):

        return self.power_supplies.get(id)