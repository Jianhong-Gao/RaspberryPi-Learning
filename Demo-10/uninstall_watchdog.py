#!/usr/bin/env python3
import subprocess

def run_command(command):
    try:
        subprocess.run(command, check=True, shell=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"命令执行失败: {e}")
        return False

def disable_and_stop_watchdog_service():
    print("正在禁用并停止看门狗服务...")
    if run_command("sudo systemctl disable watchdog") and run_command("sudo systemctl stop watchdog"):
        print("看门狗服务已被禁用并停止。")
    else:
        print("无法禁用或停止看门狗服务。")

def remove_watchdog_configuration():
    print("正在移除看门狗配置文件...")
    if run_command("sudo rm -f /etc/watchdog.conf"):
        print("看门狗配置文件已被移除。")
    else:
        print("无法移除看门狗配置文件。")

def remove_watchdog_from_boot_config():
    print("正在从/boot/config.txt中移除看门狗硬件配置...")
    try:
        with open("/boot/config.txt", "r") as file:
            lines = file.readlines()
        with open("/boot/config.txt", "w") as file:
            for line in lines:
                if "dtparam=watchdog=on" not in line:
                    file.write(line)
        print("看门狗硬件配置已从/boot/config.txt中移除。")
    except Exception as e:
        print(f"移除看门狗硬件配置时发生错误: {e}")

def main():
    disable_and_stop_watchdog_service()
    remove_watchdog_configuration()
    remove_watchdog_from_boot_config()

if __name__ == "__main__":
    main()
