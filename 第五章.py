def main():
    s = input("请输入一个字符串：")
    letters = 0
    digits = 0
    spaces = 0
    others = 0

    for char in s:
        if char.isalpha():
            letters += 1
        elif char.isdigit():
            digits += 1
        elif char.isspace():
            spaces += 1
        else:
            others += 1

    print("英文字母：", letters)
    print("数字：", digits)
    print("空格：", spaces)
    print("其他字符：", others)


if __name__ == '__main__':
    main()