import requests
import datetime

# 1. 配置源列表
SOURCES = {
    "Singapore": "https://iptv-org.github.io/iptv/countries/sg.m3u",
    "USA": "https://iptv-org.github.io/iptv/countries/us.m3u",
    "UK": "https://iptv-org.github.io/iptv/countries/uk.m3u",
    "Australia": "https://iptv-org.github.io/iptv/countries/au.m3u",
    "Canada": "https://iptv-org.github.io/iptv/countries/ca.m3u",
    "New Zealand": "https://iptv-org.github.io/iptv/countries/nz.m3u",
    "Ireland": "https://iptv-org.github.io/iptv/countries/ie.m3u"    
}

OUTPUT_FILE = "IPTV_Channels.m3u"
ALIVE_FILE = "keep_alive.txt"

def main():
    final_output = ["#EXTM3U"]
    print("🚀 正在开始合并...")

    for country, url in SOURCES.items():
        try:
            r = requests.get(url, timeout=20)
            r.raise_for_status()
            r.encoding = 'utf-8'
            
            text = r.text.lstrip('\ufeff').strip()
            lines = text.split('\n')
            
            if lines:
                start_index = 1 if lines[0].startswith("#EXTM3U") else 0
                final_output.extend(lines[start_index:])
                print(f"✅ 已合并: {country}")
        except Exception as e:
            print(f"❌ {country} 获取失败: {e}")

    # 保存 M3U 文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
        
    # --- 关键：保持 GitHub Actions 激活的“心脏跳动” ---
    with open(ALIVE_FILE, "w", encoding="utf-8") as f:
        f.write(f"Last active: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    print(f"\n✨ 任务完成！M3U 已更新，{ALIVE_FILE} 已激活。")

if __name__ == "__main__":
    main()
