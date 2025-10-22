# CopyDownloadTime_v7.3.py
# 简洁·稳定·高效版
# 作者：enn-yaa 定制旗舰版

import time, sys, platform, subprocess
from datetime import datetime, timedelta

# ---------- colorama 自动检测 ----------
def ensure_colorama():
    if platform.system() == "Windows":
        try:
            import colorama; colorama.init()
        except ImportError:
            print("检测到未安装 colorama，正在自动安装...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", "colorama"],
                    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                import colorama; colorama.init()
                print("✅ colorama 安装成功！\n")
            except Exception as e:
                print("⚠️ colorama 自动安装失败，请手动执行：pip install colorama\n", e)

ensure_colorama()

# ---------- 单位换算 ----------
UNIT = {"m":1, "g":1024, "t":1024**2, "p":1024**3}

def parse_size(s:str)->float:
    s=s.strip().lower()
    for u in UNIT:
        if s.endswith(u): return float(s[:-1])*UNIT[u]
    return float(s)*UNIT["g"]

def auto_speed_unit(size_mb:float)->str:
    if size_mb<UNIT["t"]: return "m"
    elif size_mb<UNIT["p"]: return "g"
    else: return "t"

def parse_speed(s:str,default:str)->float:
    s=s.strip().lower()
    for u in UNIT:
        if s.endswith(u): return float(s[:-1])*UNIT[u]
    return float(s)*UNIT[default]

def fmt_time(sec:float)->str:
    sec=int(sec);h,m=divmod(sec,3600);m,s=divmod(m,60)
    return f"{h:02}:{m:02}:{s:02}"

def fmt_size(mb:float)->str:
    if mb>=UNIT["p"]: return f"{mb/UNIT['p']:.2f} PB"
    elif mb>=UNIT["t"]: return f"{mb/UNIT['t']:.2f} TB"
    elif mb>=UNIT["g"]: return f"{mb/UNIT['g']:.2f} GB"
    else: return f"{mb:.2f} MB"

def fmt_speed(mb_s:float)->str:
    if mb_s>=UNIT["p"]: return f"{mb_s/UNIT['p']:.2f} PB/s"
    elif mb_s>=UNIT["t"]: return f"{mb_s/UNIT['t']:.2f} TB/s"
    elif mb_s>=UNIT["g"]: return f"{mb_s/UNIT['g']:.2f} GB/s"
    else: return f"{mb_s:.2f} MB/s"

# ---------- 主进度逻辑 ----------
def show_progress(size_mb,speed_mb_s):
    total=size_mb/speed_mb_s
    start=datetime.now()
    bar_len=40
    print("\n📦 实时进度模拟中...（Ctrl+C 可中断）\n")

    try:
        for i in range(int(total)+1):
            elapsed=i
            done=min(speed_mb_s*elapsed,size_mb)
            progress=done/size_mb
            percent=progress*100
            remain=max(total-elapsed,0)
            finish=start+timedelta(seconds=remain)
            bar="█"*int(bar_len*progress)+"-"*(bar_len-int(bar_len*progress))

            # —— 清行并刷新 —— #
            sys.stdout.write("\033[2K\r")
            sys.stdout.write(
                f"[{bar}] {percent:6.2f}% | "
                f"{fmt_size(done)} / {fmt_size(size_mb)} | "
                f"{fmt_speed(speed_mb_s)} | "
                f"已用 {fmt_time(elapsed)} | 剩余 {fmt_time(remain)}\n"
                f"🕒 预计完成时间：{finish.strftime('%Y-%m-%d %H:%M:%S')}"
            )
            sys.stdout.flush()
            time.sleep(1)
            sys.stdout.write("\033[F")  # 光标上移一行
        # ---- 结束输出 ----
        print("\n\n✅ 传输完成！")
        print(f"📁 文件大小：{fmt_size(size_mb)}")
        print(f"🚀 速度：{fmt_speed(speed_mb_s)}")
        print(f"⏱️ 预计用时：{fmt_time(total)}")
        print(f"🕒 完成时间：{(start+timedelta(seconds=total)).strftime('%Y-%m-%d %H:%M:%S')}")
    except KeyboardInterrupt:
        used=(datetime.now()-start).total_seconds()
        prog=min(speed_mb_s*used/size_mb,1.0)
        print(f"\n\n⚠️ 手动中止。当前进度 {prog*100:.2f}%，已用 {fmt_time(used)}。")

# ---------- 主程序 ----------
def main():
    print("📦 CopyDownloadTime v7.3 - 简洁高效版")
    print("--------------------------------------------------")
    f_in=input("请输入文件大小（支持 M/G/T/P，默认GB）：").strip()
    size_mb=parse_size(f_in)
    default=auto_speed_unit(size_mb)
    hint={"m":"MB/s","g":"GB/s","t":"TB/s"}[default]
    s_in=input(f"请输入传输速度（可带单位，如 500M / 200G，不输入默认 {hint}）：").strip()
    speed_mb_s=parse_speed(s_in,default)
    show_progress(size_mb,speed_mb_s)

if __name__=="__main__":
    main()
