from datetime import datetime

def log(action):
    """
    简单日志记录函数：
    每次操作都会记录到 logs.txt 文件
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {action}\n")
