from models.action import Action
from models.parameter import Parameter

def get_actions():

    return [

        # ============================================================
        # IF CONDITION
        # ============================================================
        Action(
            id="control.if",
            name="IF Condition",
            device="system",
            category="Control",
            description="Execute child actions only if condition is true.",
            parameters=[
                Parameter(
                    id="left",
                    name="Left Operand",
                    type="string",
                    default="voltage",
                    description="Value to compare (voltage/current/number)"
                ),
                Parameter(
                    id="op",
                    name="Operator",
                    type="string",
                    default=">",
                    description="Comparison operator"
                ),
                Parameter(
                    id="right",
                    name="Right Operand",
                    type="float",
                    default=0.0,
                    description="Value to compare against"
                )
            ]
        ),

        # ============================================================
        # LOOP / REPEAT
        # ============================================================
        Action(
            id="control.loop",
            name="Repeat",
            device="system",
            category="Control",
            description="Repeat child actions N times.",
            parameters=[
                Parameter(
                    id="count",
                    name="Repeat Count",
                    type="int",
                    default=1,
                    description="Number of repetitions"
                )
            ]
        ),

        # ============================================================
        # ASSERT
        # ============================================================
        Action(
            id="control.assert",
            name="Assert",
            device="system",
            category="Control",
            description="Fail test if condition is false.",
            parameters=[
                Parameter(
                    id="left",
                    name="Left Operand",
                    type="string",
                    default="voltage",
                    description="Value to compare"
                ),
                Parameter(
                    id="op",
                    name="Operator",
                    type="string",
                    default=">",
                    description="Comparison operator"
                ),
                Parameter(
                    id="right",
                    name="Right Operand",
                    type="float",
                    default=0.0,
                    description="Value to compare against"
                )
            ]
        )
    ]
