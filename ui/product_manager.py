import customtkinter as ctk

from ui.product_editor import ProductEditor
from CTkListbox import CTkListbox
from ui.confirm_dialog import ConfirmDialog


class ProductManager(ctk.CTkToplevel):

    def __init__(self, master, serializer, action_registry):

        super().__init__(master)

        self.title("Product Manager")
        self.geometry("600x500")

        self.serializer = serializer
        self.action_registry = action_registry

        self._create_widgets()

        self.refresh_products()


    def _create_widgets(self):

        ctk.CTkLabel(
            self,
            text="Products",
            font=("", 18, "bold")
        ).pack(
            pady=10
        )


        self.products_list = CTkListbox(
            self,
            width=400,
            height=300
        )

        self.products_list.pack(
            pady=10
        )


        buttons = ctk.CTkFrame(self)

        buttons.pack(
            pady=10
        )


        ctk.CTkButton(
            buttons,
            text="New",
            command=self.new_product
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            buttons,
            text="Open",
            command=self.open_product
        ).pack(
            side="left",
            padx=5
        )


        ctk.CTkButton(
            buttons,
            text="Delete",
            command=self.delete_product
        ).pack(
            side="left",
            padx=5
        )


    def refresh_products(self):

        self.products_list.delete("all")

        for product in self.serializer.list_products():

            self.products_list.insert(
                "END",
                product
            )


    def new_product(self):

        ProductEditor(
            self,
            self.action_registry,
            self.serializer
        )


    def open_product(self):

        selected = self.products_list.get()

        if not selected:
            return

        product = self.serializer.load(
            selected
        )

        ProductEditor(
            self,
            self.action_registry,
            self.serializer,
            product
        )

    def delete_product(self):

        selected = self.products_list.get()

        if not selected:
            return

        dialog = ConfirmDialog(
            self,
            title="Delete Product",
            message=f'Are you sure you want to delete "{selected}"?\n\nThis action cannot be undone.',
            confirm_text="Delete",
            confirm_color="#C0392B",
            confirm_hover="#922B21"
        )

        if not dialog.show():
            return

        self.serializer.delete(selected)

        self.refresh_products()