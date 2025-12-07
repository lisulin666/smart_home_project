# 自动化规则系统：
# 1. 支持根据条件自动控制设备，比如温度超过某值时打开空调。
# 2. 规则可以保存成一个列表，方便以后扩展。

class AutomationRule:
    """
    自动化规则类：
    - condition: 条件函数，接收 current_state 参数，返回 True/False
    - action: 动作函数，接收 current_state 参数，执行相应操作
    """
    
    def __init__(self, condition, action):
        """
        初始化规则
        :param condition: 条件函数，函数签名：condition(current_state) -> bool
        :param action: 动作函数，函数签名：action(current_state) -> None
        """
        self.condition = condition
        self.action = action
    
    def check(self, current_state):
        """
        检查条件是否满足
        :param current_state: 当前系统状态
        :return: True 如果条件满足，False 否则
        """
        return self.condition(current_state)
    
    def execute(self, current_state):
        """
        执行动作
        :param current_state: 当前系统状态
        """
        self.action(current_state)


class AutomationManager:
    """
    自动化管理器：
    - 维护一个规则列表
    - 提供添加规则和运行所有规则的方法
    """
    
    def __init__(self):
        """初始化管理器，创建空的规则列表"""
        self.rules = []
    
    def add_rule(self, rule):
        """
        添加一条自动化规则
        :param rule: AutomationRule 对象
        """
        self.rules.append(rule)
    
    def run_all(self, current_state):
        """
        运行所有规则
        对每条规则，如果条件满足，则执行对应的动作
        :param current_state: 当前系统状态，通常是一个字典，包含设备信息等
        """
        for rule in self.rules:
            if rule.check(current_state):
                rule.execute(current_state)
