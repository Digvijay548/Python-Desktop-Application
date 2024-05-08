import customtkinter as tk
from tkinter import ttk
from Scannerpage import stored_valuesScanner
import socket


 # Global dictionary to store values
stored_valuesScanner = {}


class Inspection(tk.CTkFrame):
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.master=master
        self.dark_gray = "#0b2545" 
        self.lightgray="#8da9c4" 
        self.mainscrenn=tk.CTkFrame(self,fg_color=self.lightgray,width=widths,height=heights)
        self.mainscrenn.pack()  
        self.centerframe=tk.CTkFrame(self.mainscrenn, fg_color=self.lightgray , height=400, width=600,border_width=2,border_color=self.dark_gray )
        self.centerframe.place(relx=0.2,rely=0.2)
        # Create labels
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="Inspection",text_color="white",height=20,width=80,font=("Arial", 16))
        self.headinglabel.pack()