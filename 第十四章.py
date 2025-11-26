import calendar
import locale


def print_calendar_2023():
    """
    打印2023年日历 - 按照题目参考代码
    """
    print("2023年日历")
    print("=" * 60)

    # 创建文本日历对象
    textcal = calendar.TextCalendar()

    # 打印2023年一年的日历
    textcal.pryear(2023)


def print_calendar_with_locale():
    """
    使用本地化设置打印日历
    """
    print("\n2023年日历（本地化版本）")
    print("=" * 60)

    try:
        # 获取当前系统的locale（本地化配置）
        loc = locale.getlocale()
        print(f"当前系统locale: {loc}")

        # 创建本地化文本日历
        localtextcal = calendar.LocaleTextCalendar(locale=loc)

        # 打印2023年日历
        localtextcal.pryear(2023)

    except Exception as e:
        print(f"本地化版本失败: {e}")
        print("使用默认版本:")
        textcal = calendar.TextCalendar()
        textcal.pryear(2023)


def print_calendar_custom():
    """
    自定义格式打印日历
    """
    print("\n2023年日历（自定义格式）")
    print("=" * 60)

    # 创建文本日历，设置周一为一周的第一天
    textcal = calendar.TextCalendar(firstweekday=0)  # 0=Monday

    # 使用更紧凑的格式
    textcal.pryear(2023, w=2, l=1, c=6, m=3)


def ndays(y, m):
    """
    返回指定年月的天数
    对应题目第三题的要求
    """
    return calendar.monthrange(y, m)[1]


def test_ndays():
    """
    测试ndays函数
    """
    print("\n测试ndays函数:")
    print("=" * 30)

    # 测试用例
    test_cases = [
        (2023, 1),  # 1月31天
        (2023, 2),  # 2月28天（平年）
        (2023, 4),  # 4月30天
        (2020, 2),  # 2020年2月29天（闰年）
        (2023, 12),  # 12月31天
    ]

    for year, month in test_cases:
        days = ndays(year, month)
        month_name = calendar.month_name[month]
        print(f"{year}年{month}月 ({month_name}) 有 {days} 天")


def interactive_ndays():
    """
    交互式测试ndays函数
    """
    print("\n交互式测试ndays函数:")
    print("=" * 40)

    while True:
        try:
            print("\n请输入年份和月份（输入0退出）:")
            year = int(input("年份: "))
            if year == 0:
                break

            month = int(input("月份: "))
            if month == 0:
                break

            if month < 1 or month > 12:
                print("月份必须在1-12之间！")
                continue

            days = ndays(year, month)
            month_name = calendar.month_name[month]
            is_leap = "闰年" if calendar.isleap(year) else "平年"

            print(f"{year}年({is_leap}) {month}月({month_name}) 有 {days} 天")

        except ValueError:
            print("请输入有效的数字！")
        except Exception as e:
            print(f"发生错误: {e}")


def main():
    """
    主函数 - 整合所有功能
    """
    print("Python日期时间处理程序")
    print("=" * 50)

    while True:
        print("\n请选择功能:")
        print("1. 打印2023年日历（基础版本）")
        print("2. 打印2023年日历（本地化版本）")
        print("3. 打印2023年日历（自定义格式）")
        print("4. 测试ndays函数")
        print("5. 交互式测试ndays函数")
        print("6. 退出程序")

        choice = input("请输入选择 (1-6): ").strip()

        if choice == '1':
            print_calendar_2023()
        elif choice == '2':
            print_calendar_with_locale()
        elif choice == '3':
            print_calendar_custom()
        elif choice == '4':
            test_ndays()
        elif choice == '5':
            interactive_ndays()
        elif choice == '6':
            print("程序已退出！")
            break
        else:
            print("无效选择，请重新输入！")


# 直接运行题目要求的基础版本
if __name__ == "__main__":
    # 运行基础版本（符合题目第二题要求）
    print_calendar_2023()

    # 运行第三题测试
    test_ndays()

    # 如果想要交互式功能，可以取消下面的注释
    # main()