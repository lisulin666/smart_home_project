import json
from automation import AutomationManager
from user import User
from device import (
    Device, Light, AirConditioner, DoorLock, Camera, 
    SmartCurtain, MusicPlayer, MoodLight
)
from logger import log


class SmartHome:
    """
    智能家居系统主类：
    - 维护所有用户和设备
    - 支持用户管理（添加、删除、查看）
    - 支持设备管理（添加、删除、控制、共享）
    - 支持数据保存/加载（JSON格式）
    - 集成自动化规则管理器
    """

    def __init__(self):
        self.users = {}      # {用户名: User对象}
        self.devices = {}    # {设备ID: Device对象}
        self.load_data()     # 启动时自动尝试加载数据
        self.automation = AutomationManager()  # 自动化规则管理器
        self.load_automation_rules()  # 加载自动化规则

    # ---------------------------
    # 用户管理
    # ---------------------------
    def add_user(self, username):
        """添加新用户"""
        if username not in self.users:
            self.users[username] = User(username)
            log(f"添加用户 {username}", username=username)
            print(f"用户 {username} 已创建。")
            return True
        else:
            print("用户已存在。")
            return False

    def remove_user(self, username):
        """删除用户（同时删除该用户拥有的所有设备）"""
        if username not in self.users:
            print("用户不存在。")
            return False
        
        # 删除该用户拥有的所有设备
        user_devices = self.users[username].devices.copy()
        for device_id in user_devices:
            self.remove_device(device_id)
        
        # 删除用户
        del self.users[username]
        log(f"删除用户 {username}", username=username)
        print(f"用户 {username} 及其所有设备已删除。")
        return True

    def list_users(self):
        """列出所有用户"""
        if not self.users:
            print("当前没有用户。")
            return []
        
        user_list = []
        for username in self.users:
            device_count = len(self.users[username].devices)
            user_list.append(f"{username} (拥有 {device_count} 个设备)")
            print(f"- {username} (拥有 {device_count} 个设备)")
        return user_list

    def get_user_devices(self, username):
        """
        获取用户的所有设备（包括自己拥有的和共享给他的）
        
        :param username: 用户名
        :return: 设备ID列表
        """
        if username not in self.users:
            return []
        
        # 用户自己拥有的设备
        own_devices = self.users[username].devices.copy()
        
        # 共享给该用户的设备
        shared_devices = []
        for device_id, device in self.devices.items():
            if username in device.shared_users:
                shared_devices.append(device_id)
        
        return {
            "own": own_devices,
            "shared": shared_devices,
            "all": own_devices + shared_devices
        }

    # ---------------------------
    # 设备管理
    # ---------------------------
    def add_device(self, device_type, device_id, owner):
        """
        添加设备
        
        :param device_type: 设备类型（light/aircon/doorlock/camera/curtain/musicplayer/moodlight）
        :param device_id: 设备ID
        :param owner: 设备所有者用户名
        :return: 是否添加成功
        """
        if device_id in self.devices:
            print(f"设备ID {device_id} 已存在。")
            return False
        
        if owner not in self.users:
            print("用户不存在，不能绑定设备。")
            return False

        # 根据类型创建不同设备
        device = self._create_device(device_type, device_id)
        if device is None:
            print(f"未知的设备类型: {device_type}")
            return False

        # 添加设备
        self.devices[device_id] = device
        self.users[owner].add_device(device_id)

        log(f"添加设备 {device_type}", device=device, username=owner, 
            extra_info={"device_id": device_id})
        print(f"设备 {device_type} (ID: {device_id}) 添加成功。")
        return True

    def _create_device(self, device_type, device_id):
        """根据设备类型创建设备对象"""
        device_type_lower = device_type.lower()
        
        if device_type_lower == "light":
            return Light(device_id)
        elif device_type_lower == "aircon":
            return AirConditioner(device_id)
        elif device_type_lower == "doorlock":
            return DoorLock(device_id)
        elif device_type_lower == "camera":
            return Camera(device_id)
        elif device_type_lower == "curtain":
            return SmartCurtain(device_id)
        elif device_type_lower == "musicplayer":
            return MusicPlayer(device_id)
        elif device_type_lower == "moodlight":
            return MoodLight(device_id)
        else:
            # 默认创建基础设备
            return Device(device_type, device_id)

    def remove_device(self, device_id):
        """删除设备"""
        if device_id not in self.devices:
            print("设备不存在。")
            return False
        
        device = self.devices[device_id]
        
        # 从所有用户的设备列表中移除
        for user in self.users.values():
            user.remove_device(device_id)
        
        # 删除设备
        del self.devices[device_id]
        
        log(f"删除设备 {device.name}", device=device_id, 
            extra_info={"device_id": device_id})
        print(f"设备 {device.name} (ID: {device_id}) 已删除。")
        return True

    def show_devices(self):
        """显示所有设备"""
        if not self.devices:
            print("当前没有设备。")
            return
        
        print("\n=== 所有设备列表 ===")
        for device_id, device in self.devices.items():
            # 查找设备所有者
            owner = None
            for username, user in self.users.items():
                if device_id in user.devices:
                    owner = username
                    break
            
            print(f"\n设备: {device.name}")
            print(f"  ID: {device_id}")
            print(f"  状态: {device.status}")
            print(f"  属性: {device.attributes}")
            if owner:
                print(f"  所有者: {owner}")
            if device.shared_users:
                print(f"  共享给: {', '.join(device.shared_users)}")

    def get_device(self, device_id):
        """获取设备对象"""
        return self.devices.get(device_id)

    # ---------------------------
    # 设备控制
    # ---------------------------
    def control_device(self, device_id, action, **kwargs):
        """
        控制设备
        
        :param device_id: 设备ID
        :param action: 操作类型（turn_on/turn_off/set_attr等）
        :param kwargs: 额外参数（如属性名、属性值等）
        :return: 是否操作成功
        """
        if device_id not in self.devices:
            print("设备不存在。")
            return False
        
        device = self.devices[device_id]
        old_status = device.status
        old_attrs = device.attributes.copy()
        
        # 执行操作
        success = False
        if action == "turn_on":
            success = device.turn_on()
            if success:
                log(f"打开设备 {device.name}", device=device, 
                    extra_info={"device_id": device_id, "old_status": old_status})
        elif action == "turn_off":
            success = device.turn_off()
            if success:
                log(f"关闭设备 {device.name}", device=device,
                    extra_info={"device_id": device_id, "old_status": old_status})
        elif action == "set_attr":
            key = kwargs.get("key")
            value = kwargs.get("value")
            if key and value is not None:
                device.set_attr(key, value)
                success = True
                log(f"设置设备属性 {device.name}.{key} = {value}", device=device,
                    extra_info={"device_id": device_id, "key": key, "value": value})
        else:
            # 尝试调用设备的其他方法
            if hasattr(device, action):
                method = getattr(device, action)
                if callable(method):
                    result = method(*kwargs.get("args", []), **kwargs.get("kwargs", {}))
                    success = result if isinstance(result, bool) else True
                    log(f"执行设备操作 {device.name}.{action}", device=device,
                        extra_info={"device_id": device_id, "action": action})
        
        if success:
            print(f"设备 {device.name} (ID: {device_id}) 操作成功。")
            print(f"  当前状态: {device.status}")
            if device.attributes:
                print(f"  当前属性: {device.attributes}")
        
        return success

    # ---------------------------
    # 设备共享
    # ---------------------------
    def share_device(self, device_id, username):
        """共享设备给其他用户"""
        if device_id not in self.devices:
            print("设备不存在。")
            return False
        if username not in self.users:
            print("用户不存在。")
            return False

        if self.devices[device_id].share(username):
            log(f"设备 {device_id} 被共享给用户 {username}", 
                device=self.devices[device_id], username=username)
            print(f"设备 {device_id} 已共享给用户 {username}。")
            return True
        else:
            print(f"设备 {device_id} 已经共享给用户 {username}。")
            return False

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

        log("系统数据已保存")
        print("系统数据已保存到 data.json。")

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
                device = self._create_device(dev_data["name"], device_id)
                if device:
                    device.status = dev_data["status"]
                    device.attributes = dev_data["attributes"]
                    device.shared_users = dev_data["shared_users"]
                    self.devices[device_id] = device

            print("系统数据已从 data.json 加载。")

        except FileNotFoundError:
            print("首次启动，无保存数据。")
        except Exception as e:
            print(f"加载数据时出错: {e}")

    def load_automation_rules(self):
        """加载自动化规则（从JSON文件）"""
        try:
            with open("automation_rules.json", "r", encoding="utf-8") as f:
                rules_data = json.load(f)
                # 注意：自动化规则包含函数，无法直接序列化
                # 这里只加载规则描述，实际规则需要在运行时重新添加
                print(f"找到 {len(rules_data)} 条已保存的规则描述。")
        except FileNotFoundError:
            pass  # 没有保存的规则文件是正常的
        except Exception as e:
            print(f"加载自动化规则时出错: {e}")

    def save_automation_rules(self):
        """保存自动化规则描述（仅保存描述，不保存函数）"""
        rules_data = []
        for rule in self.automation.rules:
            rules_data.append({
                "description": rule.description
            })
        
        with open("automation_rules.json", "w", encoding="utf-8") as f:
            json.dump(rules_data, f, indent=4, ensure_ascii=False)
        
        print("自动化规则描述已保存。")
