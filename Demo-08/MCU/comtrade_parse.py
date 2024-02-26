import matplotlib.pyplot as plt
from utils.utils_comtrade import *

if '__main__' == __name__:
    recordings = r'./output_comtrade/single_channel'
    comtrade_reader = read_comtrade(recordings)
    analog_V_I = comtrade_reader.analog
    analog_data_U, analog_data_I = analog_V_I

