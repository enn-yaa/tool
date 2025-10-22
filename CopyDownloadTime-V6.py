# CopyDownloadTime.py
# CopyDownloadTime V6 — 自动单位 + 自适应刷新频率 + 智能速度显示
# 作者：enn-yaa（旗舰专业版）
# 特点：
#   ✅ 支持 MB / GB / TB / PB 单位自动识别与换算
#   ✅ 智能速度显示（自动切换 MB/s ↔ GB/s）
#   ✅ 自适应刷新频率（即使秒传也能动态显示）
#   ✅ 精准时间格式化与完成时间预测

import time
import sys
from datetime import datetime, timedelta

# ===== 工具函数 =====

def parse_file_size(size_input: str) -> float:
    """解析文件大小输入，自动识别 MB / GB / TB / PB 单位，统一转成 MB"""
    size_input = size_input.strip().lower()
    units = {"mb": 1, "gb": 1024, "tb": 1024**2, "pb": 1024**3}

    for unit, multiplier in units.items():
        if size_input.endswith(unit):
            return float(size_input.replace(unit, "")) * multiplier

    # 若无单位，默认 GB
    return float(size_input) * 1024

def format_duration(seconds: float) -> str:
    """格式化秒数为 hh:mm:ss"""
    total_seconds = int(seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def human_speed(speed_mb_s: float) -> str:
    """速度自动换算为 MB/s 或 GB/s"""
    return f"{speed_mb_s / 1024:.2f} GB/s" if speed_mb_s >= 1024 else f"{speed_mb_s:.2f} MB/s"

def human_size(mb_value: float) -> str:
    """自动选择文件大小显示单位"""
    if mb_value >= 1024**3:
        return f"{mb_value / 1024**3:.2f} PB"
    elif mb_value >= 1024**2:
        return f"{mb_value / 1024**2:.2f} TB"
    elif mb_value >= 1024:
        return f"{mb_value / 1024:.2f} GB"
    else:
        return f"{mb_value:.2f} MB"

# ===== 主进度显示逻辑 =====

def show_progress(file_size_mb: float, speed_mb_s: float):
    total_seconds = file_size_mb / speed_mb_s
    start_time = datetime.now()
    end_time = start_time + timedelta(seconds=total_seconds)

    # 自适应刷新频率：最少 0.1 秒，最多 1 秒
    refresh_interval = max(0.1, min(total_seconds / 100, 1))
    total_steps = int(total_seconds / refresh_interval)

    print("\n📦 实时下载/拷贝进度监控开始！按 Ctrl+C 可提前结束。\n")
    print(f"📁 文件大小：{human_size(file_size_mb)}")
    print(f"🚀 速度：{human_speed(speed_mb_s)}")
    print(f"⏱️ 预计用时：{format_duration(total_seconds)}")
    print(f"🕒 预计完成时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}\n")

    try:
        for step in range(total_steps + 1):
            elapsed = step * refresh_interval
            completed_mb = min(speed_mb_s * elapsed, file_size_mb)
            progress = completed_mb / file_size_mb
            percent = progress * 100

            remaining_seconds = max(0, total_seconds - elapsed)
            bar_len = 40
            filled_len = int(bar_len * progress)
            bar = "█" * filled_len + "-" * (bar_len - filled_len)

            sys.stdout.write(
                f"\r[{bar}] {percent:6.2f}% | "
                f"{human_size(completed_mb):>10} / {human_size(file_size_mb):<10} | "
                f"{human_speed(speed_mb_s):>10} | "
                f"已用 {format_duration(elapsed)} | "
                f"剩余 {format_duration(remaining_seconds)}"
            )
            sys.stdout.flush()
            time.sleep(refresh_interval)

        print("\n\n✅ 传输完成！")
        print(f"总用时：{format_duration(total_seconds)}")
        print(f"完成时间：{end_time.strftime('%Y-%m-%d %H:%M:%S')}")

    except KeyboardInterrupt:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        progress = min(speed_mb_s * elapsed_time / file_size_mb, 1.0)
        print(f"\n\n⚠️ 已手动中止。已传输 {progress*100:.2f}% ，耗时 {format_duration(elapsed_time)}。")

# ===== 主程序入口 =====

def main():
    print("📦 CopyDownloadTime V6 - 智能文件传输计时器")
    print("--------------------------------------------------")
    file_size_input = input("请输入文件大小（支持 MB / GB / TB / PB，默认GB）：").strip()
    avg_speed = float(input("请输入传输速度（MB/s）：").strip())

    file_size_mb = parse_file_size(file_size_input)
    show_progress(file_size_mb, avg_speed)

if __name__ == "__main__":
    main()
