import customtkinter as tk


class ZoomableLabel(tk.CTkLabel):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.bind("<ButtonPress-1>", self.on_start_drag)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<MouseWheel>", self.on_mousewheel)
        self.zoom_factor = 1.2

    def on_start_drag(self, event):
        self._x = event.x
        self._y = event.y

    def on_drag(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        self._x = event.x
        self._y = event.y
        self.place_configure(x=self.winfo_x() + deltax, y=self.winfo_y() + deltay)

    def on_mousewheel(self, event):
        mouse_x = event.x
        mouse_y = event.y
        if event.delta > 0:
            self.zoom_in(mouse_x, mouse_y)
        else:
            self.zoom_out(mouse_x, mouse_y)

    def zoom_in(self, mouse_x, mouse_y):
        current_font_size = self.cget("font").split()[1]
        new_font_size = int(current_font_size) + 1
        self.configure(font=("Arial", new_font_size))
        dx = mouse_x * (self.zoom_factor - 1)
        dy = mouse_y * (self.zoom_factor - 1)
        current_height = self.cget("height")
        current_width = self.cget("width")
        new_height = int(current_height) * self.zoom_factor
        new_width = int(current_width) * self.zoom_factor
        self.configure(height=new_height, width=new_width)
        self.place_configure(x=self.winfo_x() - dx, y=self.winfo_y() - dy)

    def zoom_out(self, mouse_x, mouse_y):
        current_font_size = self.cget("font").split()[1]
        new_font_size = int(current_font_size) - 1
        self.configure(font=("Arial", new_font_size))
        dx = mouse_x * (1 - 1/self.zoom_factor)
        dy = mouse_y * (1 - 1/self.zoom_factor)
        current_height = self.cget("height")
        current_width = self.cget("width")
        new_height = int(current_height) / self.zoom_factor
        new_width = int(current_width) / self.zoom_factor
        self.configure(height=new_height, width=new_width)
        self.place_configure(x=self.winfo_x() + dx, y=self.winfo_y() + dy)