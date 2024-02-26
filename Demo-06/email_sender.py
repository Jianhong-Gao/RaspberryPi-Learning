import smtplib
import time
from email.mime.text import MIMEText
from email.utils import formataddr
import datetime
import socket

def check_internet_connection():
    try:
        # 尝试连接到谷歌的DNS服务器
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        pass
    return False

def send_email(to_email, subject, message):
    # 发件人邮箱配置
    sender_email = 'gaojianhong1994@foxmail.com'
    sender_password = "lctwvkmvhwwhbbjj"  # 建议使用环境变量或加密方式存储密码
    sender_name = 'RaspberryPi'

    # 收件人信息配置
    receiver_name = 'Anybody'

    # 构建邮件内容
    msg = MIMEText(message, 'html', 'utf-8')
    msg['From'] = formataddr([sender_name, sender_email])
    msg['To'] = formataddr([receiver_name, to_email])
    msg['Subject'] = subject

    try:
        # 连接SMTP服务器
        server = smtplib.SMTP_SSL("smtp.qq.com", 465)
        # 登录邮箱
        server.login(sender_email, sender_password)
        # 发送邮件
        server.sendmail(sender_email, [to_email], msg.as_string())
        # 关闭连接
        server.quit()
        print('邮件发送成功！')
    except Exception as e:
        print('邮件发送失败:', e)

if __name__ == "__main__":
    while True:
        if check_internet_connection():
            print('网络连接正常')
            # 获取当前时间
            now = datetime.datetime.now()
            formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

            subject = "树莓派开机通知"
            message = f"""
            <p>尊敬的用户:</p>
            <p>您好，这是一份来自您的RaspberryPi的自动邮件通知。</p>
            <p>您的设备已于{formatted_time}成功开机。</p>
            """
            to_email = '772962760@qq.com'
            send_email(to_email, subject, message)
            break
        else:
            print("无法连接到互联网，将继续尝试...")
            time.sleep(5)
