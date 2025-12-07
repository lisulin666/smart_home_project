import smart_home
from automation import AutomationRule
from logger import Logger

# 创建系统实例
home = smart_home.SmartHome()
logger = Logger()

print("欢迎进入智能家居控制系统！")

def get_current_state():
    """
    获取当前系统状态（用于自动化规则）
    这里模拟一些传感器数据
    """
    # 模拟温度传感器（实际可以从真实传感器获取）
    import random
    temperature = random.randint(20, 35)  # 模拟温度 20-35度
    
    # 模拟是否有人（实际可以从运动传感器获取）
    has_person = random.choice([True, False])
    
    # 检查门锁状态
    door_locked = True
    for device in home.devices.values():
        if device.name == "doorlock":
            door_locked = device.attributes.get("locked", True)
            break
    
    return {
        "temperature": temperature,
        "has_person": has_person,
        "door_locked": door_locked,
        "devices": home.devices
    }

while True:
    print("\n" + "="*30)
    print("智能家居控制系统 - 主菜单")
    print("="*30)
    print("1. 用户管理")
    print("2. 设备管理")
    print("3. 设备控制")
    print("4. 设备共享")
    print("5. 自动化规则")
    print("6. 查看日志")
    print("7. 数据管理")
    print("8. 运行自动化规则")
    print("0. 退出系统")
    print("="*30)

    choice = input("请输入选项编号：").strip()

    # ---------------------- 用户管理 -----------------------
    if choice == "1":
        print("\n=== 用户管理 ===")
        print("1. 添加用户")
        print("2. 删除用户")
        print("3. 查看所有用户")
        print("4. 查看用户设备")
        sub_choice = input("请选择：").strip()
        
        if sub_choice == "1":
            username = input("请输入用户名：").strip()
            home.add_user(username)
        elif sub_choice == "2":
            username = input("请输入要删除的用户名：").strip()
            home.remove_user(username)
        elif sub_choice == "3":
            print("\n所有用户：")
            home.list_users()
        elif sub_choice == "4":
            username = input("请输入用户名：").strip()
            devices = home.get_user_devices(username)
            if devices:
                print(f"\n用户 {username} 的设备：")
                print(f"  拥有的设备: {devices['own']}")
                print(f"  共享的设备: {devices['shared']}")
            else:
                print("用户不存在或没有设备。")

    # ---------------------- 设备管理 -----------------------
    elif choice == "2":
        print("\n=== 设备管理 ===")
        print("1. 添加设备")
        print("2. 删除设备")
        print("3. 查看所有设备")
        sub_choice = input("请选择：").strip()
        
        if sub_choice == "1":
            print("\n支持的设备类型：")
            print("  light - 智能灯光")
            print("  aircon - 空调")
            print("  doorlock - 智能门锁")
            print("  camera - 摄像头")
            print("  curtain - 智能窗帘")
            print("  musicplayer - 音乐播放器")
            print("  moodlight - 情绪灯")
            print("  其他 - 基础设备")
            
            dtype = input("\n设备类型：").strip()
            did = input("设备ID：").strip()
            owner = input("设备所有者用户名：").strip()
            home.add_device(dtype, did, owner)
            
        elif sub_choice == "2":
            did = input("请输入要删除的设备ID：").strip()
            home.remove_device(did)
            
        elif sub_choice == "3":
            home.show_devices()

    # ---------------------- 设备控制 -----------------------
    elif choice == "3":
        print("\n=== 设备控制 ===")
        if not home.devices:
            print("当前没有设备。")
            continue
        
        print("\n可用设备：")
        device_list = list(home.devices.items())
        for idx, (device_id, device) in enumerate(device_list, 1):
            print(f"{idx}. {device.name} (ID: {device_id}, 状态: {device.status})")
        
        try:
            device_idx = int(input("\n请选择设备编号：").strip()) - 1
            if device_idx < 0 or device_idx >= len(device_list):
                print("选择无效。")
                continue
            
            device_id, device = device_list[device_idx]
            
            print(f"\n控制设备: {device.name} (ID: {device_id})")
            print("1. 打开设备")
            print("2. 关闭设备")
            print("3. 设置属性")
            
            # 根据设备类型显示特殊控制选项
            if device.name == "light":
                print("4. 设置亮度 (0-100)")
                print("5. 设置色温 (warm/cool)")
            elif device.name == "aircon":
                print("4. 设置温度 (16-30)")
                print("5. 设置模式 (cool/heat/fan)")
            elif device.name == "doorlock":
                print("4. 上锁")
                print("5. 解锁")
            elif device.name == "camera":
                print("4. 设置角度 (0-360)")
                print("5. 切换夜视模式")
            elif device.name == "curtain":
                print("4. 设置开合度 (0-100%)")
            elif device.name == "musicplayer":
                print("4. 设置音量 (0-100)")
                print("5. 设置播放模式 (single/loop/shuffle)")
                print("6. 播放歌曲")
            elif device.name == "MoodLight":
                print("4. 设置颜色")
                print("5. 随机变换颜色")
            
            action_choice = input("\n请选择操作：").strip()
            
            if action_choice == "1":
                home.control_device(device_id, "turn_on")
            elif action_choice == "2":
                home.control_device(device_id, "turn_off")
            elif action_choice == "3":
                key = input("属性名：").strip()
                value = input("属性值：").strip()
                # 尝试转换为数字
                try:
                    value = float(value) if '.' in value else int(value)
                except ValueError:
                    pass
                home.control_device(device_id, "set_attr", key=key, value=value)
            elif action_choice == "4":
                if device.name == "light":
                    brightness = int(input("亮度 (0-100)：").strip())
                    device.set_brightness(brightness)
                    home.control_device(device_id, "set_attr", key="brightness", value=brightness)
                elif device.name == "aircon":
                    temp = int(input("温度 (16-30)：").strip())
                    device.set_temperature(temp)
                    home.control_device(device_id, "set_attr", key="temperature", value=temp)
                elif device.name == "doorlock":
                    device.lock()
                    home.control_device(device_id, "turn_on")
                elif device.name == "camera":
                    angle = int(input("角度 (0-360)：").strip())
                    device.set_angle(angle)
                    home.control_device(device_id, "set_attr", key="angle", value=angle)
                elif device.name == "curtain":
                    openness = int(input("开合度 (0-100%)：").strip())
                    device.set_openness(openness)
                    home.control_device(device_id, "set_attr", key="openness", value=openness)
                elif device.name == "musicplayer":
                    volume = int(input("音量 (0-100)：").strip())
                    device.set_volume(volume)
                    home.control_device(device_id, "set_attr", key="volume", value=volume)
                elif device.name == "MoodLight":
                    color = input("颜色 (red/blue/green/purple/yellow/orange/pink)：").strip()
                    device.set_color(color)
                    home.control_device(device_id, "set_attr", key="color", value=color)
            elif action_choice == "5":
                if device.name == "light":
                    temp = input("色温 (warm/cool)：").strip()
                    device.set_color_temp(temp)
                    home.control_device(device_id, "set_attr", key="color_temp", value=temp)
                elif device.name == "aircon":
                    mode = input("模式 (cool/heat/fan)：").strip()
                    device.set_mode(mode)
                    home.control_device(device_id, "set_attr", key="mode", value=mode)
                elif device.name == "doorlock":
                    device.unlock()
                    home.control_device(device_id, "turn_off")
                elif device.name == "camera":
                    device.toggle_night_vision()
                    home.control_device(device_id, "set_attr", key="night_vision", 
                                      value=device.attributes["night_vision"])
                elif device.name == "musicplayer":
                    mode = input("播放模式 (single/loop/shuffle)：").strip()
                    device.set_play_mode(mode)
                    home.control_device(device_id, "set_attr", key="play_mode", value=mode)
                elif device.name == "MoodLight":
                    device.auto_change_color()
                    home.control_device(device_id, "set_attr", key="color", 
                                      value=device.attributes["color"])
            elif action_choice == "6" and device.name == "musicplayer":
                song = input("歌曲名称：").strip()
                device.play_song(song)
                home.control_device(device_id, "set_attr", key="current_song", value=song)
                
        except (ValueError, IndexError) as e:
            print(f"输入错误: {e}")

    # ---------------------- 设备共享 -----------------------
    elif choice == "4":
        print("\n=== 设备共享 ===")
        did = input("设备ID：").strip()
        username = input("共享给哪个用户：").strip()
        home.share_device(did, username)

    # ---------------------- 自动化规则 -----------------------
    elif choice == "5":
        print("\n=== 自动化规则管理 ===")
        print("1. 添加规则")
        print("2. 查看所有规则")
        print("3. 删除规则")
        sub_choice = input("请选择：").strip()
        
        if sub_choice == "1":
            print("\n请选择规则模板：")
            print("1. 温度 > 30°C 自动打开空调")
            print("2. 温度 < 20°C 自动关闭空调")
            print("3. 无人时自动关灯")
            print("4. 门锁未关闭超过5分钟报警")
            print("5. 自定义规则")
            
            rule_template = input("请选择：").strip()
            
            if rule_template == "1":
                def cond(state):
                    return state.get("temperature", 0) > 30
                
                def act(state):
                    print("自动化动作：温度过高，自动打开空调！")
                    for device_id, device in home.devices.items():
                        if device.name == "aircon":
                            device.turn_on()
                            logger.log_action("自动化规则触发：打开空调", device=device, 
                                            extra_info={"reason": "温度过高"})
                            break
                
                rule = AutomationRule(cond, act, "温度 > 30°C 自动打开空调")
                home.automation.add_rule(rule)
                print("规则已添加。")
                
            elif rule_template == "2":
                def cond(state):
                    return state.get("temperature", 0) < 20
                
                def act(state):
                    print("自动化动作：温度过低，自动关闭空调！")
                    for device_id, device in home.devices.items():
                        if device.name == "aircon":
                            device.turn_off()
                            logger.log_action("自动化规则触发：关闭空调", device=device,
                                            extra_info={"reason": "温度过低"})
                            break
                
                rule = AutomationRule(cond, act, "温度 < 20°C 自动关闭空调")
                home.automation.add_rule(rule)
                print("规则已添加。")
                
            elif rule_template == "3":
                def cond(state):
                    return not state.get("has_person", True)
                
                def act(state):
                    print("自动化动作：检测到无人，自动关闭所有灯光！")
                    for device_id, device in home.devices.items():
                        if device.name == "light" and device.status == "on":
                            device.turn_off()
                            logger.log_action("自动化规则触发：关闭灯光", device=device,
                                            extra_info={"reason": "无人"})
                
                rule = AutomationRule(cond, act, "无人时自动关灯")
                home.automation.add_rule(rule)
                print("规则已添加。")
                
            elif rule_template == "4":
                # 这个规则需要定时检查，这里简化处理
                def cond(state):
                    return not state.get("door_locked", True)
                
                def act(state):
                    print("⚠️ 警告：门锁未关闭！")
                    logger.log_action("自动化规则触发：门锁未关闭警告", 
                                    extra_info={"reason": "门锁未关闭"})
                
                rule = AutomationRule(cond, act, "门锁未关闭报警")
                home.automation.add_rule(rule)
                print("规则已添加。")
                
            elif rule_template == "5":
                print("自定义规则需要编写代码，请参考现有规则模板。")
        
        elif sub_choice == "2":
            print("\n当前自动化规则：")
            rules = home.automation.list_rules()
            for rule_desc in rules:
                print(f"  {rule_desc}")
        
        elif sub_choice == "3":
            rules = home.automation.list_rules()
            if not rules or rules[0] == "当前没有自动化规则。":
                print("没有可删除的规则。")
                continue
            
            print("\n当前规则：")
            for rule_desc in rules:
                print(f"  {rule_desc}")
            
            try:
                rule_idx = int(input("\n请输入要删除的规则编号（从1开始）：").strip()) - 1
                home.automation.remove_rule(rule_idx)
            except (ValueError, IndexError):
                print("输入无效。")

    # ---------------------- 查看日志 -----------------------
    elif choice == "6":
        print("\n=== 最近日志 ===")
        logs = logger.get_recent_logs(20)
        if logs:
            for log_line in logs:
                print(log_line.rstrip())
        else:
            print("暂无日志。")

    # ---------------------- 数据管理 -----------------------
    elif choice == "7":
        print("\n=== 数据管理 ===")
        print("1. 保存数据")
        print("2. 重新加载数据")
        sub_choice = input("请选择：").strip()
        
        if sub_choice == "1":
            home.save_data()
            home.save_automation_rules()
        elif sub_choice == "2":
            print("重新加载数据会丢失当前未保存的更改，是否继续？(y/n)")
            confirm = input().strip().lower()
            if confirm == "y":
                home = smart_home.SmartHome()
                print("数据已重新加载。")

    # ---------------------- 运行自动化规则 -----------------------
    elif choice == "8":
        print("\n=== 运行自动化规则 ===")
        current_state = get_current_state()
        print(f"当前系统状态：")
        print(f"  温度: {current_state['temperature']}°C")
        print(f"  是否有人: {'是' if current_state['has_person'] else '否'}")
        print(f"  门锁状态: {'已锁' if current_state['door_locked'] else '未锁'}")
        
        triggered = home.automation.run_all(current_state)
        print(f"\n共触发了 {triggered} 条规则。")

    # ---------------------- 退出系统 -----------------------
    elif choice == "0":
        print("\n退出系统，再见！")
        home.save_data()
        home.save_automation_rules()
        break

    else:
        print("无效选项，请重新输入。")
