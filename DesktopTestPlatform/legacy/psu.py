from owon_psu import OwonPSU

class PowerSupply:
    def __init__(self):
        self.psu=None
        self.connected=False
    def connect(self,port):
        self.psu=OwonPSU(port)
        self.psu.open()
        self.connected=True
        return self.psu.read_identity()
    def disconnect(self):
        if self.psu:
            try:self.psu.close()
            except: pass
        self.connected=False
    def set_voltage(self,v):
        if self.connected:self.psu.set_voltage(float(v))
    def set_current(self,c):
        if self.connected:self.psu.set_current(float(c))
    def output_on(self):
        if self.connected:self.psu.set_output(True)
    def output_off(self):
        if self.connected:self.psu.set_output(False)
    def measure_voltage(self):
        return self.psu.measure_voltage() if self.connected else 0
    def measure_current(self):
        return self.psu.measure_current() if self.connected else 0
    def measure_power(self):
        return self.measure_voltage()*self.measure_current()