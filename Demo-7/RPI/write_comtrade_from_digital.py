from utils.Comtrade import ComtradeWriter
import numpy as np
import os
from datetime import datetime
from comtrade_generator import write_comtrade_from_digital

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


# 创建ComtradeWriter实例
write_comtrade_from_digital(digital_data_U, digital_data_I)
