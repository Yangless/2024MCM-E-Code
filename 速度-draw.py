import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 读取数据
name="4.2"
file_path = name+'.speed.txt'
data = []
with open(file_path, 'r') as file:
    for line in file:
        avg_speed, count = map(float, line.strip().split())
        avg_speed*=3.6
        data.append((avg_speed, int(count)))

# 过滤掉没有车的情况（第二个数字==0），用附近值填充
filtered_data = []
for i, (avg_speed, count) in enumerate(data):
    if count == 0:
        # 用前一个非零的值填充
        if i > 0:
            filtered_data.append(filtered_data[-1])
        else:
            # 如果第一个就是0，直接用后面的第一个非零值填充
            for j in range(i + 1, len(data)):
                if data[j][1] != 0:
                    filtered_data.append(data[j])
                    break
    else:
        filtered_data.append((avg_speed, count))

# 每25个数字取一个平均数，缩小数据量
frames_per_segment = 25
segment_averages = []
for i in range(0, len(filtered_data), frames_per_segment):
    segment = filtered_data[i:i + frames_per_segment]
    if len(segment) > 0:
        avg = np.mean([x[0] for x in segment])
        segment_averages.append(avg)

# 使用滑动平均，窗口大小为20
window_size = 20
smoothed_data = []
for i in range(len(segment_averages)):
    window = segment_averages[max(0, i - window_size + 1):i + 1]
    smoothed_data.append(np.mean(window))

# 绘制速度变化折线图
plt.plot(smoothed_data)
str_label = "时间 (每" + str(frames_per_segment / 25 * 10) + "秒内平均速度)"
plt.xlabel(str_label)
plt.ylabel('平均速度(km/h)')
plt.title(name+'速度变化折线图')
plt.show()
