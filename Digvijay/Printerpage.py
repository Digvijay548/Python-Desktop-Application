import customtkinter as tk
from tkinter import ttk
from Scannerpage import stored_valuesScanner
import socket


 # Global dictionary to store values
stored_valuesScanner = {}


class SecondPage(tk.CTkFrame):
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.master=master
        self.mainscrenn=tk.CTkFrame(self,fg_color="#003060",width=widths,height=heights)
        self.mainscrenn.pack()  
        self.centerframe=tk.CTkFrame(self.mainscrenn, fg_color="#68BBE3", height=400, width=600,border_width=2,border_color="#424242" )
        self.centerframe.place(relx=0.2,rely=0.2)
        # Create labels
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="Printer Settings",text_color="white",height=20,width=80,font=("Arial", 16))
        self.label1 = tk.CTkLabel(self.centerframe, text="Enter Printer ip address",text_color="white",height=20,width=80)
        self.label2 = tk.CTkLabel(self.centerframe, text="enter Printer UsbPort",text_color="white",height=20,width=80)
        self.label3 =tk.CTkLabel(self.centerframe, text="Enter data to print",text_color="white",height=20,width=80)
        self.result_label = tk.CTkLabel(self.centerframe,text_color="white",height=20,width=80)

        # Create entry widgets
        self.entryIp = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Ip",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color="#68BBE3", font=("yu gothic ui semibold", 12))
        self.entryPort = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Port like 9100",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color="#68BBE3", font=("yu gothic ui semibold", 12))
        self.entryData = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Data to print",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color="#68BBE3", font=("yu gothic ui semibold", 12))

        # Create buttons
        self.button1 = tk.CTkButton(self.centerframe, text="Connect", command=self.button1_clicked, corner_radius=20, fg_color="#FF9800",width=120,height=30,hover_color="#ae6800")
        self.button2 = tk.CTkButton(self.centerframe, text="Send Data", command=self.button2_clicked, corner_radius=20, fg_color="#FF9800",width=120,height=30,hover_color="#ae6800")

        # Grid layout manager to arrange widgets within the label frame
        self.headinglabel.place(y=20,x=220)
        self.label1.place(y=70,x=110)    
        self.label2.place(y=140,x=110)
        self.label3.place(y=210,x=110)

        
        self.entryIp.place(y=70,x=280)
        self.entryPort.place(y=140,x=280) 
        self.entryData.place(y=210,x=280)

        self.button1.place(y=280,x=130)
        self.button2.place(y=280,x=310)   


    def button1_clicked(self):
        try:
            # Get the IP address and port from the entry fields
            ip_address = self.entryIp.get()
            port =self.entryPort.get()
            # Create a socket connection to the printer
            printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            printer_socket.connect((ip_address, int(port)))
            printer_socket.close()
            # Update result label with success message
            print("connected")           
    
        except Exception as e:              
            print("Received data:", str(e)) 
            if self.result_label.winfo_exists():
              result = f"Erro: "+str(e)
              self.result_label.configure(text=result)              
              self.result_label.place(y=330, x=50) 
            print(f"handledatareceived{result}")
    
    def button2_clicked(self):
        try:
            # Get the IP address and port from the entry fields
            ip_address = self.entryIp.get()
            port =self.entryPort.get()        
            # ZPL label data with text and barcode
            data = self.entryData.get()
             #Define your ZPL label contents
            zpl_label1d = f"""
            ^XA
            ^HH
            ^FO20,20^A0N,25,25^FD(Acg Inspection 1D)^FS
            ^FO20,100^BY3^BCN,100,Y,N,N,A^FD{data}^FS
            ^XZ
            """
            
            zpl_label2d = f"""
            ^XA
            ^HH
            ^FO20,300^A0N,25,25^FD(Acg Inspection 2D)^FS
            ^FO20,400^BXN,10,200^FD{data}^FS
            ^XZ
            """

            # Combine the ZPL labels into a single label
            combined_label = zpl_label1d + zpl_label2d
            
            # Create a socket connection to the printer
            printer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            printer_socket.connect((ip_address, int(port)))
            printer_socket.sendall(combined_label.encode('utf-8'))   
            # Close the socket connection
            printer_socket.close()  
            if self.result_label.winfo_exists():              
              self.result_label.configure(text=f"Sucessfuly send data to printer", text_color="#FF0000")              
              self.result_label.place(y=330, x=50) 
            print("Sucessfuly send data to printer")     
        except Exception as e:
            print("error"+str(e)) 
            if self.result_label.winfo_exists():
             self.result_label.config(text=f"Error in sending data", text_color="#FF0000")