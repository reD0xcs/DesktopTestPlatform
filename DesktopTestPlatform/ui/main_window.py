import customtkinter as ctk

from core.device_manager import DeviceManager


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Hardware Test Platform")
        self.geometry("1200x700")

        # Managers
        self.device_manager = DeviceManager()

        print("\n========== DEVICES ==========")

        devices = self.device_manager.get_devices()

        print("\nPower Supplies:")

        for ps in devices["power_supplies"]:
            print(f"  • {ps['name']} ({ps['id']})")

        print("=============================\n")

        ctk.CTkLabel(
            self,
            text="Hardware Test Platform",
            font=("Arial", 28, "bold")
        ).pack(pady=40)

        ctk.CTkLabel(
            self,
            text="Architecture initialized successfully",
            font=("Arial", 18)
        ).pack()
        
        print("\nChecking Raspberry Pi...")

        try:

            status = self.device_manager.pi.health()

            print(status)

        except Exception as ex:

            print(ex)