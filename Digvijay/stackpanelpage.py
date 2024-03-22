import customtkinter as tk
from Printerpage import SecondPage
from Scannerpage import FirstPage
from Camerapage import camerapage
from PIL import Image, ImageTk
from Auditlog import Auditlog
from Inspectionpage import Inspection
from VersionPage import Versionpage

class Stackpanelpage(tk.CTkFrame):
    def __init__(self, master, height, width, show_main_page_callback):
        self.selectedframe=""
        tk.CTkFrame.__init__(self, master, height=height, width=width,)

        self.show_main_page_callback = show_main_page_callback


        #  ******************** This is mainframe of stackpanel ********************

        self.frams = tk.CTkFrame(self,fg_color="#68BBE3",width=width,height=height)
        self.frams.place(x=0,y=0)


        self.Menu=ImageTk.PhotoImage(Image.open("./img/menu.png").resize([40,40]))
        self.info=ImageTk.PhotoImage(Image.open("./images/infoimg.png").resize([40,40]))
        self.Work=ImageTk.PhotoImage(Image.open("./images/work.png").resize([40,40]))
        
        self.Menubtn = tk.CTkButton(self.frams, text="",fg_color="#68BBE3", corner_radius=5,command=self.toggelframe,height=30,width=30,font=("Arial", 10),image=self.Menu)
        self.Menubtn.place(y=10,x=10)
        
        self.Menubtnwork = tk.CTkButton(self.frams, text="",fg_color="#68BBE3", corner_radius=5,command=self.toggelframeWork,height=30,width=30,font=("Arial", 10),image=self.Work)
        self.Menubtnwork.place(y=100,x=10)
        
        self.Menubtninfo = tk.CTkButton(self.frams, text="",fg_color="#68BBE3", corner_radius=5,command=self.toggelframeInfo,height=30,width=30,font=("Arial", 10),image=self.info)
        self.Menubtninfo.place(y=190,x=10)
        
        self.Menubtn4 = tk.CTkButton(self.frams, text="",fg_color="#68BBE3", corner_radius=5,height=30,width=30,font=("Arial", 10),image=self.Menu)
        self.Menubtn4.place(y=280,x=10)
        
        self.Menubtn3 = tk.CTkButton(self.frams, text="",fg_color="#68BBE3", corner_radius=5,height=30,width=30,font=("Arial", 10),image=self.Menu)
        self.Menubtn3.place(y=370,x=10)
        


        #  ******************** This is Right frame of stackpanel which load content according to scanner printer buttons ********************


        self.rightside = tk.CTkFrame(self.frams,fg_color="#003060",height=self.frams._current_height,width=self.frams._current_width)
        self.rightside.place(x=70,y=0)


        self.toggelframe()
        self.load_first_page()



    def toggelframeWork(self):

         #  ******************** This is Leftframe on stackpanel (scanner,printer,camera buttons)  ********************
        self.Menubtn.place_forget()


        self.leftside = tk.CTkFrame(self.frams, width=300,height =self.frams._current_height,fg_color="#68BBE3")
        self.leftside.place(x=0,y=0)
        
        self.leftsideinner= tk.CTkFrame(self.leftside,fg_color="#68BBE3",width=self.leftside._current_width,height=self.leftside._current_height)
        self.leftsideinner.place(x=0,y=0)

        
        self.CloseMenu = tk.CTkButton(self.leftsideinner, text="X", corner_radius=2, command=self.Closetoggelframe,height=30,width=30,font=("Arial", 14))
        self.CloseMenu.place(x=260,y=10)

        
        self.Audit=ImageTk.PhotoImage(Image.open("./images/Audit.png").resize([40,40]))


        self.inspectionbtn = tk.CTkButton(self.leftsideinner, text="Inspection",border_color="#003060",border_width=2,corner_radius=30, command=self.Load_Inspection,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.Work,)
        self.inspectionbtn.place(relx=0.5,anchor="center",y=50)



        self.rightside.configure(height=self.frams._current_height,width=self.frams._current_width-self.leftside._current_width)
        self.rightside.place(x=280,y=0)



    def toggelframeInfo(self):

         #  ******************** This is Leftframe on stackpanel (scanner,printer,camera buttons)  ********************
        self.Menubtn.place_forget()


        self.leftside = tk.CTkFrame(self.frams, width=300,height =self.frams._current_height,fg_color="#68BBE3")
        self.leftside.place(x=0,y=0)
        
        self.leftsideinner= tk.CTkFrame(self.leftside,fg_color="#68BBE3",width=self.leftside._current_width,height=self.leftside._current_height)
        self.leftsideinner.place(x=0,y=0)

        
        self.CloseMenu = tk.CTkButton(self.leftsideinner, text="X", corner_radius=2, command=self.Closetoggelframe,height=30,width=30,font=("Arial", 14))
        self.CloseMenu.place(x=260,y=10)

        
        self.Audit=ImageTk.PhotoImage(Image.open("./images/Audit.png").resize([40,40]))
        self.Auditlogbtn = tk.CTkButton(self.leftsideinner, text="Audit Log",border_color="#003060",border_width=2,corner_radius=30, command=self.Load_AuditLog,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.Audit,)
        self.Auditlogbtn.place(relx=0.5,anchor="center",y=50)

        
        self.Versioncheckpng=ImageTk.PhotoImage(Image.open("./images/infoimg.png").resize([40,40]))
        self.Versioncheck = tk.CTkButton(self.leftsideinner, text="LoadInfo",border_color="#003060",border_width=2,corner_radius=30, command=self.Load_Info,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.Versioncheckpng,)
        self.Versioncheck.place(relx=0.5,anchor="center",y=150)



        self.rightside.configure(height=self.frams._current_height,width=self.frams._current_width-self.leftside._current_width)
        self.rightside.place(x=280,y=0)









    def Load_Inspection(self):
        if(self.selectedframe!="inspection"):
         self.selectedframe="inspection"
         # Clear the right side frame  
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         inspection = Inspection(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)  #inspection right page
         inspection.pack(fill=tk.BOTH,expand=True)


    def Load_Info(self):
        if(self.selectedframe!="versionpage"):
         self.selectedframe="versionpage"
         # Clear the right side frame  
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         versionpage = Versionpage(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)  #info left page
         versionpage.pack(fill=tk.BOTH,expand=True)


    def load_main_page(self):
        self.selectedframe=""
        # Clear the right side frame
        for widget in self.rightside.winfo_children():
            widget.destroy()        
        # Call the callback to show the main page
        self.rightside.place_forget()
        self.show_main_page_callback()

    def Closetoggelframe(self):
        self.leftside.place_forget()
        self.Menubtn.place(x=10,y=10)
        self.rightside.configure(height=self.frams._current_height,width=self.frams._current_width-50)
        self.rightside.place(x=70,y=0)
       

    def toggelframe(self):

         #  ******************** This is Leftframe on stackpanel (scanner,printer,camera buttons)  ********************
        self.Menubtn.place_forget()


        self.leftside = tk.CTkFrame(self.frams, width=300,height =self.frams._current_height,fg_color="#68BBE3")
        self.leftside.place(x=0,y=0)
        
        self.leftsideinner= tk.CTkFrame(self.leftside,fg_color="#68BBE3",width=self.leftside._current_width,height=self.leftside._current_height)
        self.leftsideinner.place(x=0,y=0)

        self.homeimg=ImageTk.PhotoImage(Image.open("./images/home.png").resize([50,50]))
        self.scannerimg=ImageTk.PhotoImage(Image.open("./images/scanner.png").resize([50,50]))
        self.printerimg=ImageTk.PhotoImage(Image.open("./images/printer.png").resize([50,50]))
        self.cameraimg=ImageTk.PhotoImage(Image.open("./images/camera.png").resize([70,70]))

        
        self.CloseMenu = tk.CTkButton(self.leftsideinner, text="X", corner_radius=2, command=self.Closetoggelframe,height=30,width=30,font=("Arial", 14))
        self.CloseMenu.place(x=260,y=10)


        self.stackpanel_button = tk.CTkButton(self.leftsideinner, text="Home",border_color="#003060",border_width=2,corner_radius=30, command=self.load_main_page,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.homeimg,)
        self.stackpanel_button.place(relx=0.5,anchor="center",y=50)
        self.first_button = tk.CTkButton(self.leftsideinner, text="Scanner",border_color="#003060",border_width=2, corner_radius=30,command=self.load_first_page,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.scannerimg)
        self.first_button.place(relx=0.5,anchor="center",y=150)
        self.second_button = tk.CTkButton(self.leftsideinner, text="Printer",border_color="#003060",border_width=2, corner_radius=30,command=self.load_second_page,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.printerimg)
        self.second_button.place(relx=0.5,anchor="center",y=250)
        self.second_button = tk.CTkButton(self.leftsideinner, text="Camera",border_color="#003060",border_width=2, corner_radius=30,command=self.load_camera_page,height=70,width=180,fg_color="#68BBE3",hover_color="#003060",font=("Arial", 16),image=self.cameraimg)
        self.second_button.place(relx=0.5,anchor="center",y=350)



        self.rightside.configure(height=self.frams._current_height,width=self.frams._current_width-self.leftside._current_width)
        self.rightside.place(x=280,y=0)
     
    

    def Load_AuditLog(self):
        if(self.selectedframe!="Auditlog"):
         self.selectedframe="Auditlog"
         # Clear the right side frame  
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         auditlog = Auditlog(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)  #scanner page
         auditlog.pack(fill=tk.BOTH,expand=True)
    
    def load_first_page(self):
        if(self.selectedframe!="Scannerpage"):
         self.selectedframe="Scannerpage"
         # Clear the right side frame  
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         first_page = FirstPage(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)  #scanner page
         first_page.pack(fill=tk.BOTH,expand=True)

    def load_second_page(self):
        if(self.selectedframe!="Printerpage"):
         self.selectedframe="Printerpage"
         # Clear the right side frame
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         first_page = SecondPage(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)    #printer page
         first_page.pack(fill=tk.BOTH,expand=True)

    def load_camera_page(self):
        if(self.selectedframe!="Camerapage"):
         self.selectedframe="Camerapage"
         # Clear the right side frame
         for widget in self.rightside.winfo_children():
             widget.destroy()
         self.Closetoggelframe()
         first_page = camerapage(self.rightside,heights=self.frams._current_height,widths=self.frams._current_width)    #printer page
         first_page.pack(fill=tk.BOTH,expand=True)
