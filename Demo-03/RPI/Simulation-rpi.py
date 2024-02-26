import serial
import time
import threading

class SerialReceiver:
    def __init__(self, port_name, baud_rate=0.75e6):
        self.port_name = port_name
        self.baud_rate = baud_rate
        try:
            self.serial_port = serial.Serial(port=self.port_name, baudrate=self.baud_rate, timeout=1)
            self.serial_port.flushInput()  # 清空输入缓冲区
        except serial.SerialException as e:
            print(f"Error opening serial port {self.port_name}: {e}")
            self.serial_port = None
        self.header = b'\x00\x68\x00\x68\x00\x68'
        self.footer = b'\x00\x16\x00\x16\x00\x16'
        self.data_length = 12000  # 数据段长度
        self.last_process_time = time.time()  # 初始化上一次数据处理的时间为当前时间
        self.running = True  # 控制线程运行的标志

    def read_message(self):
        buffer = b''  # 动态缓冲区
        while self.running and self.serial_port:
            buffer += self.serial_port.read(self.serial_port.in_waiting or 1)

            while True:  # 循环处理缓冲区中的每个报文
                header_index = buffer.find(self.header)
                if header_index != -1:
                    if len(buffer) >= header_index + len(self.header) + self.data_length + len(self.footer):
                        footer_index = buffer.find(self.footer, header_index + len(self.header) + self.data_length)
                        if footer_index != -1:
                            data = buffer[header_index + len(self.header):footer_index]
                            self.process_data(data)
                            buffer = buffer[footer_index + len(self.footer):]
                            continue
                        else:
                            buffer = buffer[header_index:]
                            break
                    else:
                        break
                else:
                    buffer = buffer[-len(self.header):]
                    break

    def process_data(self, data):
        current_time = time.time()
        interval = current_time - self.last_process_time
        self.last_process_time = current_time

        timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{timemark} - Processing data... (Interval: {interval:.2f} seconds, Data length: {len(data)})")

    def start_reading(self):
        if self.serial_port is not None:
            self.thread = threading.Thread(target=self.read_message)
            self.thread.start()
        else:
            print("Serial port not available.")

    def stop_reading(self):
        self.running = False
        if self.thread:
            self.thread.join()

def main():
    port_name = '/dev/ttyAMA0'
    receiver = SerialReceiver(port_name)
    print("Listening for messages...")
    receiver.start_reading()

    try:
        while True:
            time.sleep(1)  # 主线程可以在这里执行其他任务
    except KeyboardInterrupt:
        receiver.stop_reading()
        print("Stopped listening for messages.")

if __name__ == "__main__":
    main()
