# week-01/day-02.py

# Python基础练习 - Day 02: 函数和类

# 1. 函数
print("=== 函数 ===")

def calculate_age(birth_year, current_year=2024):
    """计算年龄"""
    return current_year - birth_year

age = calculate_age(1994)
print(f"2024年出生于1994年的人年龄: {age}")

def greet(name, title="先生"):
    """带默认参数的问候函数"""
    return f"您好, {title} {name}!"

print(greet("李明"))
print(greet("张三", "博士"))

def multiply(*args):
    """可变参数"""
    result = 1
    for num in args:
        result *= num
    return result

print(f"3*4*5 = {multiply(3, 4, 5)}")

def describe_person(**kwargs):
    """关键字参数"""
    return f"{kwargs.get('name', '未知')} 是 {kwargs.get('age', '?')} 岁, 住在 {kwargs.get('city', '未知')}"

print(describe_person(name="王五", age=35, city="上海"))

# 2. 类
print("\n=== 类和对象 ===")

class Person:
    """人"""
    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def introduce(self):
        return f"我是{self.name}, {self.age}岁, 性别{self.gender}"
    
    def birthday(self):
        self.age += 1
        return f"生日快乐! 现在是{self.age}岁"

# 实例化
person1 = Person("张三", 30, "男")
print(person1.introduce())

person2 = Person("李四", 28, "女")
print(person2.introduce())

# 调用方法
print(person1.birthday())
print(person1.introduce())

# 继承
class Student(Person):
    def __init__(self, name, age, gender, student_id):
        super().__init__(name, age, gender)
        self.student_id = student_id
    
    def study(self):
        return f"{self.name}正在学习"

student = Student("王五", 20, "男", "20240001")
print(student.introduce())
print(student.study())

# 3. 练习
print("\n=== 练习 ===")

# 计算器类
class Calculator:
    def __init__(self):
        self.result = 0
    
    def add(self, a, b):
        self.result = a + b
        return self.result
    
    def subtract(self, a, b):
        self.result = a - b
        return self.result
    
    def multiply(self, a, b):
        self.result = a * b
        return self.result
    
    def divide(self, a, b):
        if b == 0:
            raise ValueError("不能除以0")
        self.result = a / b
        return self.result

calc = Calculator()
print(f"1 + 2 = {calc.add(1, 2)}")
print(f"5 - 3 = {calc.subtract(5, 3)}")
print(f"4 * 5 = {calc.multiply(4, 5)}")
print(f"10 / 2 = {calc.divide(10, 2)}")