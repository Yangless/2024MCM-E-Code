import cv2

click_count=1

# 视频文件路径
video_path = '2.1.mp4'

# 打开视频文件
cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Could not open video.")
else:
    cv2.namedWindow('Video')

    # 定义鼠标事件回调函数
    def show_mouse_coordinates(event, x, y, flags, param):
        global click_count  # 声明为全局变量
        if event == cv2.EVENT_LBUTTONDOWN:  # 检测左键点击
            # print(f"Mouse click at: ({x}, {y})")
            print(f"{x}\t{y}\t",end="")
            if click_count % 2 == 0:
                print("")
            click_count+=1

    cv2.setMouseCallback('Video', show_mouse_coordinates)

    paused = False

    while cap.isOpened():
        if not paused:
            ret, frame = cap.read()
            if not ret:
                print("Reached end of video.")
                break

            cv2.imshow('Video', frame)

        key = cv2.waitKey(30) & 0xFF
        if key == ord(' '):  # 空格键暂停/继续
            paused = not paused
        elif key == ord('q'):  # 按 'q' 退出
            break

    cap.release()
    cv2.destroyAllWindows()
