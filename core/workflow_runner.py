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
    # RUN WORKFLOW
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
        total = len(actions)

        # ==================================================
        # EXECUTE EACH ACTION
        # ==================================================
        for index, action in enumerate(actions):

            # UI updates
            if self.ui:
                self.ui.set_step_label(f"Step {index+1} / {total}")
                self.ui.set_current_action(action.action_id)
                self.ui.set_overall_progress(index / total)
                self.ui.set_step_progress(0)

            # STOP
            if stop_callback and stop_callback():
                results.append(ActionResult(
                    action_id=action.action_id,
                    success=False,
                    message="Stopped"
                ))
                break

            # PAUSE
            if pause_callback:
                pause_event = pause_callback()
                pause_event.wait()

                if stop_callback and stop_callback():
                    results.append(ActionResult(
                        action_id=action.action_id,
                        success=False,
                        message="Stopped"
                    ))
                    break

            # EXECUTE ACTION
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

            # STOP ON FAILURE
            if not result.success:
                fail_line = f"FAILED at step {action.action_id}"
                logs.append(fail_line)

                if self.ui:
                    self.ui.append_log(fail_line)

                break


            # COLLECT MEASUREMENTS
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
        # METADATA
        # ==================================================

        duration = (datetime.now() - start_time).total_seconds()

        # Industrial test ID
        test_id = f"{product.name}-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        # SSH hash
        ssh_hash = hashlib.sha256(test_id.encode()).hexdigest()

        # QR code
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
