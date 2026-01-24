import requests

# 配置需要抓取的国家源列表
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

OUTPUT_FILE = "IPTV_Channels.m3u"

def is_alive(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
    }
    try:
        # 改用 GET 并开启 stream=True
        # timeout 设为 5 秒，防止被卡死
        with requests.get(url, timeout=5, stream=True, headers=headers, allow_redirects=True) as response:
            if response.status_code == 200:
                # 检查前 1KB 数据，确保真的有数据流输出
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        return True
                    break
        return False
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
