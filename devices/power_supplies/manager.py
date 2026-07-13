import importlib
import inspect
import pkgutil

import devices.power_supplies
from devices.power_supplies.base import PowerSupplyBase
from models.action import Action
from models.parameter import Parameter

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

    def get_actions(self) -> list[Action]:

        actions = []

        for ps in self.power_supplies.values():
            actions.extend([

                Action(
                    id=f"{ps.id}.set_voltage",
                    name="Set Voltage",
                    device=ps.id,
                    category="Power Supply",
                    description=f"Set voltage on {ps.name}",
                    parameters=[
                        Parameter(
                            id="voltage",
                            name="Voltage",
                            type="float",
                            default=0.0,
                            description="Voltage (V)",
                            unit="V"
                        )
                    ]
                ),

                Action(
                    id=f"{ps.id}.set_current",
                    name="Set Current",
                    device=ps.id,
                    category="Power Supply",
                    description=f"Set current on {ps.name}",
                    parameters=[
                        Parameter(
                            id="current",
                            name="Current",
                            type="float",
                            default=0.0,
                            description="Current (A)",
                            unit="A"
                        )
                    ]
                ),

                Action(
                    id=f"{ps.id}.output_on",
                    name="Output ON",
                    device=ps.id,
                    category="Power Supply",
                    description=f"Enable output on {ps.name}"
                ),

                Action(
                    id=f"{ps.id}.output_off",
                    name="Output OFF",
                    device=ps.id,
                    category="Power Supply",
                    description=f"Disable output on {ps.name}"
                )

            ])

        return actions

    def get(self, id):

        return self.power_supplies.get(id)