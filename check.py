import requests
import re
from concurrent.futures import ThreadPoolExecutor

# 配置需要抓取的国家源
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

OUTPUT_FILE = "IPTV_Channels.m3u"

def is_alive(channel):
    """
    保留你的核心逻辑：检查前 1KB 数据，确保有流输出
    """
    info, url = channel
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) VLC/3.0.18'
    }
    try:
        # stream=True 配合 timeout 防止卡死
        with requests.get(url, timeout=5, stream=True, headers=headers, allow_redirects=True) as response:
            if response.status_code == 200:
                # 检查是否有实际数据流
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        return f"{info}\n{url}"
                    break
    except:
        pass
    return None

def main():
    all_to_check = []
    
    # 1. 汇总所有国家的频道
    for country, url in SOURCES.items():
        print(f"正在读取源: {country}")
        try:
            r = requests.get(url, timeout=10)
            # 使用正则精准匹配 #EXTINF 和 紧随其后的 URL
            # 这比循环逐行判断要稳得多，能自动过滤空白行
            found = re.findall(r'(#EXTINF:.*)\n(http.*)', r.text)
            all_to_check.extend(found)
        except Exception as e:
            print(f"读取 {country} 失败: {e}")

    print(f"共收集到 {len(all_to_check)} 个频道，开始并发检测...")

    # 2. 引入多线程：将原本需要 1 小时的任务缩短到几分钟
    valid_channels = ["#EXTM3U"]
    # max_workers=20 是 GitHub 环境下的黄金比例
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(is_alive, all_to_check))
    
    # 3. 汇总有效结果并去重
    seen_urls = set()
    for res in results:
        if res:
            url = res.split('\n')[1]
            if url not in seen_urls: # 简单去重
                valid_channels.append(res)
                seen_urls.add(url)

    # 4. 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(valid_channels))
    
    print(f"全部完成！合并后共有 {len(valid_channels) - 1} 个有效频道。")

if __name__ == "__main__":
    main()
