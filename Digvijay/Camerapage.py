import os
from pypylon import pylon
import customtkinter as tk
from tkinter import *
from PIL import Image, ImageTk,ImageEnhance,ImageOps
import cv2
import tkinter as ttk
import pylibdmtx.pylibdmtx as dmtx
import threading
import clr
from dbr import *
import numpy as np
import concurrent.futures
from ultralytics import YOLO
import time
import zxingcpp
from CTkMessagebox import CTkMessagebox
from sqlclass import sqlconnect
import re
import pygame
from custom_hovertip import CustomTooltipLabel
from datetime import datetime
from CameraCanvas import ImageZoom
import pyzbar.pyzbar as py

class camerapage(tk.CTkFrame):
    def __init__(self, master,heights,widths):
        self.i = 0
        tk.CTkFrame.__init__(self, master,heights,widths)
        self.sql_conn = sqlconnect()
        self.sql_conn.GetallData()
        pygame.init()
        mp3_file = "./beep.mp3"
        self.dark_gray = "#0b2545" 
        self.btncolor="#637081"
        self.lightgray="#8da9c4"  
        self.textcolor="#0b2545"
        self.bthover="#accbe1"
        pygame.mixer.music.load(mp3_file)
        # 2.Create an instance of Barcode Reader.
        
        self.model = YOLO("modifiedwith1d.pt")
        self.model2 = YOLO("modifiedwith1d.pt")
        self.master = master
        self.cameras = []  # List to store available cameras
        self.update_camera_list()
        self.stop_flag=True
        #******************** MainScreen ***************

        self.mainscreen = tk.CTkFrame(self, fg_color=self.lightgray , width=widths,height=heights)
        self.mainscreen.pack()         


        #******************** CenterScreen =>MainScreen ***************

        self.centerframe = tk.CTkFrame(self.mainscreen,fg_color="black", height=550, width=self.mainscreen._current_width-20)
        self.centerframe.place(x=0, y=0)
        print(f"centerframe width = > {self.centerframe._current_width}")

        
        #******************** CameraFrames =>CenterScreen ***************
        half_width = int(self.centerframe._current_width / 2)+60



        self.camera1frame = tk.CTkFrame(self.centerframe, width=int(self.centerframe._current_width/2), height=550, fg_color="black",border_width=0)
        self.camera1frame.place(x=0, y=0)        
        self.camera_label = ImageZoom(parent=self.camera1frame,height=550,width=int(self.camera1frame._current_width),position=tk.NE)


        
        # Adjusted width here to account for scrollbar
        self.camera2frame = tk.CTkFrame(self.centerframe, width=int(self.centerframe._current_width/2)-20, height=550,fg_color="black",border_width=0)
        self.camera2frame.place(x=int(self.centerframe._current_width/2)-10,y=0)        
        self.camera_label2 = ImageZoom(parent=self.camera2frame,height=550,width=int(self.camera2frame._current_width),position=tk.NW)


        #********************StartGrabing Stop Grabbing buttons => MainScreen ***************

        self.btnframe = tk.CTkFrame(self.mainscreen, width=self.mainscreen._current_width-50, height=40, fg_color=self.lightgray)
        self.btnframe.place(x=0,y=570)

        self.flipcamera1=False
        self.flipcamera2=False
        img2=ImageTk.PhotoImage(Image.open("./images/rotate.png").resize((20,20))) # flip caera horizontal logo
        self.l2=tk.CTkButton(self.btnframe,image=img2,width=20,height=20,text="",bg_color=self.lightgray ,fg_color="gray",command=self.flipcameratopbottom )
        self.l2.place(x=0,y=2)

        self.fliptxt=tk.CTkLabel(self.btnframe,text="Flip T to B",bg_color=self.lightgray,text_color=self.dark_gray,)
        self.fliptxt.place(x=50,y=0)

        self.button1 = tk.CTkButton(self.btnframe, text="Start grabbing", command=self.start_capturetread, corner_radius=20, fg_color= self.btncolor,text_color=self.textcolor, width=120, height=30,hover_color=self.bthover)
        self.button1.place(y=2, x=140)   
        self.button2 = tk.CTkButton(self.btnframe, text="Stop Grabbing", command=self.stop_capture,text_color=self.textcolor, corner_radius=20, fg_color= self.btncolor, width=120, height=30,hover_color=self.bthover)
        self.button2.place(y=2, x=350)
        self.Countbarcodetxt = tk.CTkLabel(self.btnframe,text="No of Barcode found:", width=60, height=30,text_color=self.textcolor,)
        self.Countbarcodetxt.place(y=2, x=490)
        self.Countbarcode = tk.CTkLabel(self.btnframe, width=50, height=30,text="0",text_color=self.textcolor,)
        self.Countbarcode.place(y=2, x=650)

        self.decodemultiple=tk.CTkCheckBox(self.btnframe,text="Decode multiple format",bg_color=self.lightgray,checkmark_color=self.lightgray,command=self.decodeall)
        self.decodemultiple.place(x=750,y=0)

        self.rotatecamera1=90
        self.rotatecamera2=90
        img2=ImageTk.PhotoImage(Image.open("./images/rotate.png").resize((20,20))) # rotate  logo
        self.l2=tk.CTkButton(self.btnframe,image=img2,width=20,height=20,text="",bg_color=self.lightgray ,fg_color="white",command=self.rotatecamera )
        self.l2.place(x=950,y=2)

        self.rotatetxt=tk.CTkLabel(self.btnframe,text="Rotate Camera",bg_color=self.lightgray,text_color=self.dark_gray,)
        self.rotatetxt.place(x=1000,y=0)


        self.flipcameraleftrightval1=False
        self.flipcameraleftrightval2=False

        img3=ImageTk.PhotoImage(Image.open("./images/rotate.png").resize((20,20))) # Flip left to right  logo
        self.flipcameraleftrightbtn=tk.CTkButton(self.btnframe,image=img3,width=20,height=20,text="",bg_color=self.lightgray ,fg_color="white",command=self.flipcameraleftright )
        self.flipcameraleftrightbtn.place(x=1190,y=2)

        self.flipcameraleftrighttxt=tk.CTkLabel(self.btnframe,text="Flip L to R",bg_color=self.lightgray,text_color=self.dark_gray,)
        self.flipcameraleftrighttxt.place(x=1220,y=0)



        #********************Setting Camera like expos gain buttons => MainScreen ***************

        self.settingframe = tk.CTkFrame(self.mainscreen,width=self.mainscreen._current_width, height=200, fg_color=self.lightgray ,)
        self.settingframe.place(y=620, x=400)

        self.Seriallabel = tk.CTkLabel(self.settingframe, text_color=self.textcolor, text="Serial Number", height=20, width=80)
        self.Seriallabel.place(x=70, y=10)

        self.Serialcombobox = tk.CTkComboBox(self.settingframe, corner_radius=5,bg_color=self.lightgray , values=self.cameras, width=180, height=30)
        self.Serialcombobox.place(x=170, y=10)
        self.Serialcombobox.bind("<<ComboboxSelected>>", self.on_serial_selection)
        

        self.exposure_value=""        
        self.labelExposure = tk.CTkLabel(self.settingframe, text="Set Exposure", text_color=self.textcolor , height=20, width=120)               
        self.labelExposure.place(x=420, y=10)        
        self.entryExposure = tk.CTkSlider(self.settingframe, corner_radius=20, fg_color="white",bg_color=self.lightgray  ,width=200, height=10, number_of_steps=200,from_=0,to=50000,button_color=self.dark_gray)
        self.entryExposure.place(x=530, y=10)
        self.entryExposure.bind("<Enter>", self.update_tooltip_textExposure) 
        self.exposureinfo=CustomTooltipLabel(anchor_widget=self.entryExposure, text=self.exposure_value, background="white",foreground="black", width=30, justify=tk.LEFT,hover_delay=0)

        self.gain_value=""
        self.labelGain = tk.CTkLabel(self.settingframe, text="Set Gain", text_color=self.textcolor , height=20, width=120)
        self.labelGain.place(x=710, y=10)
        self.entryGain = tk.CTkSlider(self.settingframe, corner_radius=20, fg_color="white",bg_color=self.lightgray , width=200, height=10, number_of_steps=20,from_=0,to=20,button_color=self.dark_gray)
        self.entryGain.place(x=830, y=10)
        self.entryGain.bind("<Enter>", self.update_tooltip_textGain) 
        self.gaininfo=CustomTooltipLabel(anchor_widget=self.entryGain, text=self.gain_value, background="white",foreground="black", width=30, justify=tk.LEFT,hover_delay=0)

        self.savecambtn = tk.CTkButton(self.settingframe, text="Save", bg_color=self.lightgray, command=self.set_camera, corner_radius=20, fg_color= self.btncolor, width=120, height=30,hover_color=self.bthover,text_color=self.textcolor,)
        self.savecambtn.place(x=370, y=80)
        
        self.resetcambtn = tk.CTkButton(self.settingframe, text="Reset",bg_color=self.lightgray, command=self.reset_cam_settings, corner_radius=20, fg_color= self.btncolor, width=120,text_color=self.textcolor, height=30,hover_color=self.bthover)
        self.resetcambtn.place(x=580, y=80)

        self.capture_running = False
        self.camera2=None
        self.decoded_objects=[]
        self.zoom_factor = 1.2
        self.last_scroll_event_time = 0
        self.decodeallvar=False

    
    def decodeallvalues(self,img):
       decoded_values = []
       barcodes = py.decode(img)
       
       # Iterate through detected barcodes
       for barcode in barcodes:
           barcode_data = barcode.data.decode('utf-8')
           decoded_values.append(barcode_data)
           
           # Extract bounding box coordinates
           x, y, w, h = barcode.rect
           
           # Draw a rectangle around the barcode
           cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
       
       return img, decoded_values
    
    def decodeall(self):
          print(f"self.decodemultiple.get() => {self.decodemultiple.get()}")
          if(self.decodemultiple.get()==1):
               self.decodeallvar=True
          else:
                self.decodeallvar=False  
       

    def flipcameraleftright(self):
       print(f"getting self.Serialcombobox.get() => {self.Serialcombobox.get()}")
       if(self.Serialcombobox.get()==self.cameras[0]):
          if(self.flipcameraleftrightval1==False):
             self.flipcameraleftrightval=True
          else:
              self.flipcameraleftrightval1=False  
       else:
          if(self.flipcameraleftrightval2==False):
             self.flipcameraleftrightval2=True
          else:
              self.flipcameraleftrightval2=False
       

    def flipcameratopbottom(self):
       print(f"getting self.Serialcombobox.get() => {self.Serialcombobox.get()}")
       if(self.Serialcombobox.get()==self.cameras[0]):
          if(self.flipcamera1==False):
             self.flipcamera1=True
          else:
              self.flipcamera1=False  
       else:
          if(self.flipcamera2==False):
             self.flipcamera2=True
          else:
              self.flipcamera2=False

    

    def rotatecamera(self):
       print(f"getting self.Serialcombobox.get() => {self.Serialcombobox.get()}")
       if(self.Serialcombobox.get()==self.cameras[0]):
          print(f"self.rotatecamera1 Before => {self.rotatecamera1}")
          self.rotatecamera1+=90
          print(f"self.rotatecamera1 After => {self.rotatecamera1}")
       else:
          print(f"self.rotatecamera2 Before => {self.rotatecamera2}")
          self.rotatecamera2+=90
          print(f"self.rotatecamera2 After => {self.rotatecamera2}")
       if(self.rotatecamera1>=360):
          self.rotatecamera1=0
       if(self.rotatecamera2>=360):
          self.rotatecamera2=0
    

    def update_tooltip_textGain(self, event=None):
        gain_value = str(self.entryGain.get())
        self.gain_value = f"Gain Value = {gain_value}"
        self.gaininfo.text=self.gain_value
        self.gaininfo._hide_event()
        self.gaininfo._show_event()
        print("Gain value="+gain_value)

    def update_tooltip_textExposure(self, event=None):
        exposure_value = str(self.entryExposure.get())
        self.exposure_value = f"Exposure Value = {exposure_value}" 
        self.exposureinfo.text=self.exposure_value
        self.exposureinfo._hide_event()
        self.exposureinfo._show_event()         
        print("Exposure value="+exposure_value)

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

    def DecodeDatamatrix2(self,label,heights,widths,image,camera):
            if(label is not None and heights is not None and widths is not None and image is not None):
                imgtodisplay=image
                self.decoded_objects.clear()
                img = Image.fromarray(image)                 
                self.third_thread_complete2 = threading.Event()
                def ThirdDecodeDatamatrix2():  
                    i=1
                    results = self.model2(img)
                    start_time = time.time()
                    for r in results:
                        boxes = r.boxes
                        for box in boxes:
                            x1, y1, x2, y2 = box.xyxy[0]
                            cx1, cy1, cx2, cy2 = int(x1), int(y1), int(x2), int(y2)
                            width, height = img.size
                            # Extend the bounding box
                            extension = 20  # Adjust the extension value as needed
                            x1 = max(0, cx1 - extension)
                            y1 = max(0, cy1 - extension)                    
                            x2 = min(width, cx2 + extension)
                            y2 = min(height, cy2 + extension)                    
                            region = img.crop((x1, y1, x2, y2))                 
                            
                            try:
                             if x1 < x2 and y1 < y2:
                               region = imgtodisplay[y1:y2, x1:x2]
                               decoded_objects=None
                               decoded_objects = zxingcpp.read_barcodes(region,try_downscale=False)  
                               #print("Decoded objects directly lenght= > "+str(len(decoded_objects)))                      
                               if(len(decoded_objects)>0):                                   
                                    for objects in decoded_objects:
                                        pattern = r'\(21\)(.*?)\(91\)'
                                        stringformate=str(objects.text)
                                        matches = re.search(pattern, stringformate)
                                        if matches:
                                           extracted_data = matches.group(1)
                                           status=self.sql_conn.InsertSrNo(extracted_data)
                                           print("Sr No=> "+extracted_data+ " and original data = >"+str(objects.text))
                                        else:
                                           print("unknown barcodes with code => "+str(objects.text))  
                                          # print("unknown barcodes and original data = >"+str(objects.text)) 
                                           status=-1                                    
                                        if(status==1): #accepted
                                         cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 255, 0), 7) # green
                                        elif(status==2):  #rejected
                                         cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 0, 255), 7) #red
                                        elif(status==3):  # Dublicate
                                         cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 165, 255), 7) #orange    
                                        elif(status==0):
                                           cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (255, 0, 0), 7)  #blue    
                                        elif(status==-1):
                                           cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 255, 0), 7)  #Pink                                        
                                    self.decoded_objects.append(decoded_objects)     

                            except Exception  as e : 
                              print(str(e)) 
                            i=i+1       
                    end_time = time.time()
                    elapsed_time = (end_time - start_time) * 1000 
                    print("Time taken for decoding:", elapsed_time, "MS")

                    if(self.decodeallvar==True):
                      decoded_values = []
                      barcodes = py.decode(img)
                      # Iterate through detected barcodes
                      for barcode in barcodes:
                          barcode_data = barcode.data.decode('utf-8')
                          decoded_values.append(barcode_data)
                          # Extract bounding box coordinates
                          x, y, w, h = barcode.rect
                          # Draw a rectangle around the barcode
                          cv2.rectangle(imgtodisplay, (x, y), (x + w, y + h), (0, 255, 0), 7)
                      for value in decoded_values:
                         print(f"One D Barcode => {value}")


                    image_rgb = cv2.cvtColor(imgtodisplay, cv2.COLOR_BGR2RGB)
                    image_pils = Image.fromarray(image_rgb) 
                    image_pils = image_pils.rotate(self.rotatecamera2)
                    if(self.rotatecamera2==90 or self.rotatecamera2==180):
                       self.camera_label2.canvas.place_configure(x=-160,y=0)
                    if(self.flipcamera2):
                       image_pils = image_pils.transpose(Image.FLIP_TOP_BOTTOM)
                    if(self.flipcameraleftrightval2):
                       image_pils = image_pils.transpose(Image.FLIP_LEFT_RIGHT)  
                    self.camera_label2.set_image(image_pil=image_pils)                          
                    if(self.decoded_objects.__len__()>0):
                       self.Countbarcode.configure(text=str(len(self.decoded_objects)))          
                    self.third_thread_complete2.set()  
                thread32 = threading.Thread(target=ThirdDecodeDatamatrix2)
                thread32.start()                
                def check_completion_and_proceed():        
                 self.third_thread_complete2.wait()
   
                check_completion_and_proceed() 
            self.thread_DecodeDatamatrix2.set()
            #print(" ************* self.thread_DecodeDatamatrix2.set() called=>> ***************")
            thread = threading.Thread(target=self.capture_image2,args=(camera,label,heights,widths))
            thread.start()

    def DecodeDatamatrix(self,label,heights,widths,image,camera):
        if(label is not None and heights is not None and widths is not None and image is not None):
                #print(" ************* entered in DecodeDatamatrix=>> ***************")
                imgtodisplay=image
                self.decoded_objects.clear()
                img = Image.fromarray(image)
                img = img.convert('L')
                self.third_thread_complete = threading.Event()
                def ThirdDecodeDatamatrix():  
                    i=1                    
                    results = self.model(img)
                    start_time = time.time()
                    for r in results:
                        boxes = r.boxes
                        for box in boxes:                            
                            x1, y1, x2, y2 = box.xyxy[0]
                            cx1, cy1, cx2, cy2 = int(x1), int(y1), int(x2), int(y2)
                            width, height = img.size
                            # Extend the bounding box
                            extension = 25  # Adjust the extension value as needed
                            x1 = max(0, cx1 - (extension+20))
                            y1 = max(0, cy1 - (extension+20))                    
                            x2 = min(width, cx2 + (extension+20))
                            y2 = min(height, cy2 + (extension+20))                    
                            
                            try:
                             if x1 < x2 and y1 < y2:
                               region = img.crop((x1, y1, x2, y2))  
                               region=region.convert('L')                              
                               decoded_objects=None                            
                               decoded_objects = zxingcpp.read_barcodes(region,try_downscale=False,try_rotate=True)                      
                               if(len(decoded_objects)>0):                                                                           
                                    for objects in decoded_objects:
                                          pattern = r'\(21\)(.*?)\(91\)'
                                          stringformate=str(objects.text)
                                          matches = re.search(pattern, stringformate)
                                          if matches:
                                             extracted_data = matches.group(1)
                                             status=self.sql_conn.InsertSrNo(extracted_data)
                                             #print("Sr No=> "+extracted_data+ " and original data = >"+str(objects.text))
                                          else:
                                             #print("unknown barcodes")
                                             print("unknown barcodes and original data = >"+str(objects.text))  
                                             status=-1 
                                          if(status==1): #accepted
                                           cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, y2), (0, 255, 0), 7) # green
                                          elif(status==2):  #rejected
                                           cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 0, 255), 7) #red
                                          elif(status==3):  # Dublicate
                                           cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 165, 255), 7) #orange 
                                          elif(status==0):
                                             cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (255, 0, 0), 7)  #blue
                                          elif(status==-1):
                                             cv2.rectangle(imgtodisplay, (cx1, cy1), (cx2, cy2), (0, 255, 0), 7)  #Pink      
                                    self.decoded_objects.append(decoded_objects)    
                            except Exception  as e : 
                              print(str(e)) 
                            i=i+1          
                    end_time = time.time()
                    elapsed_time = (end_time - start_time) * 1000 
                    print("Time taken for decoding:", elapsed_time, "MS")

                    if(self.decodeallvar==True):
                      decodedvalues = []
                      barcodes = py.decode(img)
                      # Iterate through detected barcodes
                      for barcode in barcodes:
                          barcode_data = barcode.data.decode('utf-8')
                          decodedvalues.append(barcode_data)
                          # Extract bounding box coordinates
                          x, y, w, h = barcode.rect
                          # Draw a rectangle around the barcode
                          cv2.rectangle(imgtodisplay, (x, y), (x + w, y + h), (0, 255, 0), 7)
                      for value in decodedvalues:
                         print(f"One D Barcode => {value}")


                    image_rgb = cv2.cvtColor(imgtodisplay, cv2.COLOR_BGR2RGB)
                    image_pils = Image.fromarray(image_rgb) 
                    image_pils = image_pils.rotate(self.rotatecamera1)
                    if(self.rotatecamera1==90 or self.rotatecamera1==180):
                       self.camera1frame.place_configure(x=150,y=0)   
                    if(self.flipcamera1):
                       image_pils = image_pils.transpose(Image.FLIP_TOP_BOTTOM)
                    if(self.flipcameraleftrightval1):
                       image_pils = image_pils.transpose(Image.FLIP_LEFT_RIGHT)   
                    self.camera_label.set_image(image_pil=image_pils)                         
                    if(self.decoded_objects.__len__()>0):
                       self.Countbarcode.configure(text=str(len(self.decoded_objects)))          
                    self.third_thread_complete.set()
                
                
                thread3 = threading.Thread(target=ThirdDecodeDatamatrix)
                thread3.start()
                
                def check_completion_and_proceed():        
                 self.third_thread_complete.wait()
  
                check_completion_and_proceed() 
        self.thread_DecodeDatamatrix.set()
        #print(" ************* self.thread_DecodeDatamatrix.set() called=>> ***************")
        thread = threading.Thread(target=self.capture_image,args=(camera,label,heights,widths))
        thread.start()

    def capture_image(self, camera, label,heights,widths):
         if(self.capture_running):
            try :                 
                 # Grab a single frame from the camera
                 print("************entered in captureimg **************")
                 camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                 grabResult = camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)
                 camera.StopGrabbing()
                 converter = pylon.ImageFormatConverter()
                 converter.OutputPixelFormat = pylon.PixelType_BGR8packed  
                 converted_image = converter.Convert(grabResult)
                 image_data = converted_image.GetArray()
                 grabResult.Release() 
                 thread = threading.Thread(target=self.DecodeDatamatrix,args=(label, heights,widths,image_data,camera))
                 thread.start()
                 #pygame.mixer.music.play()
                 def check_completion_and_proceed(): 
                    self.thread_DecodeDatamatrix.wait()
                 check_completion_and_proceed()    

            except Exception as e:  
              print(f"Error: {e}")   

         # Close the camera
         

    def capture_image2(self, camera, label,heights,widths):
          if(self.capture_running):
            try :                 
                 # Grab a single frame from the camera
                 print("************entered in captureimg 2 **************")
                 camera.StartGrabbing(pylon.GrabStrategy_LatestImageOnly)
                 grabResult = camera.RetrieveResult(500, pylon.TimeoutHandling_ThrowException)
                 camera.StopGrabbing()
                 converter = pylon.ImageFormatConverter()
                 converter.OutputPixelFormat = pylon.PixelType_BGR8packed  
                 converted_image = converter.Convert(grabResult)
                 image_datas = converted_image.GetArray()    
                 grabResult.Release() 
                 self.decoded_objects=[]
                 thread2 = threading.Thread(target=self.DecodeDatamatrix2,args=(label, heights,widths,image_datas,camera))
                 thread2.start()
                 #pygame.mixer.music.play()
                 def check_completion_and_proceed(): 
                    self.thread_DecodeDatamatrix2.wait()
                 check_completion_and_proceed()    

            except Exception as e:  
              print(f"Error: {e}")   

        
         
    def start_capturetread(self):         
          self.capture_running = True           
          self.thread = threading.Thread(target=self.start_capture) 
          self.thread.start()                       
        

    def wait(self):
     if(len(self.cameras)>1):
      self.thread_DecodeDatamatrix.wait()
      self.thread_DecodeDatamatrix2.wait()    
     else :
        self.thread_DecodeDatamatrix.wait()

    def start_capture(self):
         self.capture_running = True
         # Create camera objects
         self.update_camera_list()
         print("************************ Number of cameras found => "+str(len(self.cameras)))  

         if(len(self.cameras)>1):
           try :  
             print("************************ Logger 0  ***********")
             decices=pylon.TlFactory.GetInstance().EnumerateDevices()
             self.camera1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(decices[0]))
             print("************************ Logger 0  ***********")
             self.camera2 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(decices[1]))
             print("************************ Logger 1  ***********")
           except Exception as e:
              print(str(e))   
         elif len(self.cameras) == 1:
            self.camera1 = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateFirstDevice())
         else:
           print("No cameras found")
           msg = CTkMessagebox(master=self,title="No Camera Found", message=f"There is no camera attached...",icon="warning", option_1="Ok", option_2="Cancel")           
           return
         
         if(len(self.cameras)>1):       
           self.thread = threading.Thread(target=self.StartGrabingWithTwo) 
           self.thread.start()
         else :               
           self.thread = threading.Thread(target=self.StartGrabingWithOne) 
           self.thread.start()


    def StartGrabingWithTwo(self):
            self.thread_DecodeDatamatrix = threading.Event()
            self.thread_DecodeDatamatrix2=threading.Event()
            capturedthrea1=threading.Thread(target=self.capture_image,args=(self.camera1, self.camera_label,int(self.camera1frame._current_height),int(self.camera1frame._current_width)))
            capturedthrea1.start()
            capturedthrea2=threading.Thread(target=self.capture_image2,args=(self.camera2, self.camera_label2,int(self.camera2frame._current_height),int(self.camera2frame._current_width)))
            capturedthrea2.start()
            self.wait()


    def StartGrabingWithOne(self):
            self.thread_DecodeDatamatrix = threading.Event()
            capturedthrea1=threading.Thread(target=self.capture_image,args=(self.camera1, self.camera_label,int(self.camera1frame._current_height),int(self.camera1frame._current_width)))
            capturedthrea1.start()
            self.wait()
      
                  
    def stop_capture(self):
        self.capture_running = False
        if(len(self.cameras)>1):
          self.camera1.Close()
          self.camera2.Close()
        else:
           self.camera1.Close()  

    def reset_cam_settings(self):
        pass

    def set_camera(self):
        try:
            # Find the camera with the selected serial number
            for device in pylon.TlFactory.GetInstance().EnumerateDevices():
                print("Saved settings log 1 ")
                if device.GetSerialNumber() == self.Serialcombobox.get():
                    camera = pylon.InstantCamera(pylon.TlFactory.GetInstance().CreateDevice(device))
                    print("Saved settings log 2 ")
                    camera.Open()
                    print("Saved settings log 3 ")
                    # Set exposure and gain values for the camera
                    camera.ExposureTime.SetValue(int(self.entryExposure.get()))
                    print("Saved settings log 4 ")
                    camera.Gain.SetValue(float(self.entryGain.get()))
                    print("Saved settings log 5 ")
                    camera.Close()      
                    break
            
            print("Saved settings log 6 ")
            msg = CTkMessagebox(master=self,title="Saved", message=f"Setting saved for camera Sr.No:- {str(self.Serialcombobox.get())}",icon="check", option_1="Ok", option_2="Cancel")
            response = msg.get()
             
            self.start_capturetread() 
            self.stop_capture()   
        except Exception as e:
            print(f"Error setting camera: {e}")

    