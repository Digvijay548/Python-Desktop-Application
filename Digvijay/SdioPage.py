import customtkinter as tk
from tkinter import ttk
import socket
from sdio import SDIOclass

stored_valuesScanner = {}
class SdioPage(tk.CTkFrame):
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
        self.centerframe=tk.CTkFrame(self.mainscrenn, fg_color=self.lightgray , height=400, width=600,border_width=2,border_color=self.lightgray )
        self.centerframe.place(relx=0.2,rely=0.2) 
        # Create labels
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="SDIO Settings",text_color=self.textcolor,height=20,width=80,font=("Arial", 16))
        #self.label1 = tk.CTkLabel(self.centerframe, text="Enter Sdio ip address",text_color=self.textcolor,height=20,width=80)
        self.label2 = tk.CTkLabel(self.centerframe, text="Enter SDIO COM Port",text_color=self.textcolor,height=20,width=80)
        self.label3 =tk.CTkLabel(self.centerframe, text="Data Received from SDIO",text_color=self.textcolor,height=20,width=80)
        self.result_label = tk.CTkLabel(self.centerframe,text_color=self.textcolor,height=20,width=80)

        # Create entry widgets
       # self.entryIp = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter Ip",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        self.board_options = ['COM1', 'COM2', 'COM3','COM4']
        self.selected_board = tk.StringVar()
        self.selected_board.set(self.board_options[0])
        self.entryPort = tk.CTkComboBox(self.centerframe, corner_radius=15,values=self.board_options,width=150,height=30,border_width=0,fg_color="white",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        port_value = None
        if "port" in stored_valuesScanner:
           port_value = stored_valuesScanner.get("port")
        if port_value in self.board_options:
          self.entryPort.set(port_value)
        self.entryData = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Send Data To Sdio => Hello, SDIO!",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))

        # Create buttons
        self.button1 = tk.CTkButton(self.centerframe, text="Connect",text_color=self.textcolor, command=self.connect_to_sdio, corner_radius=20, fg_color= self.btncolor,width=120,height=30,hover_color=self.bthover)
        self.button2 = tk.CTkButton(self.centerframe, text="Send Data",text_color=self.textcolor, command=self.send_data, corner_radius=20, fg_color= self.btncolor,width=120,height=30,hover_color=self.bthover)

        # Grid layout manager to arrange widgets within the label frame
        self.headinglabel.place(y=20,x=220)
        #self.label1.place(y=70,x=110)    
        self.label2.place(y=140,x=110)
        self.label3.place(y=210,x=110)

        
        #self.entryIp.place(y=70,x=280)
        self.entryPort.place(y=140,x=280) 
        self.entryData.place(y=210,x=280)

        self.button1.place(y=280,x=130)
        self.button2.place(y=280,x=310)   

    def connect_to_sdio(self):
        com_port = self.entryPort.get()
        if com_port:
            self.sdio = SDIOclass(com_port, 115200)
            if self.sdio.connect_to_board():            
              self.result_label.configure(text=f"SDIO Sucessfuly Connected", text_color="#00FF00")              
              self.result_label.place(y=330, x=50)
            else:       
              self.result_label.configure(text=f"SDIO not Connected", text_color="#FF0000")              
              self.result_label.place(y=330, x=50)
        else:
              self.result_label.configure(text=f"Please Enter Com Port", text_color="#FF0000")              
              self.result_label.place(y=330, x=50)

    def send_data(self):
        print(self.sdio)
        if self.sdio:
            SdioSendData=self.entryData.get()
            if self.sdio.send_to_instrument("0M123\n"):
              received_data = self.sdio.read_from_instrument()
              if received_data:
               self.result_label.configure(text=f"Received data => {received_data}", text_color="#00FF00")              
               self.result_label.place(y=330, x=50)
              else:
               self.result_label.configure(text=f"No data received from SDIO", text_color="#FF0000")              
               self.result_label.place(y=330, x=50)
            else:
              self.result_label.configure(text=f"Error in sending data", text_color="#FF0000")              
              self.result_label.place(y=330, x=50)