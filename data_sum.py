import os
import numpy as np


# 读取每个子文件夹中的txt文件
def read_vehicle_data(file_path):
    """读取车辆数量数据的txt文件"""
    return np.loadtxt(file_path)


def read_speed_data(file_path):
    """读取速度数据的txt文件"""
    return np.loadtxt(file_path)


# 计算流量、车速和密度
def calculate_flow_speed_density(vehicle_counts, speed_data):
    """计算流量、平均车速和密度"""
    # Flow: 计算每个时间段通过的车辆数
    flow = vehicle_counts[:, -1]  # 假设总车辆数在最后一列

    # Average speed: 每个时间段的平均车速
    avg_speeds = speed_data[:, 0]

    # 防止除以0，处理平均速度为0的情况
    avg_speeds[avg_speeds == 0] = np.nan

    # Density: K(t) = Q(t) / V(t)
    density = flow / avg_speeds

    # 替换 NaN 为 0
    density = np.nan_to_num(density)

    return flow, avg_speeds, density


# 写入txt文件
def write_to_file(data, file_path):
    """将数据写入到txt文件中"""
    np.savetxt(file_path, data, fmt='%.6f')


# 遍历DATA文件夹
def process_data_folder(data_folder):
    """遍历DATA文件夹中的所有子文件夹，读取数据，计算并写入结果"""
    for folder_name in os.listdir(data_folder):
        folder_path = os.path.join(data_folder, folder_name)
        if os.path.isdir(folder_path):  # 检查是否为文件夹

            # 找到每个文件夹下的所有文件
            txt_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

            # 根据文件名的前缀来进行分组处理
            file_groups = {}
            for file in txt_files:
                file_prefix = '_'.join(file.split('_')[:-1])  # 提取文件名前缀
                if file_prefix not in file_groups:
                    file_groups[file_prefix] = []
                file_groups[file_prefix].append(file)

            # 遍历每个文件组，读取并计算
            for file_prefix, files in file_groups.items():
                # three_lane_file = [f for f in files if f.endswith('_three_lane.txt')]
                three_lane_file = [f for f in files if '_three_lane.txt' in f]

                count_file = [f for f in files if f.endswith('_count.txt')]
                speed_file = [f for f in files if f.endswith('_speed.txt')]

                # 确保该组文件包含所有需要的文件
                if  count_file and speed_file:  #three_lane_file and
                    # three_lane_file_path = os.path.join(folder_path, three_lane_file[0])
                    count_file_path = os.path.join(folder_path, count_file[0])
                    speed_file_path = os.path.join(folder_path, speed_file[0])

                    # 读取文件数据
                    vehicle_counts = read_vehicle_data(count_file_path)
                    speed_data = read_speed_data(speed_file_path)

                    # 计算流量、车速和密度
                    flow, avg_speeds, density = calculate_flow_speed_density(vehicle_counts, speed_data)

                    # 写入计算结果到sum.txt文件
                    sum_file = os.path.join(folder_path, f'{file_prefix}_sum.txt')

                    with open(sum_file, 'w') as f:
                        f.write("Flow:\n")
                        np.savetxt(f, flow, fmt='%.6f')
                        f.write("\nAverage Speed:\n")
                        np.savetxt(f, avg_speeds, fmt='%.6f')
                        f.write("\nDensity:\n")
                        np.savetxt(f, density, fmt='%.6f')

                    print(f'Processed {file_prefix}: flow, speed, and density data written to {sum_file}.')


# 主程序入口
data_folder = '../yolov8counting-trackingvehicles-main/Data_only'  # DATA文件夹路径
process_data_folder(data_folder)
