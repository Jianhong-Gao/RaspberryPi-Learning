import serial
import time


class SerialCommunicator:
    def __init__(self, port_name, baud_rate=0.75e6):
        self.port_name = port_name
        self.baud_rate = baud_rate
        self.serial_port = serial.Serial(port_name, baudrate=baud_rate)
        self.serial_port.flush()

    def write_data(self, content):
        write_start = time.time()
        self.serial_port.write(content)
        write_end = time.time()
        return write_end - write_start


