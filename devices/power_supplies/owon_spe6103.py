from devices.power_supplies.owon_base import OwonBase
from models.action import Action
from models.parameter import Parameter

class OwonSPE6103(OwonBase):

    @property
    def id(self):
        return "owon_spe6103"

    @property
    def name(self):
        return "OWON SPE6103"

    def connect(self, port):
        print(f"[DEBUG] Trying to connect SPE6103 on port {port}")

        if not super().connect(port):
            return False

        ident = self.psu.read_identity()
        if "SPE6103" not in ident:
            print("[DEBUG] Wrong device: expected SPE6103")
            self.disconnect()
            return False

        return True

    def get_actions(self):
        return [
            Action(
                id=f"{self.id}.set_voltage",
                name="Set Voltage",
                device=self.id,
                category=self.id,
                description="Set voltage on OWON SPE6103",
                parameters=[
                    Parameter(
                        id="voltage",
                        name="Voltage",
                        type="float",
                        default=12.0,
                        unit="V",
                        minimum=0,
                        maximum=30
                    )
                ]
            ),
            Action(
                id=f"{self.id}.set_current",
                name="Set Current",
                device=self.id,
                category=self.id,
                description="Set current on OWON SPE6103",
                parameters=[
                    Parameter(
                        id="current",
                        name="Current",
                        type="float",
                        default=1.0,
                        unit="A",
                        minimum=0,
                        maximum=5
                    )
                ]
            ),
            Action(
                id=f"{self.id}.output_on",
                name="Output ON",
                device=self.id,
                category=self.id,
                description="Enable output"
            ),
            Action(
                id=f"{self.id}.output_off",
                name="Output OFF",
                device=self.id,
                category=self.id,
                description="Disable output"
            )
        ]
