import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import PolynomialFeatures

# 读取表格
df = pd.read_excel('坐标/2.1.xlsx')

# 计算前后轮中心点坐标
df['center_x'] = (df['前轮x'] + df['后轮x']) / 2
df['center_y'] = (df['前轮y'] + df['后轮y']) / 2

# 计算前后轮的像素欧拉距离
df['distance'] = np.sqrt((df['前轮x'] - df['后轮x'])**2 + (df['前轮y'] - df['后轮y'])**2)

# 假设这些车的实际前后距离都是2.5m
actual_distance = 2.5

# 定义比例系数k=现实/画面
df['k'] = actual_distance / df['distance']

# 使用多项式特征进行拟合
X = df[['center_x', 'center_y']]
y = df['k']

# 创建多项式特征
poly = PolynomialFeatures(degree=2, include_bias=False)
X_poly = poly.fit_transform(X)

# 线性回归模型
reg = LinearRegression().fit(X_poly, y)

# 打印回归系数和截距
print(f"Regression coefficients: {reg.coef_}")
print(f"Intercept: {reg.intercept_}")

# 获取回归系数和截距
coefficients = reg.coef_
intercept = reg.intercept_

# 获取回归系数和截距
coefficients = reg.coef_
intercept = reg.intercept_

# 打印回归方程
equation = (
    f"k = {intercept:.10e} + "
    f"{coefficients[0]:.10e} * x + "
    f"{coefficients[1]:.10e} * y + "
    f"{coefficients[2]:.10e} * x**2 + "
    f"{coefficients[3]:.10e} * y**2 + "
    f"{coefficients[4]:.10e} * x * y"
)

print("Regression equation:")
print(equation)




# 计算R2和MSE
y_pred = reg.predict(X_poly)
r2 = reg.score(X_poly, y)
mse = mean_squared_error(y, y_pred)

print(f"R^2: {r2}")
print(f"MSE: {mse}")

# 绘制三维图形和回归平面
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.scatter(df['center_x'], df['center_y'], df['k'], c='r', marker='o')
ax.set_xlabel('Center X')
ax.set_ylabel('Center Y')
ax.set_zlabel('Scale Factor k')

# 绘制回归平面
x_surf, y_surf = np.meshgrid(np.linspace(df['center_x'].min(), df['center_x'].max(), 100),
                             np.linspace(df['center_y'].min(), df['center_y'].max(), 100))
x_surf_flat = x_surf.ravel()
y_surf_flat = y_surf.ravel()
z_surf = reg.predict(poly.transform(np.c_[x_surf_flat, y_surf_flat])).reshape(x_surf.shape)

ax.plot_surface(x_surf, y_surf, z_surf, color='b', alpha=0.3)

plt.show()
