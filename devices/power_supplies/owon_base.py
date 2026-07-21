import time
from abc import ABC
from devices.power_supplies.base import PowerSupplyBase
from devices.power_supplies.owon_psu import OwonPSU


class OwonBase(PowerSupplyBase, ABC):

    def __init__(self):
        self.psu = None
        self.connected = False

    def connect(self, port):
        print(f"[DEBUG] Trying to connect OWON on port {port}")

        self.psu = OwonPSU(port)
        self.psu.open()

        print(f"[DEBUG] Port opened: {self.psu.ser.is_open}")
        print(f"[DEBUG] Identity read attempt...")

        try:
            ident = self.psu.read_identity()
            print(f"[DEBUG] Identity response: {ident}")
        except Exception as e:
            print(f"[DEBUG] Identity read failed: {e}")

        self.connected = True
        print(f"[DEBUG] Connected flag set to True")
        return True


    def disconnect(self):
        if self.psu:
            try:
                self.psu.close()
            except Exception:
                pass
        self.connected = False

    def is_connected(self):
        print("[DEBUG] is_connected() called")

        if self.psu is None:
            print("[DEBUG] psu is None → NOT CONNECTED")
            self.connected = False
            return False

        try:
            print(f"[DEBUG] Serial open: {self.psu.ser.is_open}")
            self.connected = self.psu.ser.is_open
            print(f"[DEBUG] Final connected state: {self.connected}")
            return self.connected

        except Exception as e:
            print(f"[DEBUG] Exception in is_connected(): {e}")
            self.connected = False
            return False


    # ==================================================
    # ACTIONS WITH INDUSTRIAL DELAY
    # ==================================================

    def set_voltage(self, voltage):
        if self.connected:
            self.psu.set_voltage(float(voltage))
            time.sleep(0.25)   # OWON lag

    def set_current(self, current):
        if self.connected:
            self.psu.set_current(float(current))
            time.sleep(0.25)   # OWON lag

    def output_on(self):
        if self.connected:
            self.psu.set_output(True)
            time.sleep(0.35)   # OWON lag

    def output_off(self):
        if self.connected:
            self.psu.set_output(False)
            time.sleep(0.35)   # OWON lag

    # ==================================================
    # MEASUREMENTS
    # ==================================================

    def measure_voltage(self):
        if not self.connected:
            return 0.0
        return self.psu.measure_voltage()

    def measure_current(self):
        if not self.connected:
            return 0.0
        return self.psu.measure_current()
