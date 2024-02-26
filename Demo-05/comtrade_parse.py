from utils.utils_comtrade import *

if '__main__'==__name__:
    recordings=r'./output_comtrade/single_channel'
    comtrade_reader = read_comtrade(recordings)
    print(dir(comtrade_reader))