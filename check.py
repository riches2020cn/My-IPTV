import subprocess
import re
from concurrent.futures import ThreadPoolExecutor

# 配置需要抓取的国家源列表
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

def is_truly_alive(url):
    """
    使用 ffprobe 探测流媒体信息
    """
    cmd = [
        'ffprobe', 
        '-v', 'error', 
        '-show_entries', 'stream=codec_type', 
        '-of', 'default=noprint_wrappers=1:nokey=1', 
        '-select_streams', 'v:0', # 只看视频流
        '-timeout', '5000000',    # 微秒单位，5秒超时
        url
    ]
    try:
        # 执行命令，捕获输出
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=7)
        # 如果输出了 'video'，说明流是可以解码的
        if "video" in result.stdout:
            return True
    except Exception:
        return False
    return False

def check_channel(info, url):
    # 先用 requests 快速初筛，节省 ffprobe 的开销
    print(f"正在深度检测: {url[:50]}...")
    if is_truly_alive(url):
        return f"{info}\n{url}"
    return None

# ... main 函数逻辑（参考上一轮，将 check_url 替换为 check_channel） ...
