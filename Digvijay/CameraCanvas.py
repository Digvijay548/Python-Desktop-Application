import customtkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class ImageZoom:
    def __init__(self, parent, width, height,position):
        self.parent = parent
        self.width = width+180
        self.height = height+130
        self.zoom_level = 1.0
        self.mouse_x = 0
        self.mouse_y = 0
        self.position=position


        self.canvas = tk.CTkCanvas(self.parent, width=self.width, height=self.height,borderwidth=0,highlightthickness=0,bg="#0b2545")
        self.canvas.place(x=0,y=0)

        self.image = None
        self.image_tk = None
        self.image_id = None

        self.canvas.bind("<ButtonPress-1>", self.pan_start)
        self.canvas.bind("<B1-Motion>", self.pan_move)
        self.canvas.bind("<MouseWheel>", self.zoom)

        self.zoom_level = 1.0
        self.mouse_x = 0
        self.mouse_y = 0

    def set_image(self, image_pil):
       if image_pil is not None:
           self.image = image_pil  # Update the image object
           self.image_tk = ImageTk.PhotoImage(self.image.resize((self.width, self.height)))  # Resize the image
           if self.image_id:
               self.canvas.itemconfig(self.image_id, image=self.image_tk)
           else:
               if(self.position==tk.NW):
                self.image_id = self.canvas.create_image(0, 0, anchor=self.position, image=self.image_tk)
               elif(self.position==tk.NE) :
                   self.image_id = self.canvas.create_image(self.width, 0, anchor=self.position, image=self.image_tk)
       else:
           self.display_blank_image()

    def display_blank_image(self):
        self.image = Image.new("RGB", (self.width, self.height), "black")
        self.image_tk = ImageTk.PhotoImage(self.image)
        self.image_id = self.canvas.create_image(0, 0, anchor=self.position, image=self.image_tk)

    def pan_start(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y

    def pan_move(self, event):
        delta_x = event.x - self.mouse_x
        delta_y = event.y - self.mouse_y
        self.canvas.move(self.image_id, delta_x, delta_y)
        self.mouse_x = event.x
        self.mouse_y = event.y


    def zoom(self, event):
    # Zoom only if there's an image
      print("Zooming...")
      if self.image_id:
          factor = 0.9 if event.delta < 0 else 1.1  # Invert factor for zoom direction
          new_zoom_level = self.zoom_level * factor
          # Check if the zoom level has changed significantly
          if abs(new_zoom_level - self.zoom_level) > 0.05:  # Adjust threshold as needed
              print("Zoom level changed significantly")
              self.zoom_level = new_zoom_level
              self.width = int(self.width * factor)
              self.height = int(self.height * factor)
              print(f"New width: {self.width}, New height: {self.height}")
              self.image_tk = ImageTk.PhotoImage(self.image.resize((self.width, self.height)))  # Resize the image
              print("Image resized")
              self.canvas.itemconfig(self.image_id, image=self.image_tk)
              print("Canvas item configured")
   