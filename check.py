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
    # M3U 文件头
    final_output = ["#EXTM3U"]
    
    print("🚀 开始快速合并频道列表 (无去重/无检测)...")

    for country, url in SOURCES.items():
        try:
            # 获取内容并强制指定编码为 utf-8 以防止乱码
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            r.encoding = 'utf-8' 
            
            # 处理内容，去掉首行的 #EXTM3U
            # .lstrip('\ufeff') 是为了移除可能存在的 UTF-8 BOM 字符
            raw_text = r.text.lstrip('\ufeff').strip()
            lines = raw_text.split('\n')
            
            if lines:
                if lines[0].startswith("#EXTM3U"):
                    content_without_header = lines[1:]
                else:
                    content_without_header = lines
                
                final_output.extend(content_without_header)
                print(f"✅ 已成功合并: {country} (共 {len(content_without_header)//2} 个频道左右)")
        except Exception as e:
            print(f"❌ 无法抓取 {country}: {e}")

    # 3. 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
    
    print(f"\n✨ 全部任务完成！合并后的文件：{OUTPUT_FILE}")

if __name__ == "__main__":
    main()
