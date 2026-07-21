from datetime import datetime
import hashlib
import qrcode
import os

from core.action_executor import ActionExecutor
from core.report_generator import ReportGenerator
from models.action_result import ActionResult


class WorkflowRunner:

    def __init__(self, device_manager, ui=None):
        self.device_manager = device_manager
        self.executor = ActionExecutor(device_manager)
        self.report_generator = ReportGenerator()
        self.ui = ui  # RunWindow injectat

    # ==================================================
    # CONDITION EVALUATOR
    # ==================================================
    def eval_condition(self, values):
        left = values.get("left")
        op = values.get("op")
        right = float(values.get("right"))

        # citim valorile runtime
        if left == "voltage":
            lv = self.device_manager.power_supplies.measure_voltage()
        elif left == "current":
            lv = self.device_manager.power_supplies.measure_current()
        else:
            lv = float(left)

        if op == ">": return lv > right
        if op == "<": return lv < right
        if op == "==": return lv == right
        if op == "!=": return lv != right
        if op == ">=": return lv >= right
        if op == "<=": return lv <= right

        return False

    # ==================================================
    # RECURSIVE ACTION EXECUTION
    # ==================================================
    def run_actions(
        self,
        actions,
        results,
        logs,
        measurements,
        progress_callback,
        stop_callback,
        pause_callback
    ):

        for action in actions:

            # STOP
            if stop_callback and stop_callback():
                results.append(ActionResult(action_id=action.action_id, success=False, message="Stopped"))
                return

            # PAUSE
            if pause_callback:
                pause_event = pause_callback()
                pause_event.wait()

                if stop_callback and stop_callback():
                    results.append(ActionResult(action_id=action.action_id, success=False, message="Stopped"))
                    return

            # ==================================================
            # CONTROL: IF
            # ==================================================
            if action.action_id == "control.if":
                cond = self.eval_condition(action.values)

                if cond:
                    self.run_actions(
                        action.children,
                        results,
                        logs,
                        measurements,
                        progress_callback,
                        stop_callback,
                        pause_callback
                    )
                else:
                    self.run_actions(
                        action.else_children,
                        results,
                        logs,
                        measurements,
                        progress_callback,
                        stop_callback,
                        pause_callback
                    )
                continue

            # ==================================================
            # CONTROL: LOOP
            # ==================================================
            if action.action_id == "control.loop":
                count = int(action.values.get("count", 1))

                for _ in range(count):
                    self.run_actions(
                        action.children,
                        results,
                        logs,
                        measurements,
                        progress_callback,
                        stop_callback,
                        pause_callback
                    )
                continue

            # ==================================================
            # CONTROL: ASSERT
            # ==================================================
            if action.action_id == "control.assert":
                cond = self.eval_condition(action.values)

                if not cond:
                    msg = f"Assertion failed: {action.values}"
                    results.append(ActionResult(action_id=action.action_id, success=False, message=msg))
                    logs.append(msg)
                    return

                continue

            # ==================================================
            # NORMAL ACTION
            # ==================================================
            result = self.executor.execute(
                action,
                progress_callback=progress_callback,
                stop_callback=stop_callback,
                pause_callback=pause_callback
            )

            results.append(result)

            log_line = (
                f"[{datetime.now().isoformat(timespec='seconds')}] "
                f"{action.action_id} → {result.success}"
            )
            logs.append(log_line)

            if self.ui:
                self.ui.append_log(log_line)

            if not result.success:
                logs.append(f"FAILED at step {action.action_id}")
                return

            # MEASUREMENTS
            if result.outputs:
                if "voltage" in result.outputs:
                    measurements["voltage"].append(
                        (result.outputs.get("time", 0), result.outputs["voltage"])
                    )
                if "current" in result.outputs:
                    measurements["current"].append(
                        (result.outputs.get("time", 0), result.outputs["current"])
                    )

    # ==================================================
    # RUN WORKFLOW (ENTRY POINT)
    # ==================================================
    def run(
        self,
        product,
        actions,
        progress_callback=None,
        stop_callback=None,
        pause_callback=None
    ):

        results = []
        logs = []
        measurements = {"voltage": [], "current": []}

        start_time = datetime.now()

        # ==================================================
        # EXECUTE WORKFLOW (recursive)
        # ==================================================
        self.run_actions(
            actions,
            results,
            logs,
            measurements,
            progress_callback,
            stop_callback,
            pause_callback
        )

        # ==================================================
        # METADATA
        # ==================================================
        duration = (datetime.now() - start_time).total_seconds()

        test_id = f"{product.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        ssh_hash = hashlib.sha256(test_id.encode()).hexdigest()

        qr_path = os.path.join(os.getcwd(), f"{test_id}_qr.png")
        qrcode.make(test_id).save(qr_path)

        metadata = {
            "software_version": "1.0.0",
            "hardware_version": "1.0.0",
            "procedure_id": "PSU_VALIDATION_V1.0",
            "batch_number": getattr(product, "batch_number", None),
            "serial_number": getattr(product, "serial_number", None),
            "logs": logs,
            "duration": duration,
            "test_id": test_id,
            "ssh_hash": ssh_hash,
            "qr_path": qr_path
        }

        # ==================================================
        # GENERATE REPORT
        # ==================================================
        report_path = self.report_generator.generate(
            product,
            results,
            metadata,
            measurements
        )

        return results, report_path
