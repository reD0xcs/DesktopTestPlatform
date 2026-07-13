from models.action import Action
from models.parameter import Parameter


def get_actions():

    return [

        Action(
            id="system.delay",
            name="Delay",
            device="system",
            category="System",
            description="Wait for a specified amount of time.",
            parameters=[
                Parameter(
                    id="seconds",
                    name="Seconds",
                    type="float",
                    default=1.0,
                    description="Delay in seconds",
                    unit="s"
                )
            ]
        ),

        Action(
            id="system.message",
            name="Message",
            device="system",
            category="System",
            description="Display a message to the operator."
        )
    ]