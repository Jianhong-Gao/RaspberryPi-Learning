import serial
import time
import threading

def calculate_and_show_speed(content, elapsed_time, operation_type):
    """计算并显示数据传输速度。
    :param content: 传输的数据内容
    :param elapsed_time: 传输耗时
    :param operation_type: 操作类型（'read'或'write'）
    """
    length_content = len(content)
    speed_bps = length_content * 8 / elapsed_time
    speed_kbps = speed_bps / 1024
    print(f"[{operation_type.capitalize()} Speed] {speed_kbps:.2f} kbps ({length_content} bytes in {elapsed_time:.2f} seconds)")

def read_data_in_real_time(serial_port, size=50):
    """实时读取串口数据。
    :param serial_port: 串口对象
    :param size: 每次读取的数据大小
    """
    data_buffer = b''
    recording_flag = True
    try:
        while True:
            data = serial_port.read(size)
            if data:
                if recording_flag:
                    recording_flag = False
                    read_start_time = time.perf_counter()
                data_buffer += data
                if len(data_buffer) >= size:
                    recording_flag = True
                    read_end_time = time.perf_counter()
                    last_read_duration = read_end_time - read_start_time
                    output = data_buffer[:size]
                    calculate_and_show_speed(output, last_read_duration, "read")
                    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                    print(f"[{timestamp}] Read {len(output)} bytes")
                    data_buffer = data_buffer[size:]
    except KeyboardInterrupt:
        print("\n[Info] Reading stopped by user.")

def delay(time_delay):
    """简化的延时函数，使用time.sleep。
    :param time_delay: 延时时长（秒）
    """
    time.sleep(time_delay)

def main():
    try:
        print("[Info] The process is running...")
        sender_port_name = '/dev/ttyAMA3'
        receiver_port_name = '/dev/ttyAMA0'
        print(f"[Info] Sender: {sender_port_name} is sending")
        print(f"[Info] Receiver: {receiver_port_name} is receiving")

        with serial.Serial(sender_port_name, baudrate=9600) as sender_serial, \
                serial.Serial(receiver_port_name, baudrate=9600) as receiver_serial:

            receiver_thread = threading.Thread(target=read_data_in_real_time, args=(receiver_serial, 5000))
            receiver_thread.start()

            # Increase the content size for more accurate time measurements
            content = b'\x01\x02' * 2500  # Increased content size
            while True:
                write_start_time = time.perf_counter()
                sender_serial.write(content)
                write_end_time = time.perf_counter()
                last_write_duration = write_end_time - write_start_time
                calculate_and_show_speed(content, last_write_duration, "write")

    except KeyboardInterrupt:
        print("\n[Info] Process stopped by user.")

if __name__ == "__main__":
    main()
