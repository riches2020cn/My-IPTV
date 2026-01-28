import requests
import re

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
    # 使用字典进行去重：Key 是 URL，Value 是 #EXTINF 信息
    # 这样如果有完全相同的 URL，字典会自动去重
    unique_channels = {} 
    
    print("开始获取并合并频道列表...")

    for country, url in SOURCES.items():
        print(f"--- 正在下载: {country} ---")
        try:
            # 获取网页内容，超时设为 15 秒确保稳定
            r = requests.get(url, timeout=15)
            r.raise_for_status()
            
            # 使用正则表达式成对提取 #EXTINF 行和紧随其后的 http 链接
            # 这能完美解决空行、乱码导致的错位问题
            pattern = r'(#EXTINF:.*)\n(http.*)'
            matches = re.findall(pattern, r.text)
            
            count = 0
            for info, link in matches:
                clean_link = link.strip()
                if clean_link not in unique_channels:
                    # 如果 URL 没出现过，存入字典
                    unique_channels[clean_link] = info.strip()
                    count += 1
            
            print(f"从 {country} 中新增了 {count} 个唯一频道")
                    
        except Exception as e:
            print(f"获取 {country} 失败: {e}")

    # 2. 构建最终的 M3U 内容
    final_output = ["#EXTM3U"]
    for link, info in unique_channels.items():
        final_output.append(info)
        final_output.append(link)

    # 3. 写入文件
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(final_output))
    
    print("-" * 30)
    print(f"全部完成！")
    print(f"合并后总频道数（已去重）: {len(unique_channels)}")
    print(f"输出文件: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
