import multiprocessing
import time
import queue  # 用于处理队列相关的异常
import threading

class CollectorProcess(multiprocessing.Process):
    def __init__(self, to_algorithm_queue, start_event):
        super().__init__()
        self.to_algorithm_queue = to_algorithm_queue
        self.start_event = start_event

    def run(self):
        for i in range(10):  # 模拟实时采集10条报文
            data = f"报文{i}"
            print(f"进程1: 收集到数据 {data}")
            try:
                self.to_algorithm_queue.put(data, timeout=1)  # 尝试发送数据，避免无限等待
                self.start_event.set()  # 通知算法进程开始处理
            except queue.Full:
                print("队列已满，等待下一次发送")
            time.sleep(0.5)  # 根据报文发送间隔休眠

class AlgorithmProcess(multiprocessing.Process):
    def __init__(self, from_collector_queue, to_section_queue, start_event):
        super().__init__()
        self.from_collector_queue = from_collector_queue
        self.to_section_queue = to_section_queue
        self.start_event = start_event

    def run(self):
        while True:
            self.start_event.wait()  # 等待CollectorProcess的通知
            try:
                data = self.from_collector_queue.get(timeout=1)  # 从收集器进程接收数据
                print(f"进程2: 接收到数据 {data}, 判断是否启动")
                # 模拟判断逻辑
                if True:  # 假设总是需要启动
                    self.to_section_queue.put(data)  # 将数据发送给选段算法进程
            except queue.Empty:
                print("等待数据...")
            self.start_event.clear()  # 清除事件，准备下次接收

class SectionProcess(multiprocessing.Process):
    def __init__(self, from_algorithm_queue, to_alert_queue):
        super().__init__()
        self.from_algorithm_queue = from_algorithm_queue
        self.to_alert_queue = to_alert_queue

    def run(self):
        while True:
            data = self.from_algorithm_queue.get()  # 从算法进程接收数据
            print(f"进程3: 进行故障选段处理 {data}")
            # 模拟选段算法，假设总是故障
            fault_detected = True
            if fault_detected:
                self.to_alert_queue.put(data)  # 将故障信息发送给通信告警进程



class AlertProcess(multiprocessing.Process):
    def __init__(self, from_section_queue):
        super().__init__()
        self.from_section_queue = from_section_queue
        self.heartbeat_interval = 5  # 心跳包发送间隔（秒）

    def run(self):
        # 启动心跳线程
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True  # 设置为守护线程，确保主进程退出时线程也会退出
        heartbeat_thread.start()

        while True:
            data = self.from_section_queue.get()  # 从选段算法进程接收故障信息
            print(f"进程4: 接收到故障信息 {data}, 执行通信告警")

    def send_heartbeat(self):
        """
        发送心跳包的线程函数
        """
        while True:
            print("心跳包：AlertProcess 运行中...")
            time.sleep(self.heartbeat_interval)  # 等待指定的心跳间隔


if __name__ == "__main__":
    # 创建队列和事件用于进程间通信
    collector_to_algorithm_queue = multiprocessing.Queue()
    algorithm_to_section_queue = multiprocessing.Queue()
    section_to_alert_queue = multiprocessing.Queue()
    start_event = multiprocessing.Event()

    # 实例化并启动进程
    collector = CollectorProcess(collector_to_algorithm_queue, start_event)
    algorithm = AlgorithmProcess(collector_to_algorithm_queue, algorithm_to_section_queue, start_event)
    section = SectionProcess(algorithm_to_section_queue, section_to_alert_queue)
    alert = AlertProcess(section_to_alert_queue)

    collector.start()
    algorithm.start()
    section.start()
    alert.start()

    collector.join()
    algorithm.join()
    section.join()
    alert.join()
