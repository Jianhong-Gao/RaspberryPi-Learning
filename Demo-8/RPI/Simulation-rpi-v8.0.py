import serial
import time
import threading
from logger_setup import setup_logger
from comtrade_generator import write_comtrade_from_digital

loggers = setup_logger()

def convert_data(data_all):
    def get_s16(value):
        return value - 0x10000 if value >= 0x8000 else value
    data = []
    for i in range(int(len(data_all) / 2)):
        high = data_all[2 * i]
        low = data_all[2 * i + 1]
        data_16 = (high << 8) | low
        data_10 = get_s16(data_16)
        data.append(data_10)
    return data


class SerialReceiver:
    def __init__(self, port_name, baud_rate=0.75e6):
        self.port_name = port_name
        self.baud_rate = baud_rate
        try:
            self.serial_port = serial.Serial(port=self.port_name, baudrate=self.baud_rate, timeout=1)
            self.serial_port.flushInput()
        except serial.SerialException as e:
            error_content=f"Error opening serial port {self.port_name}: {e}"
            loggers['error'].error(error_content)
            print(error_content)
            self.serial_port = None
        self.header = b'\x00\x68\x00\x68\x00\x68'
        self.footer = b'\x00\x16\x00\x16\x00\x16'
        self.data_length = 12000 + 2
        self.last_process_time = time.time()
        self.running = True
        self.expected_sequence_number = None
        self.process_count=0
        self.timeout_threshold = 0.8  # Timeout threshold in seconds

    def read_message(self):
        buffer = b''
        last_receive_time = time.time()
        while self.running and self.serial_port:
            if time.time() - last_receive_time > self.timeout_threshold and self.expected_sequence_number is not None:
                self.expected_sequence_number = None
                self.id_frame_receive = 0
                error_content=f"Timeout detected, resetting sequence numbering."
                loggers['error'].error(error_content)

            buffer += self.serial_port.read(self.serial_port.in_waiting or 1)
            while True:
                header_index = buffer.find(self.header)
                if header_index != -1:
                    if len(buffer) >= header_index + len(self.header) + self.data_length + len(self.footer):
                        footer_index = buffer.find(self.footer, header_index + len(self.header) + self.data_length)
                        if footer_index != -1:
                            seq_num_bytes = buffer[header_index + len(self.header):header_index + len(self.header) + 2]
                            seq_num = int.from_bytes(seq_num_bytes, byteorder='big')
                            if self.expected_sequence_number is None:
                                self.expected_sequence_number = seq_num
                                self.id_frame_receive = 0
                            elif seq_num != self.expected_sequence_number:
                                self.id_frame_receive = 0
                                error_content=f"Unexpected sequence number: {seq_num}. Expected: {self.expected_sequence_number}"
                                loggers['error'].error(error_content)

                            else:
                                self.id_frame_receive += 1
                            self.expected_sequence_number = (seq_num + 1) % 10
                            last_receive_time = time.time()  # Update last receive time after processing a message
                            data = buffer[header_index + len(self.header) + 2:footer_index]
                            self.process_data(data, self.id_frame_receive)
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


    def process_data(self, data, sequence_number):
        current_time = time.time()
        interval = current_time - self.last_process_time
        self.last_process_time = current_time
        data=convert_data(data)
        num_data_items = len(data) // 2  # 因为每个uint16占2字节
        V_digital=data[:num_data_items]
        I_digital=data[num_data_items:]
        # timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        # if sequence_number%1==0:
        timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{timemark} - Processing data... (Interval: {interval:.2f} seconds, Data length: {len(data)}, Sequence Number: {sequence_number})")

        self.process_count += 1  # 每次处理数据时计数器加1
        if self.process_count >= 1000:  # 每处理20次数据后生成一次COMTRADE文件
            self.write_comtrade_in_thread(V_digital, I_digital)
            self.process_count = 0  # 重置计数器

    def write_comtrade_in_thread(self, V_digital, I_digital):
        write_thread = threading.Thread(target=write_comtrade_from_digital, args=(V_digital, I_digital))
        write_thread.start()

    def start_reading(self):
        if self.serial_port is not None:
            self.thread = threading.Thread(target=self.read_message)
            self.thread.start()
        else:
            error_content="Serial port not available."
            loggers['error'].error(error_content)
            print(error_content)

    def stop_reading(self):
        self.running = False
        if self.thread:
            self.thread.join()

def main():
    port_name = '/dev/ttyAMA0'
    receiver = SerialReceiver(port_name)
    loggers['info'].info("Listening for messages...")
    receiver.start_reading()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        receiver.stop_reading()
        error_content="Stopped listening for messages by user."
        loggers['error'].error(error_content)
        print(error_content)
if __name__ == "__main__":
    main()
