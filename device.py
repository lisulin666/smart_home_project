import random

class Device:
    """
    设备类：所有智能家居设备的基础类
    """

    def __init__(self, name, device_id):
        self.name = name
        self.device_id = device_id
        self.status = "off"           # 初始状态：关闭
        self.attributes = {}          # 属性字典，例如亮度、温度
        self.shared_users = []        # 可访问此设备的用户（除了主人）

    def turn_on(self):
        """打开设备"""
        if self.status == "on":
            print(f"{self.name} 已经是开启状态。")
        else:
            self.status = "on"

    def turn_off(self):
        """关闭设备"""
        if self.status == "off":
            print(f"{self.name} 已经是关闭状态。")
        else:
            self.status = "off"

    def set_attr(self, key, value):
        """设置设备属性，例如亮度、温度"""
        self.attributes[key] = value

    def share(self, username):
        """把设备共享给其他用户"""
        if username not in self.shared_users:
            self.shared_users.append(username)

    def __repr__(self):
        """打印设备信息"""
        return f"{self.name}(ID={self.device_id}, 状态={self.status}, 属性={self.attributes})"
    import random

class MoodLight(Device):
    """
    创意设备：情绪灯，会随机变颜色
    """

    def __init__(self, device_id):
        super().__init__("MoodLight", device_id)
        self.attributes["color"] = "blue"

    def auto_change_color(self):
        """自动随机变换颜色"""
        colors = ["red", "blue", "green", "purple", "yellow"]
        self.attributes["color"] = random.choice(colors)
