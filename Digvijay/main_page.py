import customtkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox
from custom_hovertip import CustomTooltipLabel

class MainPage(tk.CTkFrame):
    def __init__(self, master, height, width, show_stackpanel_page_callback):
        tk.CTkFrame.__init__(self, master, height=height, width=width)
        self.master = master 

        self.show_stackpanel_page_callback = show_stackpanel_page_callback

        # Define light and dark colors
        light_gray = "#F5F5F5"   # Light gray for mainframe
        self.dark_gray = "#0b2545"    # Dark gray for subframe
        white = "#FFFFFF" 
        self.btncolor="#637081"   
        self.textcolor="#0b2545"
        self.lightgray="#8da9c4"   
        self.bthover="#accbe1"

        self.mainframe = tk.CTkFrame(self, fg_color=self.lightgray, height=height, width=width)
        self.mainframe.place(relx=0.5, rely=0.5, anchor="center")
        
        img1=ImageTk.PhotoImage(Image.open("./img/pattern.png"))
        self.l1=tk.CTkLabel(self.mainframe,image=img1)
        self.l1.place(relwidth=1.0,relheight=1.0)

        self.subframe = tk.CTkFrame(self.l1, height=450, width=900,fg_color=self.lightgray ,bg_color=self.lightgray )
        self.subframe.place(relx=0.5, rely=0.5, anchor="center")


       # img2=ImageTk.PhotoImage(Image.open("./img/loginlogob.png").resize([400,150])) # verishield logo
        img2=ImageTk.PhotoImage(Image.open("./images/vector.png")) # vectpr login logo
        self.l2=tk.CTkLabel(self.subframe,image=img2,width=50,text="",bg_color=self.lightgray ,fg_color=self.lightgray )
        self.l2.place(relheight=1.0,x=0,y=0)



        # Create labels
        self.headinglabel = tk.CTkLabel(self.subframe, text="Login Screen", text_color=self.textcolor, height=20, width=80, font=("yu gothic ui semibold", 20),)
        self.label1 = tk.CTkLabel(self.subframe, text="Enter Username", text_color=self.textcolor , height=20, width=80)
        self.label2 = tk.CTkLabel(self.subframe, text="Enter Password", text_color=self.textcolor , height=20, width=80)

        # Create entry widgets
        self.entryusername = tk.CTkEntry(self.subframe, corner_radius=13, width=280, height=30, placeholder_text="Enter Username",border_width=0,fg_color="white",placeholder_text_color=self.textcolor,bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        self.entrypassword = tk.CTkEntry(self.subframe, corner_radius=13, width=280, height=30, placeholder_text="Enter Password",show="*",border_width=0,fg_color="white",placeholder_text_color=self.textcolor,bg_color=self.lightgray , font=("yu gothic ui semibold", 12))
        
        self.imgshow=ImageTk.PhotoImage(Image.open("./images/showp.png").resize([18,15]))
        
        self.imghide=ImageTk.PhotoImage(Image.open("./images/hidep.png").resize([18,15]))

        self.showpassword=tk.CTkButton(self.subframe,text="",command=self.toggle_passwordshow,border_width=0,fg_color="white",image=self.imgshow,width=10,height=10,corner_radius=10)
        

        # Create buttons
        self.Loginbtn = tk.CTkButton(self.subframe, text="Login", command=self.onlogin, corner_radius=20, fg_color= self.btncolor, width=120, height=30, font=("yu gothic ui semibold", 12),hover_color=self.bthover,text_color=self.textcolor)
        CustomTooltipLabel(anchor_widget=self.Loginbtn, text="Before login please verify username and password.", background="grey",foreground="black", width=80, justify=tk.CENTER)
        self.Forgetbtn = tk.CTkButton(self.subframe, text="Forget Password", corner_radius=20, fg_color= self.btncolor, width=120, height=30, font=("yu gothic ui semibold", 12),hover_color=self.bthover,text_color=self.textcolor)
        CustomTooltipLabel(anchor_widget=self.Forgetbtn, text="Forget password will redirect you to another page.", background="grey",foreground="black", width=80, justify=tk.CENTER)
        # Arrange labels and entries
        self.headinglabel.place(y=30, x=500)
        #self.label1.place(y=115, x=410)
        #self.label2.place(y=185, x=410)
        self.entryusername.place(y=110, x=430)

        # Bind the <KeyRelease> event to the CTkEntry widget
        self.entryusername.bind("<KeyRelease>", self.on_entry_input)
        self.entrypassword.bind("<KeyRelease>", self.on_entry_input)
        self.entrypassword.place(y=180, x=430)
        self.showpassword.place(y=183,x=720)
        self.Loginbtn.place(y=280, x=430)
        self.Forgetbtn.place(y=280, x=580)

    def on_entry_input(self, event):
            if(self.entryusername.get()!=""):
             self.entryusername.configure(border_color="",border_width=0)
            if(self.entrypassword.get()!=""):
             self.entrypassword.configure(border_color="",border_width=0)

    def toggle_passwordshow(self):
            self.entrypassword.configure(show="")
            self.showpassword.pack_forget()
            self.showpassword=tk.CTkButton(self.subframe,text="",command=self.toggle_passwordhide,border_width=0,fg_color="white",image=self.imghide,width=20,height=20,corner_radius=10)
            self.showpassword.place(y=183,x=720)

    def toggle_passwordhide(self):
            self.entrypassword.configure(show="*")
            self.showpassword.pack_forget()
            self.showpassword=tk.CTkButton(self.subframe,text="",command=self.toggle_passwordshow,border_width=0,fg_color="white",image=self.imgshow,width=20,height=20,corner_radius=10)
            self.showpassword.place(y=183,x=720)

    def onlogin(self):
        # Capture a fingerprint
        if self.entryusername.get() == "Digvijay" and self.entrypassword.get() == "1234567":
             # get yes/no answers
            msg = CTkMessagebox(self,title="Checked", message="Login Done....",
                                icon="check", option_1="Yes")
            response = msg.get()
            print(response)            
            if response=="Yes":  
                 self.load_stackpanel_page()            
        else:
            messagebox.showerror("Error", "Please enter both username and password.")
            self.entryusername.configure(border_color="red",border_width=2)
            self.entrypassword.configure(border_color="red",border_width=2)

    def load_stackpanel_page(self):
        self.show_stackpanel_page_callback()
