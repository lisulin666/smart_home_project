import random

class Device:
    """
    设备类：所有智能家居设备的基础类
    - 提供基本的开关控制和属性设置功能
    - 支持设备共享给其他用户
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
            return False
        else:
            self.status = "on"
            return True

    def turn_off(self):
        """关闭设备"""
        if self.status == "off":
            print(f"{self.name} 已经是关闭状态。")
            return False
        else:
            self.status = "off"
            return True

    def set_attr(self, key, value):
        """设置设备属性，例如亮度、温度"""
        self.attributes[key] = value

    def get_attr(self, key, default=None):
        """获取设备属性"""
        return self.attributes.get(key, default)

    def share(self, username):
        """把设备共享给其他用户"""
        if username not in self.shared_users:
            self.shared_users.append(username)
            return True
        return False

    def __repr__(self):
        """打印设备信息"""
        return f"{self.name}(ID={self.device_id}, 状态={self.status}, 属性={self.attributes})"


class Light(Device):
    """
    智能灯光设备：
    - 支持亮度调节（0-100）
    - 支持色温调节（暖光/冷光）
    """

    def __init__(self, device_id):
        super().__init__("light", device_id)
        self.attributes["brightness"] = 50  # 默认亮度 50%
        self.attributes["color_temp"] = "warm"  # 色温：warm/cool

    def set_brightness(self, brightness):
        """设置亮度（0-100）"""
        if 0 <= brightness <= 100:
            self.attributes["brightness"] = brightness
            return True
        else:
            print("亮度值必须在 0-100 之间。")
            return False

    def set_color_temp(self, temp):
        """设置色温（warm/cool）"""
        if temp in ["warm", "cool"]:
            self.attributes["color_temp"] = temp
            return True
        else:
            print("色温只能是 'warm' 或 'cool'。")
            return False


class AirConditioner(Device):
    """
    空调设备：
    - 支持温度设置（16-30度）
    - 支持模式切换（制冷/制热/送风）
    """

    def __init__(self, device_id):
        super().__init__("aircon", device_id)
        self.attributes["temperature"] = 26  # 默认温度 26度
        self.attributes["mode"] = "cool"  # 模式：cool/heat/fan

    def set_temperature(self, temp):
        """设置温度（16-30度）"""
        if 16 <= temp <= 30:
            self.attributes["temperature"] = temp
            return True
        else:
            print("温度值必须在 16-30 度之间。")
            return False

    def set_mode(self, mode):
        """设置模式（cool/heat/fan）"""
        if mode in ["cool", "heat", "fan"]:
            self.attributes["mode"] = mode
            return True
        else:
            print("模式只能是 'cool'、'heat' 或 'fan'。")
            return False


class DoorLock(Device):
    """
    智能门锁设备：
    - 支持上锁/解锁
    - 记录最后操作时间
    """

    def __init__(self, device_id):
        super().__init__("doorlock", device_id)
        self.attributes["locked"] = True  # 默认上锁
        self.attributes["last_action_time"] = None

    def lock(self):
        """上锁"""
        if self.attributes.get("locked", False):
            print("门锁已经是上锁状态。")
            return False
        else:
            self.attributes["locked"] = True
            from datetime import datetime
            self.attributes["last_action_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True

    def unlock(self):
        """解锁"""
        if not self.attributes.get("locked", True):
            print("门锁已经是解锁状态。")
            return False
        else:
            self.attributes["locked"] = False
            from datetime import datetime
            self.attributes["last_action_time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            return True

    def turn_on(self):
        """打开设备（上锁）"""
        return self.lock()

    def turn_off(self):
        """关闭设备（解锁）"""
        return self.unlock()


class Camera(Device):
    """
    智能摄像头设备：
    - 支持旋转角度设置（0-360度）
    - 支持夜视模式开关
    """

    def __init__(self, device_id):
        super().__init__("camera", device_id)
        self.attributes["angle"] = 0  # 旋转角度
        self.attributes["night_vision"] = False  # 夜视模式

    def set_angle(self, angle):
        """设置旋转角度（0-360度）"""
        if 0 <= angle <= 360:
            self.attributes["angle"] = angle
            return True
        else:
            print("角度值必须在 0-360 之间。")
            return False

    def toggle_night_vision(self):
        """切换夜视模式"""
        self.attributes["night_vision"] = not self.attributes["night_vision"]
        return True


class SmartCurtain(Device):
    """
    智能窗帘设备：
    - 支持开合度设置（0-100%）
    - 0% 表示完全关闭，100% 表示完全打开
    """

    def __init__(self, device_id):
        super().__init__("curtain", device_id)
        self.attributes["openness"] = 0  # 开合度 0-100

    def set_openness(self, openness):
        """设置开合度（0-100%）"""
        if 0 <= openness <= 100:
            self.attributes["openness"] = openness
            if openness == 0:
                self.status = "off"
            elif openness == 100:
                self.status = "on"
            else:
                self.status = "on"  # 部分打开也算开启状态
            return True
        else:
            print("开合度值必须在 0-100 之间。")
            return False

    def turn_on(self):
        """打开窗帘（100%开合度）"""
        self.set_openness(100)
        return True

    def turn_off(self):
        """关闭窗帘（0%开合度）"""
        self.set_openness(0)
        return True


class MusicPlayer(Device):
    """
    智能音乐播放器设备：
    - 支持音量调节（0-100）
    - 支持播放模式（单曲/循环/随机）
    - 支持当前播放歌曲名称
    """

    def __init__(self, device_id):
        super().__init__("musicplayer", device_id)
        self.attributes["volume"] = 50  # 默认音量 50%
        self.attributes["play_mode"] = "single"  # 播放模式：single/loop/shuffle
        self.attributes["current_song"] = "无"

    def set_volume(self, volume):
        """设置音量（0-100）"""
        if 0 <= volume <= 100:
            self.attributes["volume"] = volume
            return True
        else:
            print("音量值必须在 0-100 之间。")
            return False

    def set_play_mode(self, mode):
        """设置播放模式（single/loop/shuffle）"""
        if mode in ["single", "loop", "shuffle"]:
            self.attributes["play_mode"] = mode
            return True
        else:
            print("播放模式只能是 'single'、'loop' 或 'shuffle'。")
            return False

    def play_song(self, song_name):
        """播放指定歌曲"""
        self.attributes["current_song"] = song_name
        self.status = "on"
        return True


class MoodLight(Device):
    """
    创意设备：情绪灯，会随机变颜色
    - 支持多种颜色模式
    - 可以自动随机变换颜色
    """

    def __init__(self, device_id):
        super().__init__("MoodLight", device_id)
        self.attributes["color"] = "blue"
        self.attributes["auto_change"] = False  # 是否自动变换颜色

    def set_color(self, color):
        """设置颜色"""
        colors = ["red", "blue", "green", "purple", "yellow", "orange", "pink"]
        if color in colors:
            self.attributes["color"] = color
            return True
        else:
            print(f"颜色只能是以下之一：{', '.join(colors)}")
            return False

    def auto_change_color(self):
        """自动随机变换颜色"""
        colors = ["red", "blue", "green", "purple", "yellow", "orange", "pink"]
        self.attributes["color"] = random.choice(colors)
        return True
