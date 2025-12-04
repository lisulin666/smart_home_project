class User:
    """
    用户类：用来表示每一个智能家居用户
    """

    def __init__(self, username):
        self.username = username
        self.devices = []   # 保存此用户拥有的设备 ID

    def add_device(self, device_id):
        """给用户添加设备"""
        if device_id not in self.devices:
            self.devices.append(device_id)

    def remove_device(self, device_id):
        """删除用户的设备"""
        if device_id in self.devices:
            self.devices.remove(device_id)

    def __repr__(self):
        """便于打印查看用户信息"""
        return f"User({self.username}, devices={self.devices})"
