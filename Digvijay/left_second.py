import customtkinter as tk

class SecondPageleft(tk.CTkFrame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Second Page Content")
        label.pack(fill="both", expand=True)
