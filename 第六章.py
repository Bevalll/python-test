def analyze_blood_pressure():
    # 读取血压记录文件
    try:
        with open('xueyajilu.txt', 'r', encoding='utf-8') as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("错误：找不到血压记录文件 'xueyajilu.txt'")
        return

    # 初始化数据列表
    left_systolic = []  # 左臂高压
    left_diastolic = []  # 左臂低压
    right_systolic = []  # 右臂高压
    right_diastolic = []  # 右臂低压
    heart_rates = []  # 心率

    # 解析数据
    for line in lines:
        parts = line.strip().split(',')
        if len(parts) >= 6:
            left_systolic.append(int(parts[1]))
            left_diastolic.append(int(parts[2]))
            right_systolic.append(int(parts[3]))
            right_diastolic.append(int(parts[4]))
            heart_rates.append(int(parts[5]))

    # 计算左臂和右臂的各项指标
    left_stats = {
        'max_systolic': max(left_systolic),
        'max_diastolic': max(left_diastolic),
        'avg_pulse_pressure': sum([s - d for s, d in zip(left_systolic, left_diastolic)]) / len(left_systolic),
        'avg_systolic': sum(left_systolic) / len(left_systolic),
        'avg_diastolic': sum(left_diastolic) / len(left_diastolic)
    }

    right_stats = {
        'max_systolic': max(right_systolic),
        'max_diastolic': max(right_diastolic),
        'avg_pulse_pressure': sum([s - d for s, d in zip(right_systolic, right_diastolic)]) / len(right_systolic),
        'avg_systolic': sum(right_systolic) / len(right_systolic),
        'avg_diastolic': sum(right_diastolic) / len(right_diastolic)
    }

    # 输出对比表
    print("项目        左臂        右臂")
    print("-" * 30)
    print(f"高压最大值  {left_stats['max_systolic']:<11} {right_stats['max_systolic']}")
    print(f"低压最大值  {left_stats['max_diastolic']:<11} {right_stats['max_diastolic']}")
    print(f"压差平均值  {left_stats['avg_pulse_pressure']:<11.2f} {right_stats['avg_pulse_pressure']:.2f}")
    print(f"高压平均值  {left_stats['avg_systolic']:<11.2f} {right_stats['avg_systolic']:.2f}")
    print(f"低压平均值  {left_stats['avg_diastolic']:<11.2f} {right_stats['avg_diastolic']:.2f}")
    print()

    # 比较左臂和右臂的指标
    left_higher_count = 0
    total_items = 5

    if left_stats['max_systolic'] > right_stats['max_systolic']:
        left_higher_count += 1
    if left_stats['max_diastolic'] > right_stats['max_diastolic']:
        left_higher_count += 1
    if left_stats['avg_pulse_pressure'] > right_stats['avg_pulse_pressure']:
        left_higher_count += 1
    if left_stats['avg_systolic'] > right_stats['avg_systolic']:
        left_higher_count += 1
    if left_stats['avg_diastolic'] > right_stats['avg_diastolic']:
        left_higher_count += 1

    # 输出结论
    if left_higher_count > total_items / 2:
        print("结论：左臂血压偏高")
    elif left_higher_count == total_items / 2:
        print("结论：左臂血压与右臂血压相当")
    else:
        print("结论：右臂血压偏高")

    # 输出心率平均值
    avg_heart_rate = sum(heart_rates) / len(heart_rates)
    print(f"心率平均值：{avg_heart_rate:.2f}")


# 运行程序
if __name__ == "__main__":
    analyze_blood_pressure()