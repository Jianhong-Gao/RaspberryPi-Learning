import numpy as np
import os
from datetime import datetime
from utils.Comtrade import ComtradeWriter
from email_sender import send_email_with_multiple_attachments


def write_comtrade_from_digital(digital_data_U, digital_data_I, output_dir='output_comtrade',
                                station_name='FZU', rec_dev_id='01', sampling_rate=6000,
                                adc_resolution_bits=16, adc_full_scale_voltage=10.0):
    start_time = datetime.now()
    samples_count = len(digital_data_U)
    time_us = np.round(np.linspace(0, samples_count / sampling_rate, samples_count, endpoint=False) * 1e6).astype(int)
    adc_max_value = 2 ** (adc_resolution_bits - 1) - 1

    # Update the base_filepath to include detailed timestamp information
    timestamp_str = start_time.strftime("%Y%m%d_%H%M%S_%f")[:-3]  # Format: YYYYMMDD_HHMMSS_mmm
    base_filepath = os.path.join(output_dir, f"{station_name}_{rec_dev_id}_{timestamp_str}")

    os.makedirs(output_dir, exist_ok=True)

    # Create ComtradeWriter instance
    comtrade_writer = ComtradeWriter(filename=base_filepath + '.cfg', start=start_time, trigger=start_time,
                                     station_name=station_name, rec_dev_id=rec_dev_id, frequency=50,
                                     timemult=1, nrates=1, sampling_rate=sampling_rate)
    a = (2 * adc_full_scale_voltage) / (2 ** adc_resolution_bits)

    # Adding analog channels
    comtrade_writer.add_analog_channel(id="Ua", ph='A', ccbm='Ua', uu='V', a=a * 6.5, b=0, skew=0,
                                       min=-adc_max_value, max=adc_max_value, primary=10e3 / np.sqrt(3),
                                       secondary=6.5 / 3, PS='s')
    comtrade_writer.add_analog_channel(id="Ia", ph='A', ccbm='Ia', uu='A', a=a * 2, b=0, skew=0,
                                       min=-adc_max_value, max=adc_max_value, primary=20, secondary=1, PS='s')

    # Adding sample records
    for i in range(samples_count):
        comtrade_writer.add_sample_record_new(time_us[i], [digital_data_U[i], digital_data_I[i]], [])

    # Finalizing COMTRADE file writing
    comtrade_writer.finalize()

    # 邮件主题和正文
    subject = "COMTRADE文件"
    message = """
    <p>尊敬的用户:</p>
    <p>您好，这是一份来自设备的COMTRADE文件。</p>
    """

    # 发送邮件
    attachment_paths = [base_filepath + '.cfg', base_filepath + '.dat']  # COMTRADE文件路径
    to_email = '772962760@qq.com'  # 替换为您的邮箱地址
    send_email_with_multiple_attachments(to_email, subject, message, attachment_paths)

    print("COMTRADE文件已发送到您的邮箱。")