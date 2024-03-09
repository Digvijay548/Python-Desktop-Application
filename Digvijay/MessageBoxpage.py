import customtkinter as tk

class CustumMessegbox(tk.CTkToplevel):
    def __init__(self, parent, message,btnno):
        super().__init__(parent)
        self.geometry("300x150")
        self.title("Confirmation")
        # BooleanVar to store user's choice
        self.user_choice = False

        # Message label
        self.message_label = tk.CTkLabel(self, text=message,)
        self.message_label.pack(pady=10)

        # OK and Cancel buttons
        self.ok_button = tk.CTkButton(self, text="OK", command=self.ok_action)
        self.ok_button.pack(side="left", padx=10)
        if(btnno>1):
         self.cancel_button = tk.CTkButton(self, text="Cancel", command=self.cancel_action)
         self.cancel_button.pack(side="right", padx=10)

    def ok_action(self):
        self.user_choice=True
        self.destroy()

    def cancel_action(self):
        self.user_choice=False
        self.destroy()