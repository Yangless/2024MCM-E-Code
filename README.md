![](https://vanilla-picture-with-picgo.oss-cn-shenzhen.aliyuncs.com/img-from-picgo/20240922-205348.png)

2024年数学建模研究生赛E题从视频中提取数据的代码。主要包括三个部分：车流量计算、各车道车流量计算和平均速度计算。主要讲述了代码的使用方法，包括需要修改的参数和文件路径，以及一些特殊情况的处理方法。同时还提供了参数估计和绘图的相关代码，以及如何根据不同视频视角调整代码。

[代码链接](https://github.com/hsh778205/2024-MCM-Huawei-Cup-E-Data-Extraction-Code)

# 2024“华为杯”数模研赛E数据提取代码

**首先需要将所有视频文件直接复制到文件夹目录下**

## 计算车流量

核心代码为`1.py`，运行代码会生成`x.x.txt`，然后使用`1-draw.py`读取txt，绘制折线图

需要修改内容如下：

**第8行**

```python
# 导入视频
txt_name='4.2.txt'
video_path = '4.2.mp4'  # 视频文件路径

```

修改对应的路径、视频编号。

**第31行**

```python
# 设定通过线的位置
point2x=0
point2y=int(height*0.50)
point1x=width
point1y=int(height*0.45)
```

这是检测线的个端点，**合适的参数**请查看`参数记录.txt`的前半部分

**1-draw.txt**中的**第6行**

```python
file_path = '1.1.txt'
```

修改成你需要绘制的视频编号

**1-draw.txt**中的**第31行**

```python
window_size = 5
```

可稍作修改，建议5~20之间

## 各车道车流量计算

核心代码为`三车道.py`，绘图代码为`三车道-draw.py`

相比于普通的车流量计算，还需要修改车道线的划分。

**第38行**

```python
# 车道划分
side1=int(width*0.25)
side2=int(width*0.4)
```

需要调整参数。**合适的参数**也在`最佳参数.txt`中，如：

```
1
point1x=0
point1y=int(height*0.2)
point2x=width
point2y=int(height*0.5)

0.25 0.4
```

表示1系列视频需要调整两个划分线为0.25和0.4

**三车道draw**中的**第46行**

```python
plt.plot(smoothed_total, label='总车流量')
plt.plot(smoothed_lane3, label='快车道车流量')
plt.plot(smoothed_lane2, label='慢车道车流量')
plt.plot(smoothed_lane1, label='应急车道车流量')
```

由于拍摄视角原因，可能需要交换“应急车道”和“快车道”，即变成

```python
plt.plot(smoothed_total, label='总车流量')
plt.plot(smoothed_lane1, label='快车道车流量')
plt.plot(smoothed_lane2, label='慢车道车流量')
plt.plot(smoothed_lane3, label='应急车道车流量')
```

以画出图例正确的折线图

## 计算平均速度

### 估算k

使用代码`标点.py`启动视频，空格暂停，鼠标左键在画面中点击以生成坐标。请点击每辆车的前后两个轮子的位置。生成每行四个数据，复制到`坐标\x.x.xlsx`中，注意excel需要保留表头。

使用代码`估算k.py`读取excel表格，使用多项式以拟合函数$k(x,y)$。

上述操作**可以跳过**，比较好的表达式已经保存在`参数估计.txt`的后半部分

### 计算速度

核心代码为`速度.py`，绘图代码为`速度-draw.py`

对于不同视角的视频，将k的表达式复制到核心代码的**第12行**

```python
def calc_k(x,y):
    k = 3.5060369468e-01 + 2.4844164330e-04 * x + -1.6744365346e-03 * y + 4.2032717049e-07 * x ** 2 + -1.3060908122e-06 * y ** 2 + 2.4295921693e-06 * x * y
    return k
```

替换其中的k的表达式。

由于是计算速度，所以不需要管检测线和车道线，也就是说只需要修改**视频文件路径**和**k的表达式**即可。