import importlib
import inspect
import pkgutil
import serial.tools.list_ports

import devices.power_supplies
from devices.power_supplies.base import PowerSupplyBase


class PowerSupplyManager:

    def __init__(self):
        self.power_supplies = {}
        self._load_power_supplies()

        # salvăm porturile inițiale
        self.last_ports = self.get_current_ports()

        # încercăm conectarea automată
        self._auto_connect()

    def get_actions(self):
        actions = []

        for ps in self.power_supplies.values():

            # fiecare PSU expune propriile acțiuni
            if hasattr(ps, "get_actions"):
                actions.extend(ps.get_actions())

        return actions


    # --------------------------------------------------
    # PORT DETECTION
    # --------------------------------------------------

    def get_current_ports(self):
        return {port.device for port in serial.tools.list_ports.comports()}

    def check_for_changes(self):
        current = self.get_current_ports()

        if current != self.last_ports:
            print("🔄 Port change detected — reloading power supplies...")
            self.last_ports = current
            self._load_power_supplies()
            self._auto_connect()

    # --------------------------------------------------
    # AUTO CONNECT
    # --------------------------------------------------

    def _auto_connect(self):
        for ps in self.power_supplies.values():
            if not ps.is_connected():
                try:
                    if ps.id == "owon_spe3051":
                        ps.connect("COM12")
                except Exception as e:
                    print(f"⚠ Failed to connect {ps.name}: {e}")

    # --------------------------------------------------
    # LOAD DRIVERS
    # --------------------------------------------------

    def _load_power_supplies(self):

        self.power_supplies.clear()

        for _, module_name, _ in pkgutil.iter_modules(devices.power_supplies.__path__):
            if module_name == "base":
                continue

            module = importlib.import_module(f"devices.power_supplies.{module_name}")

            for _, obj in inspect.getmembers(module, inspect.isclass):

                # ignorăm clasele abstracte
                if inspect.isabstract(obj):
                    continue

                # ignorăm clasa de bază
                if obj is PowerSupplyBase:
                    continue

                # încărcăm doar driverele reale
                if issubclass(obj, PowerSupplyBase):
                    instance = obj()
                    self.power_supplies[instance.id] = instance
                    print(f"✓ Loaded Power Supply: {instance.name}")


    # --------------------------------------------------
    # PUBLIC API
    # --------------------------------------------------

    def get_available(self):
        self.check_for_changes()
        return list(self.power_supplies.values())

    def get(self, id):
        return self.power_supplies.get(id)
    
    
