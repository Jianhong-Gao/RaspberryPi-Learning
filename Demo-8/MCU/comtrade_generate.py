from utils.Comtrade import ComtradeWriter
import numpy as np
import os
from datetime import datetime

def create_analog_data(samples_count, sampling_rate, frequency, amplitude):
    time = np.linspace(0, samples_count / sampling_rate, samples_count, endpoint=False)
    time_us = np.round(time * 1e6).astype(int)
    analog_data = amplitude * np.sin(2 * np.pi * frequency * time)
    return time_us, analog_data

def ad_conversion(analog_data, adc_resolution_bits, adc_full_scale_voltage):
    adc_max_value = 2**(adc_resolution_bits - 1) - 1
    digital_data = (analog_data / adc_full_scale_voltage) * adc_max_value
    return digital_data.astype(int),adc_max_value

# 基本参数
station_name = 'TestStation'
rec_dev_id = '01'
sampling_rate = 6000  # Hz
samples_count = 3000  # 总样本数
adc_resolution_bits = 16
adc_full_scale_voltage = 10.0  # 假设满量程为±10V
start_time = datetime.now()

# 模拟数据生成
time_us, analog_data_U = create_analog_data(samples_count, sampling_rate, 50, 1*1.41)
_, analog_data_I = create_analog_data(samples_count, sampling_rate, 50, 0.5*1.41)

# AD转换
digital_data_U,adc_max_value = ad_conversion(analog_data_U, adc_resolution_bits, adc_full_scale_voltage)
digital_data_I,adc_max_value = ad_conversion(analog_data_I, adc_resolution_bits, adc_full_scale_voltage)

# 输出文件路径
output_dir = 'output_comtrade'
os.makedirs(output_dir, exist_ok=True)
base_filepath = os.path.join(output_dir, 'single_channel')

# 创建ComtradeWriter实例
comtrade_writer = ComtradeWriter(filename=base_filepath + '.cfg', start=start_time, trigger=start_time,
                                 station_name=station_name, rec_dev_id=rec_dev_id, frequency=50,
                                 timemult=1, nrates=1, sampling_rate=sampling_rate)

# 添加模拟通道
a = (2 * adc_full_scale_voltage) / (2**adc_resolution_bits)
comtrade_writer.add_analog_channel(id="Ua", ph='A', ccbm='Ua', uu='V', a=a*6.5, b=0, skew=0,
                                   min=-adc_max_value, max=adc_max_value, primary=10e3/np.sqrt(3), secondary=6.5/3, PS='s')
comtrade_writer.add_analog_channel(id="Ia", ph='A', ccbm='Ia', uu='A', a=a*2, b=0, skew=0,
                                   min=-adc_max_value, max=adc_max_value, primary=20, secondary=1, PS='s')

# 添加样本记录
for i in range(samples_count):
    comtrade_writer.add_sample_record_new(time_us[i], [digital_data_U[i], digital_data_I[i]], [])

# 完成COMTRADE文件的写入
comtrade_writer.finalize()

print(f"Generated COMTRADE files at {base_filepath}.cfg and {base_filepath}.dat")
