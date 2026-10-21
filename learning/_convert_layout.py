import re
import pathlib

root = pathlib.Path(r"D:\my-site")
targets = [root / f for f in ["index.html", "projects.html", "music.html", "notes.html"]]
targets += sorted((root / "notes").glob("*.html"))

header_pat = re.compile(r'<header class="site-header">.*?</header>', re.S)
footer_pat = re.compile(r'<footer class="site-footer">.*?</footer>', re.S)

for f in targets:
    text = f.read_text(encoding="utf-8")
    prefix = "../" if f.parent.name == "notes" else ""

    has_header = header_pat.search(text)
    has_footer = footer_pat.search(text)
    if not has_header or not has_footer:
        print(f"跳过 {f.name}（缺 header 或 footer）")
        continue

    text = header_pat.sub('  <div id="site-header"></div>', text, count=1)
    text = footer_pat.sub('  <div id="site-footer"></div>', text, count=1)

    script_tag = f'<script src="{prefix}layout.js"></script>'
    if "layout.js" not in text:
        text = text.replace("</body>", f"{script_tag}\n</body>", 1)

    f.write_text(text, encoding="utf-8", newline="\n")
    print(f"已处理 {f.relative_to(root)}   prefix='{prefix}'")
