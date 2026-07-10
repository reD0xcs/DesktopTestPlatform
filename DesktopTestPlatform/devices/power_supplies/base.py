from abc import ABC, abstractmethod


class PowerSupplyBase(ABC):

    @property
    @abstractmethod
    def id(self) -> str:
        """Unique identifier"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Display name"""
        pass

    @abstractmethod
    def connect(self, port: str):
        pass

    @abstractmethod
    def disconnect(self):
        pass

    @abstractmethod
    def set_voltage(self, voltage: float):
        pass

    @abstractmethod
    def set_current(self, current: float):
        pass

    @abstractmethod
    def output_on(self):
        pass

    @abstractmethod
    def output_off(self):
        pass

    @abstractmethod
    def measure_voltage(self) -> float:
        pass

    @abstractmethod
    def measure_current(self) -> float:
        pass

    def measure_power(self) -> float:
        return self.measure_voltage() * self.measure_current()