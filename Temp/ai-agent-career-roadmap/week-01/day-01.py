# week-01/day-01.py

# Python基础练习 - Day 01

# 1. 变量和数据类型
print("=== 变量和数据类型 ===")

# 整数
age = 30
print(f"我的年龄: {age} (类型: {type(age)})")

# 浮点数
height = 1.75
print(f"我的身高: {height} 米")

# 字符串
name = "AI Agent 设计师"
print(f"我的名字: {name}")

# 布尔值
is_student = True
print(f"我是学生: {is_student}")

# 列表
skills = ["Python", "FastAPI", "React", "Git"]
print(f"我的技能: {skills}")

# 元组
favorite_frameworks = ("LangChain", "CrewAI", "AutoGPT")
print(f"我喜欢的框架: {favorite_frameworks}")

# 字典
experience = {
    "Python": "熟练",
    "FastAPI": "中级",
    "PostgreSQL": "基础",
    "Docker": "了解"
}
print(f"我的技术栈: {experience}")

# 运算符
print("\n=== 运算符 ===")
a, b = 10, 5
print(f"{a} + {b} = {a + b}")
print(f"{a} - {b} = {a - b}")
print(f"{a} * {b} = {a * b}")
print(f"{a} / {b} = {a / b}")
print(f"{a} % {b} = {a % b}")

# 控制流
print("\n=== 控制流 ===")

# if-else
score = 85
if score >= 90:
    print("优秀！")
elif score >= 80:
    print("良好")
elif score >= 70:
    print("及格")
else:
    print("需要努力")

# while 循环
count = 1
while count <= 5:
    print(f"计数: {count}")
    count += 1

# for 循环
print("\n我的技能列表:")
for skill in skills:
    print(f"  - {skill}")

# 列表推导式
even_numbers = [x for x in range(1, 11) if x % 2 == 0]
print(f"偶数列表: {even_numbers}")

# 函数
def greet(name, age):
    return f"你好, {name}! 今年 {age} 岁了"

message = greet("李明", 28)
print(message)

# 异常处理
print("\n=== 异常处理 ===")
try:
    result = 10 / 0
except ZeroDivisionError:
    print("错误: 不能除以0")
except Exception as e:
    print(f"发生错误: {e}")

# 结束
print("\n=== 练习完成 ===")
print("Day 01 Python基础练习已完成！")