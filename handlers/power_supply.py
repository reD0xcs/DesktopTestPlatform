from models.action_result import ActionResult


class PowerSupplyHandler:

    def __init__(self, device_manager):
        self.psu = device_manager.power_supply

    def set_voltage(self, values):

        voltage = values["voltage"]

        self.psu.set_voltage(voltage)

        return ActionResult(
            action_id="power_supply.set_voltage",
            success=True,
            message=f"Voltage set to {voltage} V"
        )

    def set_current(self, values):

        current = values["current"]

        self.psu.set_current(current)

        return ActionResult(
            action_id="power_supply.set_current",
            success=True,
            message=f"Current set to {current} A"
        )

    def output_on(self, values):

        self.psu.output_on()

        return ActionResult(
            action_id="power_supply.output_on",
            success=True,
            message="Output ON"
        )

    def output_off(self, values):

        self.psu.output_off()

        return ActionResult(
            action_id="power_supply.output_off",
            success=True,
            message="Output OFF"
        )