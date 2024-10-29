import os
import cv2
import torch

# 加载YOLOv5模型
model = torch.hub.load('ultralytics/yolov5:v6.0', 'yolov5x')

# 定义数据文件夹路径
data_folder = '../yolov8counting-trackingvehicles-main/Data_only'

# 遍历数据文件夹中的所有子文件夹
for root, dirs, files in os.walk(data_folder):
    for file in files:
        if file.endswith('.mp4'):
            video_path = os.path.join(root, file)
            folder_name = os.path.basename(root)  # 获取文件夹名称
            txt_name = f"{folder_name}_{file}_three_lane.txt"
            txt_path = os.path.join(root, txt_name)

            # 打开视频文件
            cap = cv2.VideoCapture(video_path)

            # 视频属性
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))  # 获取帧率
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取帧宽
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取帧高

            # 初始化视频写入
            output_path = f"{folder_name}_{file}.output_video.mp4"
            # output_path = 'output_video.mp4'  # 输出视频文件路径
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

            # 输出到文本文档
            txt = []

            # 初始化车辆计数和已通过车辆集合
            total_car_count = 0  # 总车辆计数
            passed_cars = set()  # 存储已通过车辆的边界框

            # 设定通过线的位置
            point2x = 0
            point2y = int(height * 0.2)
            point1x = width
            point1y = int(height * 0.5)

            # 车道划分
            side1 = int(width * 0.25)
            side2 = int(width * 0.4)

            def which_side(x, y):
                if x < side1:
                    return 0
                if x < side2:
                    return 1
                return 2

            # 跟踪设置
            T = 12
            D = 50
            Area = 100

            # 存储每一帧中，所有车辆的信息
            mess = []  # 第 i 帧 第 j 辆车的信息，信息格式为 x,y,a,b,ID=0,book 分别为中心点坐标,ID,是否已经有后继车辆
            ID = 0  # 唯一识别符
            cross = set()  # 已经跨线的车辆ID

            # 欧拉距离
            def dis(x1, y1, x2, y2):
                return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5

            def superposition(xc1, yc1, a1, b1, xc2, yc2, a2, b2):
                l1 = xc1 - a1 / 2
                r1 = xc1 + a1 / 2
                t1 = yc1 - b1 / 2
                d1 = yc1 + b1 / 2

                l2 = xc2 - a2 / 2
                r2 = xc2 + a2 / 2
                t2 = yc2 - b2 / 2
                d2 = yc2 + b2 / 2

                x1 = max(l1, l2)
                x2 = min(r1, r2)
                y1 = max(t1, t2)
                y2 = min(d1, d2)
                if x2 > x1 and y2 > y1:
                    return (x2 - x1) * (y2 - y1)
                return 0

            def judge_side(x, y):
                ax = point2x - point1x
                ay = point2y - point1y
                bx = x - point1x
                by = y - point1y

                cross_product = ax * by - ay * bx
                return cross_product >= 0

            def hex_to_bgr(hex_color):
                """将十六进制颜色字符串转换为RGB元组"""
                hex_color = hex_color.lstrip('#')  # 移除开头的'#'（如果有）
                return tuple(int(hex_color[i:i + 2], 16) for i in (4, 2, 0))

            # 逐帧处理视频
            num = 0
            now_side_cross_sum = [0, 0, 0]
            while cap.isOpened():
                num += 1
                ret, frame = cap.read()  # 读取视频帧
                if not ret:
                    break  # 如果没有读取到帧，退出循环

                results = model(frame)  # 使用YOLO模型进行推断
                detections = results.pandas().xyxy[0]  # 将检测结果转换为DataFrame格式

                # 过滤出车辆检测结果
                cars = detections[detections['name'].isin(['car', 'truck', 'traffic light', 'bus'])]  # 筛选出车辆
                now_mess = []
                now_cross = 0
                now_side_cross = [0, 0, 0]
                # 计数车辆
                for index, row in cars.iterrows():
                    car_box = (row.xmin, row.ymin, row.xmax, row.ymax)
                    car_x = (row.xmin + row.xmax) / 2
                    car_y = (row.ymin + row.ymax) / 2
                    car_w = row.xmax - row.xmin
                    car_h = row.ymax - row.ymin
                    now_car = [car_x, car_y, car_w, car_h, 0, 0]

                    # 跟踪
                    min_t, min_i, max_area = 0, 0, 0

                    # find who 4 != 0
                    for t in range(max(0, num - 1 - T), num - 1):
                        for i in range(len(mess[t])):
                            old_car = mess[t][i]
                            if old_car[5] == True or old_car[4] == 0:
                                continue
                            if superposition(car_x, car_y, car_w, car_h, old_car[0], old_car[1], old_car[2], old_car[3]) >= max_area:
                                min_t, min_i, max_area = t, i, superposition(car_x, car_y, car_w, car_h, old_car[0], old_car[1], old_car[2], old_car[3])
                    if max_area <= Area:
                        for t in range(max(0, num - 1 - T), num - 1):
                            for i in range(len(mess[t])):
                                old_car = mess[t][i]
                                if old_car[5] == True:
                                    continue
                                if superposition(car_x, car_y, car_w, car_h, old_car[0], old_car[1], old_car[2], old_car[3]) >= max_area:
                                    min_t, min_i, max_area = t, i, superposition(car_x, car_y, car_w, car_h, old_car[0], old_car[1], old_car[2], old_car[3])

                    if max_area >= Area:
                        old_car = mess[min_t][min_i]
                        if old_car[4] == 0:
                            ID += 1
                            mess[min_t][min_i][4] = now_car[4] = ID
                        else:
                            now_car[4] = old_car[4]
                        mess[min_t][min_i][5] = True
                        # cross white line
                        if (now_car[4] not in cross) and (judge_side(old_car[0], old_car[1]) != judge_side(car_x, car_y)):
                            cross.add(now_car[4])
                            now_cross += 1
                            now_side_cross[which_side(car_x, car_y)] += 1
                            now_side_cross_sum[which_side(car_x, car_y)] += 1

                    now_mess.append(now_car)

                    car_color = hex_to_bgr("FF0000")
                    if now_car[4] in cross:
                        car_color = hex_to_bgr("000000")
                    else:
                        if judge_side(now_car[0], now_car[1]):
                            car_color = hex_to_bgr("00CCFF")
                        else:
                            car_color = hex_to_bgr("FF0000")

                    # 在帧上绘制矩形框标记车辆
                    frame = cv2.rectangle(frame, (int(row.xmin), int(row.ymin)),
                                          (int(row.xmax), int(row.ymax)),
                                          car_color, 2)
                    # 在矩形框的左上角显示车辆ID
                    cv2.putText(frame, f'ID: {now_car[4]}', (int(row.xmin), int(row.ymin) - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

                now_side_cross.append(now_cross)
                txt.append(now_side_cross.copy())
                mess.append(now_mess)
                print("frame = ", num, "ID =", ID, "Cross = ", len(cross), "Cross_side = ", now_side_cross_sum)
                # 在视频帧上显示当前车辆计数
                cv2.putText(frame, f'Total Car Count: {len(cross)}',
                            (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1,
                            (255, 255, 255), 2)

                # 绘制虚拟线
                cv2.line(frame, (point1x, point1y), (point2x, point2y), (0, 255, 0), 2)

                # 绘制车道线
                cv2.line(frame, (side1, 0), (side1, height), (128, 128, 128), 2)
                cv2.line(frame, (side2, 0), (side2, height), (128, 128, 128), 2)

                # 写入输出视频
                out.write(frame)  # 将处理后的帧写入输出视频

                # 显示视频帧
                cv2.imshow('Frame', frame)

                # 按'z'键退出
                if cv2.waitKey(1) & 0xFF == ord('z'):
                    break

            # 释放资源
            cap.release()  # 释放视频对象
            out.release()  # 释放输出视频对象
            cv2.destroyAllWindows()  # 关闭所有OpenCV窗口

            # 输出总车辆计数
            print(f'Total Car Count: {len(cross)}')  # 打印总车辆计数

            with open(txt_path, 'w') as file:
                for item in txt:
                    for item2 in item:
                        file.write(f"{item2} ")
                    file.write("\n")

            print(f"处理完成: {video_path} -> {txt_path}")