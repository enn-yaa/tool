# CopyDownloadTime_v6.6.py
# 智能输入 + 自动速度单位匹配版
# 作者：enn-yaa 定制智能版

from datetime import datetime, timedelta

UNIT_MAP = {
    "m": 1,  # MB
    "g": 1024,  # GB
    "t": 1024 * 1024,  # TB
    "p": 1024 * 1024 * 1024,  # PB
}

def parse_file_size(size_input: str) -> float:
    """解析文件大小输入，支持 M/G/T/P，默认GB"""
    size_input = size_input.strip().lower()
    for u in UNIT_MAP:
        if size_input.endswith(u):
            return float(size_input[:-1]) * UNIT_MAP[u]
    return float(size_input) * UNIT_MAP["g"]  # 默认GB

def parse_speed_input(speed_input: str, default_unit: str) -> float:
    """解析速度输入，允许带单位或默认匹配"""
    speed_input = speed_input.strip().lower()
    for u in UNIT_MAP:
        if speed_input.endswith(u):
            return float(speed_input[:-1]) * UNIT_MAP[u]
    # 无单位则使用自动匹配的默认单位
    return float(speed_input) * UNIT_MAP[default_unit]

def auto_speed_unit(file_size_mb: float) -> str:
    """根据文件大小自动选择速度单位"""
    if file_size_mb < UNIT_MAP["t"]:  # < 1 TB
        return "m"  # MB/s
    elif file_size_mb < UNIT_MAP["p"]:  # < 1 PB
        return "g"  # GB/s
    else:
        return "t"  # TB/s

def format_duration(seconds: float) -> str:
    total_seconds = int(seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def format_size(mb_value: float) -> str:
    """格式化文件大小为合适单位"""
    if mb_value >= UNIT_MAP["p"]:
        return f"{mb_value / UNIT_MAP['p']:.2f} PB"
    elif mb_value >= UNIT_MAP["t"]:
        return f"{mb_value / UNIT_MAP['t']:.2f} TB"
    elif mb_value >= UNIT_MAP["g"]:
        return f"{mb_value / UNIT_MAP['g']:.2f} GB"
    else:
        return f"{mb_value:.2f} MB"

def format_speed(mb_s: float) -> str:
    """格式化速度为合适单位"""
    if mb_s >= UNIT_MAP["p"]:
        return f"{mb_s / UNIT_MAP['p']:.2f} PB/s"
    elif mb_s >= UNIT_MAP["t"]:
        return f"{mb_s / UNIT_MAP['t']:.2f} TB/s"
    elif mb_s >= UNIT_MAP["g"]:
        return f"{mb_s / UNIT_MAP['g']:.2f} GB/s"
    else:
        return f"{mb_s:.2f} MB/s"

def main():
    print("📦 CopyDownloadTime v6.6 - 智能匹配输入版")
    print("--------------------------------------------------")

    file_size_input = input("请输入文件大小（支持 M/G/T/P，默认GB）：").strip()
    file_size_mb = parse_file_size(file_size_input)
    default_speed_unit = auto_speed_unit(file_size_mb)

    # 根据文件大小给出提示
    unit_hint = {"m": "MB/s", "g": "GB/s", "t": "TB/s"}[default_speed_unit]
    speed_input = input(f"请输入传输速度（可输入单位，如 100G / 500M，不输入默认 {unit_hint}）：").strip()

    speed_mb_s = parse_speed_input(speed_input, default_speed_unit)

    total_seconds = file_size_mb / speed_mb_s
    finish_time = datetime.now() + timedelta(seconds=total_seconds)

    print("\n---------------- 计算结果 ----------------")
    print(f"📁 文件大小：{format_size(file_size_mb)}")
    print(f"🚀 速度：{format_speed(speed_mb_s)}")
    print(f"⏱️ 预计用时：{format_duration(total_seconds)}")
    print(f"🕒 预计完成时间：{finish_time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("------------------------------------------")

if __name__ == "__main__":
    main()
