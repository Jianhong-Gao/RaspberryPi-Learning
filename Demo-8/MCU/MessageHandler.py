import time
import math

class MessageHandler:
    def __init__(self):
        # Initialize the sequence number
        self.sequence_number = 0

    @staticmethod
    def show_speed(content, elapsed, operation_type,interval,con_comm):
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
        if con_comm:
            print(
                f"{timemark} - {operation_type.capitalize()} speed: {speed_kbps:.2f} kbps, message length: {len_content},"
                f"Interval time: {interval:.2f},Data transmission time:{elapsed:.2f},Condition-Communication:{con_comm}")

        else:
            print(f"{timemark} - {operation_type.capitalize()} speed: {speed_kbps:.2f} kbps, message length: {len_content},"
                  f"Interval time: {interval:.2f},Data transmission time:{elapsed:.2f}")


    def create_message(self,u_Vs=[2]*10, i_As=[0.2]*10, header=b'\x00\x68'*3, footer=b'\x00\x16'*3,error=None):

        data = b''  # 初始化数据部分为空字节串
        sequence_bytes = self.sequence_number.to_bytes(2, byteorder='big')
        self.sequence_number = (self.sequence_number + 1) % 10
        # 处理电压数据

        for v_V in u_Vs:

            v_trans, _ = MessageHandler.calc_transformed_signals(v_V, 0)  # 假设电流为0，只计算电压
            v_digital_high_low, _ = MessageHandler.analog_to_digital(v_trans, 0)  # 只处理电压
            data += bytes([v_digital_high_low[0], v_digital_high_low[1]])


        # 处理电流数据
        for i_A in i_As:
            _, i_trans = MessageHandler.calc_transformed_signals(0, i_A)  # 假设电压为0，只计算电流
            _, i_digital_high_low = MessageHandler.analog_to_digital(0, i_trans)  # 只处理电流
            data += bytes([i_digital_high_low[0], i_digital_high_low[1]])


        if error == 'missing_header':
            message = sequence_bytes + data + footer
        elif error == 'missing_footer':
            message = header + sequence_bytes + data
        elif error == 'missing_header_footer':
            message = sequence_bytes + data
        elif error == 'corrupted_data':
            message = header + sequence_bytes + data[:-10] + footer
        elif error == 'missing_sequence':
            message = header + data + footer
        elif error == 'missing_part_data_header':
            message = data[:-10]+ footer
        elif error == 'missing_part_data_footer':
            message = header +  data[:-10]
        elif error == 'random_noise':
            # Insert random noise before and after the message
            noise_prefix = bytes([0xFF] * 5)  # Example prefix noise
            noise_suffix = bytes([0xEE] * 5)  # Example suffix noise
            message = noise_prefix + header + sequence_bytes + data + footer + noise_suffix
        else:
            message = header + sequence_bytes + data + footer

        return message

    @staticmethod
    def calc_transformed_signals(v_V, i_A, curr_to_volt_ratio=1/0.5,
                                 volt_to_volt_ratio=6.5/1):

        v_trans = (v_V )/ volt_to_volt_ratio
        i_trans = (i_A) / curr_to_volt_ratio

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
            normalized_signal = ((signal) / (voltage_max - voltage_min)) * max_digital_value
            digital_signal = int(normalized_signal)
            # Ensure the signal is within the range
            digital_signal = max(-max_digital_value, min(max_digital_value, digital_signal))
            # Convert to high and low bytes
            high_byte = (digital_signal >> 8) & 0xFF
            low_byte = digital_signal & 0xFF
            return high_byte, low_byte

        v_digital_high_low = convert_signal(v_trans)
        i_digital_high_low = convert_signal(i_trans)

        return v_digital_high_low, i_digital_high_low