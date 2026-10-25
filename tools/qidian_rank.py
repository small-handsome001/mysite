"""起点月票榜 → assets/rank.json

用法：
    python tools/qidian_rank.py

依赖：requests / lxml / fontTools
说明：
    起点有反爬，必须带登录态 cookie。cookie 从浏览器 F12 → Network →
    任意请求的 Request Headers 里复制，存成 tools/cookie.json（字典）。

    脚本只取榜单前 20 条，不翻页、不高频请求。
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

import requests
from fontTools.ttLib import TTFont
from lxml import etree

ROOT = Path(__file__).resolve().parent.parent
COOKIE_FILE = ROOT / "tools" / "cookie.json"
OUT_FILE = ROOT / "assets" / "rank.json"

URL = "https://www.qidian.com/rank/yuepiao"

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

# 字体里的字母名 → 真实数字
NUMBER_MAP = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
    "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9,
    "period": ".",
}


def load_cookies():
    if not COOKIE_FILE.exists():
        sys.exit(
            f"缺少 {COOKIE_FILE}\n"
            "从浏览器 F12 → Network 复制请求头里的 Cookie，"
            '存成 {"名称": "值", ...} 的 JSON。'
        )
    with open(COOKIE_FILE, encoding="utf-8") as f:
        return json.load(f)


def build_cmap(woff_bytes):
    """把字体里的乱码字符映射回真实数字。"""
    tmp = ROOT / "tools" / ".font.woff"
    tmp.write_bytes(woff_bytes)

    cmap = TTFont(str(tmp)).getBestCmap()
    tmp.unlink(missing_ok=True)

    result = {}
    for code, name in cmap.items():
        # name 形如 "uniE3A1" 时跳过，只认 one/two/period 这种
        if name in NUMBER_MAP:
            result[code] = NUMBER_MAP[name]
    return result


def decode(text, cmap):
    """把一串乱码字符换成 '107593' 这样的字符串。"""
    out = []
    for ch in text:
        if ch in ".0123456789":      # 有些条目没被加密
            out.append(ch)
        else:
            digit = cmap.get(ord(ch))
            if digit is not None:
                out.append(str(digit))
    return "".join(out)


def main():
    cookies = load_cookies()

    print("请求榜单页 ...")
    resp = requests.get(URL, headers=HEADERS, cookies=cookies, timeout=20)
    if "book-mid-info" not in resp.text:
        sys.exit(
            f"没拿到榜单（HTTP {resp.status_code}）。"
            "八成是 cookie 过期，重新复制一份。"
        )

    tree = etree.HTML(resp.text)
    titles = tree.xpath("//div[@class='book-mid-info']/h2/a/text()")
    tickets = tree.xpath("//span/span/text()")

    print(f"解析到 {len(titles)} 本书，下载字体 ...")
    font_url = re.findall(r"format\('eot'\); src: url\('(.*?)'\) format\('woff'\)", resp.text)[0]
    font_resp = requests.get(font_url, headers=HEADERS, cookies=cookies, timeout=20)
    cmap = build_cmap(font_resp.content)

    books = []
    for index, (title, raw) in enumerate(zip(titles, tickets), start=1):
        books.append({
            "rank": index,
            "title": title,
            "tickets": int(decode(raw, cmap) or 0),
        })

    OUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "source": URL,
        "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(books),
        "books": books,
    }
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    print(f"已写入 {OUT_FILE}（{len(books)} 条）")
    for b in books[:3]:
        print(f"  {b['rank']}. {b['title']}  {b['tickets']}")


if __name__ == "__main__":
    main()
