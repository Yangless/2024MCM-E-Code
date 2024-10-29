import os
import matplotlib.pyplot as plt
from pylab import mpl
import numpy as np

# 设置字体
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']
mpl.rcParams['axes.unicode_minus'] = False

# 定义文件夹路径
data_folder = '../yolov8counting-trackingvehicles-main/Data_only'
output_folder = 'OUTPUT_density'

# 确保输出文件夹存在
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 定义分段和窗口大小
frames_per_segment = 25
window_size = 20

# 数据处理函数
def process_density(data):
    # 计算密度 K(t) = V(t) / 车辆数
    density_data = []
    for avg_speed, count in data:
        if count > 0:  # 确保车辆数不为0
            density = avg_speed / count
        else:
            density = 0
        density_data.append(density)

    # 每25个数据取平均数，缩小数据量
    segment_averages = []
    for i in range(0, len(density_data), frames_per_segment):
        segment = density_data[i:i + frames_per_segment]
        if len(segment) > 0:
            avg = np.mean(segment)
            segment_averages.append(avg)

    # 使用滑动平均，窗口大小为20
    smoothed_data = []
    for i in range(len(segment_averages)):
        window = segment_averages[max(0, i - window_size + 1):i + 1]
        smoothed_data.append(np.mean(window))

    return smoothed_data

# 遍历DATA文件夹中的所有子文件夹
for folder_name in os.listdir(data_folder):
    folder_path = os.path.join(data_folder, folder_name)

    # 检查是否为文件夹
    if os.path.isdir(folder_path):
        # 遍历文件夹中的所有文件
        for file_name in os.listdir(folder_path):
            if file_name.endswith('_speed.txt'):
                file_path = os.path.join(folder_path, file_name)

                # 读取数据
                data = []
                with open(file_path, 'r') as file:
                    for line in file:
                        avg_speed, count = map(float, line.strip().split())
                        avg_speed *= 3.6  # 转换为 km/h
                        data.append((avg_speed, int(count)))

                # 处理数据，计算密度
                smoothed_density_data = process_density(data)

                # 生成输出文件名
                folder_name = folder_name.replace('speed', 'density')
                output_file_name = f"{folder_name}_density_{file_name}"
                output_file_name = output_file_name.replace('speed', 'density')

                output_file_path = os.path.join(output_folder, output_file_name)

                # 写入处理后的密度数据到新文件
                with open(output_file_path, 'w') as output_file:
                    for density in smoothed_density_data:
                        output_file.write(f"{density}\n")

                # 绘制密度变化折线图
                plt.plot(smoothed_density_data)
                str_label = f"时间 (每{frames_per_segment / 25 * 10}秒内密度)"
                plt.xlabel(str_label)
                plt.ylabel('密度 (km/车辆数)')
                file_name = file_name.replace('speed', 'density')
                plt.title(f"{folder_name}_{file_name} 密度变化折线图")
                plt.savefig(os.path.join(output_folder, f"{folder_name}_{file_name}_密度变化折线图.png"))
                plt.close()

print("密度图处理完成！")
