import requests
import json

API_URL = "https://www.ziyuanzu.com/api/v1/sources"
OUTPUT_FILE = "libretv-sources.json"

try:
    resp = requests.get(API_URL, timeout=30)
    resp.raise_for_status()
    raw_list = resp.json()
except Exception as e:
    print(f"接口拉取失败:{e}")
    raw_list = []

out_sources = []
for item in raw_list:
    name = item.get("name","未知源")
    api_url = item.get("api","")
    if not api_url:
        continue
    out_sources.append({
        "name": name,
        "url": api_url,
        "detail": api_url,
        "isAdult": False
    })

result = {
    "name": "Ziyuanzu自动更新源",
    "version": 2,
    "sources": out_sources,
    "liveSources": [
        {
            "name": "国内IPTV",
            "url": "https://iptv.whaleclouds.com/iptv.m3u",
            "epg": "https://epg.whaleclouds.com/epg.xml.gz"
        }
    ]
}

with open(OUTPUT_FILE,"w",encoding="utf-8") as f:
    json.dump(result,f,ensure_ascii=False,indent=2)

print(f"生成完成，有效源数量：{len(out_sources)}")
