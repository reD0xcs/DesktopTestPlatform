from handlers.power_supply import PowerSupplyHandler
from handlers.pi import PiHandler

from models.action_result import ActionResult


class ActionExecutor:

    def __init__(self, device_manager):

        psu = PowerSupplyHandler(device_manager)
        pi = PiHandler(device_manager)

        self.handlers = {

            "power_supply.set_voltage": psu.set_voltage,

            "power_supply.set_current": psu.set_current,

            "power_supply.output_on": psu.output_on,

            "power_supply.output_off": psu.output_off,

            "pi.rgb": pi.rgb,
        }

    def execute(self, action):

        handler = self.handlers.get(action.action_id)

        if handler is None:

            return ActionResult(
                action_id=action.action_id,
                success=False,
                message="Unknown action"
            )

        try:

            return handler(action.values)

        except Exception as e:

            return ActionResult(
                action_id=action.action_id,
                success=False,
                message=str(e)
            )