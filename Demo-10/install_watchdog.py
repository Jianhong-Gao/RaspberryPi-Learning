#!/usr/bin/env python3
import subprocess
import os
import time

def reboot_system():
    print("准备重启系统，请确保所有工作都已保存。")
    time.sleep(5)  # 给用户5秒时间取消重启（如果需要）
    print("正在重启...")
    subprocess.run("sudo reboot", shell=True)

def is_watchdog_service_active():
    result = run_command("sudo systemctl is-active watchdog")
    if result["success"] and "active" in result["output"]:
        return True
    else:
        return False

def run_command(command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return {"success": True, "output": result.stdout, "error": result.stderr}
    except subprocess.CalledProcessError as e:
        print(f"Command execution failed: {e}")
        return {"success": False, "output": None, "error": str(e)}


def check_watchdog_in_boot_config():
    with open('/boot/config.txt', 'r') as file:
        for line in file:
            if 'dtparam=watchdog=on' in line:
                return True
    return False

def enable_watchdog_in_boot_config():
    with open('/boot/config.txt', 'a') as file:
        file.write('dtparam=watchdog=on\n')
    print("看门狗硬件启用配置已添加到 /boot/config.txt。")

def check_watchdog_service_installed():
    result = run_command("dpkg -l | grep watchdog")
    if result["success"] and "watchdog" in result["output"]:
        print("Watchdog service is installed.")
        return True
    else:
        print("Watchdog service is not installed.")
        return False


def start_and_enable_watchdog():
    if is_watchdog_service_active():
        print("Watchdog service is already active.")
    else:
        enable_result = run_command("sudo systemctl enable watchdog")
        start_result = run_command("sudo systemctl start watchdog")

        if enable_result["success"] and start_result["success"]:
            print("Watchdog service enabled and started successfully.")
        else:
            print("Failed to enable or start watchdog service.")



def install_watchdog_service():
    print("安装看门狗服务...")
    return run_command("sudo apt-get update && sudo apt-get install -y watchdog")

def configure_watchdog_service():
    desired_configs = {
        "watchdog-device": "/dev/watchdog",
        "max-load-1": "2",
    }

    # 尝试读取现有配置文件
    try:
        with open("/etc/watchdog.conf", "r") as file:
            existing_configs = file.readlines()
    except FileNotFoundError:
        print("/etc/watchdog.conf 文件不存在，将会创建一个新的。")
        existing_configs = []
    # 预处理现有配置行，移除末尾的换行符并分割键值对
    existing_config_dict = {}
    for line in existing_configs:
        if "=" in line:
            key, value = line.strip().split("=", 1)
            existing_config_dict[key.strip()] = value.strip()

    # 更新或添加配置
    updated_configs = {**existing_config_dict, **desired_configs}

    # 写入更新后的配置
    with open("/etc/watchdog.conf", "w") as file:
        for key, value in updated_configs.items():
            file.write(f"{key} = {value}\n")

    print("看门狗配置已更新。")

def main():
    if not check_watchdog_in_boot_config():
        print("启用树莓派的看门狗硬件...")
        enable_watchdog_in_boot_config()
    else:
        print("看门狗硬件已在 /boot/config.txt 中启用。")

    if not check_watchdog_service_installed():
        if install_watchdog_service():
            print("看门狗服务安装成功。")
        else:
            print("看门狗服务安装失败。")
            return
    else:
        print("看门狗服务已安装。")

    print("配置看门狗服务...")
    configure_watchdog_service()

    if run_command("sudo systemctl enable watchdog") and run_command("sudo systemctl start watchdog"):
        if is_watchdog_service_active():
            print("看门狗服务启动成功并设置为开机自启。")
            # 如果看门狗服务成功启动和配置，可能需要重启来应用某些更改
            # reboot_system()  # 调用重启函数
        else:
            print("看门狗服务启动失败。")
    else:
        print("看门狗服务启动失败。")

if __name__ == "__main__":
    if os.geteuid() != 0:
        exit("该脚本需要以root权限运行")
    main()
