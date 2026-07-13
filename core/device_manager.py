from devices.raspberry_pi.pi_client import PiClient
from devices.power_supplies.manager import PowerSupplyManager
from config.settings import settings


class DeviceManager:

    def __init__(self):

        self.power_supplies = PowerSupplyManager()

        # momentan localhost deoarece putem testa direct pe Pi
        self.pi = PiClient(
            host=settings.raspberry_pi["host"],
            port=settings.raspberry_pi["port"]
        )

    def get_actions(self):

        actions = []

        actions.extend(self.power_supplies.get_actions())
        actions.extend(self.pi.get_actions())

        return actions

    def is_pi_connected(self):

        try:
            self.pi.health()
            return True
        except Exception:
            return False

    def get_devices(self):
        return {
            "power_supplies": self.power_supplies.get_available(),
            "raspberry_pi": {
                "connected": self.is_pi_connected()
            }
        }