import requests
import time
from concurrent.futures import ThreadPoolExecutor

# 保持源不变
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

def is_alive_ultra(url, retries=2):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    
    for i in range(retries):
        try:
            # 增加等待时间，防止请求过快
            time.sleep(0.5) 
            
            # 这里的 timeout 给到 15 秒，stream=True 是关键
            with requests.get(url, timeout=15, stream=True, headers=headers, allow_redirects=True) as r:
                if r.status_code == 200:
                    # 检查内容长度或类型
                    content_type = r.headers.get('Content-Type', '').lower()
                    if 'html' in content_type: # 如果回的是网页，说明是报错页或验证码
                        return False
                    
                    # 尝试读取至少 512KB 内容
                    chunk_count = 0
                    for chunk in r.iter_content(chunk_size=128 * 1024):
                        if chunk:
                            chunk_count += 1
                        if chunk_count >= 4: # 128KB * 4 = 512KB
                            return True
            return False
        except:
            if i == retries - 1:
                return False
            time.sleep(2) # 失败后等 2 秒再重试
    return False

def process_source(country, url):
    valid_channels = []
    print(f"--- 正在精测 {country} ---")
    try:
        r = requests.get(url, timeout=20)
        lines = r.text.split('\n')
        tasks = []
        temp_info = None
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                temp_info = line
            elif line.startswith("http") and temp_info:
                tasks.append((temp_info, line))
                temp_info = None

        # 核心：将并发数控制在 5 以内，宁可慢，也要准
        with ThreadPoolExecutor(max_workers=5) as executor:
            results = list(executor.map(lambda x: (x[0], x[1], is_alive_ultra(x[1])), tasks))

        for info, link, alive in results:
            if alive:
                valid_channels.append(info)
                valid_channels.append(link)
    except Exception as e:
        print(f"Error: {e}")
    return valid_channels

# ... main 函数保持不变 ...
