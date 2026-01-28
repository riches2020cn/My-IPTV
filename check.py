import requests

# 配置源列表
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

OUTPUT_FILE = "IPTV_Channels.m3u"

def main():
    merged_content = ["#EXTM3U"]
    
    for country, url in SOURCES.items():
        print(f"正在合并: {country}")
        try:
            # 下载源文件
            r = requests.get(url, timeout=15)
            r.raise_for_status() # 如果下载失败会抛出异常
            
            # 将内容按行拆分
            lines = r.text.splitlines()
            
            # 过滤掉第一行的 #EXTM3U，只保留频道数据
            for line in lines:
                line = line.strip()
                if line and not line.startswith("#EXTM3U"):
                    merged_content.append(line)
                    
        except Exception as e:
            print(f"无法获取 {country} 的数据: {e}")

    # 将所有内容写入最终文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(merged_content))
    
    print(f"\n合并完成！文件已保存为 {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
