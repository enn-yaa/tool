# CopyDownloadTime.py
# 实时进度显示版 - 文件下载/拷贝计时器
# 作者：enn-yaa（增强版模板）
# 功能：
#   输入文件总大小（默认MB，支持G/g），输入预计平均速度（MB/s）
#   程序实时显示进度、剩余时间与已用时间

import time
import sys
from datetime import datetime, timedelta

def parse_file_size(size_input: str) -> float:
    """解析文件大小输入，默认MB，若带G或g则转换为MB"""
    size_input = size_input.strip().lower()
    if size_input.endswith('g'):
        return float(size_input[:-1]) * 1024
    return float(size_input)

def format_duration(seconds: float) -> str:
    """格式化秒数为 hh:mm:ss"""
    total_seconds = int(seconds)
    h = total_seconds // 3600
    m = (total_seconds % 3600) // 60
    s = total_seconds % 60
    return f"{h:02}:{m:02}:{s:02}"

def show_progress(file_size_mb, speed_mb_s):
    """实时模拟进度显示"""
    total_seconds = file_size_mb / speed_mb_s
    start_time = datetime.now()
    print("\n📦 实时下载/拷贝进度监控开始！按 Ctrl+C 可提前结束。\n")

    try:
        for i in range(int(total_seconds) + 1):
            elapsed = i
            completed_mb = speed_mb_s * elapsed
            progress = min(completed_mb / file_size_mb, 1.0)
            percent = progress * 100

            remaining_seconds = total_seconds - elapsed
            bar_len = 40
            filled_len = int(bar_len * progress)
            bar = "█" * filled_len + "-" * (bar_len - filled_len)

            sys.stdout.write(
                f"\r[{bar}] {percent:6.2f}% | "
                f"{completed_mb:8.2f}/{file_size_mb:.2f} MB | "
                f"{speed_mb_s:.2f} MB/s | "
                f"已用 {format_duration(elapsed)} | "
                f"剩余 {format_duration(remaining_seconds)}"
            )
            sys.stdout.flush()
            time.sleep(1)
        print("\n\n✅ 传输完成！")
        print(f"总用时：{format_duration(total_seconds)}")
        print(f"完成时间：{(start_time + timedelta(seconds=total_seconds)).strftime('%Y-%m-%d %H:%M:%S')}")
    except KeyboardInterrupt:
        elapsed_time = (datetime.now() - start_time).total_seconds()
        progress = min(speed_mb_s * elapsed_time / file_size_mb, 1.0)
        print(f"\n\n⚠️ 已手动中止。已传输 {progress*100:.2f}% ，耗时 {format_duration(elapsed_time)}。")

def main():
    print("📦 CopyDownloadTime - 实时进度计时器")
    print("--------------------------------------------------")
    file_size_input = input("请输入文件总大小（默认MB，输入1025G表示GB）：").strip()
    avg_speed = float(input("请输入预计平均速度（MB/s）：").strip())

    file_size_mb = parse_file_size(file_size_input)

    show_progress(file_size_mb, avg_speed)

if __name__ == "__main__":
    main()
