from abc import ABC
from devices.power_supplies.base import PowerSupplyBase
from owon_psu import OwonPSU

class OwonBase(PowerSupplyBase, ABC):

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

    def is_connected(self):
        if self.psu is None:
            self.connected = False
            return False

        try:
            if not self.psu.ser.is_open:
                self.connected = False
                return False

            self.psu.ser.write(b"*IDN?\n")
            resp = self.psu.ser.read(50).strip()
            self.connected = bool(resp)
            return self.connected

        except Exception:
            self.connected = False
            return False

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
            return 0.0
        return self.psu.measure_voltage()

    def measure_current(self):
        if not self.connected:
            return 0.0
        return self.psu.measure_current()
