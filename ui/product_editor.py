import customtkinter as ctk
from CTkListbox import CTkListbox

from models.product import Product
from models.product_action import ProductAction
from ui.confirm_dialog import ConfirmDialog
from ui.info_dialog import InfoDialog


class ProductEditor(ctk.CTkToplevel):

    def __init__(
            self,
            master,
            action_registry,
            serializer,
            product=None
    ):

        super().__init__(master)

        self.title("Product Editor")
        self.geometry("1000x650")

        self.product = product if product else Product()

        self.action_registry = action_registry
        self.serializer = serializer

        self.available_lookup = {}
        self.action_lookup = {}

        self._create_widgets()

        self.load_actions()

        self.refresh_product_steps()
        self.product_name.insert(
            0,
            self.product.name
        )

        self.serializer = serializer

        self.save_button.configure(
            command=self.save_product
        )


    # =========================================
    # GUI
    # =========================================

    def _create_widgets(self):

        # TOP BAR
        top = ctk.CTkFrame(self)
        top.pack(
            fill="x",
            padx=10,
            pady=10
        )


        ctk.CTkLabel(
            top,
            text="Product Name:"
        ).pack(
            side="left",
            padx=5
        )


        self.product_name = ctk.CTkEntry(
            top,
            width=250
        )

        self.product_name.pack(
            side="left"
        )


        self.save_button = ctk.CTkButton(
            top,
            text="Save"
        )

        self.save_button.pack(
            side="right",
            padx=5
        )

        self.load_button = ctk.CTkButton(
            top,
            text="Load",
            command=self.open_load_window
        )

        self.load_button.pack(
            side="right",
            padx=5
        )

        self.new_button = ctk.CTkButton(
            top,
            text="New",
            command=self.new_product
        )

        self.new_button.pack(
            side="right",
            padx=5
        )


        # MAIN BODY

        body = ctk.CTkFrame(self)

        body.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )


        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(2, weight=1)
        body.grid_rowconfigure(0, weight=1)



        # LEFT - AVAILABLE ACTIONS

        left = ctk.CTkFrame(body)

        left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=10
        )


        ctk.CTkLabel(
            left,
            text="Available Actions",
            font=("",16,"bold")
        ).pack(
            pady=10
        )


        self.available_actions = CTkListbox(
            left,
            width=350,
            height=450
        )

        self.available_actions.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )



        # CENTER BUTTONS

        center = ctk.CTkFrame(body)

        center.grid(
            row=0,
            column=1,
            sticky="ns"
        )


        self.add_button = ctk.CTkButton(
            center,
            text="Add →",
            command=self.add_action
        )

        self.add_button.pack(
            pady=80,
            padx=10
        )


        self.remove_button = ctk.CTkButton(
            center,
            text="← Remove",
            command=self.remove_action
        )

        self.remove_button.pack(
            pady=10
        )


        self.up_button = ctk.CTkButton(
            center,
            text="▲ Up",
            command=self.move_up
        )

        self.up_button.pack(
            pady=20
        )


        self.down_button = ctk.CTkButton(
            center,
            text="▼ Down",
            command=self.move_down
        )

        self.down_button.pack()



        # RIGHT

        right = ctk.CTkFrame(body)

        right.grid(
            row=0,
            column=2,
            sticky="nsew",
            padx=10
        )


        ctk.CTkLabel(
            right,
            text="Product Steps",
            font=("",16,"bold")
        ).pack(
            pady=10
        )


        self.product_steps = CTkListbox(
            right,
            width=350,
            height=250,
            command=self.select_product_action
        )

        self.product_steps.pack(
            padx=10,
            pady=10
        )


        ctk.CTkLabel(
            right,
            text="Parameters",
            font=("",16,"bold")
        ).pack(
            pady=10
        )


        self.parameters_frame = ctk.CTkFrame(right)

        self.parameters_frame.pack(
            fill="x",
            padx=10,
            pady=10
        )



    # =========================================
    # ACTION LOADING
    # =========================================


    def load_actions(self):

        self.available_actions.delete("all")

        self.available_lookup.clear()
        self.action_lookup.clear()


        for action in self.action_registry.get_actions():

            display = (
                f"[{action.category}] {action.name}"
            )


            self.available_actions.insert(
                "END",
                display
            )


            self.available_lookup[display] = action
            self.action_lookup[action.id] = action



    # =========================================
    # ADD REMOVE
    # =========================================


    def add_action(self):

        selected = self.available_actions.get()

        if not selected:
            return


        action = self.available_lookup.get(selected)

        if not action:
            return


        product_action = ProductAction(
            action_id=action.id
        )


        self.product.actions.append(
            product_action
        )


        self.refresh_product_steps()



    def remove_action(self):

        index = self.product_steps.curselection()

        if index is None:
            return


        del self.product.actions[index]

        self.refresh_product_steps()



    # =========================================
    # ORDER
    # =========================================

    def move_up(self):

        index = self.product_steps.curselection()

        if index is None or index == 0:
            return

        self.product.actions[index], self.product.actions[index - 1] = (
            self.product.actions[index - 1],
            self.product.actions[index]
        )

        self.refresh_product_steps(index - 1)

    def move_down(self):

        index = self.product_steps.curselection()

        if index is None:
            return

        if index >= len(self.product.actions) - 1:
            return

        self.product.actions[index], self.product.actions[index + 1] = (
            self.product.actions[index + 1],
            self.product.actions[index]
        )

        self.refresh_product_steps(index + 1)



    # =========================================
    # PRODUCT STEPS DISPLAY
    # =========================================

    def refresh_product_steps(self, selected_index=None):

        self.product_steps.delete("all")

        for index, product_action in enumerate(
                self.product.actions,
                start=1
        ):

            action = self.action_lookup.get(
                product_action.action_id
            )

            if action:
                self.product_steps.insert(
                    "END",
                    f"{index}. {action.name}"
                )

        if selected_index is not None:
            self.product_steps.select(
                selected_index
            )


    # =========================================
    # PARAMETERS
    # =========================================


    def select_product_action(self, selected):

        index = self.product_steps.curselection()

        if index is None:
            return


        product_action = self.product.actions[index]

        self.show_parameters(
            product_action
        )

    def show_parameters(self, product_action):

        for widget in self.parameters_frame.winfo_children():
            widget.destroy()

        action = self.action_lookup.get(
            product_action.action_id
        )

        if not action:
            return

        for parameter in action.parameters:
            print("----------------")
            print("PARAMETER ID  :", parameter.id)
            print("PARAMETER NAME:", parameter.name)
            frame = ctk.CTkFrame(
                self.parameters_frame
            )

            frame.pack(
                fill="x",
                pady=5
            )

            ctk.CTkLabel(
                frame,
                text=parameter.name
            ).pack(
                side="left"
            )

            entry = ctk.CTkEntry(frame)

            entry.pack(
                side="right"
            )

            value = product_action.values.get(
                parameter.id,
                parameter.default
            )

            entry.insert(
                0,
                str(value)
            )

            entry.bind(
                "<FocusOut>",
                lambda e,
                       pid=parameter.id,
                       ent=entry,
                       pa=product_action:
                self.update_parameter(
                    pa,
                    pid,
                    ent.get()
                )
            )



    def update_parameter(
        self,
        product_action,
        name,
        value
    ):
        print("UPDATE:")
        print("KEY  :", name)
        print("VALUE:", value)

        product_action.values[name] = value

    def save_product(self):

        name = self.product_name.get().strip()

        if not name:
            InfoDialog(
                self,
                title="Save Product",
                message="Please enter a product name."
            ).show()
            return

        self.product.name = name

        self.serializer.save(self.product)

        InfoDialog(
            self,
            title="Save Product",
            message=f'Product "{name}" was saved successfully.'
        ).show()

    def open_load_window(self):

        dialog = ConfirmDialog(
            self,
            title="Load Product",
            message=(
                "Current product contains unsaved changes.\n\n"
                "Discard them and load another product?"
            ),
            confirm_text="Load"
        )

        if not dialog.show():
            return

        window = ctk.CTkToplevel(self)

        window.title("Load Product")

        window.geometry("400x400")

        products = self.serializer.list_products()

        if not products:
            ctk.CTkLabel(
                window,
                text="No products found"
            ).pack(
                pady=20
            )

            return

        listbox = CTkListbox(
            window,
            width=300,
            height=250
        )

        listbox.pack(
            padx=20,
            pady=20
        )

        for product in products:
            listbox.insert(
                "END",
                product
            )

        def load_selected():

            selected = listbox.get()

            if not selected:
                return

            product = self.serializer.load(
                selected
            )

            self.product = product

            self.product_name.delete(
                0,
                "end"
            )

            self.product_name.insert(
                0,
                product.name
            )

            self.refresh_product_steps()

            window.destroy()

        ctk.CTkButton(
            window,
            text="Load",
            command=load_selected
        ).pack(
            pady=10
        )

    def new_product(self):

        if self.has_product_data():

            dialog = ConfirmDialog(
                self,
                title="New Product",
                message=(
                    "Current product contains unsaved changes.\n\n"
                    "Discard them and create a new product?"
                ),
                confirm_text="New"
            )

            if not dialog.show():
                return

        self.reset_product()


        InfoDialog(
            self,
            title="New Product",
            message="A new empty product has been created successfully."
        ).show()
        
    def reset_product(self):

        self.product = Product()

        self.product_name.delete(
            0,
            "end"
        )

        self.product_steps.delete(
            "all"
        )

        for widget in self.parameters_frame.winfo_children():
            widget.destroy()

    def has_product_data(self):

        if self.product_name.get().strip():
            return True

        if len(self.product.actions) > 0:
            return True

        return False