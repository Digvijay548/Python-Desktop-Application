import customtkinter as tk
from tkinter import ttk
import clr
clr.AddReference('D:\\OneDrive - ACG Associated Capsules Pvt. Ltd\\Desktop\\python poc\\Digvijay\\Dll\\Events.dll')  # Load the C# DLL
from Events import SerialPortManager
    
    

# Global dictionary to store values
stored_valuesScanner = {}


class FirstPage(tk.CTkFrame):
       
    def __init__(self, master,heights,widths):     
        tk.CTkFrame.__init__(self, master,heights,widths)
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
        self.mainscrenn=tk.CTkFrame(self,fg_color="#E0E0E0",width=widths,height=heights)
        self.mainscrenn.pack()         

        self.centerframe=tk.CTkFrame(self.mainscrenn,fg_color="white", height=400, width=600, corner_radius=10,border_width=2,border_color="#424242"  )
        self.centerframe.place(relx=0.2,rely=0.2)

        # Create labels
        self.result_label = tk.CTkLabel(self.centerframe, text_color="#FFA000",height=20,width=300)
        
        self.headinglabel = tk.CTkLabel(self.centerframe, text="Scanner Settings",text_color="#212121",height=20,width=80,font=("Arial", 16))
        # self.label1 = tk.CTkLabel(self.centerframe, text="Enter scanner Ip",text_color="#212121",height=20,width=80)  comment out for reson ip not required in scanner
        self.label2 = tk.CTkLabel(self.centerframe, text="enter scanner Boardrate",text_color="#212121",height=20,width=80)
        self.label3 = tk.CTkLabel(self.centerframe, text="Select scanner Port",text_color="#212121",height=20,width=80)

        # Create entry widgets
        #self.entryIP = tk.CTkEntry(self.centerframe, corner_radius=5,fg_color="#FFFFFF",width=150,height=30,placeholder_text="Enter Ip")comment out for reson ip not required in scanner
        self.board_options = ['COM1', 'COM2', 'COM3','COM4']
        self.selected_board = tk.StringVar()
        self.selected_board.set(self.board_options[0])
        self.entryPort = tk.CTkComboBox(self.centerframe, corner_radius=15,values=self.board_options,width=150,height=30,border_width=0,fg_color="#C6C6C6",bg_color="white", font=("yu gothic ui semibold", 12))
        port_value = None
        if "port" in stored_valuesScanner:
           port_value = stored_valuesScanner.get("port")
        if port_value in self.board_options:
          self.entryPort.set(port_value)

        # self.entryBaord['values'] = self.board_options
        self.entryBaord = tk.CTkEntry(self.centerframe, corner_radius=15,width=150,height=30,placeholder_text="Enter boudrate",border_width=0,fg_color="#C6C6C6",placeholder_text_color="#4C4C4C",bg_color="white", font=("yu gothic ui semibold", 12))
        board_rate_value = None
        if "board_rate" in stored_valuesScanner:
           board_rate_value = stored_valuesScanner["board_rate"]
           self.entryBaord.insert(0,board_rate_value)
        # Create buttons
        self.button1 = tk.CTkButton(self.centerframe, text="Connect", command=self.button1_clicked, corner_radius=20, fg_color="#FF9800",width=120,height=30,text_color="#3f5b72",hover_color="#ae6800")
        self.button2 = tk.CTkButton(self.centerframe, text="Disconnect", command=self.button2_clicked, corner_radius=20,fg_color="#FF9800",width=120,height=30,text_color="#3f5b72",hover_color="#ae6800")

        # Arrange labels and entries
        self.headinglabel.place(y=20,x=200)
        #self.label1.place(y=70,x=110) comment out for reson ip not required in scanner
        self.label2.place(y=140,x=110)
        self.label3.place(y=210,x=110)

        #self.entryIP.place(y=70,x=280) comment out for reson ip not required in scanner
        self.entryBaord.place(y=140,x=280)       
        self.entryPort.place(y=210,x=280)

        self.button1.place(y=280,x=130)
        self.button2.place(y=280,x=310) 


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
          print("Openport status=>  "+resultopenport)
          # Storing values in the global dictionary
          #stored_valuesScanner['ip'] = ip
          stored_valuesScanner['board_rate'] = board_rate
          stored_valuesScanner['port'] = port 
          # Perform your operations here using the input values
          result = f"Connected to scanner with board rate {board_rate} on port {port}"
          self.result_label.configure(text=result)                
          self.result_label.place(y=330,x=50)       
        except Exception as e:
            self.result_label.place(y=330,x=50) 
            self.result_label.config(text=f"Error:on connect scanner", text_color="#FF0000") 

    def button2_clicked(self):         
        self.serial_port_manager.ClosePort()
        result = f"Scanner Disconnected...!"
        self.result_label.configure(text=result)                
        self.result_label.place(y=330,x=50)
           

