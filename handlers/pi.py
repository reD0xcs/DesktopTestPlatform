from models.action_result import ActionResult


class PiHandler:

    def __init__(self, device_manager):
        self.pi = device_manager.pi

    def rgb(self, values):

        result = self.pi.run_test("rgb")

        return ActionResult(
            action_id="pi.rgb",
            success=result["success"],
            message=result.get("message", ""),
            outputs=result.get("data", {})
        )