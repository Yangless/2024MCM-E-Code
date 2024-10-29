import os
import matplotlib as mpl
import matplotlib.pyplot as plt

# 设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 定义文件夹路径
data_folder = '../yolov8counting-trackingvehicles-main/Data_only'
output_folder = 'OUTPUT'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义分段和窗口大小
frames_per_segment = 25
window_size = 20


# 分段求和函数
def segment_sum(data):
    return [sum(data[i:i + frames_per_segment]) for i in range(0, len(data), frames_per_segment)]


# 平滑处理函数
def smooth(data):
    smoothed = []
    for i in range(len(data)):
        window = data[max(0, i - window_size + 1):i + 1]
        smoothed.append(sum(window) / len(window))
    return smoothed


# 遍历DATA文件夹中的所有子文件夹
for folder_name in os.listdir(data_folder):
    folder_path = os.path.join(data_folder, folder_name)

    # 检查是否为文件夹
    if os.path.isdir(folder_path):
        # 遍历文件夹中的所有文件
        for file_name in os.listdir(folder_path):
            if file_name.endswith('_three_lane.txt'):
                file_path = os.path.join(folder_path, file_name)

                # 读取数据
                with open(file_path, 'r') as file:
                    data = [list(map(int, line.strip().split())) for line in file]

                # 分别获取每列的数据
                total_cross = [row[3] for row in data]
                lane1_cross = [row[0] for row in data]
                lane2_cross = [row[1] for row in data]
                lane3_cross = [row[2] for row in data]

                # 分段求和
                total_segment_sums = segment_sum(total_cross)
                lane1_segment_sums = segment_sum(lane1_cross)
                lane2_segment_sums = segment_sum(lane2_cross)
                lane3_segment_sums = segment_sum(lane3_cross)

                # 平滑处理
                smoothed_total = smooth(total_segment_sums)
                smoothed_lane1 = smooth(lane1_segment_sums)
                smoothed_lane2 = smooth(lane2_segment_sums)
                smoothed_lane3 = smooth(lane3_segment_sums)

                # 生成输出文件名
                output_file_name = f"{folder_name}_three_lane_{file_name}"
                output_file_path = os.path.join(output_folder, output_file_name)

                # 写入处理后的数据到新文件
                with open(output_file_path, 'w') as output_file:
                    for i in range(len(smoothed_total)):
                        output_file.write(
                            f"{smoothed_lane1[i]}\t{smoothed_lane2[i]}\t{smoothed_lane3[i]}\t{smoothed_total[i]}\n")

                # 绘制车流量变化折线图
                plt.plot(smoothed_total, label='总车流量')
                plt.plot(smoothed_lane3, label='快车道车流量')
                plt.plot(smoothed_lane2, label='慢车道车流量')
                plt.plot(smoothed_lane1, label='应急车道车流量')

                time_label = f"时间 (每{frames_per_segment / 25 * 10}秒内车辆数)"
                plt.xlabel(time_label)
                plt.ylabel('车数量')
                plt.title(f"{folder_name}_{file_name} 车流量变化折线图")
                plt.legend()
                plt.savefig(os.path.join(output_folder, f"{folder_name}_{file_name}_车流量变化折线图.png"))
                plt.close()

print("处理完成！")