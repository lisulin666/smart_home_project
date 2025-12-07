from datetime import datetime

class Logger:
    """
    日志记录类：
    - 记录所有设备操作和系统事件
    - 支持详细的日志信息（操作类型、用户、设备、状态变化等）
    """

    def __init__(self, log_file="logs.txt"):
        """初始化日志记录器"""
        self.log_file = log_file

    def log_action(self, action, device=None, username=None, extra_info=None):
        """
        记录操作日志
        
        :param action: 操作描述（字符串）
        :param device: 设备对象或设备ID（可选）
        :param username: 用户名（可选）
        :param extra_info: 额外信息字典（可选）
        """
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 构建日志条目
        log_entry = f"[{timestamp}] {action}"
        
        # 添加用户名信息
        if username:
            log_entry += f" | 用户: {username}"
        
        # 添加设备信息
        if device:
            if isinstance(device, str):
                # 如果是设备ID字符串
                log_entry += f" | 设备ID: {device}"
            else:
                # 如果是设备对象
                log_entry += f" | 设备: {device.name}({device.device_id})"
                if device.status:
                    log_entry += f" | 状态: {device.status}"
        
        # 添加额外信息
        if extra_info:
            for key, value in extra_info.items():
                log_entry += f" | {key}: {value}"
        
        # 写入文件
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")
        
        return log_entry

    def get_recent_logs(self, lines=10):
        """
        获取最近的日志条目
        
        :param lines: 要获取的行数
        :return: 日志行列表
        """
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                return all_lines[-lines:] if len(all_lines) > lines else all_lines
        except FileNotFoundError:
            return []


# 创建全局日志记录器实例
_logger = Logger()

def log(action, device=None, username=None, extra_info=None):
    """
    便捷的日志记录函数（保持向后兼容）
    
    :param action: 操作描述
    :param device: 设备对象或设备ID
    :param username: 用户名
    :param extra_info: 额外信息
    """
    return _logger.log_action(action, device, username, extra_info)
