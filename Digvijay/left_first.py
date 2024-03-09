import customtkinter as tk

class FirstPageleft(tk.CTkFrame):
    def __init__(self, parent):
        tk.CTkFrame.__init__(self, parent)
        label = tk.CTkLabel(self, text="First Page Content")
        label.pack(fill="both", expand=True)
