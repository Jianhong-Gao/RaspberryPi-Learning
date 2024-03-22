import os
import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import subprocess

class EmailSender:
    def __init__(self, sender_email, sender_password, sender_name='RaspberryPi'):
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.sender_name = sender_name
        self.smtp_server = "smtp.qq.com"
        self.smtp_port = 465

    def send_email(self, subject, message, receiver_email, receiver_name='User'):
        msg = MIMEText(message, 'html', 'utf-8')
        msg['From'] = formataddr([self.sender_name, self.sender_email])
        msg['To'] = formataddr([receiver_name, receiver_email])
        msg['Subject'] = subject

        try:
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                server.login(self.sender_email, self.sender_password)
                server.sendmail(self.sender_email, [receiver_email], msg.as_string())
            print('通知邮件成功发送！')
        except Exception as e:
            print(f'发送通知邮件失败: {e}')

def get_service_status(service_name):
    try:
        result = subprocess.run(['systemctl', 'status', service_name], capture_output=True, text=True, check=True)
        return result.stdout.replace('\n', '<br>')
    except subprocess.CalledProcessError as e:
        return f"服务状态检查失败: <br>{e.output.decode('utf-8')}"

def setup_systemd_service(email_sender, service_name, script_path):
    service_path = f"/etc/systemd/system/{service_name}"
    receiver_email = '772962760@qq.com'  # Set the receiver's email address here

    email_sender.send_email("服务部署开始", f"树莓派服务部署进程已于 {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} 开始。", receiver_email)

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

        subprocess.run(["sudo", "systemctl", "daemon-reload"], check=True)
        subprocess.run(["sudo", "systemctl", "enable", service_name], check=True)
        subprocess.run(["sudo", "systemctl", "start", service_name], check=True)

        service_status = get_service_status(service_name)
        email_sender.send_email("服务部署成功及状态报告", f"服务 {service_name} 已成功部署并启动。当前状态：<br>{service_status}", receiver_email)

        # Optional: If you wish to reboot or shutdown the system after setup, consider adding those commands here.
    except Exception as e:
        error_message = f"服务部署失败: {e}. 时间戳: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        print(error_message)
        email_sender.send_email("服务部署失败", error_message, receiver_email)

