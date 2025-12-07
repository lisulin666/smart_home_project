import smart_home

import logger


home = smart_home.SmartHome()


print("欢迎进入智能家居控制系统！")

while True:
    print("\n========= 菜单 =========")
    print("1. 添加用户")
    print("2. 添加设备")
    print("3. 查看所有设备")
    print("4. 共享设备")
    print("5. 保存数据")
    print("6. 退出系统")
    print("7. 添加自动化规则")
    print("========================")

    choice = input("请输入选项编号：").strip()

    # ---------------------- 添加用户 -----------------------
    if choice == "1":
        username = input("请输入用户名：").strip()
        home.add_user(username)
        print(f"用户 {username} 已创建。")

    # ---------------------- 添加设备 -----------------------
    elif choice == "2":
        dtype = input("设备类型（如 light / aircon / moodlight）：").strip()
        did = input("设备ID：").strip()
        owner = input("设备所有者用户名：").strip()

        home.add_device(dtype, did, owner)

    # ---------------------- 查看所有设备 -----------------------
    elif choice == "3":
        print("\n当前系统设备：")
        home.show_devices()

    # ---------------------- 共享设备 -----------------------
    elif choice == "4":
        did = input("设备ID：").strip()
        username = input("共享给哪个用户：").strip()

        home.share_device(did, username)
        print("共享完成。")

    # ---------------------- 保存数据 -----------------------
    elif choice == "5":
        home.save_data()
        print("数据已保存。")

    # ---------------------- 退出系统 -----------------------
    elif choice == "6":
        print("退出系统，再见！")
        break
    elif choice == "7":
        print("\n=== 添加自动化规则 ===")
        from automation import AutomationRule
        
        def cond(state):
            return state.get("temperature", 0) > 30
    
        def act(state):
            print("自动化动作：打开空调！")
            # 遍历所有设备，找到类型为 aircon 的设备并打开
            for device_id, device in home.devices.items():
                if device.name == "aircon":
                    device.turn_on()
                    print(f"已自动打开空调设备 {device_id}")
                    break
        
        rule = AutomationRule(cond, act)
        home.automation.add_rule(rule)
        print("规则已添加。")

    else:
        print("无效选项，请重新输入。")
