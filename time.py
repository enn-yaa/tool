from datetime import datetime, timedelta

def calculate_finish_time(video_time_str, speed):
    """计算视频播放完成时间和播放时长"""
    # 获取当前时间
    current_time = datetime.now()

    # 解析视频时长
    if ':' in video_time_str:
        h, m, s = 0, 0, 0
        time_parts = video_time_str.split(':')
        if len(time_parts) == 3:
            h, m, s = map(int, time_parts)
        elif len(time_parts) == 2:
            h, m = map(int, time_parts)
        elif len(time_parts) == 1:
            m = int(time_parts[0])
        total_seconds = h * 3600 + m * 60 + s
    else:
        total_seconds = int(video_time_str) * 60

    # 计算倍速后的播放时长
    playback_time_seconds = total_seconds / speed

    # 计算视频播放完成时间
    finish_time = current_time + timedelta(seconds=playback_time_seconds)

    # 如果播放时间超过一天，显示日期
    if finish_time.date() > current_time.date():
        finish_time_str = finish_time.strftime("%Y-%m-%d %H:%M:%S")
    else:
        # 否则仅格式化为时间
        finish_time_str = finish_time.strftime("%H:%M:%S")

    playback_duration_str = format_duration(playback_time_seconds)

    return finish_time_str, playback_duration_str

def format_duration(total_seconds):
    """格式化时长输出"""
    total_minutes = int(total_seconds) // 60
    seconds = int(total_seconds) % 60

    if total_minutes < 60:
        # Less than 60 minutes: display MM:SS
        return f"{total_minutes:02}:{seconds:02}"
    elif 60 <= total_minutes < 100:
        # Between 60 and 100 minutes: display MM:SS
        return f"{total_minutes}:{seconds:02}"
    else:
        # 100 minutes or more: display H:MM:SS and MM:SS
        hours = total_minutes // 60
        minutes = total_minutes % 60
        return f"{hours}:{minutes:02}:{seconds:02} ({total_minutes}:{seconds:02})"

if __name__ == "__main__":
    video_time_str = input("请输入视频时长（格式：6:22:22，或分钟数，136）：")
    speed = float(input("请输入播放速度（倍速，例如 1.5 或 2）："))

    finish_time_str, playback_duration_str = calculate_finish_time(video_time_str, speed)

    print(f"视频倍速后的花费时长是：{playback_duration_str}")
    print(f"视频播放完成时间为：{finish_time_str}")
