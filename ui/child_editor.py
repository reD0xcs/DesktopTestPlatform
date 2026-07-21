import customtkinter as ctk
from CTkListbox import CTkListbox

from models.product import Product
from models.product_action import ProductAction


class ChildEditor(ctk.CTkToplevel):

    def __init__(self, master, action_registry, product_action, is_else=False):
        super().__init__(master)

        self.title("Edit Children" if not is_else else "Edit ELSE Children")
        self.geometry("900x600")

        self.action_registry = action_registry
        self.product_action = product_action
        self.is_else = is_else

        # children list to edit
        self.child_list = (
            product_action.else_children if is_else else product_action.children
        )

        self.available_lookup = {}
        self.action_lookup = {}

        self._create_widgets()
        self.load_actions()
        self.refresh_child_steps()

    # ============================================================
    # GUI
    # ============================================================

    def _create_widgets(self):

        body = ctk.CTkFrame(self)
        body.pack(fill="both", expand=True, padx=10, pady=10)

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(2, weight=1)
        body.grid_rowconfigure(0, weight=1)

        # LEFT — available actions
        left = ctk.CTkFrame(body)
        left.grid(row=0, column=0, sticky="nsew", padx=10)

        ctk.CTkLabel(left, text="Available Actions", font=("", 16, "bold")).pack(pady=10)

        self.available_actions = CTkListbox(left, width=350, height=450)
        self.available_actions.pack(fill="both", expand=True, padx=10, pady=10)

        # CENTER — buttons
        center = ctk.CTkFrame(body)
        center.grid(row=0, column=1, sticky="ns")

        ctk.CTkButton(center, text="Add →", command=self.add_action).pack(pady=80, padx=10)
        ctk.CTkButton(center, text="← Remove", command=self.remove_action).pack(pady=10)
        ctk.CTkButton(center, text="▲ Up", command=self.move_up).pack(pady=20)
        ctk.CTkButton(center, text="▼ Down", command=self.move_down).pack()

        # RIGHT — child steps + parameters
        right = ctk.CTkFrame(body)
        right.grid(row=0, column=2, sticky="nsew", padx=10)

        ctk.CTkLabel(right, text="Child Steps", font=("", 16, "bold")).pack(pady=10)

        self.child_steps = CTkListbox(right, width=350, height=250, command=self.select_child_action)
        self.child_steps.pack(padx=10, pady=10)

        ctk.CTkLabel(right, text="Parameters", font=("", 16, "bold")).pack(pady=10)

        self.parameters_frame = ctk.CTkFrame(right)
        self.parameters_frame.pack(fill="x", padx=10, pady=10)

        # SAVE CHILDREN BUTTON
        ctk.CTkButton(self, text="Save Children", command=self.save_children).pack(pady=10)

    # ============================================================
    # LOAD AVAILABLE ACTIONS
    # ============================================================

    def load_actions(self):
        self.available_actions.delete("all")
        self.available_lookup.clear()
        self.action_lookup.clear()

        for action in self.action_registry.get_actions():
            display = f"[{action.category}] {action.name}"
            self.available_actions.insert("END", display)
            self.available_lookup[display] = action
            self.action_lookup[action.id] = action

    # ============================================================
    # CHILD LIST MANAGEMENT
    # ============================================================

    def add_action(self):
        selected = self.available_actions.get()
        if not selected:
            return

        action = self.available_lookup.get(selected)
        if not action:
            return

        pa = ProductAction(action_id=action.id)
        self.child_list.append(pa)
        self.refresh_child_steps()

    def remove_action(self):
        index = self.child_steps.curselection()
        if index is None:
            return

        del self.child_list[index]
        self.refresh_child_steps()

    def move_up(self):
        index = self.child_steps.curselection()
        if index is None or index == 0:
            return

        self.child_list[index], self.child_list[index - 1] = (
            self.child_list[index - 1],
            self.child_list[index]
        )
        self.refresh_child_steps(index - 1)

    def move_down(self):
        index = self.child_steps.curselection()
        if index is None or index >= len(self.child_list) - 1:
            return

        self.child_list[index], self.child_list[index + 1] = (
            self.child_list[index + 1],
            self.child_list[index]
        )
        self.refresh_child_steps(index + 1)

    def refresh_child_steps(self, selected_index=None):
        self.child_steps.delete("all")

        for index, pa in enumerate(self.child_list, start=1):
            action = self.action_lookup.get(pa.action_id)
            if action:
                self.child_steps.insert("END", f"{index}. {action.name}")

        if selected_index is not None:
            self.child_steps.select(selected_index)

    # ============================================================
    # PARAMETERS
    # ============================================================

    def select_child_action(self, selected):
        index = self.child_steps.curselection()
        if index is None:
            return

        pa = self.child_list[index]
        self.show_parameters(pa)

    def show_parameters(self, pa):
        for widget in self.parameters_frame.winfo_children():
            widget.destroy()

        action = self.action_lookup.get(pa.action_id)
        if not action:
            return

        for parameter in action.parameters:
            frame = ctk.CTkFrame(self.parameters_frame)
            frame.pack(fill="x", pady=5)

            ctk.CTkLabel(frame, text=parameter.name).pack(side="left")

            entry = ctk.CTkEntry(frame)
            entry.pack(side="right")

            value = pa.values.get(parameter.id, parameter.default)
            entry.insert(0, str(value))

            entry.bind(
                "<FocusOut>",
                lambda e, pid=parameter.id, ent=entry, pa=pa:
                self.update_parameter(pa, pid, ent.get())
            )

    def update_parameter(self, pa, name, value):
        pa.values[name] = value

    # ============================================================
    # SAVE CHILDREN
    # ============================================================

    def save_children(self):
        if self.is_else:
            self.product_action.else_children = self.child_list
        else:
            self.product_action.children = self.child_list

        self.destroy()
