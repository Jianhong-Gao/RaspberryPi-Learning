import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import subprocess
import time


def send_email(subject, message):
    sender_email = 'gaojianhong1994@foxmail.com'
    sender_password = "lctwvkmvhwwhbbjj"
    receiver_email = '772962760@qq.com'
    sender_name = 'RaspberryPi'
    receiver_name = 'User'

    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = formataddr([sender_name, sender_email])
    msg['To'] = formataddr([receiver_name, receiver_email])
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        server.quit()
        print('通知邮件成功发送！')
    except Exception as e:
        print(f'发送通知邮件失败: {e}')


def get_service_status(service_name):
    try:
        result = subprocess.run(['systemctl', 'status', service_name], stdout=subprocess.PIPE, text=True, check=True)
        status_info = result.stdout
        formatted_status = status_info.replace('\n', '<br>')
        return formatted_status
    except subprocess.CalledProcessError as e:
        error_info = str(e.output.decode('utf-8') if e.output else e)
        formatted_error = error_info.replace('\n', '<br>')
        return f"服务状态检查失败: <br>{formatted_error}"


def setup_systemd_service():
    service_name = "email_sender.service"
    script_path = "/home/pi/Desktop/Demo-6/email_sender.py"
    service_path = f"/etc/systemd/system/{service_name}"

    send_email("服务部署开始", f"树莓派服务部署进程已于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始。")

    try:
        if not os.path.exists(script_path):
            raise FileNotFoundError(f"脚本 {script_path} 不存在。")

        service_content = f"""[Unit]
Description=树莓派开机自启动邮件发送服务
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 {script_path}

[Install]
WantedBy=multi-user.target
"""

        with open(service_path, 'w') as service_file:
            service_file.write(service_content)

        os.system("sudo systemctl daemon-reload")
        os.system(f"sudo systemctl enable {service_name}")
        os.system(f"sudo systemctl start {service_name}")

        service_status = get_service_status(service_name)
        send_email("服务部署成功及状态报告", f"服务 {service_name} 已成功部署并启动。当前状态：<br>{service_status}")

        # 发送关机前的邮件通知
        shutdown_message = "树莓派将在5秒后关机。"
        send_email("树莓派关机通知", shutdown_message)

        # 延时以确保邮件发送出去
        print("系统将在5秒后重启...")
        time.sleep(5)

        # 执行重启命令
        os.system("sudo reboot")

    except Exception as e:
        error_message = f"服务部署失败: {e}. 时间戳: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(error_message)
        send_email("服务部署失败", error_message)


if __name__ == "__main__":
    setup_systemd_service()
