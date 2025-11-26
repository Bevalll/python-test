# 知识点1：类的定义和继承
# 定义一个基类 Income，表示普通收入
class Income:
    def __init__(self, amount):
        self.amount = amount  # 收入金额

    # 知识点2：方法定义
    def getTax(self):
        # 普通收入税率20%
        return self.amount * 0.2

# 知识点3：类的继承
# Salary 类继承自 Income 类
class Salary(Income):
    def getTax(self):
        # 工资收入超过5000元的部分税率10%，低于5000不收税
        if self.amount <= 5000:
            return 0
        else:
            return (self.amount - 5000) * 0.1

# SpecialAllowance 类继承自 Income 类
class SpecialAllowance(Income):
    def getTax(self):
        # 津贴收入不用交税
        return 0

# 知识点4：组合模式
# TotalTax 类用于管理多种收入类型并计算总税收
class TotalTax:
    def __init__(self):
        # 知识点5：列表的使用
        self.incomes = []  # 存储收入对象的列表

    # 知识点6：方法定义，用于添加收入对象
    def addIncome(self, income):
        self.incomes.append(income)

    # 知识点7：方法定义，计算总税收
    def getTotalTax(self):
        total_tax = 0
        # 遍历所有收入对象，累加税收
        for income in self.incomes:
            total_tax += income.getTax()
        return total_tax

# 知识点8：实例化对象和方法调用
# 创建 TotalTax 对象
tax = TotalTax()
# 创建不同类型的收入对象
income = Income(3000)
salary = Salary(8500)
specialAllowance = SpecialAllowance(10550)
# 将收入对象添加到 TotalTax 对象中
tax.addIncome(income)
tax.addIncome(salary)
tax.addIncome(specialAllowance)
# 打印总税收
print("Total tax: ", tax.getTotalTax())