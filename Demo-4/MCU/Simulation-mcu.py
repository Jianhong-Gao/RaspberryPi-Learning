from SerialCommunicator import SerialCommunicator
from MessageHandler import MessageHandler
import time
import threading

class DataSender:
    def __init__(self, communicator):
        self.communicator = communicator
        self.running = True  # 控制线程运行的标志
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # 设置为守护线程，确保主程序退出时线程也会退出
        self.last_send_time = None  # 记录上一次发送数据的完成时间

    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        next_send_time = time.time() + 0.5
        while self.running:
            current_time = time.time()
            if current_time >= next_send_time:
                self.send_data()
                next_send_time = current_time + 0.5

    def send_data(self):
        # 创建并发送数据
        content = MessageHandler.create_message(v_kVs=[2]*3000, i_As=[0.2]*3000)
        start_time = time.time()  # 发送开始时间
        elapsed_time = self.communicator.write_data(content)
        current_time = time.time()  # 发送完成的当前时间
        if self.last_send_time is not None:
            interval = current_time - self.last_send_time
        else:
            interval=0
        self.last_send_time = current_time
        MessageHandler.show_speed(content, elapsed_time, "write",interval)

def main():
    ser_name = '/dev/ttyAMA0'
    communicator = SerialCommunicator(ser_name)
    print("The process is running...")
    print(f'UART type: {ser_name}')

    sender = DataSender(communicator)
    sender.start()

    try:
        while True:
            time.sleep(1)  # 主线程继续运行，或执行其他任务
    except KeyboardInterrupt:
        print("Stopping sender.")
        sender.stop()

if __name__ == "__main__":
    main()
