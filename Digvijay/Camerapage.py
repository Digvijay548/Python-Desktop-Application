import os
from pypylon import pylon
import customtkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import cv2
import pylibdmtx.pylibdmtx as dmtx



class camerapage(tk.CTkFrame):
    def __init__(self, master,heights,widths):
        self.i = 0
        tk.CTkFrame.__init__(self, master,heights,widths)
       # hv.init_halcon()
        self.master = master
        self.cameras = []  # List to store available cameras
        self.update_camera_list()

        #******************** MainScreen ***************

        self.mainscreen = tk.CTkFrame(self, fg_color="#E0E0E0", width=widths,height=heights)
        self.mainscreen.pack()         


        #******************** CenterScreen =>MainScreen ***************

        self.centerframe = tk.CTkFrame(self.mainscreen,fg_color="#E0E0E0", height=550, width=self.mainscreen._current_width-20)
        self.centerframe.place(x=20, y=0)


        #******************** CameraFrames =>CenterScreen ***************

        self.camera_label = tk.CTkLabel(self.centerframe,text="",fg_color="#000000", width=self.centerframe._current_width/2, height=self.centerframe._current_height)
        self.camera_label.place(x=0,y=0)        

        self.camera_label2 = tk.CTkLabel(self.centerframe,text="", fg_color="white", height=self.centerframe._current_height, width=self.centerframe._current_width/2)
        self.camera_label2.place(x=self.camera_label._current_width-20,y=0)



        #********************StartGrabing Stop Grabbing buttons => MainScreen ***************

        self.btnframe = tk.CTkFrame(self.mainscreen, width=self.mainscreen._current_width-300, height=40, fg_color="#E0E0E0")
        self.btnframe.place(y=570, x=300)

        self.button1 = tk.CTkButton(self.btnframe, text="Start grabbing", command=self.start_grabbing, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.button1.place(y=2, x=90)   
        self.button2 = tk.CTkButton(self.btnframe, text="Stop Grabbing", command=self.stop_grabbing, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.button2.place(y=2, x=280)
        self.Countbarcodetxt = tk.CTkLabel(self.btnframe,text="No of Barcode found:", width=60, height=30)
        self.Countbarcodetxt.place(y=2, x=440)
        self.Countbarcode = tk.CTkLabel(self.btnframe, width=50, height=30,text="0")
        self.Countbarcode.place(y=2, x=610)



        #********************Setting Camera like expos gain buttons => MainScreen ***************

        self.settingframe = tk.CTkFrame(self.mainscreen,width=1050, height=200, fg_color="#E0E0E0", border_color="black")
        self.settingframe.place(y=620, x=80)

        self.Seriallabel = tk.CTkLabel(self.settingframe, text_color="black", text="Serial Number", height=20, width=80)
        self.Seriallabel.place(x=70, y=10)

        self.Serialcombobox = tk.CTkComboBox(self.settingframe, corner_radius=5, fg_color="#FFFFFF", values=self.cameras, width=180, height=30)
        self.Serialcombobox.place(x=170, y=10)
        self.Serialcombobox.bind("<<ComboboxSelected>>", self.on_serial_selection)

        self.entryExposure = tk.CTkEntry(self.settingframe, corner_radius=20, fg_color="#FFFFFF", width=150, height=30, placeholder_text="Enter Exposure")
        self.entryExposure.place(x=440, y=10)

        self.entryGain = tk.CTkEntry(self.settingframe, corner_radius=20, fg_color="#FFFFFF", width=150, height=30, placeholder_text="Enter Gain")
        self.entryGain.place(x=680, y=10)

        self.savecambtn = tk.CTkButton(self.settingframe, text="Save", command=self.set_camera, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.savecambtn.place(x=370, y=80)
        
        self.resetcambtn = tk.CTkButton(self.settingframe, text="Reset", command=self.reset_cam_settings, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.resetcambtn.place(x=580, y=80)

        self.capture = None
        self.camera = None
        self.initicapure = True
        self.valuesstartgrab=False

    def update_camera_list(self):
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            self.cameras = [device.GetSerialNumber() for device in devices]
            print(self.cameras)
        except Exception as e:
            print(f"Error updating camera list: {e}")

    def start_grabbing(self):        
        try:
            self.update_camera_list()
            if self.cameras and self.camera is None:


                tl_factory = pylon.TlFactory.GetInstance()
                devices = tl_factory.EnumerateDevices()
                for device in devices:
                 if device.GetSerialNumber()==self.Serialcombobox.get() :
                  self.camera =pylon.InstantCamera(tl_factory.CreateDevice(device))



                if self.camera.IsOpen():
                    self.camera.Close()
                    self.camera=None
                self.camera.Open()
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, pylon.GrabLoop_ProvidedByUser)
                self.show_frame()
                #self.camera.Close()
            else:
                self.camera.Open()
                self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, pylon.GrabLoop_ProvidedByUser)
                self.show_frame()
               
        except Exception as e:
            print(f"Error: {e}")


    
    def show_frame(self):
      try:
        self.i = 0
        while self.camera.IsGrabbing():
            for i in range(self.i, 1):
                grab_result = self.camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)
                if grab_result.GrabSucceeded():
                    self.i = self.i + 1
                    converter = pylon.ImageFormatConverter()
                    converter.OutputPixelFormat = pylon.PixelType_BGR8packed  
                    converted_image = converter.Convert(grab_result)
                    self.image_data = converted_image.GetArray()
                    self.CameraCapuredImg = cv2.cvtColor(self.image_data, cv2.COLOR_RGB2GRAY)
                    self.decode_datamatrix()   
                    # Convert the image to RGB format
                    rgb_img = cv2.cvtColor(self.flipped_image, cv2.COLOR_BGR2RGB)
                    self.pil_img = Image.fromarray(rgb_img)
                    self.pil_img = self.pil_img.resize((self.camera_label.winfo_width(), self.camera_label.winfo_height()))            
                    img_tk = ImageTk.PhotoImage(self.pil_img)
                    self.camera_label.configure(image=img_tk)            
                    # Save the image
                    folder_path = "D:/ImgFromPython"
                    file_name = f"captured_image{self.i}.jpg"
                    file_path = os.path.join(folder_path, file_name)
                    self.pil_img.save(file_path)
                    print(f"Image saved to: {file_path}")
                    grab_result.Release()                    
                else:
                    print("Error: Image grab failed.")
            self.camera.StopGrabbing()
            self.continius=self.after(10,self.start_grabbing) 
      except Exception as e:
        print(f"Error: {e}")

    def draw_rectangles(self):
      offset = -60
      self.flipped_image = cv2.flip(self.image_data, 0)
      print("Decoded obj==" + str(self.decoded_objects))
      for obj in self.decoded_objects:
        left = obj.rect.left
        top = obj.rect.top
        width = obj.rect.width
        height = obj.rect.height
        rect_points = obj.rect

        right = left + width
        bottom = top + height 
        rect_points = obj.rect
        
        
        cv2.circle(self.flipped_image,(right,top),4,(0,0,255),10)
        cv2.circle(self.flipped_image,(right,bottom),4,(255,0,255),10)
        cv2.rectangle(self.flipped_image, (right, bottom), (left, top), (0, 255, 0), 3)
        # cv2.rectangle(self.image_data, (left, (top+offset)), (left + width, top + height+offset), (0, 255, 0), 3)

        # Draw the decoded value at the bottom of the rectangle
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1
        font_thickness = 2
        # Example string
        data_string = obj.data.decode('utf-8')
        
        
        # Split the string into two parts using slicing
        first_part = data_string[18:37]        
        print("First Part:", first_part)
        text_size = cv2.getTextSize(first_part, font, font_scale, font_thickness)[0]
        text_width, text_height = text_size[0], text_size[1]
        text_x = rect_points[0] + (rect_points[2] - text_width) // 2
        text_y = rect_points[1] + rect_points[3] + text_height + 5
        cv2.putText(self.flipped_image, first_part, (text_x, text_y), font, font_scale, (0, 255, 0), font_thickness, cv2.LINE_AA)

    def decode_datamatrix(self):
     img_pils = Image.fromarray(self.image_data)
    #  self.decoded_objects = dmtx.decode(img_pils, timeout=300)
    #  num = 0
    #  for obj in self.decoded_objects:
    #      num += 1
    #      print("DataMatrix code:", obj.data.decode('utf-8'))
    #  self.draw_rectangles()
    #  self.Countbarcode.configure(text=str(num))




     # Convert PIL image to Halcon image halcon decoding
     halcon_image = hv.image_from_pil(img_pils)
 
     # Find DataMatrix codes in the image
     self.decoded_objects = hv.find_data_code_2d(halcon_image, 'datamatrix_ecc_200')
 
     # Decode DataMatrix codes
     num = 0
     for code in self.decoded_objects:
         num += 1
         decoded_string = hv.decode_data_code_2d(code, 'decoded_data')
         print("Decoded DataMatrix using halcon:", decoded_string)
     self.draw_rectangles()
     self.Countbarcode.configure(text=str(num))


    def stop_grabbing(self):
        try:
            if self.continius is not None:
              self.after_cancel(self.continius)
              self.continius = None
            print("Camera closed from Stop Capture" + str(self.camera.IsOpen()))
            if self.camera.IsOpen():
                self.camera.StopGrabbing()
                self.camera.Close()
                self.camera = None
                print("Camera closed")
        except Exception as e:
            print(f"Error: {e}")

    def on_serial_selection(self, eventObject):
        selected_serial = eventObject.widget.get()  # Get the selected serial number
        print(f"Selected serial: {selected_serial}")

        # Set the camera based on the selected serial
        self.start_grabbing()

    def set_camera(self):
        try:
            if self.camera and self.camera.IsOpen():
                self.camera.StopGrabbing()
                self.camera.Close()

            # Find the camera with the selected serial number
            for device in pylon.TlFactory.GetInstance().EnumerateDevices():
                if device.GetSerialNumber() == self.Serialcombobox.get():
                    self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device))
                    self.camera.Open()

                    # Set exposure and gain values for the camera
                    self.set_exposure_and_gain()

                    # Start grabbing
                    self.camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly, pylon.GrabLoop_ProvidedByUser)
                    self.show_frame()
                    break

        except Exception as e:
            print(f"Error setting camera: {e}")



    def reset_cam_settings(self):
        try:
            if self.camera and self.camera.IsOpen():
                self.camera.StopGrabbing()
                self.camera.Close()

            # Find the camera with the selected serial number
            for device in pylon.TlFactory.GetInstance().EnumerateDevices():
                if device.GetSerialNumber() == self.Serialcombobox.get():
                    self.camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device))
                    self.camera.Open()

                # Reset exposure and gain settings to default values
                self.camera.ExposureTime.SetValue(self.camera.ExposureTime.GetMin())
                self.camera.Gain.SetValue(self.camera.Gain.GetMin())
                print("Gain value reset")
    
                # Update the GUI to display default values
                self.entryExposure.delete(0, 'end')
                self.entryExposure.insert(0, str(self.camera.ExposureTime.GetValue()))
                print("Exposure value reset")
    
                self.entryGain.delete(0, 'end')
                self.entryGain.insert(0, str(self.camera.Gain.GetValue()))
    
        except Exception as e:
            print(f"Error resetting camera settings: {e}")

    
    def set_exposure_and_gain(self):
        try:
            exposure_value = float(self.entryExposure.get())
            gain_value = float(self.entryGain.get())

            # Set exposure time          
            self.camera.ExposureTime.SetValue(exposure_value)

            # Set gain value            
            self.camera.Gain.SetValue(gain_value)
            print("setting saved for exposure and gain values")

        except Exception as e:
            print(f"Error setting exposure and gain values: {e}")
