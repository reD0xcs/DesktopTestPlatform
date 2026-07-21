import serial

class OwonPSU:

    SUPPORTED_DEVICES = {"OWON,SPE", "OWON,SPM", "OWON,P4","KIPRIM,DC"}

    def __init__(self, port, default_timeout=0.5):
        self.ser = None
        self.port = port
        self.timeout = default_timeout

    def open(self):
        self.ser = serial.Serial(self.port, 115200, timeout=self.timeout)
        identity = self.read_identity()
        if not any([s in identity for s in self.SUPPORTED_DEVICES]):
            self.close()
            raise Exception("Not connected to a supported PSU!")

    def close(self):
        self.ser.close()

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *args, **kwargs):
        self.close()

    # --------------------------------------------------
    # FIXED RAW READ (critical for SPE3051)
    # --------------------------------------------------
    def _cmd(self, command, accept_silent=False, timeout=None):
        if self.ser is None:
            raise Exception("Connection is not open!")

        self.ser.write(bytes(command, 'utf-8') + b"\n")
        self.ser.timeout = timeout if timeout is not None else self.timeout

        ret = self.ser.read(64).decode('utf-8', errors='ignore').strip()

        if len(ret) == 0 and not accept_silent:
            raise Exception(f"No response for command: '{command}'!")

        return ret

    def _silent_cmd(self, command, timeout=0.01):
        if self._cmd(command, accept_silent=True, timeout=timeout) == "ERR":
            raise Exception(f"Error while executing command: '{command}'")

    # --------------------------------------------------
    # IDENTITY
    # --------------------------------------------------
    def read_identity(self):
        return self._cmd("*IDN?")

    # --------------------------------------------------
    # MEASUREMENTS (SCPI — works with RAW read)
    # --------------------------------------------------
    def measure_voltage(self):
        return float(self._cmd("MEASure:VOLTage?"))

    def measure_current(self):
        return float(self._cmd("MEASure:CURRent?"))

    # --------------------------------------------------
    # GETTERS
    # --------------------------------------------------
    def get_voltage(self):
        return float(self._cmd("VOLTage?"))

    def get_current(self):
        return float(self._cmd("CURRent?"))

    def get_voltage_limit(self):
        return float(self._cmd("VOLTage:LIMit?"))

    def get_current_limit(self):
        return float(self._cmd("CURRent:LIMit?"))

    # --------------------------------------------------
    # SETTERS
    # --------------------------------------------------
    def set_voltage(self, voltage):
        return self._silent_cmd(f"VOLTage {voltage:.3f}")

    def set_current(self, current):
        return self._silent_cmd(f"CURRent {current:.3f}")

    def set_voltage_limit(self, voltage):
        return self._silent_cmd(f"VOLTage:LIMit {voltage:.3f}")

    def set_current_limit(self, current):
        return self._silent_cmd(f"CURRent:LIMit {current:.3f}")

    # --------------------------------------------------
    # OUTPUT CONTROL
    # --------------------------------------------------
    def get_output(self):
        ret = self._cmd(f"OUTPut?")
        if ret in ["0", "1"]:
            return ret == "1"

        if ret not in ["ON", "OFF"]:
            raise Exception(f"Unknown return for get output command: {ret}")
        return ret == "ON"

    def set_output(self, enabled):
        self._silent_cmd(f"OUTPut {'ON' if enabled else 'OFF'}")

    # --------------------------------------------------
    # SYSTEM CONTROL
    # --------------------------------------------------
    def set_keylock(self, enabled):
        if enabled:
            self._silent_cmd("SYST:REM")
        else:
            self._silent_cmd("SYST:LOC")
