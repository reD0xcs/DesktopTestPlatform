from time import sleep

from models.action_result import ActionResult


class ActionExecutor:

    def __init__(self, device_manager):

        self.device_manager = device_manager

    # ==================================================
    # PUBLIC
    # ==================================================

    def execute(self, product_action):

        try:

            action_id = product_action.action_id

            if action_id.startswith("system."):

                return self._execute_system(
                    action_id,
                    product_action.values
                )

            if action_id.startswith("pi."):

                return self._execute_pi(
                    action_id,
                    product_action.values
                )

            return self._execute_power_supply(
                action_id,
                product_action.values
            )

        except Exception as e:

            return ActionResult(
                action_id=product_action.action_id,
                success=False,
                message=str(e)
            )

    # ==================================================
    # SYSTEM
    # ==================================================

    def _execute_system(self, action_id, values):

        command = action_id.split(".")[1]

        if command == "delay":

            print("VALUES:", values)

            seconds = float(
                values.get("seconds", 0)
            )

            print("SECONDS:", seconds)

            sleep(seconds)

            return ActionResult(
                action_id=action_id,
                success=True,
                message=f"Delayed {seconds}s"
            )

        elif command == "message":

            print(
                values.get("message", "")
            )

            return ActionResult(
                action_id=action_id,
                success=True,
                message="Message displayed"
            )

        return ActionResult(
            action_id=action_id,
            success=False,
            message="Unknown system action"
        )

    # ==================================================
    # POWER SUPPLY
    # ==================================================

    def _execute_power_supply(self, action_id, values):

        device_id, command = action_id.split(".", 1)

        psu = self.device_manager.power_supplies.get(
            device_id
        )

        if psu is None:

            return ActionResult(
                action_id=action_id,
                success=False,
                message="Power supply not found"
            )

        if command == "set_voltage":

            psu.set_voltage(
                values.get("voltage", 0)
            )

        elif command == "set_current":

            psu.set_current(
                values.get("current", 0)
            )

        elif command == "output_on":

            psu.output_on()

        elif command == "output_off":

            psu.output_off()

        else:

            return ActionResult(
                action_id=action_id,
                success=False,
                message="Unknown PSU action"
            )

        return ActionResult(
            action_id=action_id,
            success=True,
            message="OK"
        )

    # ==================================================
    # RASPBERRY PI
    # ==================================================

    def _execute_pi(self, action_id, values):

        test_id = action_id.replace(
            "pi.",
            ""
        )

        self.device_manager.pi.run_test(
            test_id
        )

        return ActionResult(
            action_id=action_id,
            success=True,
            message="OK"
        )