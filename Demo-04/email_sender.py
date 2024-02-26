# email_sender.py

import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr

def send_email(to_email, subject, message):
    # 发件人邮箱配置
    sender_email = 'gaojianhong1994@foxmail.com'
    sender_password = "lctwvkmvhwwhbbjj"
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
    subject = "设备离线通知"
    message = """
    <p>尊敬的用户:</p>
    <p>您好，很抱歉打扰到您，这是一份来自RaspberryPi的邮件通知，该设备当前处于离线状态。</p>
    """
    to_email = '772962760@qq.com'
    send_email(to_email, subject, message)
