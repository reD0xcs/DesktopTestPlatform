import customtkinter as ctk
from tkinter import messagebox
from archive.psu import PowerSupply

ctk.set_appearance_mode("dark")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("OWON SPE6103")
        self.geometry("420x420")
        self.psu=PowerSupply()

        ctk.CTkLabel(self,text="COM Port").pack()
        self.port=ctk.CTkEntry(self)
        self.port.insert(0,"COM5")
        self.port.pack()

        self.status=ctk.CTkLabel(self,text="Disconnected")
        self.status.pack(pady=5)

        ctk.CTkButton(self,text="Connect",command=self.connect).pack()

        ctk.CTkLabel(self,text="Voltage").pack()
        self.volt=ctk.CTkEntry(self); self.volt.insert(0,"12.0"); self.volt.pack()

        ctk.CTkLabel(self,text="Current").pack()
        self.curr=ctk.CTkEntry(self); self.curr.insert(0,"1.0"); self.curr.pack()

        ctk.CTkButton(self,text="Apply",command=self.apply).pack(pady=5)
        ctk.CTkButton(self,text="Output ON",command=self.psu.output_on).pack()
        ctk.CTkButton(self,text="Output OFF",command=self.psu.output_off).pack()

        self.mv=ctk.CTkLabel(self,text="Voltage: --- V"); self.mv.pack(pady=8)
        self.mi=ctk.CTkLabel(self,text="Current: --- A"); self.mi.pack()
        self.mp=ctk.CTkLabel(self,text="Power: --- W"); self.mp.pack()

        self.after(500,self.update_values)

    def connect(self):
        try:
            idn=self.psu.connect(self.port.get())
            self.status.configure(text=idn)
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def apply(self):
        try:
            self.psu.set_voltage(float(self.volt.get()))
            self.psu.set_current(float(self.curr.get()))
        except Exception as e:
            messagebox.showerror("Error",str(e))

    def update_values(self):
        if self.psu.connected:
            try:
                v=self.psu.measure_voltage()
                i=self.psu.measure_current()
                self.mv.configure(text=f"Voltage: {v:.3f} V")
                self.mi.configure(text=f"Current: {i:.3f} A")
                self.mp.configure(text=f"Power: {v*i:.3f} W")
            except:
                pass
        self.after(500,self.update_values)

App().mainloop()