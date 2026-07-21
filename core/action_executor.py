from time import sleep, time
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
        start = time()
        action_id = product_action.action_id

        try:
            # SYSTEM ACTIONS
            if action_id.startswith("system."):
                result = self._execute_system(
                    action_id,
                    product_action.values,
                    progress_callback,
                    stop_callback,
                    pause_callback
                )

            # RASPBERRY PI ACTIONS
            elif action_id.startswith("pi."):
                result = self._execute_pi(
                    action_id,
                    product_action.values
                )

            # POWER SUPPLY ACTIONS
            else:
                result = self._execute_power_supply(
                    action_id,
                    product_action.values
                )

            # complete result with duration + timestamp
            result.duration = time() - start
            result.timestamp = start

            return result

        except Exception as e:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=str(e),
                outputs={},
                duration=time() - start,
                timestamp=start
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

        # ----------------------------------------------
        # DELAY
        # ----------------------------------------------
        if command == "delay":
            seconds = float(values.get("seconds", 0))
            steps = max(int(seconds * 20), 1)

            for i in range(steps):

                # STOP
                if stop_callback and stop_callback():
                    return ActionResult(
                        action_id=action_id,
                        success=False,
                        message="Stopped",
                        outputs={}
                    )

                # PAUSE
                if pause_callback:
                    pause_event = pause_callback()
                    pause_event.wait()

                    if stop_callback and stop_callback():
                        return ActionResult(
                            action_id=action_id,
                            success=False,
                            message="Stopped",
                            outputs={}
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
                message=f"Delayed {seconds}s",
                outputs={"delay": seconds}
            )

        # ----------------------------------------------
        # MESSAGE
        # ----------------------------------------------
        elif command == "message":
            msg = values.get("message", "")
            print(msg)
            return ActionResult(
                action_id=action_id,
                success=True,
                message="Message displayed",
                outputs={"message": msg}
            )

        return ActionResult(
            action_id=action_id,
            success=False,
            message="Unknown system action",
            outputs={}
        )

    # ==================================================
    # POWER SUPPLY (ROBUST)
    # ==================================================

    def _execute_power_supply(self, action_id, values):

        # --------------------------------------------------
        # PARSE ACTION
        # --------------------------------------------------
        device_id, command = action_id.split(".", 1)
        psu = self.device_manager.power_supplies.get(device_id)

        print(f"[DEBUG] Executing PSU action: {action_id}")
        print(f"[DEBUG] PSU object: {psu}")

        # --------------------------------------------------
        # PSU NOT FOUND
        # --------------------------------------------------
        if psu is None:
            print(f"[DEBUG] PSU '{device_id}' not found in manager")
            return ActionResult(
                action_id=action_id,
                success=False,
                message=f"Power supply '{device_id}' not found",
                outputs={}
            )

        # --------------------------------------------------
        # CHECK CONNECTION
        # --------------------------------------------------
        connected = psu.is_connected()
        print(f"[DEBUG] PSU connected state before action: {connected}")

        if not connected:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=f"Power supply '{psu.name}' is not connected",
                outputs={}
            )

        # --------------------------------------------------
        # EXECUTE COMMAND
        # --------------------------------------------------
        try:
            print(f"[DEBUG] Executing command '{command}' on PSU '{device_id}'")

            if command == "set_voltage":
                voltage = values.get("voltage", 0)
                print(f"[DEBUG] set_voltage({voltage})")
                psu.set_voltage(voltage)

            elif command == "set_current":
                current = values.get("current", 0)
                print(f"[DEBUG] set_current({current})")
                psu.set_current(current)

            elif command == "output_on":
                print("[DEBUG] output_on()")
                psu.output_on()

            elif command == "output_off":
                print("[DEBUG] output_off()")
                psu.output_off()

            else:
                print(f"[DEBUG] Unknown PSU command: {command}")
                return ActionResult(
                    action_id=action_id,
                    success=False,
                    message=f"Unknown PSU action '{command}'",
                    outputs={}
                )

            # --------------------------------------------------
            # READ MEASUREMENTS (CORRECT API)
            # --------------------------------------------------
            voltage = psu.measure_voltage()
            current = psu.measure_current()

            print(f"[DEBUG] PSU voltage read: {voltage}")
            print(f"[DEBUG] PSU current read: {current}")

            return ActionResult(
                action_id=action_id,
                success=True,
                message="OK",
                outputs={
                    "voltage": voltage,
                    "current": current,
                    "time": time()
                }
            )

        except Exception as e:
            print(f"[DEBUG] Exception while executing PSU action: {e}")
            return ActionResult(
                action_id=action_id,
                success=False,
                message=str(e),
                outputs={}
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
                message="OK",
                outputs={"pi_test": test_id}
            )

        except Exception as e:
            return ActionResult(
                action_id=action_id,
                success=False,
                message=str(e),
                outputs={}
            )
