def fact_recursive(n):
    """递归方式实现阶乘"""
    if n == 0 or n == 1:
        return 1
    else:
        return n * fact_recursive(n - 1)


def fact_iterative(n):
    """非递归方式实现阶乘"""
    if n < 0:
        return None  # 阶乘只定义在非负整数
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def main():
    """主函数，测试阶乘函数"""
    try:
        n = int(input("请输入整数n(n>=0): "))
        if n < 0:
            print("输入错误：n必须大于等于0")
            return

        # 使用递归方式计算
        result_recursive = fact_recursive(n)
        print(f"递归方式: {n}! = {result_recursive}")

        # 使用非递归方式计算
        result_iterative = fact_iterative(n)
        print(f"非递归方式: {n}! = {result_iterative}")

        # 验证两种方法结果是否一致
        if result_recursive == result_iterative:
            print("✓ 两种方法计算结果一致")
        else:
            print("✗ 两种方法计算结果不一致")

    except ValueError:
        print("输入错误：请输入整数")


# 运行测试
if __name__ == "__main__":
    main()