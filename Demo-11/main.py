import subprocess
import os

# 检查 UART 设备是否生效
uart_devices = ['/dev/ttyAMA0', '/dev/ttyAMA1', '/dev/ttyAMA2', '/dev/ttyAMA3', '/dev/ttyAMA4']
uart_device_exists = all(os.path.exists(device) for device in uart_devices)

if uart_device_exists:
    print("所有 UART 设备已存在，无需配置。")
else:
    print("UART 设备尚未全部配置，开始进行配置。")
    # 执行命令编辑 /boot/config.txt
    subprocess.run(['sudo', 'nano', '/boot/config.txt'])

    # 在文件结尾添加指定内容
    config_lines = [
        "dtoverlay=uart2",
        "dtoverlay=uart3",
        "dtoverlay=uart4",
        "dtoverlay=uart5"
    ]
    with open('/boot/config.txt', 'a') as f:
        f.write('\n'.join(config_lines) + '\n')

    # 退出 nano 编辑器
    subprocess.run(['sudo', 'systemctl', 'restart', 'getty@tty1.service'])

    # 重启树莓派
    subprocess.run(['sudo', 'reboot'])