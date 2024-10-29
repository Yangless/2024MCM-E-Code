import matplotlib.pyplot as plt
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 读取数据
name="4.2"
file_path = name+'.side.txt'
with open(file_path, 'r') as file:
    data = [list(map(int, line.strip().split())) for line in file]

# 分别获取每列的数据
total_cross = [row[3] for row in data]
lane1_cross = [row[0] for row in data]
lane2_cross = [row[1] for row in data]
lane3_cross = [row[2] for row in data]

print(sum(total_cross),sum(lane1_cross),sum(lane2_cross),sum(lane3_cross),sep='\t')

# 分段求和
frames_per_segment = 25  # 每10秒相当于25帧
def segment_sum(data):
    return [sum(data[i:i + frames_per_segment]) for i in range(0, len(data), frames_per_segment)]

total_segment_sums = segment_sum(total_cross)
lane1_segment_sums = segment_sum(lane1_cross)
lane2_segment_sums = segment_sum(lane2_cross)
lane3_segment_sums = segment_sum(lane3_cross)

# 平滑处理
window_size = 20
def smooth(data):
    smoothed = []
    for i in range(len(data)):
        window = data[max(0, i - window_size + 1):i + 1]
        smoothed.append(sum(window) / len(window))
    return smoothed

smoothed_total = smooth(total_segment_sums)
smoothed_lane1 = smooth(lane1_segment_sums)
smoothed_lane2 = smooth(lane2_segment_sums)
smoothed_lane3 = smooth(lane3_segment_sums)

# 绘制车流量变化折线图
plt.plot(smoothed_total, label='总车流量')
plt.plot(smoothed_lane3, label='快车道车流量')
plt.plot(smoothed_lane2, label='慢车道车流量')
plt.plot(smoothed_lane1, label='应急车道车流量')

time_label = f"时间 (每{frames_per_segment / 25 * 10}秒内车辆数)"
plt.xlabel(time_label)
plt.ylabel('车数量')
plt.title(name+'车流量变化折线图')
plt.legend()
plt.show()
