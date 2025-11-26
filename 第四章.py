def generate_pascal_triangle(n):
    """生成杨辉三角的前n行"""
    triangle = []
    for i in range(n):
        row = [1] * (i + 1)
        if i > 1:
            for j in range(1, i):
                row[j] = triangle[i - 1][j - 1] + triangle[i - 1][j]
        triangle.append(row)
    return triangle


def print_pascal_triangle(triangle):
    """格式化打印杨辉三角"""
    n = len(triangle)
    # 计算最后一行字符串长度，用于居中
    max_width = len(' '.join(map(str, triangle[-1])))

    for row in triangle:
        # 将每行数字转换为字符串并用空格连接
        row_str = ' '.join(map(str, row))
        # 居中对齐打印
        print(row_str.center(max_width))


# 主程序
n = int(input("请输入杨辉三角的行数: "))
pascal_triangle = generate_pascal_triangle(n)
print_pascal_triangle(pascal_triangle)