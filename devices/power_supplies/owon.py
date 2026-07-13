from owon_psu import OwonPSU

from devices.power_supplies.base import PowerSupplyBase
from models.action import Action
from models.parameter import Parameter


class OwonPowerSupply(PowerSupplyBase):

    @property
    def id(self):
        return "owon"

    @property
    def name(self):
        return "OWON SPE6103"

    def __init__(self):
        self.psu = None
        self.connected = False

    def connect(self, port):

        self.psu = OwonPSU(port)
        self.psu.open()

        self.connected = True

        return self.psu.read_identity()

    def disconnect(self):

        if self.psu:

            try:
                self.psu.close()
            except Exception:
                pass

        self.connected = False

    def set_voltage(self, voltage):

        if self.connected:
            self.psu.set_voltage(float(voltage))

    def set_current(self, current):

        if self.connected:
            self.psu.set_current(float(current))

    def output_on(self):

        if self.connected:
            self.psu.set_output(True)

    def output_off(self):

        if self.connected:
            self.psu.set_output(False)

    def measure_voltage(self):

        if not self.connected:
            return 0

        return self.psu.measure_voltage()

    def measure_current(self):

        if not self.connected:
            return 0

        return self.psu.measure_current()

    def get_actions(self):

        return [

            Action(
                id="owon.set_voltage",
                name="Set Voltage",
                category="Power Supply",
                description="Set output voltage.",
                parameters=[
                    Parameter(
                        id="voltage",
                        name="Voltage",
                        type="float",
                        default=12.0,
                        unit="V",
                        minimum=0,
                        maximum=60
                    )
                ]
            ),

            Action(
                id="owon.set_current",
                name="Set Current",
                category="Power Supply",
                description="Set output current.",
                parameters=[
                    Parameter(
                        id="current",
                        name="Current",
                        type="float",
                        default=1.0,
                        unit="A",
                        minimum=0
                    )
                ]
            ),

            Action(
                id="owon.output_on",
                name="Output ON",
                category="Power Supply",
                description="Enable power output."
            ),

            Action(
                id="owon.output_off",
                name="Output OFF",
                category="Power Supply",
                description="Disable power output."
            )
        ]