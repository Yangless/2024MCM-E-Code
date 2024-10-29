import os
import matplotlib.pyplot as plt
from pylab import mpl

# 设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 定义文件夹路径
data_folder = '../yolov8counting-trackingvehicles-main/Data_only'
output_folder = 'OUTPUT_count'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义分段和窗口大小
frames_per_segment = 25
window_size = 5


# 数据处理函数
def process_data(data):
    # 分段求和
    segment_sums = []
    for i in range(0, len(data), frames_per_segment):
        segment_sums.append(sum(data[i:i + frames_per_segment]))

    # 平滑处理
    smoothed_data = []
    for i in range(len(segment_sums)):
        window = segment_sums[max(0, i - window_size + 1):i + 1]
        smoothed_data.append(sum(window) / len(window))

    return smoothed_data


# 遍历DATA文件夹中的所有子文件夹
for folder_name in os.listdir(data_folder):
    folder_path = os.path.join(data_folder, folder_name)

    # 检查是否为文件夹
    if os.path.isdir(folder_path):
        # 遍历文件夹中的所有文件
        for file_name in os.listdir(folder_path):
            if file_name.endswith('_count.txt'):
                file_path = os.path.join(folder_path, file_name)

                # 读取数据
                with open(file_path, 'r') as file:
                    data = [int(line.strip()) for line in file]

                # 处理数据
                smoothed_data = process_data(data)

                # 生成输出文件名
                output_file_name = f"{folder_name}_count_{file_name}"
                output_file_path = os.path.join(output_folder, output_file_name)

                # 写入处理后的数据到新文件
                with open(output_file_path, 'w') as output_file:
                    for count in smoothed_data:
                        output_file.write(f"{count}\n")

                # 绘制车流量变化折线图
                plt.plot(smoothed_data)
                str_label = f"时间 (每{frames_per_segment / 25 * 10}秒内车辆数)"
                plt.xlabel(str_label)
                plt.ylabel('车数量')
                plt.title(f"{folder_name}_{file_name} 车流量变化折线图")
                plt.savefig(os.path.join(output_folder, f"{folder_name}_{file_name}_车流量变化折线图.png"))
                plt.close()

print("处理完成！")