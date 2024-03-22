import customtkinter as tk
from tkinter import ttk
from Scannerpage import stored_valuesScanner
import socket


 # Global dictionary to store values
stored_valuesScanner = {}


class Auditlog(tk.CTkFrame):
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.master=master
        self.mainscrenn=tk.CTkFrame(self,fg_color="#003060",width=widths,height=heights)
        self.mainscrenn.pack()  
        self.centerframe=tk.CTkFrame(self.mainscrenn, fg_color="#68BBE3", height=400, width=600,border_width=2,border_color="#424242" )
        self.centerframe.place(relx=0.2,rely=0.2)
        # Create labels
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="Auditlog Settings",text_color="white",height=20,width=80,font=("Arial", 16))
        self.headinglabel.pack()