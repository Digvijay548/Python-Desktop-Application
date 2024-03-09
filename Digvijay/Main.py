import customtkinter as tk
from main_page import MainPage
from stackpanelpage import Stackpanelpage
from Scannerpage import FirstPage
from Printerpage import SecondPage
from Camerapage import camerapage
from PIL import Image, ImageTk
from datetime import datetime

class SampleApp(tk.CTk):
    def __init__(self):
        tk.CTk.__init__(self, fg_color="blue")
        self.title("Track And Trace Project")
        self.overrideredirect(True)   # this is for hiding the windows close button on mainwindow

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the x and y coordinates to center the window
        x_coordinate = int((screen_width - 1100) / 2)
        y_coordinate = int((screen_height - 950) / 2)

        # Set the main window position
        self.geometry(f"{screen_width}x{screen_height}+{0}+{0}")





        #*********************************** This is Header section *******************************

        self.header=tk.CTkFrame(self,height=50,width=screen_width,bg_color="#372b47",fg_color="#372b47")
        self.header.place(x=0,y=0)

        #*********************************** This is Acglog on header *******************************
        
        self.LogoFrame=tk.CTkFrame(self.header,height=50,width=200,fg_color="#372b47")
        self.LogoFrame.place(x=0,y=0)
        logo=ImageTk.PhotoImage(Image.open("./images/acglogo.png").resize([170,60]))
        self.Logowidget=tk.CTkLabel(self.LogoFrame,image=logo,text="",height=50)
        self.Logowidget.place(x=0,y=0)

        #*********************************** This is timmer/clock *******************************
        
        self.timingframe=tk.CTkFrame(self.header,height=50,width=140,fg_color="#372b47")
        self.timingframe.place(x=screen_width-130,y=0)
        clock=ImageTk.PhotoImage(Image.open("./images/clock.png").resize([50,50]))
        self.Clockwidget=tk.CTkLabel(self.timingframe,image=clock,height=50,width=50,text="")
        self.Clockwidget.place(x=0,y=0)
        self.time_label=tk.CTkLabel(self.timingframe,height=50,width=50,text_color="white",font=("yu gothic ui semibold", 14))
        self.time_label.place(x=60,y=0)

        

        #*********************************** This is footer section *******************************

        self.footer=tk.CTkFrame(self,height=50,width=screen_width,bg_color="black",fg_color="black")
        self.footer.place(x=0,y=screen_height-50)



        #*********************************** This is Main body section *******************************
        

        self.body=tk.CTkFrame(self,height=screen_height-100,width=screen_width,bg_color="red",fg_color="red")
        self.body.place(y=50,x=0)

        self.stackpanel_page = Stackpanelpage(master=self.body,height=self.body._current_height, width=self.body._current_width, show_main_page_callback=self.show_main_page)
        
        self.update_time()
        self.show_main_page()



    def update_time(self):
        current_time = datetime.now().strftime('%H:%M:%S')
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)  # Update every second

        
    def show_main_page(self):
        self. main_page = MainPage(master=self.body, height=self.body._current_height+2, width=self.body._current_width, show_stackpanel_page_callback=self.show_stackpanel_page)
        self.main_page.place(x=0,y=0)
        if(self.stackpanel_page.winfo_ismapped):
         self.stackpanel_page.place_forget()

    def show_stackpanel_page(self):
        if(self.main_page.winfo_ismapped):
         self.main_page.place_forget()
        self.stackpanel_page = Stackpanelpage(master=self.body,height=self.body._current_height, width=self.body._current_width, show_main_page_callback=self.show_main_page)
        self.stackpanel_page.place(x=0,y=0)


if __name__ == "__main__":
    tk.set_appearance_mode("Light")
    app = SampleApp()
    app.resizable(False, False)  # Set resizable to True for both x and y directions
    app.mainloop()
