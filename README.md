# RaspberryPi-Learning
## 项目介绍
这个项目旨在展示如何在树莓派（Raspberry Pi）上进行各种人工智能和嵌入式系统的学习和实践。以下是项目中包含的各种示例和演示：

| 序号  |                  名称                   | 进度  |
|:---:|:-------------------------------------:|:---:|
|  1  |           [串口自发自收](#Demo-1)           | 已完成 |
|  2  |           [串口间通信](#Demo-2)            | 已完成 |
|  3  |        [模拟单片机-树莓派通信](#Demo-3)         | 已完成 |
|  4  |           [脚本发送邮件](#Demo-4)           | 已完成 |
|  5  |         [录波文件解析与构建](#Demo-5)          | 已完成 |
|  6  |           [开机自启动](#Demo-6)            | 已完成 |
|  7  |       [模拟单片机-树莓派通信v2](#Demo-7)        | 已完成  |
|  8  |           [通信冗余设计](#Demo-8)           | 已完成 |
|  9  |           [多进程通信](#Demo-9)            | 已完成 |
| 10  |          [树莓派看门狗](#Demo-10)           | 已完成 |
| 11  |          [树莓派开启串口](#Demo-11)          | 已完成 |
| 12  |          [树莓派固定IP](#Demo-12)          | 已完成 |
| 13  | [Python文件转化为Share Object文件](#Demo-13) | 已完成 |
| 14  |      [树莓派系统压备份(镜像文件)](#Demo-14)       | 已完成 |

<span id="Demo-1"></span>
## 01-串口自发自收  

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
| UART2  | RX  | Normal |    Normal     | Normal  |
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
## 02-串口间通信

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
## 03-模拟单片机-树莓派通信

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
## 04-脚本发送邮件

### 案例介绍
通过Python脚本向指定邮箱发送指定内容的邮件

### 使用说明
在Demo-4目录中的终端执行以下命令：
```bash
python send_email.py
```


<span id="Demo-5"></span>
## 05-录波文件解析与构建

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
## 06-开机自启动

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
## 07-模拟单片机-树莓派通信v2

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
## 08-通信冗余设计

### 案例介绍

本案例基于Demo-7代码的基础上，进一步考虑实际应用场景中可能会出现的通信问题，并增加冗余设计。通过对报文解析逻辑的优化，提高系统对于数据传输错误、数据丢失或损坏的鲁棒性，确保数据通信的可靠性和稳定性。
在单片机发给树莓派的报文中增加了校验位，为不计溢出的校验位，长度为1位字节。

### 原始报文解析逻辑
1. **初始化和配置串口通信**：设置串口通信的基本参数，如端口名称、波特率，以及必要的超时设置。初始化时，尝试打开串口并清空输入缓冲区，以准备数据接收。
2. **定义报文格式**：明确报文的开始和结束标志（头部和尾部），以及预期的数据段长度。这些参数对于后续的报文识别和提取至关重要。
3. **持续监听和数据缓冲**：在一个后台线程中持续读取串口数据，将接收到的数据累积到动态缓冲区中。这一过程确保了即使数据分多次到达，也能被完整地收集和处理。
4. **报文识别和提取**：循环检查缓冲区数据，寻找定义好的报文头部。一旦找到头部，根据预设的数据长度和尾部标志来确定报文的完整性。如果确认报文完整，则从缓冲区中提取出报文数据进行进一步处理。
5. **数据处理**：对每个提取的报文计算接收时间间隔，并记录相关信息，如数据长度和处理时间。这些信息对于监控通信性能和诊断问题非常有用。

### 冗余设计分析
1. **多报文处理**：为了确保在一次读取操作中接收到的所有报文都能得到正确处理，实施循环检测和处理机制至关重要。该策略通过持续监测输入缓冲区，识别和处理每一个到达的报文，确保数据的完整性和准确性，避免因漏读报文而导致的信息丢失或错误。
2. **通信异常场景**：在MCU与树莓派的通信过程中，报文丢失是一个常见的问题，特别是在通信中断恢复之后。报文丢失的情况多样，包括：  
- 单一报文头丢失：影响报文的识别和处理。
- 单一数据点丢失：可能导致接收到的信息不完整或误解。
- 单一报文尾丢失：可能会导致报文解析错误，影响后续报文的处理。
- 报文头和部分数据丢失：同时影响报文的识别和内容的完整性。
- 部分数据和报文尾丢失：影响报文完整性和正确解析尾部信息。
- 报文头和报文尾丢失：整个报文的开始和结束都无法识别，造成严重的数据接收问题。
3. **故障记录与分析**：系统设计中必须包括故障记录与分析机制，以便于后续的问题诊断和系统优化。通过详细记录通信中断及恢复的事件，包括故障发生的时间、持续时长、恢复尝试次数等信息，可以为系统的持续改进提供宝贵的数据支持。这些记录不仅帮助技术团队快速定位问题原因，还能促进对系统薄弱环节的认识，从而采取有效措施防止未来的故障发生。

### 内部程序执行问题
4. **内部程序执行问题**：对于内部程序执行过程中可能出现的问题，如程序死锁、资源竞争、异常崩溃等，需要通过代码优化、多线程管理和异常捕获机制来确保程序的稳定运行。此外，实施定期的代码审查和性能测试，可以帮助识别潜在的风险点，并在问题发生前预防或修复，从而提高系统的整体稳定性和可靠性。



<span id="Demo-9"></span>
## 09-多进程通信

### 案例介绍
本案例演示了如何在树莓派上实现多进程通信，特别是在涉及实时数据采集、数据处理、故障检测和告警通知的应用场景中。通过四个独立的进程，模拟了一个完整的数据流和处理流程，从数据的实时采集到最终的告警通知。

### 功能特点
- 实时数据采集：通过串口从单片机实时采集数据。
- 数据处理与算法启动：根据采集到的数据判断是否启动特定算法。
- 故障选段：对数据应用选段算法，确定故障区段。
- 告警通信：当检测到故障时，通过特定的通道发送告警信息。
- 心跳包交互：通过独立的线程在告警进程中实现心跳包发送，以监控进程健康状态。
### 环境要求
- 树莓派4B或其他型号。
- Raspbian OS或其他兼容的操作系统。
- Python 3.7或更高版本。
- 必要的Python库，如multiprocessing和queue。
### 实现策略
- 使用multiprocessing模块创建进程，并通过Queue实现进程间的通信。
- 在告警进程中，使用threading模块创建一个心跳包发送线程，以定期向监控系统或日志记录心跳信息。
- 每个进程都专注于一个特定的任务，确保了程序的模块化和易于维护。
### 使用说明
1. ***初始化和启动进程***：在项目的主脚本中，初始化所有必要的队列和事件，然后创建并启动每个进程。
2. ***数据采集与处理***：数据采集进程负责从硬件接口（如串口）实时读取数据，并将其发送到处理队列中。处理进程监听队列，接收并处理数据，根据逻辑判断是否将数据传递给下一个进程。
3. ***故障检测与告警***：当选段进程检测到故障时，它会将故障信息发送到告警队列。告警进程负责从队列中读取这些信息并执行告警动作，同时通过心跳线程向外部系统或日志记录其运行状态。
### 注意事项
- 在实际部署前，请确保树莓派的硬件接口（如串口）已正确配置，并且与单片机等外部设备的连接正确无误。
- 根据应用场景的需求调整每个进程的具体实现逻辑。
- 确保心跳线程的间隔适当，以避免过多的网络流量或日志记录。
通过这种设计，该案例不仅展示了多进程通信的实现方式，还通过心跳包机制增加了系统的健壮性和可监控性，适用于需要高可靠性和实时性的嵌入式系统和物联网应用。



<span id="Demo-10"></span>
## 10-看门狗配置
手动执行一些步骤来测试和观察看门狗功能
1. **检查看门狗硬件是否启用**  

首先，检查/boot/config.txt文件，确保看门狗硬件已经启用。
```bash
grep 'dtparam=watchdog=on' /boot/config.txt
```
如果这条命令没有返回任何内容，你需要编辑/boot/config.txt文件，并添加下面这行
```bash
dtparam=watchdog=on
```
然后重启树莓派：
```bash
sudo reboot
```
2. **安装看门狗服务（如果尚未安装）**
```bash
sudo apt-get update
sudo apt-get install watchdog
```
3. **配置看门狗**  
编辑/etc/watchdog.conf文件，设置你想要的配置。例如，你可以设置：
```bash
watchdog-device = /dev/watchdog
max-load-1 = 24
```
使用你喜欢的文本编辑器编辑这个文件，如nano：
```bash
sudo nano /etc/watchdog.conf
```
4. **启用并启动看门狗服务**  
```bash
sudo systemctl enable watchdog
sudo systemctl start watchdog
```

5. **检查看门狗服务状态**  
确认看门狗服务已经启动并且处于活动状态。
```bash
sudo systemctl status watchdog
```
6. **手动增加系统负载**  
你可以通过执行资源密集型任务来增加系统负载，例如：
```bash
yes > /dev/null &
```
这个命令会在后台运行，并尽可能快地输出到/dev/null，从而增加CPU负载。根据你的系统，你可能需要运行多个这样的命令来显著增加负载
7. **监控系统负载**  
你可以使用top或htop（如果安装了的话）来监控系统负载。
```bash
top
```
或者
```bash
htop
```
8. **检查是否触发重启**
根据你的/etc/watchdog.conf配置，如果系统负载超过了设置的阈值，看门狗应该会在一定时间后重启系统。确保你已经保存所有重要工作，因为当看门狗触发时，系统将会立即重启。


<span id="Demo-11"></span>
## 11-树莓派串口开启

### 案例介绍
本案例用于开启树莓派串口。默认情况下UART2~UART5禁用，使用本案例将所有串口开启。

设备名称映射：
- UART0: /dev/ttyAMA0
- UART2: /dev/ttyAMA1
- UART3: /dev/ttyAMA2
- UART4: /dev/ttyAMA3
- UART5: /dev/ttyAMA4

### 使用说明
- 本案例需要使用终端命令来授权运行，具体操作如下，在终端输入命令：
 ```bash
cd Desktop （进入代码所在文件夹，以防找不到代码，此处Desktop为举例文件夹名）
sudo python3 main.py
```
- 然后等待树莓派重启使操作生效
- 可以在终端输入命令查看串口是否开启：ls /dev/ttyAMA*
- 结果应显示如下：/dev/ttyAMA0 /dev/ttyAMA1 /dev/ttyAMA2 /dev/ttyAMA3 /dev/ttyAMA4



<span id="Demo-12"></span>
## 12-树莓派固定IP

### 案例介绍
本案例用于设置树莓派的固定IP，将固定IP设置为110.110.110.110。(192.168.3.130)
### 配置流程
- 首先在网线连接下查看自己局域网的IP网段，树莓派终端上运行指令：ifconfig，如下图所示：

<div style="text-align:center;">
    <img src="./assets/images/image_demo12_1.png" width="100%">
</div>

- 然后修改网络配置文件/dhcpcd.conf：

1- 树莓派终端上运行指令：
```bash
sudo nano /etc/dhcpcd.conf
```
2- 找到#interface eth0，在其注释下方，填写相关信息如下图所示。其中需要将IP地址和routers分别修改为110.110.110.110/24 与 110.110.110.1。
添加内容为：
```bash
interface eth0
static ip_address=110.110.110.110/24
static routers=110.110.110.1
static domain_name_servers=223.5.5.5
```
or
```bash
interface eth0
static ip_address=192.168.3.130/24
static routers=192.168.3.1
static domain_name_servers=223.5.5.5
```
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_2.png" width="100%">
</div>

3- 填写IP信息完成后保存并重启树莓派：
- 完成后检查是否设置成功：

1- 物理连接：将树莓派通过网线直接连接笔记本电脑，若笔记本电脑已经使用有线方式连接互联网，占用了网口，则需要使用usb网口转换器拓展笔记本网口。若笔记本连接的是无线网，则直接连接即可。  
2- PC端：网络设置：打开网络适配器设置，此时我们可以看到已经连接互联网的网络和与树莓派连接的网络，如下图所示。

<div style="text-align:center;">
    <img src="./assets/images/image_demo12_3.png" width="100%">
</div>


①	右键点击“未识别的网络”，选择右键菜单中的属性栏：  
②	在以太网属性窗口选择“Internet协议版本4（TCP/IPv4）”  
③	选中“Internet协议版本4（TCP/IPv4）”，属性按钮被激活，选中；   
操作如下图所示。
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_4.png" width="100%">
</div>
④	在Internet协议版本4（TCP/IPv4）属性窗口中选中“使用下面的IP地址”  
⑤	IP地址和子网掩码分别填写：110.110.110.1和255.255.255.0  
⑥	完成操作4和5后，点击确认；  
操作如下图所示。
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_5.png" width="100%">
</div>

3、	PC端：远程桌面连接：  
①	登入远程桌面连接；  
②	填写信息如下图所示；
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_6.png" width="100%">
</div>

③	若初次连接，会出现确认安全菜单，全部选择确认，然后再次输入账号密码即可登入；非初次连接，会出现账户密码输入选项，如下图所示，输入默认密码（pi），输入完成后即可登入。
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_7.png" width="100%">
</div>

④	点击确认后，出现远程连接桌面，如下图所示。至此，树莓派网线直连操作已完成。
<div style="text-align:center;">
    <img src="./assets/images/image_demo12_8.png" width="100%">
</div>

<span id="Demo-13"></span>
## 13-Python文件转化为Share Object文件

### 案例介绍
这个工具提供了一种简便的方式来编译Python文件为C扩展，并将生成的文件移动到指定的输出目录

### 功能
* **编译Python文件**：使用Cython将单个Python文件编译为C扩展（.so或.pyd文件，取决于操作系统）。
* **自动移动**：将编译生成的C扩展自动移动到指定的输出目录。
* **清理临时文件**：在编译和移动操作完成后，自动清理临时生成的文件和目录，包括Cython生成的.c文件和build目录 
### 使用方法

1. **安装依赖**：确保你的环境中安装了Cython和setuptools。如果还未安装，可以使用以下命令安装：
```bash
pip install Cython setuptools
```
2. **编写Python脚本**：创建一个Python脚本并导入compile_and_move_extension函数。指定你想要编译的Python文件路径、目标输出目录以及生成文件的扩展名。

3. **执行脚本**：运行你的Python脚本来编译并移动生成的C扩展。

示例代码：

```bash
from utils_deploy.compile_and_deploy import compile_and_move_extension
if __name__ == "__main__":
    python_file = "path/to/your/python_file.py"
    output_dir = "path/to/your/output_directory"
    compile_and_move_extension(python_file, output_dir)
```
确保替换path/to/your/python_file.py和path/to/your/output_directory为你自己的路径。

### 注意事项

* 生成的文件扩展名（.so或.pyd）取决于你的操作系统。默认情况下，Windows上为.pyd，Linux和macOS上为.so。

* 这个工具假定build目录是编译过程的默认输出目录。如果你的项目配置修改了这一默认行为，请相应调整代码中的build_lib_path变量

<span id="Demo-14"></span>
## 14-树莓派系统压备份(镜像文件)

### 案例介绍
本案例介绍将配置好的树莓派系统进行压缩备份，存储为镜像文件(.image)

### 环境要求
如果电脑是windows系统,需要提前安装虚拟机。
1.Ubuntu 64位 版本号：18.04;
2.FileZila软件
### 操作步骤

1. 将配置好环境的树莓派sd使用读卡器插入电脑，连接虚拟机；
2. 先用lsblk命令查看SD卡的盘符
```bash
lsblk
```
<div style="text-align:center;">
    <img src="assets/images/image_demo14_1.png" width="100%">
</div>

3. 备份
```bash
sudo  dd  if=/dev/sdb  of=./rpi-tw-0322.img  bs=8M
```
4. 压缩
```bash
sudo pishrink.sh -s rpi-tw-0322.img rpi-tw-0322-compressed.img
```
5. 文件转移
使用FileZila,连接上虚拟机的IP
1) 首先，filezilla与虚拟机之间是通过ssh连接，所以需在虚拟机上安装ssh-server
```bash
apt-get install openssh-server
```
2) 查看虚拟机的IP
```bash
ip addr
```
3) 连接FileZila，选择image文件传输
6. 烧写系统
