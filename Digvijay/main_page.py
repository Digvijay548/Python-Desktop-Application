import customtkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from CTkMessagebox import CTkMessagebox

class MainPage(tk.CTkFrame):
    def __init__(self, master, height, width, show_stackpanel_page_callback):
        tk.CTkFrame.__init__(self, master, height=height, width=width)
        self.master = master 

        self.show_stackpanel_page_callback = show_stackpanel_page_callback

        # Define light and dark colors
        light_gray = "#F5F5F5"   # Light gray for mainframe
        dark_gray = "#424242"    # Dark gray for subframe
        white = "#FFFFFF"        # White for text and buttons

        self.mainframe = tk.CTkFrame(self, fg_color="#D6D6D6", height=height, width=width)
        self.mainframe.place(relx=0.5, rely=0.5, anchor="center")
        
        img1=ImageTk.PhotoImage(Image.open("./img/pattern.png"))
        self.l1=tk.CTkLabel(self.mainframe,image=img1)
        self.l1.place(relwidth=1.0,relheight=1.0)

        self.subframe = tk.CTkFrame(self.l1, height=450, width=900,fg_color="#055C9D",bg_color="#055C9D")
        self.subframe.place(relx=0.5, rely=0.5, anchor="center")


        img2=ImageTk.PhotoImage(Image.open("./img/loginlogob.png").resize([400,150])) # verishield logo
        self.l2=tk.CTkLabel(self.subframe,image=img2,width=50,text="",bg_color="#68BBE3",fg_color="#68BBE3")
        self.l2.place(relheight=1.0,x=0,y=0)



        # Create labels
        self.headinglabel = tk.CTkLabel(self.subframe, text="Login Screen", text_color="white", height=20, width=80, font=("yu gothic ui semibold", 20),)
        self.label1 = tk.CTkLabel(self.subframe, text="Enter Username", text_color=dark_gray, height=20, width=80)
        self.label2 = tk.CTkLabel(self.subframe, text="Enter Password", text_color=dark_gray, height=20, width=80)

        # Create entry widgets
        self.entryusername = tk.CTkEntry(self.subframe, corner_radius=13, width=280, height=30, placeholder_text="Enter Username",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color="#055C9D", font=("yu gothic ui semibold", 12))
        self.entrypassword = tk.CTkEntry(self.subframe, corner_radius=13, width=280, height=30, placeholder_text="Enter Password",show="*",border_width=0,fg_color="white",placeholder_text_color="#4C4C4C",bg_color="#055C9D", font=("yu gothic ui semibold", 12))
        
        self.imgshow=ImageTk.PhotoImage(Image.open("./images/showp.png").resize([18,15]))
        
        self.imghide=ImageTk.PhotoImage(Image.open("./images/hidep.png").resize([18,15]))

        self.showpassword=tk.CTkButton(self.subframe,text="",command=self.toggle_passwordshow,border_width=0,fg_color="white",image=self.imgshow,width=10,height=10,corner_radius=10)
        

        # Create buttons
        self.Loginbtn = tk.CTkButton(self.subframe, text="Login", command=self.onlogin, corner_radius=20, fg_color="#FF9800", width=120, height=30, font=("yu gothic ui semibold", 12),hover_color="#ae6800")
        self.Forgetbtn = tk.CTkButton(self.subframe, text="Forget Password", corner_radius=20, fg_color="#FF9800", width=120, height=30, font=("yu gothic ui semibold", 12),hover_color="#ae6800")

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
