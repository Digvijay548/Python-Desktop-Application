import customtkinter as tk
from tkinter import ttk
from plcfiles.client import ModbusClient
 # Global dictionary to store values
stored_valuesScanner = {}


class PLCPage(tk.CTkFrame):
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.master=master
        self.dark_gray = "#0b2545" 
        self.lightgray="#8da9c4" 
        self.btncolor="#637081"
        self.textcolor="#0b2545"
        self.bthover="#accbe1"
        self.mainscrenn=tk.CTkFrame(self,fg_color=self.dark_gray,width=widths,height=heights)
        self.mainscrenn.pack()  
        self.centerframe=tk.CTkFrame(self.mainscrenn, fg_color=self.lightgray , height=400, width=800,border_width=2,border_color=self.lightgray )
        self.centerframe.place(relx=0.2,rely=0.2)
        # Create labels
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="PLC Settings",text_color=self.textcolor,height=20,width=80,font=("Arial", 16))
        self.label1 = tk.CTkLabel(self.centerframe, text="Enter PLC ip address",text_color=self.textcolor,height=20,width=80)
        self.label2 = tk.CTkLabel(self.centerframe, text="enter PLC Baudrate",text_color=self.textcolor,height=20,width=80)
        self.label3 =tk.CTkLabel(self.centerframe, text="Enter data to Send",text_color=self.textcolor,height=20,width=80)
        self.result_label = tk.CTkLabel(self.centerframe,text_color=self.textcolor,height=20,width=80)

        # Create entry widgets
        self.entryIp = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Ip",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        self.entryPort = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Port like 9100",
                                     border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray , 
                                     font=("yu gothic ui semibold", 12))
        self.entryAdd = tk.CTkEntry(self.centerframe, corner_radius=15,width=120,height=30,placeholder_text="Enter Address",
                                    border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray ,
                                      font=("yu gothic ui semibold", 12))
        
        self.entrydata = tk.CTkEntry(self.centerframe, corner_radius=15,width=120,height=30,placeholder_text="Enter Data",
                                    border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray ,
                                      font=("yu gothic ui semibold", 12))
            
        # Create buttons
        self.button1 = tk.CTkButton(self.centerframe, text="Connect",text_color=self.textcolor, 
                                    command=self.ConnectToPlc, corner_radius=20, fg_color= self.btncolor,width=120,
                                    height=30,hover_color=self.bthover)
        self.button2 = tk.CTkButton(self.centerframe, text="Send Data",text_color=self.textcolor,
                                     command=self.SendData, corner_radius=20, fg_color= self.btncolor,width=120
                                     ,height=30,hover_color=self.bthover)

        # Grid layout manager to arrange widgets within the label frame
        self.headinglabel.place(y=20,x=220)
        self.label1.place(y=70,x=110)    
        self.label2.place(y=140,x=110)
        self.label3.place(y=210,x=90)

        
        self.entryIp.place(y=70,x=280)
        self.entryPort.place(y=140,x=280) 
        self.entryAdd.place(y=210,x=200)
        self.entrydata.place(y=210,x=360)

        self.button1.place(y=280,x=130)
        self.button2.place(y=280,x=310)   


    def ConnectToPlc(self):
        try:
            # Get the IP address and port from the entry fields
            ip_address = self.entryIp.get()
            port =self.entryPort.get()            
            self.c = ModbusClient(host=str(ip_address),port=int(port), auto_open=True)
            self.c.open()
            if(self.c.is_open):         
             self.result_label.configure(text="PLC Connected...", text_color="green")              
             self.result_label.place(y=330, x=50) 
            else:   
                self.result_label.configure(text="Error in connecting...", text_color="red")              
                self.result_label.place(y=330, x=50)     
    
        except Exception as e:    
           self.result_label.configure(text=f"{str(e)}", text_color="red")              
           self.result_label.place(y=330, x=50)      
    
    def SendData(self):
        try:
            address=int(self.entryAdd.get())
            data=int(self.entrydata.get())
            if self.c.is_open:
               if self.c.write_single_coil(address,data):
                self.result_label.configure(text=f"Data send to {address} and data => {data}", text_color="green")              
                self.result_label.place(y=330, x=50)
               else:
                self.result_label.configure(text=f"failed to send Data on {address}", text_color="red")              
                self.result_label.place(y=330, x=50)                  
        except Exception as e:
            print(f"Entered step {str(e)}")