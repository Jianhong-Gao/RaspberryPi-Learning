import time
import math

class MessageHandler:
    @staticmethod
    def show_speed(content, elapsed, operation_type,interval):
        """
        显示数据传输速度，并打印操作时间。
        :param content: 传输的数据内容
        :param elapsed: 传输耗时
        :param operation_type: 操作类型（'read'或'write'）
        """
        len_content = len(content)
        speed_bps = len_content * 8 / elapsed
        speed_kbps = speed_bps / 1024
        timemark = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        print(f"{timemark} - {operation_type.capitalize()} speed: {speed_kbps:.2f} kbps, message length: {len_content},"
              f"Interval time: {interval:.2f},Data transmission time:{elapsed:.2f}")

    @staticmethod
    def create_message(v_kVs=[2]*10, i_As=[0.2]*10, header=b'\x00\x68'*3, footer=b'\x00\x16'*3):
        """
        根据电压和电流数据序列创建报文，格式为【报文头，电压1，电压2，电流1，电流2，报文尾】。
        :param v_kVs: 原始电压数据序列（kV），长度为10
        :param i_As: 原始电流数据序列（A），长度为10
        :param header: 报文头的字节序列
        :param footer: 报文尾的字节序列
        :return: 完整的报文
        """
        data = b''  # 初始化数据部分为空字节串
        # 处理电压数据
        for v_kV in v_kVs:
            v_trans, _ = MessageHandler.calc_transformed_signals(v_kV, 0)  # 假设电流为0，只计算电压
            v_digital_high_low, _ = MessageHandler.analog_to_digital(v_trans, 0)  # 只处理电压
            data += bytes([v_digital_high_low[0], v_digital_high_low[1]])

        # 处理电流数据
        for i_A in i_As:
            _, i_trans = MessageHandler.calc_transformed_signals(0, i_A)  # 假设电压为0，只计算电流
            _, i_digital_high_low = MessageHandler.analog_to_digital(0, i_trans)  # 只处理电流
            data += bytes([i_digital_high_low[0], i_digital_high_low[1]])

        # 拼接报文头、数据部分、报文尾
        message = header + data + footer
        return message

    @staticmethod
    def calc_transformed_signals(v_kV, i_A, v_pri_kV=10 / math.sqrt(3), v_sec_V=6.5 / 3, i_pri_A=20, i_sec_A=1, curr_to_volt_ratio=1/0.5,
                                 volt_to_volt_ratio=6.5/1):
        """
        Calculate the transformed signals for AD7606 input based on transformer ratios, considering signal direction.

        Parameters:
        - v_kV (float): Original voltage in kV, can be negative to indicate direction.
        - i_A (float): Original current in A, can be negative to indicate direction.
        - v_pri_kV (float): Primary voltage of voltage transformer in kV.
        - v_sec_V (float): Secondary voltage of voltage transformer in V.
        - i_pri_A (float): Primary current of current transformer in A.
        - i_sec_A (float): Secondary current of current transformer in A.
        - curr_to_volt_ratio (float): Internal current-to-voltage transformer ratio, default 1:1.
        - volt_to_volt_ratio (float): Internal voltage-to-voltage transformer ratio, default 1:1.

        Returns:
        tuple: (v_transformed, i_transformed) Transformed voltage and current signals considering their directions.
        """
        v_ratio = (v_pri_kV * 1000) / v_sec_V
        i_ratio = i_pri_A / i_sec_A

        v_trans = (v_kV * 1000) / v_ratio * volt_to_volt_ratio
        i_trans = (i_A / i_ratio) * curr_to_volt_ratio

        return v_trans, i_trans

    @staticmethod
    def analog_to_digital(v_trans, i_trans, adc_resolution=16, voltage_range=(-10, 10)):
        """
        Convert transformed analog signals to digital values based on ADC resolution and voltage range,
        considering signal saturation if out of range. Then, split the digital value into high and low bytes.

        Parameters:
        - v_trans (float): Transformed voltage signal.
        - i_trans (float): Transformed current signal.
        - adc_resolution (int): Resolution of the ADC in bits. Default is 16 for AD7606.
        - voltage_range (tuple): Operating voltage range of the ADC as a tuple (min, max). Default is (-10, 10) for AD7606.

        Returns:
        tuple: Each element is a tuple representing the high and low bytes of the digital representations of the voltage and current signals.
        """
        voltage_min, voltage_max = voltage_range
        max_digital_value = 2 ** adc_resolution - 1

        def convert_signal(signal):
            # Normalize and scale the signal within the digital range
            normalized_signal = ((signal - voltage_min) / (voltage_max - voltage_min)) * max_digital_value
            digital_signal = int(normalized_signal)
            # Ensure the signal is within the range
            digital_signal = max(0, min(max_digital_value, digital_signal))
            # Convert to high and low bytes
            high_byte = (digital_signal >> 8) & 0xFF
            low_byte = digital_signal & 0xFF
            return high_byte, low_byte

        v_digital_high_low = convert_signal(v_trans)
        i_digital_high_low = convert_signal(i_trans)

        return v_digital_high_low, i_digital_high_low