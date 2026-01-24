import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 配置源
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

def is_alive(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    }
    try:
        # 1. 增加超时到 10 秒，给高清源更多响应时间
        # 2. stream=True 持续观察流
        response = requests.get(url, timeout=10, stream=True, headers=headers, allow_redirects=True)
        
        if response.status_code == 200:
            # 检查是否为常见的视频流格式
            content_type = response.headers.get('Content-Type', '').lower()
            valid_types = ['video', 'mpegurl', 'application/octet-stream', 'application/x-mpegurl']
            
            if any(vt in content_type for vt in valid_types):
                # 核心改进：尝试读取 512KB 数据并计时
                start_time = time.time()
                bytes_received = 0
                for chunk in response.iter_content(chunk_size=1024 * 64):
                    if chunk:
                        bytes_received += len(chunk)
                    # 只要能读到 256KB 且没花太长时间，就认为是有内容的流
                    if bytes_received >= 1024 * 256:
                        return True
                    if time.time() - start_time > 5: # 超过5秒还没读够，说明流太慢，放弃
                        break
        return False
    except:
        return False

# ... 其余 process_source 和 main 函数保持不变 ...
