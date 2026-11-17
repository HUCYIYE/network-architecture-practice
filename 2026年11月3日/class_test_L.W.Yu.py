"""
class Phone:
#          ↑无父类则不需要括号
    def __init__(self, brand, model, color, battery):
        self.brand = brand
        self.model = model
        self.color = color
        self.battery = battery

    def call(self, phone_number):
        print(f"正在向电话号码{phone_number}拨号...")

    def introduce(self):
        print(f"我的品牌是：{self.brand}")
        print(f"我的型号是：{self.model}")
        print(f"我的颜色是：{self.color}")
        print(f"我的电量还有百分之：{self.battery}")


test1 = Phone("test", "test11", "test12", 13)
test1.call("14")
test1.introduce()
"""
