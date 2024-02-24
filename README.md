# ai-rpi-learning
## 项目介绍
这个项目旨在展示如何在树莓派（Raspberry Pi）上进行各种人工智能和嵌入式系统的学习和实践。以下是项目中包含的各种示例和演示：

| 序号  |            名称            | 进度  |
|:---:|:------------------------:|:---:|
|  1  |    [串口自发自收](#Demo-1)     | 已完成 |
|  2  |     [串口间通信](#Demo-2)     | 已完成 |
|  3  |  [模拟单片机-树莓派通信](#Demo-3)  | 已完成 |
|  4  |    [脚本发送邮件](#Demo-4)     | 已完成 |
|  5  |   [录波文件解析与构建](#Demo-5)   | 已完成 |
|  6  |     [开机自启动](#Demo-6)     | 已完成 |
|  7  | [模拟单片机-树莓派通信v2](#Demo-7) | 已完成  |
|  8  |    [通信冗余设计](#Demo-8)     | 待完成 |
|  9  |         [模型效率评估]         | 待完成 |
| 10  |          [看门狗]           | 待完成 |

<span id="Demo-1"></span>
## 1-串口自发自收  

### 案例介绍
本案例展示如何使用树莓派通过串口实现数据的自发送和自接收。这对于测试和验证树莓派串口功能非常有用，尤其是在开发需要串口通信的应用时。
  
### 功能特点
- **自发自收测试**：通过树莓派的串口发送数据，并通过同一串口接收，验证串口的发送和接收功能。
- **速度显示**：计算并显示数据传输的速度，包括bps、kbps和Mbps。
- **实时数据处理**：接收到的数据会实时显示，包括数据长度和接收时间。

### 环境要求
- 树莓派 4B
- Raspbian OS
- Python 3.9.2
- PySerial 库

### 硬件连接
请确保树莓派的TXD和RXD引脚正确连接，以便实现自发自收。下图展示了GPIO引脚的示意图：

<div style="text-align:center;">
    <img src="./assets/images/GPIO-Pin.png" width="100%">
</div>


### 树莓派GPIO到串口设备映射表

- UART0： GPIO14 = TXD0 -> ttyAMA0     GPIO15 = RXD0 -> ttyAMA0
- UART1： ttyS0
- UART2： GPIO0  = TXD2 -> ttyAMA1     GPIO1  = RXD2 -> ttyAMA1
- UART3： GPIO4  = TXD3 -> ttyAMA2     GPIO5  = RXD3 -> ttyAMA2
- UART4： GPIO8  = TXD4 -> ttyAMA3     GPIO9  = RXD4 -> ttyAMA3
- UART5： GPIO12 = TXD5 -> ttyAMA4     GPIO13 = RXD5 -> ttyAMA4

### 树莓派串口测试结果

| 树莓派信息 | 分类 |  黑壳Pi  | 220120E | 211128E |
|:------:|:---:|:------:|:-------:|:-------:|
| UART0  | TX  | Normal |  Normal  | Normal  |
| UART0  | RX  | Normal | Error  | Normal  |
| UART2  | TX  | Normal |    Normal     | Normal  |
| UART2  | RX  | Normal |    Error     | Normal  |
| UART3  | TX  | Normal |     Normal    | Normal  |
| UART3  | RX  | Normal |    Error     | Normal  |
| UART4  | TX  | Error |     Normal    | Normal  |
| UART4  | RX  | Error  |   Error      | Normal  |
| UART5  | TX  | Error |     Normal    | Normal  |
| UART5  | RX  | Error |    Error     | Normal  |


### 使用说明(在Demo-1目录中的终端执行)
```bash
python Serial-self-send-self-receive.py
```
<span id="Demo-2"></span>
## 2-串口间通信

### 案例介绍
本案例展示如何使用树莓派通过不同串口实现数据的发送和接收。
  
### 功能特点
- 设备间直接通信：展示了如何设置树莓派串口，实现两台设备之间的直接数据传输。
- 数据传输与反馈：发送端将数据包发送至接收端，接收端收到数据后，能够对接收到的数据进行处理并反馈。
- 通信性能测量：通过计算数据传输的速度（kbps），可以评估串口通信的性能。

### 环境要求
- 至少两台树莓派 4B 或一台树莓派支持多个串口通信。
- Raspbian OS
- Python 3.9.2
- PySerial 库

### 硬件连接
进行串口间通信时，确保将发送端的TX（发送）引脚连接到接收端的RX（接收）引脚，反之亦然。同时，两台设备的GND（地）引脚也需要连接。这样的硬件连接确保了数据能够正确从一个设备传输到另一个设备。

### 注意事项
- 在连接硬件之前，请确保所有设备都已关闭电源，以避免损坏。
- 根据实际的设备和需求，可能需要调整脚本中的串口配置参数，如波特率和串口设备文件。
- 在进行长时间的通信测试时，监控设备温度和电源状况，确保设备运行在安全的环境中。

### 使用说明(在Demo-2目录中的终端执行)
```bash
python Serial-between-UART.py
```
<span id="Demo-3"></span>
## 3-模拟单片机-树莓派通信

### 案例介绍

本案例通过模拟单片机（MCU）与树莓派（RPI）之间的串口通信，展示了如何在不同硬件平台间进行数据的发送与接收。案例中的MCU部分负责定时发送数据包，而RPI部分则接收这些数据包并进行处理。

### 功能特点

- **双向通信**：展示了MCU与RPI之间如何通过串口进行双向数据传输。
- **数据处理与显示**：RPI接收到数据后，对数据进行处理并显示相关信息，如数据长度、传输速度及接收时间。
- **模拟数据发送**：MCU部分通过定时器模拟数据的生成与发送，展现了在实际应用中可能的数据交互场景。


### 环境要求
-树莓派 4B 或其他版本，作为接收端使用。
-任意支持串口通信的单片机或开发板，作为发送端模拟。
-Raspbian OS 
-Python 3.9.2 
-PySerial库，用于在Python中实现串口通信

### 硬件连接
1. 将MCU的TX（发送）引脚连接到RPI的RX（接收）引脚。
2. 将MCU的RX（接收）引脚连接到RPI的TX（发送）引脚。
3. 确保MCU与RPI的GND（地）引脚相连，以共享公共电位。

### 使用说明
- 在MCU端，运行模拟数据发送脚本。
```bash
python Simulation-mcu.py
```
- 在RPI端，启动数据接收脚本。
```bash
python Simulation-rpi.py
```
- 观察RPI端接收到的数据，并通过日志或终端输出验证通信是否成功。

### 注意事项
- 在这个demo中，两台树莓派分别模拟MCU和RPI端。一台运行发送数据的脚本，另一台运行接收数据的脚本。
- 需要确保两台树莓派之间通过串口线（TX到RX，RX到TX，GND到GND）正确连接。虽然代码示例中使用了ttyAMA0，但实际使用的端口应根据你的硬件连接和配置进行选择。务必确保选用的端口的TXD和RXD引脚已正确连接并可以使用。


<span id="Demo-4"></span>
## 4-脚本发送邮件

### 案例介绍
通过Python脚本向指定邮箱发送指定内容的邮件

### 使用说明
在Demo-4目录中的终端执行以下命令：
```bash
python send_email.py
```


<span id="Demo-5"></span>
## 5-录波文件解析与构建

### 案例介绍
本案例涉及到录波文件的解析与构建。通过comtrade_generate.py脚本，用户可以生成COMTRADE格式的录波文件，模拟实际电力系统中的电压和电流波形。comtrade_parse.py脚本则用于读取和解析这些录波文件，以便进一步分析

### 使用说明
- **解析录波文件**： 首先确保已经通过comtrade_generate.py生成了录波文件。然后，在comtrade_parse.py中指定录波文件的路径，该脚本将解析录波文件，并提供有关其内容的信息。
```bash
recordings=r'./output_comtrade/single_channel'
comtrade_reader = read_comtrade(recordings)
print(dir(comtrade_reader))
```
- **构建录波文件**：使用comtrade_generate.py脚本，用户可以定义电压和电流信号的参数（例如频率、幅度等），以及采样率等信息，生成COMTRADE格式的录波文件。这些文件可以用于测试或教学目的。


<span id="Demo-6"></span>
## 6-开机自启动

### 案例介绍
本案例演示如何在树莓派开机时自动启动Python脚本或服务。这在需要树莓派进行自动化操作，如环境监测、数据采集或远程控制时非常有用。

### 功能特点
- **自动服务配置**：通过 `setup_service.py`，轻松设置服务在树莓派开机时自动运行。
- **邮件通知**：利用 `email_sender.py` 实现开机时自动发送电子邮件，用于系统状态通知或报告。

### 环境要求
- 树莓派4B或其他型号
- Raspbian OS或其他兼容Linux操作系统
- Python 3.9.2或以上版本
- 有效的网络连接以发送电子邮件

### 配置步骤
1. 根据需要配置 `email_sender.py`，包括设置收件人地址和邮件内容。
2. 执行 `setup_service.py` 创建并启动新的系统服务，以实现开机自启动。
```bash
python setup_service.py
```

### 注意事项
- 在运行 setup_service.py 前，请确保具备相应的系统权限。
- 对于 email_sender.py 脚本，需提供SMTP服务器的详细配置信息。
- 配置服务后，重启树莓派验证开机自启动功能是否正常工作。


<span id="Demo-7"></span>
## 7-模拟单片机-树莓派通信v2

### 案例介绍
本案例是模拟单片机与树莓派间通信的进阶版本，通过更加复杂的示例演示了串口通信、数据处理和记录的自动化。案例包含从基础的串口通信到高级的数据记录和分析等多个方面。

### 功能特点
- **高级串口通信**：演示了树莓派和单片机之间的高级通信策略，包括错误处理和数据流控制。
- **COMTRADE录波文件生成与解析**：通过自动生成和解析COMTRADE格式的文件，模拟电力系统中的电压和电流波形，便于分析和教学。
- **数据处理与记录**：介绍了如何使用Python脚本处理接收到的数据，并记录在日志文件中，以便后续分析。

### 环境要求
- 树莓派 4B 或其他型号
- Raspbian OS 或其他兼容的操作系统
- Python 3.9.2 或更高版本
- PySerial 库，用于串口通信
- 其他依赖库，具体参见各脚本的导入部分

### 硬件连接
- 确保树莓派的TX和RX引脚与模拟单片机相连，以实现串口通信。
- 根据需要连接其他相关硬件，如电源和网络连接。

### 使用说明
- **MCU端**：运行 `Simulation-mcu.py` 脚本模拟数据发送。
- **RPI端**：运行 `Simulation-rpi.py` 或 `Simulation-rpi-v7.0.py` 脚本接收和处理数据。
- **数据记录**：使用 `comtrade_generate.py` 和 `comtrade_parse.py` 脚本进行COMTRADE文件的生成和解析。

### 注意事项
- 请根据实际硬件配置调整串口连接设置。
- 确保所有依赖库都已安装。
- 在进行硬件连接之前，务必断电以避免损坏设备。




<span id="Demo-8"></span>
## 8-通信冗余设计

### 案例介绍

本案例基于Demo-7代码的基础上，进一步考虑实际应用场景中可能会出现的通信问题，并增加冗余设计。通过对报文解析逻辑的优化，提高系统对于数据传输错误、数据丢失或损坏的鲁棒性，确保数据通信的可靠性和稳定性。

### 原始报文解析逻辑
1. **初始化和配置串口通信**：设置串口通信的基本参数，如端口名称、波特率，以及必要的超时设置。初始化时，尝试打开串口并清空输入缓冲区，以准备数据接收。
2. **定义报文格式**：明确报文的开始和结束标志（头部和尾部），以及预期的数据段长度。这些参数对于后续的报文识别和提取至关重要。
3. **持续监听和数据缓冲**：在一个后台线程中持续读取串口数据，将接收到的数据累积到动态缓冲区中。这一过程确保了即使数据分多次到达，也能被完整地收集和处理。
4. **报文识别和提取**：循环检查缓冲区数据，寻找定义好的报文头部。一旦找到头部，根据预设的数据长度和尾部标志来确定报文的完整性。如果确认报文完整，则从缓冲区中提取出报文数据进行进一步处理。
5. **数据处理**：对每个提取的报文计算接收时间间隔，并记录相关信息，如数据长度和处理时间。这些信息对于监控通信性能和诊断问题非常有用。

### 冗余设计分析
1. **多报文处理**：为了确保在一次读取操作中接收到的所有报文都能得到正确处理，
实施循环检测和处理机制至关重要。该策略通过持续监测输入缓冲区，识别和处理每一个到达的报文，
确保数据的完整性和准确性，避免因漏读报文而导致的信息丢失或错误。
2. **MCU通信中断后恢复**：在MCU与树莓派的通信过程中，报文丢失是一个常见的问题，
特别是在通信中断恢复之后。报文丢失的情况多样，包括：  
- 单一报文头丢失：影响报文的识别和处理。
- 单一数据点丢失：可能导致接收到的信息不完整或误解。
- 单一报文尾丢失：可能会导致报文解析错误，影响后续报文的处理。
- 完整报文丢失：重要信息可能完全未被接收方接收。
- 报文头和部分数据丢失：同时影响报文的识别和内容的完整性。
- 部分数据和报文尾丢失：影响报文完整性和正确解析尾部信息。
- 报文头和报文尾丢失：整个报文的开始和结束都无法识别，造成严重的数据接收问题。
3. **故障记录与分析**：系统设计中必须包括故障记录与分析机制，以便于后续的问题诊断和系统优化。
通过详细记录通信中断及恢复的事件，包括故障发生的时间、持续时长、恢复尝试次数等信息，
可以为系统的持续改进提供宝贵的数据支持。这些记录不仅帮助技术团队快速定位问题原因，
还能促进对系统薄弱环节的认识，从而采取有效措施防止未来的故障发生。

4. **内部程序执行问题**




