import customtkinter as tk
from main_page import MainPage
from stackpanelpage import Stackpanelpage
from Scannerpage import FirstPage
from Printerpage import SecondPage
from Camerapage import camerapage
from PIL import Image, ImageTk
from datetime import datetime
import signal
import sys
from tkinter import Menu
from CTkMessagebox import CTkMessagebox

class LoadingWindow(tk.CTk):
    def __init__(self):
        tk.CTk.__init__(self, fg_color="blue")
        
        self.geometry("450x300")
        self.overrideredirect(True)

        # Get the screen width and height
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position of the window
        x = (screen_width - self.winfo_reqwidth()) // 2
        y = (screen_height - self.winfo_reqheight()) // 2

        # Set the window position
        self.geometry("+{}+{}".format(x, y))
        self.title("Loading...")
        self.attributes("-topmost", True)  # Keep the loading window on top
        self.continius2=self.after(5000, self.close_window)  # Close the window after 5 seconds

        # Load the GIF frames using Pillow
        self.frames = []
        self.load_frames()

        # Create a label to display the GIF
        self.label = tk.CTkLabel(self,text="",height=self._current_height,width=self._current_width)
        self.label.pack()

        # Display the GIF frames
        self.display_frame(0)

    def load_frames(self):
        # Load the GIF frames using Pillow
        try:
            gif = Image.open("./img/loading2.gif")
            while True:
                frame = gif.copy()
                self.frames.append(ImageTk.PhotoImage(frame))
                gif.seek(gif.tell() + 1)
        except EOFError:
            pass

    def display_frame(self, index):
         self.label.configure(image=self.frames[index])
         self.continius=self.after(30, lambda: self.display_frame((index + 1) % len(self.frames)))



    def close_window(self):
        self.after_cancel(self.continius2)
        self.after_cancel(self.continius)
        self.destroy()
        start_main_application()






def start_main_application():
    app = SampleApp()
    app._set_appearance_mode("Light")
    app.resizable(False, False)  
    app.deiconify()
    app.mainloop()       

         



class SampleApp(tk.CTk):
    def __init__(self):
        tk.CTk.__init__(self, fg_color="#372b47")
        self.title("Track And Trace Project")
        self.overrideredirect(True) 

        
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
        self.logo=ImageTk.PhotoImage(Image.open("./images/acglogo.png").resize([170,60]))
        self.Logowidget=tk.CTkLabel(self.LogoFrame,image= self.logo,text="",height=50)
        self.Logowidget.place(x=0,y=0)

        

        #*********************************** This is footer section *******************************

        self.footer=tk.CTkFrame(self,height=50,width=screen_width,bg_color="black",fg_color="#372b47")
        self.footer.place(x=0,y=screen_height-50)

        # Create a button        
        self.off=ImageTk.PhotoImage(Image.open("./img/off.png").resize([50,50]))
        self.shutdown_button = tk.CTkButton(self.footer, text="",image=self.off,height=40,width=40,corner_radius=5,fg_color="#372b47",bg_color="transparent")
        self.shutdown_button.place(x=0,y=0)

        # Create a menu
        self.menu = Menu(self.master, tearoff=0,font=("Helvetica", 12))
        self.menu.add_command(label="Shutdown", command=self.shutdown)
        self.menu.add_command(label="Restart", command=self.restart)

        # Bind menu to the button
        self.shutdown_button.bind("<Enter>", self.show_menu)
        self.shutdown_button.bind("<Leave>", self.hide_menu)

        

        #*********************************** This is timmer/clock *******************************
        
        self.timingframe=tk.CTkFrame(self.footer,height=50,width=140,fg_color="#372b47")
        self.timingframe.place(x=screen_width-130,y=0)
        clock=ImageTk.PhotoImage(Image.open("./images/clock.png").resize([50,50]))
        self.Clockwidget=tk.CTkLabel(self.timingframe,image=clock,height=50,width=50,text="")
        self.Clockwidget.place(x=0,y=0)
        self.time_label=tk.CTkLabel(self.timingframe,height=50,width=50,text_color="white",font=("yu gothic ui semibold", 14))
        self.time_label.place(x=60,y=0)


        #*********************************** This is Main body section *******************************
        

        self.body=tk.CTkFrame(self,height=screen_height-100,width=screen_width,bg_color="#372b47",fg_color="#372b47")
        self.body.place(y=50,x=0)

        self.stackpanel_page = Stackpanelpage(master=self.body,height=self.body._current_height, width=self.body._current_width, show_main_page_callback=self.show_main_page)
        
        self.update_time()
        self.show_main_page()



    def show_menu(self, event):
     # Calculate the position of the menu
     x = self.footer.winfo_rootx() + self.shutdown_button.winfo_x()
     y = self.footer.winfo_rooty() + self.shutdown_button.winfo_y() + self.shutdown_button.winfo_height()
     # Display the menu
     self.menu.post(x, y)

    def hide_menu(self, event):
        self.menu.unpost()

    def shutdown(self):
        print("Shutdown initiated")
         # get yes/no answers
        msg = CTkMessagebox(self,title="Exit?", message="Do you want to Shutdown the program?",
                            icon="warning", option_1="Cancel", option_2="No", option_3="Yes")
        response = msg.get()
        print(response)
        
        if response=="Yes":
         self.destroy()                
        else:
            print("Click 'Yes' to exit!")

    def restart(self):
        print("Restart initiated")
        # You can put your restart logic here



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
    def signal_handler(sig, frame):
        print("Ctrl+C detected. Exiting gracefully...")
        sys.exit(0)

    # Register the signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    loading_window = LoadingWindow()
    loading_window.mainloop()