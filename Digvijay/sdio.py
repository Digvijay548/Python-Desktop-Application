import tkinter as tk
from tkinter import messagebox
import serial

class SDIOclass:
    def __init__(self, com_port, baud_rate):
        self.com_port = com_port
        self.baud_rate = baud_rate
        self.sdio_device = None
        
    def connect_to_board(self):
        try:
            # Establish connection with the SDIO device
            self.sdio_device = serial.Serial(self.com_port, 115200)
            print(self.com_port, 115200)
            self.sdio_device.open
            print('ENTER')
            print()
            print("Serial port opened successfully.")
            return True
        except Exception as e:
            print("Error:", e)
            return False

    def send_to_instrument(self, data):
        try:
            # Send data to the SDIO device
            if self.sdio_device.is_open:
                print("Device connected ")
               # string.Format("*{0}#", data)
                self.sdio_device.write(data.encode('utf-8'))   
                #CJMRR
                print("Data sent:", data)
                return True
        except Exception as e:
            print("Error:", e)
            return False

    def read_from_instrument(self):
        try:
            # Read data from the SDIO device
            if self.sdio_device is not None:
                data_received = self.sdio_device.read_all()
                print("Data received:", data_received)
                #messagebox.showinfo("Received Data", data_received)  # Display received data in a messagebox
                return str(data_received)
        except Exception as e:
            print("Error:", e)
            return None

    def disconnect(self):
        try:
            # Disconnect from the SDIO device
            if self.sdio_device is not None:
                self.sdio_device.close()
                print("Serial port closed.")
        except Exception as e:
            print("Error:", e)
    
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("SDIO Interface")
        self.root.geometry("300x200")

        self.com_port_entry = tk.Entry(root, width=10)
        self.com_port_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Label(root, text="COM Port:").grid(row=0, column=0, padx=5, pady=5)

        self.connect_button = tk.Button(root, text="Connect", command=self.connect_to_sdio)
        self.connect_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

        self.send_button = tk.Button(root, text="Send Data", command=self.send_data)
        self.send_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

        self.receive_label = tk.Label(root, text="Received Data:")
        self.receive_label.grid(row=3, column=0, padx=5, pady=5)

        self.receive_text = tk.Text(root, height=4, width=20)
        self.receive_text.grid(row=3, column=1, padx=5, pady=5)

        self.disconnect_button = tk.Button(root, text="Disconnect", command=self.disconnect)
        self.disconnect_button.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

        self.sdio = None

    def connect_to_sdio(self):
        com_port = self.com_port_entry.get()
        if com_port:
            self.sdio = SDIOclass(com_port, 115200)
            if self.sdio.connect_to_board():
                messagebox.showinfo("Connection", "Connected to SDIO")
            else:
                messagebox.showerror("Connection", "Failed to connect to SDIO")
        else:
            messagebox.showerror("Connection", "Please enter COM Port")

    def send_data(self):
        print(self.sdio)
        if self.sdio:
            if self.sdio.send_to_instrument("Hello, SDIO!\n"):
                messagebox.showinfo("Send Data", "Data sent successfully")
                received_data = self.sdio.read_from_instrument()
                if received_data:
                    self.receive_text.insert(tk.END, received_data)
            else:
                messagebox.showerror("Send Data", "Failed to send data")

    def disconnect(self):
        if self.sdio:
            self.sdio.disconnect()
            messagebox.showinfo("Disconnect", "Disconnected from SDIO")
            self.sdio = None

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
