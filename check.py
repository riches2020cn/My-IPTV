import requests

# 配置需要抓取的国家源列表
SOURCES = {
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u",
    "Hong Kong": "https://iptv-org.github.io/iptv/countries/hk.m3u",
    "Macau": "https://iptv-org.github.io/iptv/countries/mo.m3u",
    "Taiwan": "https://iptv-org.github.io/iptv/countries/tw.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u"
}

OUTPUT_FILE = "live_channels.m3u"

def is_alive(url):
    """检测链接是否有效"""
    try:
        # 使用 HEAD 请求节省流量，超时设为 3 秒
        response = requests.head(url, timeout=3, allow_redirects=True)
        return response.status_code == 200
    except:
        return False

def main():
    merged_list = ["#EXTM3U"]
    total_valid = 0

    for country, url in SOURCES.items():
        print(f"--- 正在处理: {country} ---")
        try:
            r = requests.get(url, timeout=10)
            lines = r.text.split('\n')
            
            current_info = None
            for line in lines:
                line = line.strip()
                if line.startswith("#EXTINF"):
                    current_info = line
                elif line.startswith("http"):
                    # 执行检测
                    if is_alive(line):
                        if current_info:
                            merged_list.append(current_info)
                        merged_list.append(line)
                        total_valid += 1
                        print(f"[OK] {line[:50]}...")
                    current_info = None
        except Exception as e:
            print(f"处理 {country} 时出错: {e}")

    # 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_list))
    
    print(f"\n全部完成！合并后共有 {total_valid} 个有效频道。")

if __name__ == "__main__":
    main()
