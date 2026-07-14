import customtkinter as ctk

from core.device_manager import DeviceManager
from core.action_registry import ActionRegistry
from core.product_serializer import ProductSerializer

from ui.product_editor import ProductEditor
from ui.product_manager import ProductManager

class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Desktop Test Platform")
        self.geometry("500x300")

        self.device_manager = DeviceManager()
        self.action_registry = ActionRegistry(self.device_manager)
        self.serializer = ProductSerializer()

        ctk.CTkButton(
            self,
            text="Product Editor",
            width=200,
            command=self.open_product_editor
        ).pack(pady=20)

        ctk.CTkButton(
            self,
            text="Product Manager",
            width=200,
            command=self.open_product_manager
        ).pack(pady=20)

    def open_product_editor(self):

        ProductEditor(
            self,
            self.action_registry,
            self.serializer
        )

    def open_product_manager(self):
        ProductManager(
            self,
            self.serializer,
            self.action_registry
        )