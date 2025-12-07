# 自动化规则系统：
# 1. 支持根据条件自动控制设备，比如温度超过某值时打开空调。
# 2. 规则可以保存成一个列表，方便以后扩展。

class AutomationRule:
    """
    自动化规则类：
    - condition: 条件函数，接收 current_state 参数，返回 True/False
    - action: 动作函数，接收 current_state 参数，执行相应操作
    - description: 规则描述，便于用户理解和管理
    """

    def __init__(self, condition, action, description="未命名规则"):
        """
        初始化规则
        
        :param condition: 条件函数，函数签名：condition(current_state) -> bool
        :param action: 动作函数，函数签名：action(current_state) -> None
        :param description: 规则描述文本
        """
        self.condition = condition
        self.action = action
        self.description = description

    def check(self, current_state):
        """
        检查条件是否满足
        
        :param current_state: 当前系统状态
        :return: True 如果条件满足，False 否则
        """
        try:
            return self.condition(current_state)
        except Exception as e:
            print(f"规则检查出错: {e}")
            return False

    def execute(self, current_state):
        """
        执行动作
        
        :param current_state: 当前系统状态
        """
        try:
            self.action(current_state)
        except Exception as e:
            print(f"规则执行出错: {e}")

    def __repr__(self):
        """返回规则的字符串表示"""
        return f"AutomationRule(描述: {self.description})"


class AutomationManager:
    """
    自动化管理器：
    - 维护一个规则列表
    - 提供添加规则、删除规则和运行所有规则的方法
    """

    def __init__(self):
        """初始化管理器，创建空的规则列表"""
        self.rules = []

    def add_rule(self, rule):
        """
        添加一条自动化规则
        
        :param rule: AutomationRule 对象
        :return: 是否添加成功
        """
        if isinstance(rule, AutomationRule):
            self.rules.append(rule)
            return True
        else:
            print("错误：只能添加 AutomationRule 对象。")
            return False

    def remove_rule(self, index):
        """
        删除指定索引的规则
        
        :param index: 规则在列表中的索引（从0开始）
        :return: 是否删除成功
        """
        if 0 <= index < len(self.rules):
            removed_rule = self.rules.pop(index)
            print(f"已删除规则: {removed_rule.description}")
            return True
        else:
            print("规则索引无效。")
            return False

    def list_rules(self):
        """
        列出所有规则
        
        :return: 规则描述列表
        """
        if not self.rules:
            return ["当前没有自动化规则。"]
        
        rule_list = []
        for idx, rule in enumerate(self.rules):
            rule_list.append(f"{idx + 1}. {rule.description}")
        return rule_list

    def run_all(self, current_state):
        """
        运行所有规则
        对每条规则，如果条件满足，则执行对应的动作
        
        :param current_state: 当前系统状态，通常是一个字典，包含设备信息等
        :return: 触发的规则数量
        """
        triggered_count = 0
        for rule in self.rules:
            if rule.check(current_state):
                rule.execute(current_state)
                triggered_count += 1
        return triggered_count

    def get_rules_count(self):
        """获取规则总数"""
        return len(self.rules)
