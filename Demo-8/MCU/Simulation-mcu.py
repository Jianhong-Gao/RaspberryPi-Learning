from SerialCommunicator import SerialCommunicator
from MessageHandler import MessageHandler
import time
import threading
from utils.utils_comtrade import *

class DataSender:
    def __init__(self, communicator):
        self.communicator = communicator
        self.message_handler = MessageHandler()
        self.running = True  # 控制线程运行的标志
        self.thread = threading.Thread(target=self.run)
        self.thread.daemon = True  # 设置为守护线程，确保主程序退出时线程也会退出
        self.last_send_time = None  # 记录上一次发送数据的完成时间
        self.comtrade_reader = read_comtrade(r'./output_comtrade/single_channel')
        self.analog_V_I = self.comtrade_reader.analog
        self.analog_data_U, self.analog_data_I = self.analog_V_I
        self.segment_size = 3000  # 每个数据段的大小
        self.current_segment_index = 0  # 当前发送的数据段索引
        self.send_data_count=0
        self.inter_time=0.5
    def start(self):
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def run(self):
        next_send_time = time.time() + self.inter_time
        while self.running:
            current_time = time.time()
            if current_time >= next_send_time:
                self.send_data()
                next_send_time = current_time + self.inter_time

    def send_data(self):
        segment_count_U = len(self.analog_data_U) // self.segment_size
        segment_count_I = len(self.analog_data_I) // self.segment_size

        # 确保U和I数据的段数相等
        segment_count = min(segment_count_U, segment_count_I)

        # 如果所有段都已发送，重置索引以循环发送
        if self.current_segment_index >= segment_count:
            self.current_segment_index = 0

        # 计算当前段的起始和结束索引
        start_index = self.current_segment_index * self.segment_size
        end_index = start_index + self.segment_size

        # 从原始数据中切片当前段
        u_Vs_segment = self.analog_data_U[start_index:end_index]
        i_As_segment = self.analog_data_I[start_index:end_index]

        # 创建并发送当前数据段
        if self.send_data_count%10==0 and self.send_data_count!=0:
            con_comm='normal'
        # 1) missing_header
        # 2) missing_footer
        # 3) missing_header_footer
        # 4) corrupted_data
        # 5) missing_sequence
        # 6) missing_part_data_footer
        # 7) missing_part_data_header

        else:
            con_comm =None
        self.send_data_count+=1
        content = self.message_handler.create_message(u_Vs=u_Vs_segment, i_As=i_As_segment,error=con_comm)
        start_time = time.time()
        elapsed_time = self.communicator.write_data(content)
        current_time = time.time()
        if self.last_send_time is not None:
            interval = current_time - self.last_send_time
        else:
            interval = 0
        self.last_send_time = current_time
        MessageHandler.show_speed(content, elapsed_time, "write", interval,con_comm)

        # 准备发送下一个数据段
        self.current_segment_index += 1

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
