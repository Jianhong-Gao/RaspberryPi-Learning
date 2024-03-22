from utils_deploy.utils_self_start import *

if __name__ == "__main__":
    email_sender = EmailSender(sender_email='gaojianhong1994@foxmail.com', sender_password="lctwvkmvhwwhbbjj")
    script_path_absolute='/home/pi/Desktop/sender_email/email_sender.py'
    setup_systemd_service(email_sender, "email_sender.service", script_path_absolute)
