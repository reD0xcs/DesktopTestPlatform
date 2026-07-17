import customtkinter as ctk


class DeviceManagerWindow(ctk.CTkToplevel):

    def __init__(self, master, device_manager):

        super().__init__(master)

        self.device_manager = device_manager
        self.power_supply_rows = []

        self.title("Device Manager")
        self.geometry("700x500")

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self._create_widgets()
        self._load_power_supplies()

        self.after(100, self._bring_to_front)
        self.after(3000, self._refresh_loop)

    def _bring_to_front(self):
        try:
            self.lift()
            self.focus_force()
        except Exception:
            pass

    def on_close(self):
        self.destroy()

    # ==========================================
    # GUI
    # ==========================================

    def _create_widgets(self):

        ctk.CTkLabel(
            self,
            text="Device Manager",
            font=("", 22, "bold")
        ).pack(
            pady=(15, 10)
        )

        self.container = ctk.CTkScrollableFrame(
            self,
            width=650,
            height=380
        )
        self.container.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        footer = ctk.CTkFrame(self)
        footer.pack(pady=(0, 15), padx=20, fill="x")

        self.refresh_button = ctk.CTkButton(
            footer,
            text="Refresh",
            width=120,
            command=self.refresh_status
        )
        self.refresh_button.pack(side="left", padx=5, pady=10)

        self.close_button = ctk.CTkButton(
            footer,
            text="Close",
            width=120,
            command=self.destroy
        )
        self.close_button.pack(side="right", padx=5, pady=10)

        self.pi_title = ctk.CTkLabel(
            self.container,
            text="Raspberry Pi",
            font=("", 18, "bold")
        )
        self.pi_title.pack(anchor="w", padx=10, pady=(10, 4))

        self.pi_row = self._create_row(
            self.container,
            "Raspberry Pi",
            "Unknown",
            "Host: unknown"
        )

        self.psu_title = ctk.CTkLabel(
            self.container,
            text="Power Supplies",
            font=("", 18, "bold")
        )
        self.psu_title.pack(anchor="w", padx=10, pady=(18, 4))

        self.psu_placeholder = ctk.CTkLabel(
            self.container,
            text="Loading..."
        )
        self.psu_placeholder.pack(anchor="w", padx=10, pady=10)

    def _create_row(self, parent, name, status, detail=""):

        row = ctk.CTkFrame(parent)
        row.pack(fill="x", padx=10, pady=6)

        left = ctk.CTkFrame(row, fg_color="transparent")
        left.pack(side="left", fill="x", expand=True, padx=10, pady=10)

        name_label = ctk.CTkLabel(
            left,
            text=name,
            font=("", 16, "bold")
        )
        name_label.pack(anchor="w")

        detail_label = ctk.CTkLabel(
            left,
            text=detail,
            font=("", 12)
        )
        detail_label.pack(anchor="w", pady=(2, 0))

        status_label = ctk.CTkLabel(
            row,
            text=status,
            width=110,
            fg_color="#F39C12",
            text_color="white",
            corner_radius=8
        )
        status_label.pack(side="right", padx=10, pady=10)

        return {
            "row": row,
            "name_label": name_label,
            "detail_label": detail_label,
            "status_label": status_label
        }

    def _status_color(self, status):
        if status == "Connected":
            return "#27AE60"
        if status == "Offline":
            return "#C0392B"
        return "#F39C12"

    def _set_row(self, row, name=None, status=None, detail=None):

        if name is not None:
            row["name_label"].configure(text=name)

        if detail is not None:
            row["detail_label"].configure(text=detail)

        if status is not None:
            row["status_label"].configure(
                text=status,
                fg_color=self._status_color(status)
            )

    def _load_power_supplies(self):

        for row in self.power_supply_rows:
            row["row"].destroy()

        self.power_supply_rows.clear()

        # acum primim instanțe de PowerSupplyBase
        power_supplies = self.device_manager.power_supplies.get_available()

        if hasattr(self, "psu_placeholder") and self.psu_placeholder.winfo_exists():
            self.psu_placeholder.destroy()

        if not power_supplies:
            self.psu_placeholder = ctk.CTkLabel(
                self.container,
                text="No power supplies detected."
            )
            self.psu_placeholder.pack(anchor="w", padx=10, pady=10)
            return

        for ps in power_supplies:
            name = getattr(ps, "name", "Power Supply")
            detail = getattr(ps, "model", "")
            connected = ps.is_connected()

            row = self._create_row(
                self.container,
                name,
                "Connected" if connected else "Offline",
                detail
            )
            self.power_supply_rows.append(row)

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh_status(self):

        try:
            pi_connected = self.device_manager.is_pi_connected()
        except Exception:
            pi_connected = False

        try:
            pi_host = getattr(self.device_manager.pi, "host", "unknown")
        except Exception:
            pi_host = "unknown"

        self._set_row(
            self.pi_row,
            name="Raspberry Pi",
            status="Connected" if pi_connected else "Offline",
            detail=f"Host: {pi_host}"
        )

        power_supplies = self.device_manager.power_supplies.get_available()

        if len(power_supplies) != len(self.power_supply_rows):
            self._load_power_supplies()
            power_supplies = self.device_manager.power_supplies.get_available()

        for row, ps in zip(self.power_supply_rows, power_supplies):

            name = getattr(ps, "name", "Power Supply")
            detail = getattr(ps, "model", "")
            connected = ps.is_connected()

            self._set_row(
                row,
                name=name,
                status="Connected" if connected else "Offline",
                detail=detail
            )

    def _refresh_loop(self):

        if self.winfo_exists():
            self.refresh_status()
            self.after(3000, self._refresh_loop)