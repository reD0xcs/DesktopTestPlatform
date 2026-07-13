from actions.system import get_actions as get_system_actions


class ActionRegistry:

    def __init__(self, device_manager):

        self.device_manager = device_manager

        self.actions = []


    def load_actions(self):

        actions = []

        # System actions
        system = get_system_actions()
        print("SYSTEM:", [a.name for a in system])
        actions.extend(system)


        # Power supply actions
        psu = self.device_manager.power_supplies.get_actions()
        print("PSU:", [a.name for a in psu])
        actions.extend(psu)


        # Raspberry Pi actions
        try:

            pi = self.device_manager.pi.get_actions()
            print("PI:", [a.name for a in pi])
            actions.extend(pi)

        except Exception:

            print("⚠ Raspberry Pi offline")


        self.actions = actions



    def get_actions(self):

        if not self.actions:
            self.load_actions()

        return self.actions



    def get_action(self, action_id):

        for action in self.get_actions():

            if action.id == action_id:
                return action


        return None