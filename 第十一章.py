def is_anagram_method1(s1, s2):
    """
    方法一：逐字符检查
    时间复杂度：O(n²)
    """
    if len(s1) != len(s2):
        return False

    # 将字符串2转换为列表，便于删除元素
    s2_list = list(s2)

    for char1 in s1:
        found = False
        for i in range(len(s2_list)):
            if s2_list[i] == char1:
                found = True
                # 删除找到的字符，避免重复匹配
                s2_list.pop(i)
                break
        if not found:
            return False

    return len(s2_list) == 0


def is_anagram_method2(s1, s2):
    """
    方法二：排序比较
    时间复杂度：O(n log n)
    """
    if len(s1) != len(s2):
        return False

    # 将字符串转换为列表并排序
    sorted_s1 = sorted(s1)
    sorted_s2 = sorted(s2)

    return sorted_s1 == sorted_s2


def is_anagram_method3(s1, s2):
    """
    方法三：计数比较（使用字典）
    时间复杂度：O(n)
    """
    if len(s1) != len(s2):
        return False

    # 统计字符串1中每个字符的出现次数
    count_dict1 = {}
    for char in s1:
        count_dict1[char] = count_dict1.get(char, 0) + 1

    # 统计字符串2中每个字符的出现次数
    count_dict2 = {}
    for char in s2:
        count_dict2[char] = count_dict2.get(char, 0) + 1

    # 比较两个字典是否相同
    return count_dict1 == count_dict2


def is_anagram_method4(s1, s2):
    """
    方法四：使用Counter对象
    时间复杂度：O(n)
    """
    from collections import Counter

    if len(s1) != len(s2):
        return False

    return Counter(s1) == Counter(s2)


def is_anagram_method5(s1, s2):
    """
    方法五：使用固定大小的数组进行计数（优化版本）
    时间复杂度：O(n)
    空间复杂度：O(1) - 因为数组大小固定为26
    """
    if len(s1) != len(s2):
        return False

    # 创建大小为26的数组，用于统计26个小写字母的出现次数
    count = [0] * 26

    # 统计字符串1中每个字符的出现次数
    for char in s1:
        count[ord(char) - ord('a')] += 1

    # 统计字符串2中每个字符的出现次数并同时比较
    for char in s2:
        index = ord(char) - ord('a')
        count[index] -= 1
        if count[index] < 0:
            return False

    # 检查所有计数是否归零
    return all(c == 0 for c in count)


def test_anagram_functions():
    """
    测试函数
    """
    test_cases = [
        ("python", "typhon", True),
        ("heart", "earth", True),
        ("triangle", "integral", True),
        ("listen", "silent", True),
        ("hello", "world", False),
        ("abc", "abcd", False),
        ("aabb", "abab", True),
        ("test", "tset", True),
        ("apple", "pale", False)
    ]

    methods = [
        ("逐字符检查", is_anagram_method1),
        ("排序比较", is_anagram_method2),
        ("字典计数", is_anagram_method3),
        ("Counter对象", is_anagram_method4),
        ("数组计数", is_anagram_method5)
    ]

    print("变位词检测测试结果：")
    print("=" * 60)

    for method_name, method_func in methods:
        print(f"\n{method_name}方法：")
        correct_count = 0
        total_count = len(test_cases)

        for s1, s2, expected in test_cases:
            result = method_func(s1, s2)
            status = "✓" if result == expected else "✗"
            if result == expected:
                correct_count += 1
            print(f"  {status} '{s1}' vs '{s2}': {result} (期望: {expected})")

        print(f"  正确率: {correct_count}/{total_count}")


def main():
    """
    主函数：从键盘接收输入并判断是否为变位词
    """
    print("变位词检测程序")
    print("=" * 30)

    while True:
        try:
            # 从键盘接收输入
            s1 = input("\n请输入第一个字符串（输入quit退出）: ").strip().lower()
            if s1 == 'quit':
                break

            s2 = input("请输入第二个字符串: ").strip().lower()

            # 验证输入（只包含小写字母）
            if not s1.isalpha() or not s2.isalpha():
                print("错误：请输入只包含字母的字符串")
                continue

            print(f"\n检测结果：")
            print(f"字符串1: '{s1}'")
            print(f"字符串2: '{s2}'")

            # 使用所有方法进行检测
            methods = [
                ("逐字符检查", is_anagram_method1),
                ("排序比较", is_anagram_method2),
                ("字典计数", is_anagram_method3),
                ("Counter对象", is_anagram_method4),
                ("数组计数", is_anagram_method5)
            ]

            results = []
            for method_name, method_func in methods:
                result = method_func(s1, s2)
                results.append((method_name, result))
                print(f"  {method_name}: {'是变位词' if result else '不是变位词'}")

            # 检查所有方法结果是否一致
            if all(result for _, result in results) or not any(result for _, result in results):
                final_result = "是变位词" if results[0][1] else "不是变位词"
                print(f"\n最终结论: {final_result}")
            else:
                print(f"\n警告：不同方法的检测结果不一致！")

        except KeyboardInterrupt:
            print("\n\n程序已退出")
            break
        except Exception as e:
            print(f"发生错误: {e}")


def complexity_analysis():
    """
    算法复杂度分析
    """
    print("\n" + "=" * 60)
    print("算法复杂度分析：")
    print("=" * 60)

    complexities = [
        ("方法一：逐字符检查", "O(n²)", "O(n)", "对于每个字符，都需要在另一个字符串中线性搜索"),
        ("方法二：排序比较", "O(n log n)", "O(n)", "排序的时间复杂度主导"),
        ("方法三：字典计数", "O(n)", "O(k)", "k为字符集大小，这里k=26"),
        ("方法四：Counter对象", "O(n)", "O(k)", "内部实现类似字典计数"),
        ("方法五：数组计数", "O(n)", "O(1)", "使用固定大小的数组，空间复杂度为常数")
    ]

    print(f"{'方法':<20} {'时间复杂度':<12} {'空间复杂度':<12} {'说明'}")
    print("-" * 60)
    for method, time_comp, space_comp, desc in complexities:
        print(f"{method:<20} {time_comp:<12} {space_comp:<12} {desc}")


if __name__ == "__main__":
    # 运行测试用例
    test_anagram_functions()

    # 复杂度分析
    complexity_analysis()

    # 主程序
    main()