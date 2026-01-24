import requests
from concurrent.futures import ThreadPoolExecutor

# 配置源
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "Hong Kong": "https://iptv-org.github.io/iptv/countries/hk.m3u",
    "Macau": "https://iptv-org.github.io/iptv/countries/mo.m3u",
    "Taiwan": "https://iptv-org.github.io/iptv/countries/tw.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

def is_alive(url):
    """检测单个链接"""
    try:
        # 使用 GET 但只请求前几个字节，比 HEAD 更准确，比完整 GET 更快
        response = requests.get(url, timeout=5, stream=True, allow_redirects=True)
        if response.status_code == 200:
            return True
        return False
    except:
        return False

def process_source(country, url):
    """处理单个国家源并返回有效频道列表"""
    valid_channels = []
    print(f"正在抓取: {country}")
    try:
        r = requests.get(url, timeout=10)
        lines = r.text.split('\n')
        
        tasks = []
        # 预先提取频道信息和 URL 对
        temp_info = None
        for line in lines:
            line = line.strip()
            if line.startswith("#EXTINF"):
                temp_info = line
            elif line.startswith("http") and temp_info:
                tasks.append((temp_info, line))
                temp_info = None

        # 使用多线程池加速检测
        with ThreadPoolExecutor(max_workers=20) as executor:
            # 这里的 20 个线程是安全阈值，既快又不容易被封 IP
            results = list(executor.map(lambda x: (x[0], x[1], is_alive(x[1])), tasks))

        for info, link, alive in results:
            if alive:
                valid_channels.append(info)
                valid_channels.append(link)
        
        print(f"{country}: 检测完成，有效 {len(valid_channels)//2} 个")
    except Exception as e:
        print(f"{country} 处理失败: {e}")
    return valid_channels

def main():
    final_m3u = ["#EXTM3U"]
    
    for country, url in SOURCES.items():
        channels = process_source(country, url)
        final_m3u.extend(channels)

    with open("live_channels.m3u", "w", encoding="utf-8") as f:
        f.write("\n".join(final_m3u))
    print(f"所有任务已完成，结果已保存。")

if __name__ == "__main__":
    main()
