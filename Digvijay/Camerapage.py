import os
from pypylon import pylon
import customtkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk,ImageEnhance,ImageOps
import cv2
import pylibdmtx.pylibdmtx as dmtx
import threading
import clr
from dbr import *
import numpy as np
import concurrent.futures
from ultralytics import YOLO
import time
import zxingcpp


class camerapage(tk.CTkFrame):
    def __init__(self, master,heights,widths):
        self.i = 0
        tk.CTkFrame.__init__(self, master,heights,widths)

        # 2.Create an instance of Barcode Reader.
        
        self.model = YOLO("Modified.pt")




       # hv.init_halcon()
        self.master = master
        self.cameras = []  # List to store available cameras
        self.update_camera_list()
        self.stop_flag=True
        #******************** MainScreen ***************

        self.mainscreen = tk.CTkFrame(self, fg_color="#68BBE3", width=widths,height=heights)
        self.mainscreen.pack()         


        #******************** CenterScreen =>MainScreen ***************

        self.centerframe = tk.CTkFrame(self.mainscreen,fg_color="#68BBE3", height=550, width=self.mainscreen._current_width-20)
        self.centerframe.place(x=0, y=0)


        #******************** CameraFrames =>CenterScreen ***************

        self.camera_label = tk.CTkLabel(self.centerframe,text="",fg_color="#000000", width=self.centerframe._current_width/2, height=self.centerframe._current_height)
        self.camera_label.place(x=0,y=0)        

        self.camera_label2 = tk.CTkLabel(self.centerframe,text="", fg_color="#055C9D", height=self.centerframe._current_height, width=self.centerframe._current_width/2)
        self.camera_label2.place(x=self.camera_label._current_width,y=0)



        #********************StartGrabing Stop Grabbing buttons => MainScreen ***************

        self.btnframe = tk.CTkFrame(self.mainscreen, width=self.mainscreen._current_width-300, height=40, fg_color="#68BBE3")
        self.btnframe.place(y=570, x=100)

        self.button1 = tk.CTkButton(self.btnframe, text="Start grabbing", command=self.start_capturetread, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.button1.place(y=2, x=90)   
        self.button2 = tk.CTkButton(self.btnframe, text="Stop Grabbing", command=self.stop_capture, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.button2.place(y=2, x=280)
        self.Countbarcodetxt = tk.CTkLabel(self.btnframe,text="No of Barcode found:", width=60, height=30,text_color="white")
        self.Countbarcodetxt.place(y=2, x=440)
        self.Countbarcode = tk.CTkLabel(self.btnframe, width=50, height=30,text="0",text_color="white")
        self.Countbarcode.place(y=2, x=610)



        #********************Setting Camera like expos gain buttons => MainScreen ***************

        self.settingframe = tk.CTkFrame(self.mainscreen,width=self.mainscreen._current_width, height=200, fg_color="#68BBE3", border_color="black")
        self.settingframe.place(y=620, x=400)

        self.Seriallabel = tk.CTkLabel(self.settingframe, text_color="white", text="Serial Number", height=20, width=80)
        self.Seriallabel.place(x=70, y=10)

        self.Serialcombobox = tk.CTkComboBox(self.settingframe, corner_radius=5,bg_color="#68BBE3", values=self.cameras, width=180, height=30)
        self.Serialcombobox.place(x=170, y=10)
        self.Serialcombobox.bind("<<ComboboxSelected>>", self.on_serial_selection)

        self.entryExposure = tk.CTkEntry(self.settingframe, corner_radius=20, fg_color="white",bg_color="#68BBE3" ,width=150, height=30, placeholder_text="Enter Exposure")
        self.entryExposure.place(x=440, y=10)

        self.entryGain = tk.CTkEntry(self.settingframe, corner_radius=20, fg_color="white",bg_color="#68BBE3", width=150, height=30, placeholder_text="Enter Gain")
        self.entryGain.place(x=680, y=10)

        self.savecambtn = tk.CTkButton(self.settingframe, text="Save", command=self.set_camera, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.savecambtn.place(x=370, y=80)
        
        self.resetcambtn = tk.CTkButton(self.settingframe, text="Reset", command=self.reset_cam_settings, corner_radius=20, fg_color="#FF9800", width=120, height=30,hover_color="#ae6800")
        self.resetcambtn.place(x=580, y=80)

        self.capture_running = False
        self.camera2=None

    def update_camera_list(self):
        try:
            devices = pylon.TlFactory.GetInstance().EnumerateDevices()
            self.cameras = [device.GetSerialNumber() for device in devices]
            print(self.cameras)
        except Exception as e:
            print(f"Error updating camera list: {e}")


    def on_serial_selection(self, eventObject):
        selected_serial = eventObject.widget.get()  # Get the selected serial number
        print(f"Selected serial: {selected_serial}")
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
                    break

        except Exception as e:
            print(f"Error setting camera: {e}")

    def DecodeDatamatrix(self):
        self.decoded_objects.clear()
        img = Image.fromarray(self.image) 
        # Define your parameters
        image = ...  # Image object or path to image file
        formats = ...  # Barcode formats to search for
        try_rotate = ...  # Whether to try rotating the image
        try_downscale = ...  # Whether to try downscaling the image
        text_mode = ...  # Text mode for decoding
        binarizer = ...  # Binarizer for image processing
        is_pure = ...  # Whether to use pure Python implementation
        ean_add_on_symbol = ...  # EAN add-on symbol handling
        return_errors = ...  # Whether to return errors
        max_number_of_symbols = 100  # Example value within the range of uint8_t
        

        self.third_thread_complete2 = threading.Event()
       
        def ThirdDecodeDatamatrix2():  
            i=1
            
            results = self.model(img)
            start_time = time.time()
            for r in results:
                boxes = r.boxes
                for box in boxes:
                    x1, y1, x2, y2 = box.xyxy[0]
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    width, height = img.size
                    # Extend the bounding box
                    extension = 15  # Adjust the extension value as needed
                    x1 = max(0, x1 - extension)
                    y1 = max(0, y1 - extension)                    
                    x2 = min(width, x2 + extension)
                    y2 = min(height, y2 + extension)                    
                    region = img.crop((x1, y1, x2, y2))
                    try:
                     array=np.array(region)
                     decoded_objects = zxingcpp.read_barcodes(array)                         
                     if(decoded_objects):
                      for objects in decoded_objects:
                        print(f'\n "{str(i)}"from pyzxing )=> Text :"{objects.text}"')
                      self.decoded_objects.append(decoded_objects)
                      cv2.rectangle(self.image_data, (x1, y1), (x2, y2), (0, 255, 0), 3)
                     else:
                        decoded_objects = zxingcpp.read_barcodes(array) 
                        if(decoded_objects):
                         for objects in decoded_objects:
                           print(f'\n "{str(i)}"from pyzxing )=> Text :"{objects.text}"')
                         self.decoded_objects.append(decoded_objects)
                         cv2.rectangle(self.image_data, (x1, y1), (x2, y2), (0, 255, 0), 3)  
                        else:
                           decoded_objects =dmtx.decode(region,max_count=1,corrections=10,timeout=60)
                           if(decoded_objects):
                              self.decoded_objects.append(decoded_objects)
                              cv2.rectangle(self.image_data, (x1, y1), (x2, y2), (0, 255, 0), 3)
                    except Exception  as e : 
                      print(str(e)) 
                    i=i+1
             
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000 
            print("Time taken for decoding:", elapsed_time, "seconds")
            image_rgb = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
            image_pils = Image.fromarray(image_rgb) 
            image_pil = image_pils.resize([int(self.camera_label._current_width),int(self.camera_label._current_height)]) 
            img_tk = ImageTk.PhotoImage(image_pil)
            self.camera_label.configure(image=img_tk)                         
            if(self.decoded_objects.__len__()>0):
               self.Countbarcode.configure(text=str(len(self.decoded_objects)))          
            self.third_thread_complete2.set()
        
        
        thread32 = threading.Thread(target=ThirdDecodeDatamatrix2)
        thread32.start()
        
        def check_completion_and_proceed():        
         self.third_thread_complete2.wait()

        check_completion_and_proceed() 

    def capture_image(self, camera, label,heights,widths):
         while self.capture_running:
            try :                 
                 # Grab a single frame from the camera
                 camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                 grabResult = camera.RetrieveResult(200, pylon.TimeoutHandling_ThrowException)
                 grabResult2 = camera.RetrieveResult(5000, pylon.TimeoutHandling_ThrowException)
                 camera.StopGrabbing()
                 converter = pylon.ImageFormatConverter()
                 converter.OutputPixelFormat = pylon.PixelType_BGR8packed  
                 self.converted_image = converter.Convert(grabResult)
                 self.converted_image2 = converter.Convert(grabResult2)
                 self.image_data = self.converted_image.GetArray()

                 self.image = cv2.cvtColor(self.image_data, cv2.COLOR_RGB2GRAY)
                 self.images = cv2.cvtColor(self.image_data, cv2.COLOR_BGR2RGB)
                 self.img_pils = Image.fromarray(self.image)                
                 grabResult.Release() 
                 self.decoded_objects=[]
                 thread = threading.Thread(target=self.DecodeDatamatrix)
                 thread.run()

            except Exception as e:  
              print(f"Error: {e}")   

         # Close the camera
         camera.Close()

    def start_capturetread(self):               
        self.thread = threading.Thread(target=self.start_capture) 
        self.thread.start()

    def start_capture(self):
         self.capture_running = True
         # Create camera objects
         self.update_camera_list()
         print("Number of cameras found"+str(len(self.cameras)))  

         if(len(self.cameras)>1):
          print("Number of cameras found"+str(len(self.cameras)))
          self.camera1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(self.cameras[0]))
          self.camera2 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(self.cameras[1]))
         elif len(self.cameras) == 1:
            self.camera1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
         else:
           print("No cameras found")
           return

         # Create a thread pool executor
         with concurrent.futures.ThreadPoolExecutor() as executor:
            if(len(self.cameras)>1):
             print("entered in :-concurrent.futures.ThreadPoolExecutor")
             # Submit each camera's capturing task to the executor
             future1 = executor.submit(self.capture_image, self.camera1, self.camera_label,int(self.centerframe._current_height),int(self.centerframe._current_width/2))
             future2 = executor.submit(self.capture_image, self.camera2, self.camera_label2,int(self.centerframe._current_height),int(self.centerframe._current_width/2))
            else:
             future1 = executor.submit(self.capture_image, self.camera1, self.camera_label,int(self.centerframe._current_height),int(self.centerframe._current_width/2) )
         
    def stop_capture(self):
        self.capture_running = False  

    def reset_cam_settings(self):
        pass

    def set_camera(self):
        pass

