import time
import threading

import customtkinter as ctk


class RunWindow(ctk.CTkToplevel):

    def __init__(self, master, product, executor):

        super().__init__(master)

        self.product = product
        self.executor = executor

        self.stop_requested = False
        self.start_time = time.time()

        self.title(f"Running - {product.name}")
        self.geometry("700x700")

        self._create_widgets()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.on_close
        )

        threading.Thread(
            target=self.run_product,
            daemon=True
        ).start()

    def on_close(self):

        if self.close_button.cget("state") == "normal":
            self.destroy()

    # ==========================================
    # GUI
    # ==========================================

    def _create_widgets(self):

        ctk.CTkLabel(
            self,
            text=self.product.name,
            font=("", 22, "bold")
        ).pack(
            pady=(15, 5)
        )

        self.step_label = ctk.CTkLabel(
            self,
            text="Step 0 / 0",
            font=("", 14)
        )

        self.step_label.pack(
            pady=(5, 10)
        )

        ctk.CTkLabel(
            self,
            text="Overall Progress"
        ).pack()

        self.overall_progress = ctk.CTkProgressBar(
            self,
            width=600
        )

        self.overall_progress.pack(
            pady=(5, 15)
        )

        self.overall_progress.set(0)

        ctk.CTkLabel(
            self,
            text="Current Step"
        ).pack()

        self.step_progress = ctk.CTkProgressBar(
            self,
            width=600
        )

        self.step_progress.pack(
            pady=(5, 15)
        )

        self.step_progress.set(0)

        self.current_action = ctk.CTkLabel(
            self,
            text="Step 0 / 0",
            font=("", 18, "bold")
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

        self.log.configure(
            state="disabled"
        )

        buttons = ctk.CTkFrame(self)

        buttons.pack(
            pady=10
        )

        self.stop_button = ctk.CTkButton(
            buttons,
            text="Stop",
            width=120,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.stop_execution
        )

        self.stop_button.pack(
            side="left",
            padx=5
        )

        self.close_button = ctk.CTkButton(
            buttons,
            text="Close",
            width=120,
            state="disabled",
            command=self.destroy
        )

        self.close_button.pack(
            side="left",
            padx=5
        )

    # ==========================================
    # LOG
    # ==========================================

    def append_log(self, text):

        self.log.configure(
            state="normal"
        )

        self.log.insert(
            "end",
            text + "\n"
        )

        self.log.see("end")

        self.log.configure(
            state="disabled"
        )

    def stop_execution(self):

        self.stop_requested = True

        self.stop_button.configure(
            state="disabled",
            text="Stopping..."
        )

        self.append_log(
            "Stop requested..."
        )

    # ==========================================
    # EXECUTION
    # ==========================================

    def run_product(self):

        total = len(self.product.actions)

        if total == 0:
            self.append_log(
                "Nothing to execute."
            )

            self.close_button.configure(
                state="normal"
            )

            return

        for index, action in enumerate(
                self.product.actions,
                start=1
        ):

            if self.stop_requested:
                self.current_action.configure(
                    text="Stopping..."
                )

                self.append_log(
                    "Execution cancelled by user."
                )

                break

            # Reset current step progress
            self.step_progress.set(0)

            # Update UI
            self.step_label.configure(
                text=f"Step {index} / {total}"
            )

            display = action.action_id.replace(
                ".",
                " → "
            )

            self.set_current_action(display)

            # Execute action
            result = self.executor.execute(
                action,
                progress_callback=self.update_step_progress,
                stop_callback=lambda: self.stop_requested
            )

            if result.success:

                self.append_log(
                    f"✔ {display}"
                )

            else:

                self.append_log(
                    f"✖ {display} - {result.message}"
                )

                break

            # Step finished
            self.step_progress.set(1)

            self.set_overall_progress(
                index / total
            )

        elapsed = time.time() - self.start_time

        if self.stop_requested:

            self.current_action.configure(
                text="Stopped"
            )

        else:

            self.current_action.configure(
                text="Finished"
            )

        self.set_step_label(
            f"Step {index} / {total}"
        )

        self.append_log("")
        self.append_log(
            f"Finished in {elapsed:.2f} seconds."
        )

        self.disable_stop()

        self.enable_close()

    def update_step_progress(self, progress, remaining):

        def update():
            self.step_progress.set(progress)

            self.current_action.configure(
                text=f"{self.current_action.cget('text').split(' (')[0]} ({remaining:.1f}s)"
            )

        self.after(0, update)

    def set_current_action(self, text):

        self.after(
            0,
            lambda: self.current_action.configure(
                text=text
            )
        )

    def set_step_label(self, text):

        self.after(
            0,
            lambda: self.step_label.configure(
                text=text
            )
        )

    def set_overall_progress(self, value):

        self.after(
            0,
            lambda: self.overall_progress.set(value)
        )

    def enable_close(self):

        self.after(
            0,
            lambda: self.close_button.configure(
                state="normal"
            )
        )

    def disable_stop(self):

        self.after(
            0,
            lambda: self.stop_button.configure(
                state="disabled"
            )
        )