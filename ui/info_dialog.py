import customtkinter as ctk


class InfoDialog(ctk.CTkToplevel):

    def __init__(
            self,
            master,
            title="Information",
            message=""
    ):
        super().__init__(master)

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

        ctk.CTkButton(
            self,
            text="OK",
            width=120,
            command=self.destroy
        ).pack(
            pady=(0, 20)
        )

        self.protocol(
            "WM_DELETE_WINDOW",
            self.destroy
        )

    def show(self):
        self.wait_window()