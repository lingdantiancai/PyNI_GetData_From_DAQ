'''
电流测量：

SENS:FUNC 'CURR:DC'：设置为直流电流测量模式
SENS:CURR:DC:RANG:AUTO ON：设置直流电流测量范围为自动
SENS:CURR:DC:NPLC <value>：设置直流电流测量的积分周期数
电压测量：

SENS:FUNC 'VOLT:DC'：设置为直流电压测量模式
SENS:VOLT:DC:RANG:AUTO ON：设置直流电压测量范围为自动
SENS:VOLT:DC:NPLC <value>：设置直流电压测量的积分周期数
电阻测量：

SENS:FUNC 'RES'：设置为电阻测量模式
SENS:RES:RANG:AUTO ON：设置电阻测量范围为自动
SENS:RES:NPLC <value>：设置电阻测量的积分周期数
电容测量：

SENS:FUNC 'CAP'：设置为电容测量模式
SENS:CAP:RANG:AUTO ON：设置电容测量范围为自动
SENS:CAP:NPLC <value>：设置电容测量的积分周期数

'''

import pyvisa
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import datetime
import keyboard,os

# 创建一个ResourceManager对象
rm = pyvisa.ResourceManager()

# 打开与Keithley DAQ6510的连接
daq = rm.open_resource('USB0::0x05E6::0x6510::04437692::INSTR')

# 发送命令到Keithley DAQ6510设备
daq.write("*RST")
daq.write("SENS:FUNC 'RES'")  # 设置为电阻测量模式
daq.write("SENS:RES:RANG:AUTO ON")
daq.write("SENS:RES:NPLC 1")  # 设置测量速度为最快
daq.write("TRAC:CLE")  # 清除读数缓冲区

# 创建文件夹
folder_name = "0430-Micro_Structured_PDMS"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 创建一个新的图形窗口
# plt.figure()
# 创建一个新的图形窗口
fig, ax = plt.subplots()

# 创建一个Line2D对象
line, = ax.plot([], [], 'b-')

# 设置图形标题和坐标轴标题
ax.set_title('Resistance measurement')
ax.set_xlabel('Time (s)')
ax.set_ylabel('Current (mA)')

# 获取初始时间
start_time_F = str(datetime.datetime.now()).replace(':', '-')
start_time = datetime.datetime.now()

times = []
results = []

with open(os.path.join(folder_name, "Test-2-1mm-3N-3mms_%s.txt"%(start_time_F)), 'w') as f:
# 读取并绘制测量结果
    while(1):  # 这里的100是读取次数，你可以根据需要修改
        if keyboard.is_pressed('esc'):  # 如果按下了Esc键
            break  # 退出循环
        daq.write("TRAC:CLE")  # 清除读数缓冲区
        result = daq.query("READ?")

        if float(result) > 10E10:  # 如果数据大于10E15，则跳过保存
            continue
        print("%skΩ"%(float(result)/1000))

        results.append(1/float(result))#修改为测试电流，默认电压为1V，输出为mA，则除以1000
        Shijian = (datetime.datetime.now() - start_time).total_seconds()
        times.append(Shijian)
        f.write(str(Shijian) + ',' + str(1/float(result))+'\n')#修改为测试电流，默认电压为5V
        line.set_data(times, results)  # 更新线的数据
        ax.relim()  # 重新计算坐标轴的限制
        ax.autoscale_view()  # 自动调整坐标轴的范围
        fig.canvas.draw()  # 重绘图形窗口
        plt.pause(0.001)  # 暂停0.01秒
    


# for time, result in zip(times, results):
#     f.write(str(time) + ' ' + str(result) + '\n')
# 断开与Keithley DAQ6510的连接
daq.close()
plt.close()  # 关闭图形窗口 