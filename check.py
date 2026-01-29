import requests

# 1. 配置源列表
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u"
}

OUTPUT_FILE = "IPTV_Channels.m3u"

def main():
    final_output = ["#EXTM3U"]
    
    print("🚀 开始快速合并频道列表 (无去重/无检测)...")

    for country, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            
            # 简单粗暴：移除每个文件的第一行 #EXTM3U，然后合并剩余内容
            lines = r.text.strip().split('\n')
            if lines and lines[0].startswith("#EXTM3U"):
                content_without_header = lines[1:]
                final_output.extend(content_without_header)
                print(f"✅ 已合并: {country}")
        except Exception as e:
            print(f"❌ 无法获取 {country}: {e}")

    # 3. 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
    
    print(f"\n✨ 完成！结果已保存至: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
