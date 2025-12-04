import json
from user import User
from device import Device, MoodLight
from logger import log


class SmartHome:
    """
    智能家居系统主类：
    - 维护所有用户
    - 维护所有设备
    - 支持增加用户、设备、共享
    - 支持数据保存/加载
    """

    def __init__(self):
        self.users = {}      # {用户名: User对象}
        self.devices = {}    # {设备ID: Device对象}
        self.load_data()     # 启动时自动尝试加载数据

    # ---------------------------
    # 用户管理
    # ---------------------------
    def add_user(self, username):
        if username not in self.users:
            self.users[username] = User(username)
            log(f"添加用户 {username}")
        else:
            print("用户已存在。")

    # ---------------------------
    # 设备增加
    # ---------------------------
    def add_device(self, device_type, device_id, owner):
        if owner not in self.users:
            print("用户不存在，不能绑定设备。")
            return

        # 根据类型创建不同设备
        if device_type == "moodlight":
            device = MoodLight(device_id)
        else:
            device = Device(device_type, device_id)

        # 添加设备
        self.devices[device_id] = device
        self.users[owner].add_device(device_id)

        log(f"添加设备 {device_type}, ID={device_id}, Owner={owner}")
        print(f"设备 {device_type} 添加成功。")

    # ---------------------------
    # 显示所有设备
    # ---------------------------
    def show_devices(self):
        for d in self.devices.values():
            print(d)

    # ---------------------------
    # 共享设备
    # ---------------------------
    def share_device(self, device_id, username):
        if device_id not in self.devices:
            print("设备不存在。")
            return
        if username not in self.users:
            print("用户不存在。")
            return

        self.devices[device_id].share(username)
        log(f"设备 {device_id} 被共享给用户 {username}")

    # ---------------------------
    # 数据保存 / 加载
    # ---------------------------
    def save_data(self):
        """保存系统到 data.json"""
        data = {
            "users": {u: self.users[u].__dict__ for u in self.users},
            "devices": {
                d: {
                    "name": self.devices[d].name,
                    "device_id": self.devices[d].device_id,
                    "status": self.devices[d].status,
                    "attributes": self.devices[d].attributes,
                    "shared_users": self.devices[d].shared_users,
                }
                for d in self.devices
            }
        }

        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

        log("系统数据已保存。")

    def load_data(self):
        """启动时加载数据"""
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)

            # 还原用户
            for username in data["users"]:
                self.users[username] = User(username)
                self.users[username].devices = data["users"][username]["devices"]

            # 还原设备
            for device_id, dev_data in data["devices"].items():
                if dev_data["name"] == "MoodLight":
                    device = MoodLight(device_id)
                else:
                    device = Device(dev_data["name"], device_id)

                device.status = dev_data["status"]
                device.attributes = dev_data["attributes"]
                device.shared_users = dev_data["shared_users"]

                self.devices[device_id] = device

            print("系统数据已加载。")

        except FileNotFoundError:
            print("首次启动，无保存数据。")
