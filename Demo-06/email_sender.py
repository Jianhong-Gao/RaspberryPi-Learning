import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import socket
import subprocess
import re

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def get_wifi_ip():
    try:
        result = subprocess.run(['ip', '-4', 'addr', 'show', 'wlan0'], capture_output=True, text=True)
        if result.stdout:
            ip_match = re.search(r'inet (\d+\.\d+\.\d+\.\d+)', result.stdout)
            if ip_match:
                return ip_match.group(1)
        return "未知"
    except Exception:
        return "未知"

def send_email(to_email, subject, message):
    sender_email = 'gaojianhong1994@foxmail.com'
    sender_password = "lctwvkmvhwwhbbjj"
    sender_name = 'RaspberryPi'
    receiver_name = 'Anybody'

    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = formataddr([sender_name, sender_email])
    msg['To'] = formataddr([receiver_name, to_email])
    msg['Subject'] = subject

    try:
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, [to_email], msg.as_string())
        server.quit()
        print('邮件发送成功！')
    except Exception as e:
        print('邮件发送失败:', e)

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            print('网络连接正常')
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
            wifi_ip = get_wifi_ip()

            subject = "树莓派开机通知"
            message = f"""
            <p>尊敬的用户:</p>
            <p>您好，这是一份来自您的RaspberryPi的自动邮件通知。</p>
            <p>您的设备已于{formatted_time}成功开机，Wi-Fi接口的IP地址是: {wifi_ip}。</p>
            """
            to_email = 'xxxxx@qq.com'
            send_email(to_email, subject, message)
            break
        else:
            print("无法连接到互联网，将继续尝试...")
            time.sleep(5)
