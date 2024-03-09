import customtkinter as tk
from Printerpage import SecondPage
from Scannerpage import FirstPage
from Camerapage import camerapage
from PIL import Image, ImageTk

class Stackpanelpage(tk.CTkFrame):
    def __init__(self, master, height, width, show_main_page_callback):
        self.selectedframe=""
        tk.CTkFrame.__init__(self, master, height=height, width=width,)

        self.show_main_page_callback = show_main_page_callback


        #  ******************** This is mainframe of stackpanel ********************

        self.frams = tk.CTkFrame(self,fg_color="#E0E0E0",width=self.winfo_screenwidth(),height=height)
        self.frams.place(x=0,y=0)


         #  ******************** This is Leftframe on stackpanel (scanner,printer,camera buttons)  ********************


        self.leftside = tk.CTkFrame(self.frams, width=300,height =self.frams._current_height,fg_color="red")
        self.leftside.place(x=0,y=0)
        self.leftsideinner= tk.CTkFrame(self.leftside,fg_color="#C6C6C6",width=self.leftside._current_width,height=self.leftside._current_height)
        self.leftsideinner.place(x=0,y=0)
        self.homeimg=ImageTk.PhotoImage(Image.open("./images/home.png").resize([50,50]))
        self.scannerimg=ImageTk.PhotoImage(Image.open("./images/scanner.png").resize([50,50]))
        self.printerimg=ImageTk.PhotoImage(Image.open("./images/printer.png").resize([50,50]))
        self.cameraimg=ImageTk.PhotoImage(Image.open("./images/camera.png").resize([70,70]))




        #  ******************** This is Right frame of stackpanel which load content according to scanner printer buttons ********************


        self.rightside = tk.CTkFrame(self.frams,fg_color="#E0E0E0",height=self.frams._current_height,width=self.frams._current_width-self.leftside._current_width)
        self.rightside.place(x=280,y=0)
        self.stackpanel_button = tk.CTkButton(self.leftsideinner, text="Home", corner_radius=30, command=self.load_main_page,height=70,width=180,fg_color="#3f5b72",font=("Arial", 16),image=self.homeimg)
        self.stackpanel_button.place(relx=0.5,anchor="center",y=50)
        self.first_button = tk.CTkButton(self.leftsideinner, text="Scanner", corner_radius=30,command=self.load_first_page,height=70,width=180,fg_color="#3f5b72",font=("Arial", 16),image=self.scannerimg)
        self.first_button.place(relx=0.5,anchor="center",y=150)
        self.second_button = tk.CTkButton(self.leftsideinner, text="Printer", corner_radius=30,command=self.load_second_page,height=70,width=180,fg_color="#3f5b72",font=("Arial", 16),image=self.printerimg)
        self.second_button.place(relx=0.5,anchor="center",y=250)
        self.second_button = tk.CTkButton(self.leftsideinner, text="Camera", corner_radius=30,command=self.load_camera_page,height=70,width=180,fg_color="#3f5b72",font=("Arial", 16),image=self.cameraimg)
        self.second_button.place(relx=0.5,anchor="center",y=350)
        self.load_first_page()







    def load_main_page(self):
        self.selectedframe=""
        # Clear the right side frame
        for widget in self.rightside.winfo_children():
            widget.destroy()        
        # Call the callback to show the main page
        self.rightside.place_forget()
        self.show_main_page_callback()

    def load_first_page(self):
        if(self.selectedframe!="Scannerpage"):
         self.selectedframe="Scannerpage"
         # Clear the right side frame  
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.rightside.place(x=300,y=0)# Create and display content for the first page
         first_page = FirstPage(self.rightside,heights=self.rightside._current_height,widths=self.rightside._current_width)  #scanner page
         first_page.pack(fill=tk.BOTH,expand=True)

    def load_second_page(self):
        if(self.selectedframe!="Printerpage"):
         self.selectedframe="Printerpage"
         # Clear the right side frame
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.rightside.place(x=300,y=0)
         first_page = SecondPage(self.rightside,heights=self.rightside._current_height,widths=self.rightside._current_width)    #printer page
         first_page.pack(fill=tk.BOTH,expand=True)

    def load_camera_page(self):
        if(self.selectedframe!="Camerapage"):
         self.selectedframe="Camerapage"
         # Clear the right side frame
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.rightside.place(x=300,y=0)
         first_page = camerapage(self.rightside,heights=self.rightside._current_height,widths=self.rightside._current_width)    #printer page
         first_page.pack(fill=tk.BOTH,expand=True)
