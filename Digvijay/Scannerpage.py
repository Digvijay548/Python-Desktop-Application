import customtkinter as tk
from tkinter import ttk
import clr
clr.AddReference('D:\python poc\Dll\Events.dll' )  # Load the C# DLL
from Events import SerialPortManager
from CTkTable import *
from custom_hovertip import CustomTooltipLabel
    
    

# Global dictionary to store values
stored_valuesScanner = {}


class FirstPage(tk.CTkFrame):
       
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.dark_gray = "#0b2545" 
        self.btncolor="#637081"
        self.lightgray="#8da9c4"  
        self.bthover="#accbe1"
        try :
           self.serial_port_manager = SerialPortManager()
           resultport=self.serial_port_manager.ClosePort()          
           self.serial_port_manager.DataReceived +=self.handle_data_received   
           if stored_valuesScanner is None or not stored_valuesScanner and resultport==1:
             print("Enter Port and Board rate")
           else:
             resultopenport=self.serial_port_manager.OpenPort(stored_valuesScanner.get("port"),int(stored_valuesScanner.get("board_rate")))
             if resultopenport==0:
              print(f"Port=>{stored_valuesScanner.get('port')} and Board rate=> {stored_valuesScanner.get('board_rate')}")
        except Exception as e:
           print("exception in constructor") 
        self.master=master
        self.mainscrenn=tk.CTkFrame(self,fg_color=self.dark_gray,width=widths,height=heights)
        self.mainscrenn.pack()    

      # ******************************** Centerframe in scanner page ***********************************     

        self.centerframe=tk.CTkFrame(self.mainscrenn,fg_color=self.lightgray , height=400, width=600,border_width=2,border_color="#1c1c1c"  )
        self.centerframe.place(relx=0.2,y=70)
        self.result_label = tk.CTkLabel(self.centerframe,text="", text_color="white",height=20,width=300)        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="Scanner Settings",text_color="white",height=20,width=80,font=("Arial", 16))
        self.label2 = tk.CTkLabel(self.centerframe, text="enter scanner Boardrate",text_color="white",height=20,width=80)
        self.label3 = tk.CTkLabel(self.centerframe, text="Select scanner Port",text_color="white",height=20,width=80)
        self.board_options = ['COM1', 'COM2', 'COM3','COM4']
        self.selected_board = tk.StringVar()
        self.selected_board.set(self.board_options[0])
        self.entryPort = tk.CTkComboBox(self.centerframe, corner_radius=15,values=self.board_options,width=150,height=30,border_width=0,fg_color="white",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        port_value = None
        if "port" in stored_valuesScanner:
           port_value = stored_valuesScanner.get("port")
        if port_value in self.board_options:
          self.entryPort.set(port_value)
        # self.entryBaord['values'] = self.board_options
        self.entryBaord = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter boudrate",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        board_rate_value = None
        if "board_rate" in stored_valuesScanner:
           board_rate_value = stored_valuesScanner["board_rate"]
           self.entryBaord.insert(0,board_rate_value)
        # Create buttons
        self.button1 = tk.CTkButton(self.centerframe, text="Connect", command=self.button1_clicked, corner_radius=20, fg_color= self.btncolor,width=120,height=30,text_color="white",hover_color=self.bthover)
        CustomTooltipLabel(anchor_widget=self.button1, text="Connect to scanner..", background="white",foreground="black", width=20, justify=tk.LEFT)
        self.button2 = tk.CTkButton(self.centerframe, text="Disconnect", command=self.button2_clicked, corner_radius=20,fg_color= self.btncolor,width=120,height=30,text_color="white",hover_color=self.bthover)
        CustomTooltipLabel(anchor_widget=self.button1, text="If you are connected to scanner then only try", background="white",foreground="black", width=40, justify=tk.LEFT)
        # Arrange labels and entries
        self.headinglabel.place(y=20,x=220)
        #self.label1.place(y=70,x=110) comment out for reson ip not required in scanner
        self.label2.place(y=140,x=110)
        self.label3.place(y=210,x=110)
        #self.entryIP.place(y=70,x=280) comment out for reson ip not required in scanner
        self.entryBaord.place(y=140,x=280)       
        self.entryPort.place(y=210,x=280)
        self.button1.place(y=280,x=130)
        self.button2.place(y=280,x=310) 

      # ******************************** Bottom frame in scanner page ***********************************    
        self.Bottomframe=tk.CTkFrame(self.mainscrenn,fg_color=self.dark_gray , height=200, width=800)
        self.Bottomframe.place(x=280,y=500)
        self.value = [["Index","Scanner Boardrate","Scanner Port"],         [1,"9100","COM4"],         [3,"9100","COM4"],      ]

        self.table = CTkTable(self.Bottomframe, row=3, column=3,hover_color=self.btncolor, values=self.value,header_color=self.btncolor,width=200,command=self.selectedtabeldata,colors=[self.bthover,self.bthover])
        self.table.pack(expand=True, fill="both", padx=20, pady=20)


    def selectedtabeldata(self,event):

      self.tabeldataselected=self.table.get_row(event['row'])
      print(str(self.tabeldataselected))
      self.entryBaord.delete(0,tk.END)    
      self.entryBaord.insert(0,self.tabeldataselected[1])      
      self.entryPort.set(self.tabeldataselected[2])


    def handle_received_data(data):
        # This function handles the received data
       print("Received data:", data.decode().strip())
       # You can perform further processing here

    def handle_data_received(self,sender, data):   
      try:  
        print("Received data:", data) 
        if self.result_label.winfo_exists():
            result = f"Connected to scanner data received: {data}"
            self.result_label.configure(text=result)              
            self.result_label.place(y=330, x=50) 
            print(f"handledatareceived{data}")
      except Exception as e:
        print("handledatareceived5")
        result = f"Error in receiving data"
        self.result_label.configure(text=result)                
        self.result_label.place(y=330,x=50) 
         

    def button1_clicked(self):
        try:
          #ip = self.entryIP.get()  # Getting input from entryIP
          board_rate = self.entryBaord.get()  # Getting input from entryBaord
          port = self.entryPort.get()  # Getting input from entryPort
          #self.label1.configure()  
          #clr.AddReference("C:\\Users\\Digvijay.Patil\\Downloads\\1\\AdditionDll.dll")
          print ("Entryboard=")
          print(self.entryBaord.get())
          print ("entryPort=")
          print(self.entryPort.get())
          #this is for connect to scanner
          resultopenport=self.serial_port_manager.OpenPort(self.entryPort.get(),int(self.entryBaord.get()))
          try:
                if(resultopenport != "Connected"):
                   result = f"Connection failed to scanner with board rate {board_rate} on port {port}"
                   self.result_label.configure(text=result,text_color="red") 
                else:               
                 stored_valuesScanner['board_rate'] = board_rate
                 stored_valuesScanner['port'] = port 
                 # Perform your operations here using the input values
                 result = f"Connected to scanner with board rate {board_rate} on port {port}"
                 self.result_label.configure(text=result,text_color="green") 
          except Exception as e:
             print(str(e))



          self.result_label.place(y=330,x=50)       
        except Exception as e:
            self.result_label.place(y=330,x=50) 
            self.result_label.config(text=f"Error:on connect scanner", text_color="red") 

    def button2_clicked(self):         
        self.serial_port_manager.ClosePort()
        result = f"Scanner Disconnected...!"
        self.result_label.configure(text=result)                
        self.result_label.place(y=330,x=50)
           

