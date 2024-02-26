import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.utils import formataddr
import os

def send_email_with_multiple_attachments(to_email, subject, message, attachment_paths):
    # 发件人邮箱配置 - 硬编码
    sender_email = 'gaojianhong1994@foxmail.com'
    sender_password = "lctwvkmvhwwhbbjj"  # 应使用应用专用密码或确保安全性
    sender_name = 'RaspberryPi'

    # 收件人信息配置
    receiver_name = 'Anybody'

    # 构建邮件内容
    msg = MIMEMultipart()
    msg['From'] = formataddr([sender_name, sender_email])
    msg['To'] = formataddr([receiver_name, to_email])
    msg['Subject'] = subject

    # 邮件正文
    msg.attach(MIMEText(message, 'html', 'utf-8'))

    # 为每个文件添加附件
    for attachment_path in attachment_paths:
        try:
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
            encoders.encode_base64(part)
            part.add_header(
                "Content-Disposition",
                f"attachment; filename= {os.path.basename(attachment_path)}",
            )
            msg.attach(part)
        except Exception as e:
            print(f'添加附件失败: {e}')
            # 可以选择在此处返回，或继续尝试添加其他附件
            # return

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
    subject = "设备离线通知及日志"
    message = """
    <p>尊敬的用户:</p>
    <p>您好，很抱歉打扰到您，这是一份来自RaspberryPi的邮件通知。</p>
    <p>请查看附件中的设备日志了解详细信息。</p>
    """
    to_email = '772962760@qq.com'
    attachment_paths = ['path/to/your/file1.txt', 'path/to/your/file2.txt']  # 替换为实际文件路径
    send_email_with_multiple_attachments(to_email, subject, message, attachment_paths)
