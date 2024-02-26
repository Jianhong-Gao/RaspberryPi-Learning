import serial
import time
import threading

def show_speed(content, elapsed, operation_type):
    """
    显示数据传输速度，并打印操作时间。

    :param content: 传输的数据内容
    :param elapsed: 传输耗时
    :param operation_type: 操作类型（'read'或'write'）
    """
    len_content = len(content)
    speed_bps = len_content * 8 / elapsed
    speed_kbps = speed_bps / 1024
    timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(f"{timemark} - {operation_type.capitalize()} speed: {speed_kbps:.2f} kbps, data length: {len_content}")

def data_read_realtime(serial_port, size=10):
    """
    实时读取串口数据。

    :param serial_port: 串口对象
    :param size: 每次读取的数据大小
    """
    data_buffer = b''
    flag_record = True
    while True:
        data = serial_port.read_all()
        if data:
            if flag_record:
                flag_record = False
                read_start = time.time()
            data_buffer += data
            if len(data_buffer) >= size:
                flag_record = True
                read_end = time.time()
                last_read = read_end - read_start
                output = data_buffer[:size]
                timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                print(f"{timemark} - Received data length: {len(output)}")
                print(f"write and read operation is normal")
                data_buffer = data_buffer[size:]

def delay(time_delay):
    """
    实现延时功能。
    :param time_delay: 延时时长（秒）
    """
    time_start = time.time()
    while time.time() - time_start < time_delay:
        pass

def main():
    print("The process is running...")
    ser_name = '/dev/ttyAMA3'
    print(f'UART type:{ser_name}')
    serial_port = serial.Serial(ser_name, baudrate=9600)
    serial_port.flush()

    read_thread = threading.Thread(target=data_read_realtime, args=(serial_port, 500))
    read_thread.start()

    while True:
        content = b''.join([i.to_bytes(1, 'big') for i in range(5)])
        content_write = content * 100
        write_start = time.time()
        serial_port.write(content_write)
        write_end = time.time()
        last_write = write_end - write_start
        show_speed(content_write, last_write, "write")
        delay(1)

if __name__ == "__main__":
    main()
