import time
import threading
import customtkinter as ctk


class RunWindow(ctk.CTkToplevel):

    def __init__(self, master, product, runner):

        super().__init__(master)

        self.product = product
        self.runner = runner
        self.runner.ui = self

        self.stop_requested = False
        self.pause_requested = False
        self.pause_event = threading.Event()
        self.pause_event.set()

        self.start_time = time.time()

        self.title(f"Running - {product.name}")
        self.geometry("700x700")

        self._create_widgets()

        self.protocol("WM_DELETE_WINDOW", self.on_close)

        threading.Thread(
            target=self.run_product,
            daemon=True
        ).start()

    def on_close(self):
        if self.close_button.cget("state") == "normal":
            self.destroy()

    # ==================================================
    # GUI
    # ==================================================

    def _create_widgets(self):

        ctk.CTkLabel(
            self,
            text=self.product.name,
            font=("", 22, "bold")
        ).pack(pady=(15, 5))

        self.step_label = ctk.CTkLabel(
            self,
            text="Step 0 / 0",
            font=("", 14)
        )
        self.step_label.pack(pady=(5, 10))

        ctk.CTkLabel(self, text="Overall Progress").pack()

        self.overall_progress = ctk.CTkProgressBar(self, width=600)
        self.overall_progress.pack(pady=(5, 15))
        self.overall_progress.set(0)

        ctk.CTkLabel(self, text="Current Step").pack()

        self.step_progress = ctk.CTkProgressBar(self, width=600)
        self.step_progress.pack(pady=(5, 15))
        self.step_progress.set(0)

        self.current_action = ctk.CTkLabel(
            self,
            text="Step 0 / 0",
            font=("", 18, "bold")
        )
        self.current_action.pack(pady=10)

        self.log = ctk.CTkTextbox(self, width=650, height=280)
        self.log.pack(padx=20, pady=10, fill="both", expand=True)
        self.log.configure(state="disabled")

        buttons = ctk.CTkFrame(self)
        buttons.pack(pady=10)

        self.stop_button = ctk.CTkButton(
            buttons,
            text="Stop",
            width=120,
            fg_color="#C0392B",
            hover_color="#922B21",
            command=self.stop_execution
        )
        self.stop_button.pack(side="left", padx=5)

        self.pause_button = ctk.CTkButton(
            buttons,
            text="Pause",
            width=120,
            fg_color="#F39C12",
            hover_color="#D68910",
            command=self.toggle_pause
        )
        self.pause_button.pack(side="left", padx=5)

        self.close_button = ctk.CTkButton(
            buttons,
            text="Close",
            width=120,
            state="disabled",
            command=self.destroy
        )
        self.close_button.pack(side="left", padx=5)

    # ==================================================
    # LOG
    # ==================================================

    def append_log(self, text):

        def update():
            self.log.configure(state="normal")
            self.log.insert("end", text + "\n")
            self.log.see("end")
            self.log.configure(state="disabled")

        self.after(0, update)

    # ==================================================
    # STOP / PAUSE
    # ==================================================

    def stop_execution(self):

        self.stop_requested = True
        self.pause_event.set()

        self.after(0, lambda: self.stop_button.configure(
            state="disabled",
            text="Stopping..."
        ))

        self.after(0, lambda: self.pause_button.configure(
            state="disabled"
        ))

        self.append_log("Stop requested...")

    def toggle_pause(self):

        if self.stop_requested:
            return

        if self.pause_requested:
            self.pause_requested = False
            self.pause_event.set()

            self.after(0, lambda: self.pause_button.configure(text="Pause"))
            self.append_log("Resumed.")
            return

        self.pause_requested = True
        self.pause_event.clear()

        self.after(0, lambda: self.pause_button.configure(text="Resume"))
        self.append_log("Paused.")

    # ==================================================
    # EXECUTION
    # ==================================================

    def run_product(self):

        total = len(self.product.actions)

        if total == 0:
            self.append_log("Nothing to execute.")
            self.enable_close()
            self.disable_stop()
            self.disable_pause()
            return

        results, report_path = self.runner.run(
            self.product,
            self.product.actions,
            progress_callback=self.update_step_progress,
            stop_callback=lambda: self.stop_requested,
            pause_callback=lambda: self.pause_event
        )

        elapsed = time.time() - self.start_time

        self.append_log("")
        self.append_log(f"Finished in {elapsed:.2f} seconds.")
        self.append_log("====================================")
        self.append_log("            TEST REPORT             ")
        self.append_log("====================================")
        self.append_log(f"Saved to:\n{report_path}")
        self.append_log("====================================")

        self.disable_stop()
        self.disable_pause()
        self.enable_close()

    # ==================================================
    # UI UPDATE CALLBACKS
    # ==================================================

    def update_step_progress(self, progress, remaining):

        def update():
            self.step_progress.set(progress)
            text = self.current_action.cget("text")
            base_text = text.split(" (")[0]
            self.current_action.configure(text=f"{base_text} ({remaining:.1f}s)")

        self.after(0, update)

    def set_current_action(self, text):
        self.after(0, lambda: self.current_action.configure(text=text))

    def set_step_label(self, text):
        self.after(0, lambda: self.step_label.configure(text=text))

    def set_overall_progress(self, value):
        self.after(0, lambda: self.overall_progress.set(value))

    def set_step_progress(self, value):
        self.after(0, lambda: self.step_progress.set(value))

    def enable_close(self):
        self.after(0, lambda: self.close_button.configure(state="normal"))

    def disable_stop(self):
        self.after(0, lambda: self.stop_button.configure(state="disabled"))

    def disable_pause(self):
        self.after(0, lambda: self.pause_button.configure(state="disabled"))
