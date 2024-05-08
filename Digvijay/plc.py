import serial
import tkinter as tk

# Function to handle serial connection
def toggle_connection():
    global ser
    if not ser:
        # Open serial port
        try:
            ser = serial.Serial(port_entry.get(), baudrate_entry.get())
            connection_status.config(text="Connected", fg="green")
        except Exception as e:
            connection_status.config(text="Error: " + str(e), fg="red")
    else:
        # Close serial port
        ser.close()
        ser = None
        connection_status.config(text="Disconnected", fg="black")

# Function to read data from PLC
def read_from_plc():
    if ser:
        data = ser.readline().decode().strip()
        data_label.config(text="Data read from PLC: " + data)
    else:
        data_label.config(text="Not connected to PLC", fg="red")

# Function to write data to PLC
def write_to_plc():
    if ser:
        message = message_entry.get()
        ser.write(message.encode())
        write_label.config(text="Message sent to PLC: " + message)
    else:
        write_label.config(text="Not connected to PLC", fg="red")

# Create main window
root = tk.Tk()
root.title("PLC Communication")

# Serial connection widgets
connection_frame = tk.Frame(root)
connection_frame.pack(pady=10)

port_label = tk.Label(connection_frame, text="Port:")
port_label.grid(row=0, column=0)

port_entry = tk.Entry(connection_frame)
port_entry.insert(0, "/dev/ttyUSB0")  # Default port
port_entry.grid(row=0, column=1)

baudrate_label = tk.Label(connection_frame, text="Baudrate:")
baudrate_label.grid(row=0, column=2)

baudrate_entry = tk.Entry(connection_frame)
baudrate_entry.insert(0, "9600")  # Default baudrate
baudrate_entry.grid(row=0, column=3)

connect_button = tk.Button(connection_frame, text="Connect", command=toggle_connection)
connect_button.grid(row=0, column=4)

connection_status = tk.Label(connection_frame, text="Disconnected", fg="black")
connection_status.grid(row=0, column=5)

# PLC communication widgets
plc_frame = tk.Frame(root)
plc_frame.pack(pady=10)

read_button = tk.Button(plc_frame, text="Read from PLC", command=read_from_plc)
read_button.grid(row=0, column=0)

message_entry = tk.Entry(plc_frame)
message_entry.grid(row=0, column=1)

write_button = tk.Button(plc_frame, text="Write to PLC", command=write_to_plc)
write_button.grid(row=0, column=2)

data_label = tk.Label(root, text="")
data_label.pack(pady=5)

write_label = tk.Label(root, text="")
write_label.pack(pady=5)

# Initialize serial connection variable
ser = None

# Run the application
root.mainloop()

# Close serial port when the application is closed
if ser:
    ser.close()
