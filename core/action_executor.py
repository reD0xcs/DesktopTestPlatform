from time import sleep
from models.action_result import ActionResult


class ActionExecutor:

    def __init__(self, device_manager):
        self.device_manager = device_manager

    # ==================================================
    # PUBLIC
    # ==================================================

    def execute(
        self,
        product_action,
        progress_callback=None,
        stop_callback=None,
        pause_callback=None
    ):
        try:
            action_id = product_action.action_id

            # SYSTEM ACTIONS
            if action_id.startswith("system."):
                return self._execute_system(
                    action_id,
                    product_action.values,
                    progress_callback,
                    stop_callback,
                    pause_callback
                )

            # RASPBERRY PI ACTIONS
            if action_id.startswith("pi."):
                return self._execute_pi(
                    action_id,
                    product_action.values
                )

            # POWER SUPPLY ACTIONS
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

    def _execute_system(
        self,
        action_id,
        values,
        progress_callback=None,
        stop_callback=None,
        pause_callback=None
    ):
        command = action_id.split(".")[1]

        if command == "delay":
            seconds = float(values.get("seconds", 0))
            steps = max(int(seconds * 20), 1)

            for i in range(steps):

                # STOP
                if stop_callback and stop_callback():
                    return ActionResult(
                        action_id=action_id,
                        success=False,
                        message="Stopped"
                    )

                # PAUSE
                if pause_callback:
                    pause_event = pause_callback()
                    pause_event.wait()

                    if stop_callback and stop_callback():
                        return ActionResult(
                            action_id=action_id,
                            success=False,
                            message="Stopped"
                        )

                sleep(seconds / steps)

                if progress_callback:
                    progress_callback(
                        (i + 1) / steps,
                        seconds - ((i + 1) * seconds / steps)
                    )

            return ActionResult(
                action_id=action_id,
                success=True,
                message=f"Delayed {seconds}s"
            )

        elif command == "message":
            print(values.get("message", ""))
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
    # POWER SUPPLY (ROBUST)
    # ==================================================

    def _execute_power_supply(self, action_id, values):

        device_id, command = action_id.split(".", 1)

        # obținem instanța reală
        psu = self.device_manager.power_supplies.get(device_id)

        if psu is None:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=f"Power supply '{device_id}' not found"
            )

        # verificare conectare reală
        if not psu.is_connected():
            return ActionResult(
                action_id=action_id,
                success=False,
                message=f"Power supply '{psu.name}' is not connected"
            )

        try:
            if command == "set_voltage":
                psu.set_voltage(values.get("voltage", 0))

            elif command == "set_current":
                psu.set_current(values.get("current", 0))

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

        except Exception as e:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=str(e)
            )

    # ==================================================
    # RASPBERRY PI
    # ==================================================

    def _execute_pi(self, action_id, values):

        test_id = action_id.replace("pi.", "")

        try:
            self.device_manager.pi.run_test(test_id)
            return ActionResult(
                action_id=action_id,
                success=True,
                message="OK"
            )
        except Exception as e:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=str(e)
            )
