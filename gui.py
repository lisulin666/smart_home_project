"""
智能家居控制系统 - 图形界面
使用 tkinter 实现简单美观的 GUI
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import smart_home
from automation import AutomationRule
from logger import Logger

class SmartHomeGUI:
    """智能家居系统图形界面主类"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("智能家居控制系统")
        self.root.geometry("1000x700")
        
        # 创建系统实例
        self.home = smart_home.SmartHome()
        self.logger = Logger()
        
        # 当前选中的用户和设备
        self.current_user = None
        self.current_device_id = None
        
        # 创建界面
        self.create_widgets()
        
        # 初始化显示
        self.refresh_user_list()
        self.refresh_device_list()
        
    def create_widgets(self):
        """创建所有界面组件"""
        
        # 顶部工具栏
        toolbar = tk.Frame(self.root, bg="#f0f0f0", height=50)
        toolbar.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        
        tk.Button(toolbar, text="保存数据", command=self.save_data, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="运行自动化规则", command=self.run_automation, 
                 bg="#2196F3", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(toolbar, text="刷新", command=self.refresh_all, 
                 bg="#FF9800", fg="white", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        
        # 主容器（左右分栏）
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 左侧面板（用户和设备列表）
        left_panel = tk.Frame(main_container, width=300)
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, padx=(0, 5))
        left_panel.pack_propagate(False)
        
        # 用户管理区域
        user_frame = tk.LabelFrame(left_panel, text="用户管理", font=("Arial", 12, "bold"))
        user_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 用户列表
        tk.Label(user_frame, text="用户列表:", font=("Arial", 10)).pack(anchor=tk.W, padx=5, pady=2)
        self.user_listbox = tk.Listbox(user_frame, height=5, font=("Arial", 10))
        self.user_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.user_listbox.bind("<<ListboxSelect>>", self.on_user_select)
        
        # 用户操作按钮
        user_btn_frame = tk.Frame(user_frame)
        user_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(user_btn_frame, text="添加用户", command=self.add_user, 
                 bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(user_btn_frame, text="删除用户", command=self.remove_user, 
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # 设备列表区域
        device_frame = tk.LabelFrame(left_panel, text="设备列表", font=("Arial", 12, "bold"))
        device_frame.pack(fill=tk.BOTH, expand=True)
        
        tk.Label(device_frame, text="设备列表:", font=("Arial", 10)).pack(anchor=tk.W, padx=5, pady=2)
        self.device_listbox = tk.Listbox(device_frame, font=("Arial", 10))
        self.device_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=2)
        self.device_listbox.bind("<<ListboxSelect>>", self.on_device_select)
        
        # 设备操作按钮
        device_btn_frame = tk.Frame(device_frame)
        device_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(device_btn_frame, text="添加设备", command=self.add_device, 
                 bg="#4CAF50", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(device_btn_frame, text="删除设备", command=self.remove_device, 
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # 右侧面板（设备详情和控制）
        right_panel = tk.Frame(main_container)
        right_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 设备详情区域
        detail_frame = tk.LabelFrame(right_panel, text="设备详情与控制", font=("Arial", 12, "bold"))
        detail_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 设备信息显示
        self.device_info_text = scrolledtext.ScrolledText(detail_frame, height=8, 
                                                          font=("Arial", 10), wrap=tk.WORD)
        self.device_info_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 设备控制区域
        control_frame = tk.Frame(detail_frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(control_frame, text="打开设备", command=self.turn_on_device, 
                 bg="#4CAF50", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="关闭设备", command=self.turn_off_device, 
                 bg="#f44336", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        tk.Button(control_frame, text="共享设备", command=self.share_device, 
                 bg="#FF9800", fg="white", font=("Arial", 10), width=12).pack(side=tk.LEFT, padx=2)
        
        # 属性设置区域（动态创建）
        self.attr_frame = tk.Frame(detail_frame)
        self.attr_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # 自动化规则区域
        automation_frame = tk.LabelFrame(right_panel, text="自动化规则", font=("Arial", 12, "bold"))
        automation_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # 规则列表
        self.rule_listbox = tk.Listbox(automation_frame, height=4, font=("Arial", 10))
        self.rule_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 规则操作按钮
        rule_btn_frame = tk.Frame(automation_frame)
        rule_btn_frame.pack(fill=tk.X, padx=5, pady=5)
        tk.Button(rule_btn_frame, text="添加规则", command=self.add_automation_rule, 
                 bg="#2196F3", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        tk.Button(rule_btn_frame, text="删除规则", command=self.remove_automation_rule, 
                 bg="#f44336", fg="white", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
        
        # 日志显示区域
        log_frame = tk.LabelFrame(right_panel, text="最近日志", font=("Arial", 12, "bold"))
        log_frame.pack(fill=tk.BOTH, expand=True)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=6, 
                                                  font=("Consolas", 9), wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 刷新日志显示
        self.refresh_logs()
        
    def refresh_user_list(self):
        """刷新用户列表"""
        self.user_listbox.delete(0, tk.END)
        for username in self.home.users:
            device_count = len(self.home.users[username].devices)
            self.user_listbox.insert(tk.END, f"{username} ({device_count}个设备)")
    
    def refresh_device_list(self):
        """刷新设备列表"""
        self.device_listbox.delete(0, tk.END)
        if self.current_user:
            devices = self.home.get_user_devices(self.current_user)
            all_device_ids = devices["all"]
            for device_id in all_device_ids:
                if device_id in self.home.devices:
                    device = self.home.devices[device_id]
                    status_icon = "🟢" if device.status == "on" else "🔴"
                    self.device_listbox.insert(tk.END, f"{status_icon} {device.name} ({device_id})")
        else:
            for device_id, device in self.home.devices.items():
                status_icon = "🟢" if device.status == "on" else "🔴"
                self.device_listbox.insert(tk.END, f"{status_icon} {device.name} ({device_id})")
    
    def refresh_device_info(self):
        """刷新设备详情显示"""
        self.device_info_text.delete(1.0, tk.END)
        
        if not self.current_device_id or self.current_device_id not in self.home.devices:
            self.device_info_text.insert(tk.END, "请选择一个设备查看详情")
            return
        
        device = self.home.devices[self.current_device_id]
        
        # 查找设备所有者
        owner = None
        for username, user in self.home.users.items():
            if self.current_device_id in user.devices:
                owner = username
                break
        
        info = f"设备名称: {device.name}\n"
        info += f"设备ID: {device.device_id}\n"
        info += f"状态: {device.status}\n"
        if owner:
            info += f"所有者: {owner}\n"
        if device.shared_users:
            info += f"共享给: {', '.join(device.shared_users)}\n"
        info += f"\n属性:\n"
        for key, value in device.attributes.items():
            info += f"  {key}: {value}\n"
        
        self.device_info_text.insert(tk.END, info)
        
        # 刷新属性控制区域
        self.refresh_attr_controls(device)
    
    def refresh_attr_controls(self, device):
        """刷新属性控制控件"""
        # 清除现有控件
        for widget in self.attr_frame.winfo_children():
            widget.destroy()
        
        if device.name == "light":
            tk.Label(self.attr_frame, text="亮度:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
            brightness_var = tk.IntVar(value=device.attributes.get("brightness", 50))
            brightness_scale = tk.Scale(self.attr_frame, from_=0, to=100, 
                                       orient=tk.HORIZONTAL, variable=brightness_var,
                                       length=150, command=lambda v: self.set_brightness(int(v)))
            brightness_scale.pack(side=tk.LEFT, padx=2)
            
        elif device.name == "aircon":
            tk.Label(self.attr_frame, text="温度:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
            temp_var = tk.IntVar(value=device.attributes.get("temperature", 26))
            temp_scale = tk.Scale(self.attr_frame, from_=16, to=30, 
                                 orient=tk.HORIZONTAL, variable=temp_var,
                                 length=150, command=lambda v: self.set_temperature(int(v)))
            temp_scale.pack(side=tk.LEFT, padx=2)
            
        elif device.name == "curtain":
            tk.Label(self.attr_frame, text="开合度:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
            openness_var = tk.IntVar(value=device.attributes.get("openness", 0))
            openness_scale = tk.Scale(self.attr_frame, from_=0, to=100, 
                                     orient=tk.HORIZONTAL, variable=openness_var,
                                     length=150, command=lambda v: self.set_openness(int(v)))
            openness_scale.pack(side=tk.LEFT, padx=2)
            
        elif device.name == "musicplayer":
            tk.Label(self.attr_frame, text="音量:", font=("Arial", 9)).pack(side=tk.LEFT, padx=2)
            volume_var = tk.IntVar(value=device.attributes.get("volume", 50))
            volume_scale = tk.Scale(self.attr_frame, from_=0, to=100, 
                                   orient=tk.HORIZONTAL, variable=volume_var,
                                   length=150, command=lambda v: self.set_volume(int(v)))
            volume_scale.pack(side=tk.LEFT, padx=2)
    
    def refresh_automation_rules(self):
        """刷新自动化规则列表"""
        self.rule_listbox.delete(0, tk.END)
        rules = self.home.automation.list_rules()
        for rule_desc in rules:
            self.rule_listbox.insert(tk.END, rule_desc)
    
    def refresh_logs(self):
        """刷新日志显示"""
        self.log_text.delete(1.0, tk.END)
        logs = self.logger.get_recent_logs(15)
        for log_line in logs:
            self.log_text.insert(tk.END, log_line)
    
    def refresh_all(self):
        """刷新所有显示"""
        self.refresh_user_list()
        self.refresh_device_list()
        self.refresh_device_info()
        self.refresh_automation_rules()
        self.refresh_logs()
    
    def on_user_select(self, event):
        """用户选择事件"""
        selection = self.user_listbox.curselection()
        if selection:
            username = self.user_listbox.get(selection[0]).split()[0]
            self.current_user = username
            self.refresh_device_list()
    
    def on_device_select(self, event):
        """设备选择事件"""
        selection = self.device_listbox.curselection()
        if selection:
            device_text = self.device_listbox.get(selection[0])
            # 提取设备ID（在括号中）
            if "(" in device_text and ")" in device_text:
                device_id = device_text.split("(")[1].split(")")[0]
                self.current_device_id = device_id
                self.refresh_device_info()
    
    def add_user(self):
        """添加用户"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加用户")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="用户名:", font=("Arial", 10)).pack(pady=10)
        entry = tk.Entry(dialog, font=("Arial", 10), width=20)
        entry.pack(pady=5)
        entry.focus()
        
        def confirm():
            username = entry.get().strip()
            if username:
                if self.home.add_user(username):
                    self.refresh_user_list()
                    dialog.destroy()
                else:
                    messagebox.showwarning("警告", "用户已存在！")
            else:
                messagebox.showwarning("警告", "用户名不能为空！")
        
        tk.Button(dialog, text="确定", command=confirm, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=5)
        entry.bind("<Return>", lambda e: confirm())
    
    def remove_user(self):
        """删除用户"""
        selection = self.user_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的用户！")
            return
        
        username = self.user_listbox.get(selection[0]).split()[0]
        if messagebox.askyesno("确认", f"确定要删除用户 {username} 及其所有设备吗？"):
            if self.home.remove_user(username):
                self.current_user = None
                self.refresh_user_list()
                self.refresh_device_list()
    
    def add_device(self):
        """添加设备"""
        # 检查是否有用户
        if not self.home.users:
            messagebox.showwarning("警告", "请先添加用户！")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("添加设备")
        dialog.geometry("350x220")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="设备类型:", font=("Arial", 10)).pack(pady=5)
        type_var = tk.StringVar(value="light")
        type_combo = ttk.Combobox(dialog, textvariable=type_var, 
                                 values=["light", "aircon", "doorlock", "camera", 
                                        "curtain", "musicplayer", "moodlight"],
                                 state="readonly", font=("Arial", 10))
        type_combo.pack(pady=5)
        
        tk.Label(dialog, text="设备ID:", font=("Arial", 10)).pack(pady=5)
        id_entry = tk.Entry(dialog, font=("Arial", 10), width=20)
        id_entry.pack(pady=5)
        id_entry.focus()
        
        tk.Label(dialog, text="所有者:", font=("Arial", 10)).pack(pady=5)
        owner_var = tk.StringVar()
        owner_combo = ttk.Combobox(dialog, textvariable=owner_var,
                                  values=list(self.home.users.keys()),
                                  state="readonly", font=("Arial", 10))
        owner_combo.pack(pady=5)
        
        def confirm():
            dtype = type_var.get()
            did = id_entry.get().strip()
            owner = owner_var.get()
            
            if not did:
                messagebox.showwarning("警告", "设备ID不能为空！")
                return
            if not owner:
                messagebox.showwarning("警告", "请选择所有者！")
                return
            
            if self.home.add_device(dtype, did, owner):
                self.refresh_device_list()
                self.refresh_logs()
                dialog.destroy()
        
        # 按钮框架
        btn_frame = tk.Frame(dialog)
        btn_frame.pack(pady=10)
        
        tk.Button(btn_frame, text="确定", command=confirm, 
                 bg="#4CAF50", fg="white", font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="取消", command=dialog.destroy, 
                 bg="#9E9E9E", fg="white", font=("Arial", 10), width=10).pack(side=tk.LEFT, padx=5)
        
        # 绑定回车键
        id_entry.bind("<Return>", lambda e: confirm())
    
    def remove_device(self):
        """删除设备"""
        if not self.current_device_id:
            messagebox.showwarning("警告", "请先选择要删除的设备！")
            return
        
        if messagebox.askyesno("确认", f"确定要删除设备 {self.current_device_id} 吗？"):
            if self.home.remove_device(self.current_device_id):
                self.current_device_id = None
                self.refresh_device_list()
                self.refresh_device_info()
                self.refresh_logs()
    
    def turn_on_device(self):
        """打开设备"""
        if not self.current_device_id:
            messagebox.showwarning("警告", "请先选择设备！")
            return
        
        if self.home.control_device(self.current_device_id, "turn_on"):
            self.refresh_device_list()
            self.refresh_device_info()
            self.refresh_logs()
    
    def turn_off_device(self):
        """关闭设备"""
        if not self.current_device_id:
            messagebox.showwarning("警告", "请先选择设备！")
            return
        
        if self.home.control_device(self.current_device_id, "turn_off"):
            self.refresh_device_list()
            self.refresh_device_info()
            self.refresh_logs()
    
    def share_device(self):
        """共享设备"""
        if not self.current_device_id:
            messagebox.showwarning("警告", "请先选择设备！")
            return
        
        dialog = tk.Toplevel(self.root)
        dialog.title("共享设备")
        dialog.geometry("300x100")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="共享给用户:", font=("Arial", 10)).pack(pady=10)
        user_var = tk.StringVar()
        if self.home.users:
            user_combo = ttk.Combobox(dialog, textvariable=user_var,
                                     values=list(self.home.users.keys()),
                                     state="readonly", font=("Arial", 10))
            user_combo.pack(pady=5)
        else:
            tk.Label(dialog, text="没有其他用户", fg="red", font=("Arial", 9)).pack()
            return
        
        def confirm():
            username = user_var.get()
            if username:
                if self.home.share_device(self.current_device_id, username):
                    self.refresh_device_info()
                    self.refresh_logs()
                    dialog.destroy()
        
        tk.Button(dialog, text="确定", command=confirm, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=5)
    
    def set_brightness(self, value):
        """设置亮度"""
        if self.current_device_id:
            device = self.home.devices.get(self.current_device_id)
            if device and device.name == "light":
                device.set_brightness(value)
                self.refresh_device_info()
    
    def set_temperature(self, value):
        """设置温度"""
        if self.current_device_id:
            device = self.home.devices.get(self.current_device_id)
            if device and device.name == "aircon":
                device.set_temperature(value)
                self.refresh_device_info()
    
    def set_openness(self, value):
        """设置开合度"""
        if self.current_device_id:
            device = self.home.devices.get(self.current_device_id)
            if device and device.name == "curtain":
                device.set_openness(value)
                self.refresh_device_info()
    
    def set_volume(self, value):
        """设置音量"""
        if self.current_device_id:
            device = self.home.devices.get(self.current_device_id)
            if device and device.name == "musicplayer":
                device.set_volume(value)
                self.refresh_device_info()
    
    def add_automation_rule(self):
        """添加自动化规则"""
        dialog = tk.Toplevel(self.root)
        dialog.title("添加自动化规则")
        dialog.geometry("400x300")
        dialog.transient(self.root)
        dialog.grab_set()
        
        tk.Label(dialog, text="选择规则模板:", font=("Arial", 11, "bold")).pack(pady=10)
        
        rule_var = tk.StringVar()
        rules = [
            ("温度 > 30°C 自动打开空调", "temp_high"),
            ("温度 < 20°C 自动关闭空调", "temp_low"),
            ("无人时自动关灯", "no_person"),
            ("门锁未关闭报警", "door_unlocked")
        ]
        
        for desc, value in rules:
            tk.Radiobutton(dialog, text=desc, variable=rule_var, value=value,
                          font=("Arial", 10)).pack(anchor=tk.W, padx=20, pady=2)
        
        def confirm():
            rule_type = rule_var.get()
            if not rule_type:
                messagebox.showwarning("警告", "请选择规则类型！")
                return
            
            # 创建规则
            if rule_type == "temp_high":
                def cond(state):
                    return state.get("temperature", 0) > 30
                def act(state):
                    for device_id, device in self.home.devices.items():
                        if device.name == "aircon":
                            device.turn_on()
                            self.logger.log_action("自动化规则触发：打开空调", device=device,
                                                  extra_info={"reason": "温度过高"})
                            break
                rule = AutomationRule(cond, act, "温度 > 30°C 自动打开空调")
                
            elif rule_type == "temp_low":
                def cond(state):
                    return state.get("temperature", 0) < 20
                def act(state):
                    for device_id, device in self.home.devices.items():
                        if device.name == "aircon":
                            device.turn_off()
                            self.logger.log_action("自动化规则触发：关闭空调", device=device,
                                                  extra_info={"reason": "温度过低"})
                            break
                rule = AutomationRule(cond, act, "温度 < 20°C 自动关闭空调")
                
            elif rule_type == "no_person":
                def cond(state):
                    return not state.get("has_person", True)
                def act(state):
                    for device_id, device in self.home.devices.items():
                        if device.name == "light" and device.status == "on":
                            device.turn_off()
                            self.logger.log_action("自动化规则触发：关闭灯光", device=device,
                                                  extra_info={"reason": "无人"})
                rule = AutomationRule(cond, act, "无人时自动关灯")
                
            elif rule_type == "door_unlocked":
                def cond(state):
                    return not state.get("door_locked", True)
                def act(state):
                    messagebox.showwarning("警告", "门锁未关闭！")
                    self.logger.log_action("自动化规则触发：门锁未关闭警告",
                                          extra_info={"reason": "门锁未关闭"})
                rule = AutomationRule(cond, act, "门锁未关闭报警")
            
            if self.home.automation.add_rule(rule):
                self.refresh_automation_rules()
                self.refresh_logs()
                dialog.destroy()
        
        tk.Button(dialog, text="确定", command=confirm, 
                 bg="#4CAF50", fg="white", font=("Arial", 10)).pack(pady=10)
    
    def remove_automation_rule(self):
        """删除自动化规则"""
        selection = self.rule_listbox.curselection()
        if not selection:
            messagebox.showwarning("警告", "请先选择要删除的规则！")
            return
        
        if messagebox.askyesno("确认", "确定要删除选中的规则吗？"):
            if self.home.automation.remove_rule(selection[0]):
                self.refresh_automation_rules()
                self.refresh_logs()
    
    def run_automation(self):
        """运行自动化规则"""
        import random
        
        # 模拟当前系统状态
        current_state = {
            "temperature": random.randint(20, 35),
            "has_person": random.choice([True, False]),
            "door_locked": True,
            "devices": self.home.devices
        }
        
        # 检查门锁状态
        for device in self.home.devices.values():
            if device.name == "doorlock":
                current_state["door_locked"] = device.attributes.get("locked", True)
                break
        
        triggered = self.home.automation.run_all(current_state)
        messagebox.showinfo("完成", f"自动化规则检查完成！\n当前温度: {current_state['temperature']}°C\n"
                                   f"是否有人: {'是' if current_state['has_person'] else '否'}\n"
                                   f"触发了 {triggered} 条规则。")
        self.refresh_all()
    
    def save_data(self):
        """保存数据"""
        self.home.save_data()
        self.home.save_automation_rules()
        messagebox.showinfo("成功", "数据已保存！")
        self.refresh_logs()


def main():
    """主函数"""
    root = tk.Tk()
    app = SmartHomeGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

