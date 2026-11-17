"""
def greet(name):
    print(f"123{name},456")

greet("L.W.Yu")








devices = [
    {"host": "10.10.10.1", "device_name": "L.W.Yu01", "username": "python", "password": "123456"},
    {"host": "10.10.10.2", "device_name": "L.W.Yu02", "username": "python", "password": "123456"},
    {"host": "10.10.10.3", "device_name": "L.W.Yu03", "username": "python", "password": "123456"},
]


def configure_on_switch(devices):
    for device in devices:
        print(f"本主机的主机名是：{device['device_name']}，本主机的地址是：{device['host']}")


configure_on_switch(devices)
"""


def divide_by_input():
    try:
        num = int(input("请输入一个整数："))
        result = 10 / num
        print("除法结果为：", result)
    except ValueError:
        print("输入的值不是整数！")
    except ZeroDivisionError:
        print("输入的值不能为 0！")
    else:
        print("输入的值格式正确！")


divide_by_input()
