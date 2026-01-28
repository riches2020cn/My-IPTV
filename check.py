import requests
import subprocess
import concurrent.futures
import re

# 配置需要抓取的国家源列表 (iptv-org 的源)
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

OUTPUT_FILE = "IPTV_Channels.m3u"

def check_with_ffprobe(url):
    """
    使用 ffprobe 检测视频流是否真实有效
    """
    # -v error: 只显示错误
    # -show_entries: 只看视频流信息
    # -timeout: 5000000 微秒 (即 5 秒)
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'stream=codec_type', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        '-timeout', '5000000', 
        url
    ]
    try:
        # 如果 ffprobe 成功获取到视频流信息，说明频道可以打开
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if "video" in result.stdout:
            return True
    except:
        pass
    return False

def verify_channel(channel):
    info, url = channel
    # 1. 快速初筛 (HTTP 状态码)
    try:
        r = requests.head(url, timeout=3, allow_redirects=True)
        if r.status_code >= 400:
            return None
    except:
        return None

    # 2. 深度探测 (是否真的有视频数据)
    if check_with_ffprobe(url):
        print(f"[SUCCESS] {url[:50]}")
        return f"{info}\n{url}"
    else:
        print(f"[FAILED] {url[:50]}")
        return None

def main():
    tasks = []
    # 抓取源列表
    for country, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=10)
            # 提取 #EXTINF 和对应的 URL
            found = re.findall(r'(#EXTINF:.*)\n(http.*)', r.text)
            tasks.extend(found)
        except:
            continue

    print(f"开始深度检测 {len(tasks)} 个频道...")

    results = []
    # 使用线程池并发执行，提高速度
    # GitHub Actions 核心数有限，建议 max_workers 设在 10-20 左右
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        results = list(executor.map(verify_channel, tasks))

    # 汇总有效频道
    final_m3u = ["#EXTM3U"]
    for item in results:
        if item:
            final_m3u.append(item)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_m3u))

if __name__ == "__main__":
    main()
