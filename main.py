import turtle

# 设置画笔速度
turtle.speed(5)

# 绘制正六边形
for _ in range(6):
    turtle.fd(100)  # 向前移动100像素
    turtle.left(60)  # 左转60度（正六边形的外角为60度）

# 保持窗口打开
turtle.done()