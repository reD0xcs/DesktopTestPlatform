import customtkinter as ctk
import threading


class RunWindow(ctk.CTkToplevel):

    def __init__(self, master, product, executor):

        super().__init__(master)

        self.product = product
        self.executor = executor

        self.title(f"Running - {product.name}")
        self.geometry("700x500")

        self._create_widgets()

        threading.Thread(
            target=self.run_product,
            daemon=True
        ).start()

    # ==========================================
    # GUI
    # ==========================================

    def _create_widgets(self):

        ctk.CTkLabel(
            self,
            text=self.product.name,
            font=("", 22, "bold")
        ).pack(
            pady=(15, 10)
        )

        self.progress = ctk.CTkProgressBar(
            self,
            width=600
        )

        self.progress.pack(
            pady=10
        )

        self.progress.set(0)

        self.current_action = ctk.CTkLabel(
            self,
            text="Waiting..."
        )

        self.current_action.pack(
            pady=10
        )

        self.log = ctk.CTkTextbox(
            self,
            width=650,
            height=280
        )

        self.log.pack(
            padx=20,
            pady=10,
            fill="both",
            expand=True
        )

        self.close_button = ctk.CTkButton(
            self,
            text="Close",
            state="disabled",
            command=self.destroy
        )

        self.close_button.pack(
            pady=10
        )

    # ==========================================
    # LOG
    # ==========================================

    def append_log(self, text):

        self.log.insert(
            "end",
            text + "\n"
        )

        self.log.see("end")

    # ==========================================
    # EXECUTION
    # ==========================================

    def run_product(self):

        total = len(self.product.actions)

        if total == 0:

            self.append_log("Nothing to execute.")

            self.close_button.configure(
                state="normal"
            )

            return

        for index, action in enumerate(self.product.actions):

            self.current_action.configure(
                text=action.action_id
            )

            result = self.executor.execute(
                action
            )

            if result.success:

                self.append_log(
                    f"✔ {action.action_id}"
                )

            else:

                self.append_log(
                    f"✖ {action.action_id} - {result.message}"
                )

                break

            self.progress.set(
                (index + 1) / total
            )

        self.current_action.configure(
            text="Finished"
        )

        self.append_log("")
        self.append_log("Execution completed.")

        self.close_button.configure(
            state="normal"
        )