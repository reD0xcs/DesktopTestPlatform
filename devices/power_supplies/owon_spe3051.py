from owon_psu import OwonPSU

from devices.power_supplies.base import PowerSupplyBase
from models.action import Action
from models.parameter import Parameter


class OwonSPE3051(PowerSupplyBase):

    @property
    def id(self):
        return "owon_spe3051"

    @property
    def name(self):
        return "OWON SPE3051"

    def __init__(self):
        self.psu = None
        self.connected = False

    def connect(self, port: str):
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

    def is_connected(self):
        # dacă nu avem obiectul psu, clar nu e conectat
        if self.psu is None:
            self.connected = False
            return False

        try:
            # dacă portul nu mai e deschis, marcăm ca deconectat
            if not self.psu.ser.is_open:
                self.connected = False
                return False

            # verificăm dacă dispozitivul răspunde efectiv
            self.psu.ser.write(b"*IDN?\n")
            resp = self.psu.ser.read(50).strip()

            self.connected = bool(resp)
            return self.connected

        except Exception:
            # orice eroare la comunicare => considerăm deconectat
            self.connected = False
            return False

    def set_voltage(self, voltage: float):
        if self.connected:
            self.psu.set_voltage(float(voltage))

    def set_current(self, current: float):
        if self.connected:
            self.psu.set_current(float(current))

    def output_on(self):
        if self.connected:
            self.psu.set_output(True)

    def output_off(self):
        if self.connected:
            self.psu.set_output(False)

    def measure_voltage(self) -> float:
        if not self.connected:
            return 0.0
        return self.psu.measure_voltage()

    def measure_current(self) -> float:
        if not self.connected:
            return 0.0
        return self.psu.measure_current()

    def get_actions(self):
        return [

            Action(
                id="owon_spe3051.set_voltage",
                name="Set Voltage",
                category="Power Supply",
                description="Set output voltage on OWON SPE3051.",
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
                id="owon_spe3051.set_current",
                name="Set Current",
                category="Power Supply",
                description="Set output current on OWON SPE3051.",
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
                id="owon_spe3051.output_on",
                name="Output ON",
                category="Power Supply",
                description="Enable power output on OWON SPE3051."
            ),

            Action(
                id="owon_spe3051.output_off",
                name="Output OFF",
                category="Power Supply",
                description="Disable power output on OWON SPE3051."
            )
        ]