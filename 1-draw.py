import matplotlib.pyplot as plt
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False
# 读取数据
file_path = '4.2.20240501_20240501125647_20240501140806_125649.mp4.txt'
with open(file_path, 'r') as file:
    data = [int(line.strip()) for line in file]
print(len(data))
print(sum(data))

# 分段求和
frames_per_segment = 25  # 每10秒相当于25帧
segment_sums = []
for i in range(0, len(data), frames_per_segment):
    segment_sums.append(sum(data[i:i + frames_per_segment]))

# 平滑处理
window_size = 5
smoothed_data = []
for i in range(len(segment_sums)):
    window = segment_sums[max(0, i - window_size + 1):i + 1]
    smoothed_data.append(sum(window) / len(window))

# 绘制车流量变化折线图
plt.plot(smoothed_data)
str="时间 (每"+str(frames_per_segment/25*10)+"秒内车辆数)"
# plt.xlabel('Time (10-second intervals)')
plt.xlabel(str)
plt.ylabel('车数量')
plt.title('车流量变化折线图')
plt.show()
