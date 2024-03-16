#!/usr/bin/env python3
import multiprocessing
import os
import time

def cpu_intensive_task():
    # 这个函数执行计算密集型任务以增加CPU负载
    while True:
        [x**2 for x in range(10000)]

def increase_load(duration, num_processes):
    print(f"Increasing load on {num_processes} cores for {duration} seconds...")
    processes = [multiprocessing.Process(target=cpu_intensive_task) for _ in range(num_processes)]

    # 启动所有进程
    for p in processes:
        p.start()

    # 每5秒打印一次当前负载，直到达到指定的持续时间
    start_time = time.time()
    while time.time() - start_time < duration:
        print_current_load()
        time.sleep(5)

    # 停止所有进程
    for p in processes:
        p.terminate()
        p.join()

    print("Load increase complete.")

def print_current_load():
    # 打印当前系统负载
    one_min, five_min, fifteen_min = os.getloadavg()
    print(f"Current load: 1 min: {one_min}, 5 min: {five_min}, 15 min: {fifteen_min}")

if __name__ == "__main__":
    duration = 600  # 测试持续时间，单位为秒
    num_processes = multiprocessing.cpu_count()  # 根据CPU核心数量来启动进程
    increase_load(duration, num_processes)
