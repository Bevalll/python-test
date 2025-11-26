# 知识点1：模块定义和函数编写
import math


def circle_area(radius):
    """
    计算圆的面积
    公式：π * r²
    """
    return math.pi * radius ** 2


def sphere_volume(radius):
    """
    计算球体体积
    公式：(4/3) * π * r³
    """
    return (4 / 3) * math.pi * radius ** 3


# 知识点2：模块的独立运行检测
if __name__ == "__main__":
    # 知识点3：用户输入和类型转换
    radius = float(input("请输入半径："))

    # 知识点4：函数调用
    area = circle_area(radius)
    volume = sphere_volume(radius)

    # 知识点5：格式化输出，保留两位小数
    print(f"圆的面积为：{area:.2f}")
    print(f"球的体积为：{volume:.2f}")