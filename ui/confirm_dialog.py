import customtkinter as ctk


class ConfirmDialog(ctk.CTkToplevel):

    def __init__(
            self,
            master,
            title="Confirm",
            message="Are you sure?",
            confirm_text="OK",
            confirm_color="#1F6AA5",
            confirm_hover="#144870"
    ):
        super().__init__(master)

        self.result = False

        self.title(title)
        self.geometry("380x170")
        self.resizable(False, False)

        self.grab_set()
        self.focus()

        ctk.CTkLabel(
            self,
            text=message,
            wraplength=340,
            justify="center"
        ).pack(
            padx=20,
            pady=(25, 20)
        )

        buttons = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        buttons.pack(
            pady=(0, 20)
        )

        ctk.CTkButton(
            buttons,
            text="Cancel",
            width=100,
            command=self.cancel
        ).pack(
            side="left",
            padx=10
        )

        ctk.CTkButton(
            buttons,
            text=confirm_text,
            width=100,
            fg_color=confirm_color,
            hover_color=confirm_hover,
            command=self.confirm
        ).pack(
            side="left",
            padx=10
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.cancel
        )

    def confirm(self):
        self.result = True
        self.destroy()

    def cancel(self):
        self.result = False
        self.destroy()

    def show(self):
        self.wait_window()
        return self.result