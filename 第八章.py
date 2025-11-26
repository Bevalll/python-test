def gcd_iterative(a, b):
    """非递归方式实现最大公约数"""
    # 确保a >= b
    if a < b:
        a, b = b, a

    while b != 0:
        a, b = b, a % b
    return a


def gcd_recursive(a, b):
    """递归方式实现最大公约数"""
    if b == 0:
        return a
    else:
        return gcd_recursive(b, a % b)


def lcm_iterative(a, b):
    """非递归方式实现最小公倍数"""
    # 使用公式：LCM(a,b) = |a*b| / GCD(a,b)
    gcd_value = gcd_iterative(a, b)
    return abs(a * b) // gcd_value if gcd_value != 0 else 0


def lcm_recursive(a, b):
    """递归方式实现最小公倍数"""
    # 使用公式：LCM(a,b) = |a*b| / GCD(a,b)
    gcd_value = gcd_recursive(a, b)
    return abs(a * b) // gcd_value if gcd_value != 0 else 0


def main():
    """主函数，测试GCD和LCM函数"""
    try:
        # 获取用户输入
        num1 = int(input("请输入第一个整数: "))
        num2 = int(input("请输入第二个整数: "))

        # 非递归方式计算
        gcd_iter = gcd_iterative(num1, num2)
        lcm_iter = lcm_iterative(num1, num2)

        # 递归方式计算
        gcd_recur = gcd_recursive(num1, num2)
        lcm_recur = lcm_recursive(num1, num2)

        # 显示结果
        print(f"\n非递归方式:")
        print(f"GCD({num1}, {num2}) = {gcd_iter}")
        print(f"LCM({num1}, {num2}) = {lcm_iter}")

        print(f"\n递归方式:")
        print(f"GCD({num1}, {num2}) = {gcd_recur}")
        print(f"LCM({num1}, {num2}) = {lcm_recur}")

        # 验证两种方法结果是否一致
        if gcd_iter == gcd_recur and lcm_iter == lcm_recur:
            print(f"\n✓ 两种方法计算结果一致")
        else:
            print(f"\n✗ 两种方法计算结果不一致")

    except ValueError:
        print("输入错误：请输入整数")
    except ZeroDivisionError:
        print("错误：不能输入0")


# 运行测试
if __name__ == "__main__":
    main()