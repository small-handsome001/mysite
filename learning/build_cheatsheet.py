"""生成《网页开发速查卡》PDF 的 DOCX 源文件（水课用，手机可看）。

风格复用 build_handbook.py 里的排版函数。
"""

import sys

sys.path.insert(0, r"D:\my-site\learning")

from docx import Document  # noqa: E402

from build_handbook import (  # noqa: E402
    ACCENT, DARK, GREY, RED,
    add_rich, bullet, code_block, h, hrule, make_table, para, style_base,
)
from docx.shared import Cm  # noqa: E402


def build(path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(1.9)
    sec.right_margin = Cm(1.9)
    sec.top_margin = Cm(1.5)
    sec.bottom_margin = Cm(1.5)
    style_base(doc)

    # ================= 封面 =================
    para(doc, "网页开发速查卡", size=21, bold=True, color=ACCENT, space_after=2)
    para(doc, "第 1—12 课 · 一张纸看完", size=12, bold=True, color=DARK, space_after=3)
    para(doc, "幽林 · 2026-10-22 · 手机可读，不用联网", size=9, color=GREY, space_after=2)
    hrule(doc)

    para(doc, "用法：**别通读**。卡壳的时候翻到对应那一节，看完合上，回来接着写。", size=10, color=DARK)

    # ================= 一、网页怎么工作 =================
    h(doc, "一、网页是怎么工作的（一张图）", 1)

    code_block(doc, r"""浏览器 --请求--> 服务器(D:\my-site) --响应--> 浏览器渲染
         ↑                                    ↓
    地址栏 http://127.0.0.1:8123/xxx.html    画到屏幕上""", size=9)

    bullet(doc, "双击 HTML 是 `file://`，浏览器直接读硬盘；起服务器是 `http://`，浏览器发请求。**上线后只有 http 这一种**。", "记住：")
    bullet(doc, "`python -m http.server 8123` 或双击 `启动服务器.bat`，然后开 `http://127.0.0.1:8123/`。", "本地预览：")

    make_table(
        doc,
        ["F12 面板", "它回答什么问题", "什么时候看"],
        [
            ["Elements", "页面结构长什么样、哪条 CSS 生效（划线=输掉）", "样式不生效、结构乱了"],
            ["Network", "每个文件是不是 200（404=路径错）", "图片不显示、音频 0:00/0:00"],
            ["Console", "JS 报错（红字）和 console.log", "页面空白、点了没反应"],
        ],
        [2.6, 9.0, 5.6],
        font_size=9,
    )

    # ================= 二、三个模板 =================
    h(doc, "二、网页只需要背三个模板", 1)
    para(doc, "背的是**步骤**，不是整段代码。忘了细节就按步骤倒推。", size=9.5)

    para(doc, "**模板 1：一个页面**（head 里就 4 样东西）", size=10, space_after=2)
    code_block(doc, """<head>
  <meta charset="UTF-8" />                              <!-- 中文不乱码 -->
  <meta name="viewport" content="width=device-width" />  <!-- 手机上不缩成豆腐块 -->
  <title>幽林 | 主页</title>                             <!-- 标签页标题 -->
  <link rel="stylesheet" href="site.css" />              <!-- 唯一一份样式 -->
</head>""", size=8.5)

    para(doc, "**模板 2：把数据变成页面**（第 11 课，最常用）", size=10, space_after=2)
    code_block(doc, """① 数据在哪        const tracks = [...]  或 fetch("xx.json")
② 找盒子          const box = document.querySelector("#list")
③ 变字符串        const parts = tracks.map(t => `<h3>${t.title}</h3>`)
④ 粘起来          parts.join("")
⑤ 塞进页面        box.innerHTML = parts.join("")""", size=8.5)
    para(doc, "**少第 ⑤ 步 = 白屏。** 这是最常见的一种「代码没错但不显示」。", size=9, color=RED)

    para(doc, "**模板 3：点击做一件事**", size=10, space_after=2)
    code_block(doc, """const btn = document.querySelector("#btn");   // 1 拿到元素
btn.addEventListener("click", function () {   // 2 挂上监听
  document.body.classList.toggle("dark");     // 3 做点事
});""", size=8.5)
    para(doc, "`querySelector` **只接受一个**选择器参数；要多个用 `querySelectorAll`。", size=9, color=GREY)

    # ================= 三、JS 七个零件 =================
    h(doc, "三、JS 的七个零件（只记「干什么用」）", 1)

    make_table(
        doc,
        ["零件", "干什么用", "例子 / 记忆点"],
        [
            ["const / let", "给东西起名字", "不再变的用 const，会变的（计数器）用 let"],
            ["数组 + 对象", "描述「一堆东西」", "`[ ]` 装很多个，`{ }` 装一个的各个属性"],
            ["function", "把一串动作打包", "入口（参数）→ 干活 → 出口（return）"],
            ["map", "每一项都变一次", "进去是数组，出来还是数组（数量不变）"],
            ["join", "把数组粘成一个字符串", "`parts.join(\"\")`，括号里是连接符"],
            ["模板字符串", "在字符串里插变量", "反引号 ` 包住，里面写 `${变量}`"],
            ["innerHTML", "把字符串塞进页面", "盒子变内容；塞错误东西会有 XSS 风险"],
        ],
        [3.0, 5.6, 8.6],
        font_size=9,
    )

    para(doc, "**名字要能看出是什么**：`tracks`（数组，复数）、`track`（单个）、`listEl`（元素，El 结尾）。", size=9.5)

    # ================= 四、错误长相表 =================
    h(doc, "四、错误长相表（网页世界的「报错信息」）", 1)
    para(doc, "网页**不会主动报错**，你要靠现象反推。这张表就是替代品。", size=9.5)

    make_table(
        doc,
        ["你看到的", "真正的原因", "怎么查"],
        [
            ["改完没变化", "忘了 Ctrl+S 保存", "先看标题栏有没有圆点"],
            ["页面空白 + 没红字", "请求成功了但没画（缺第 ⑤ 步）", "Network 看 200，再查 innerHTML"],
            ["页面空白 + 有红字", "语法错 / 变量名错 / 函数不存在", "从第一条红字往下读"],
            ["顶部多一个字符", "head 里混进了普通文字（如多余 `\\`）", "Elements 看 head 在哪结束"],
            ["导航或页头不显示", "script 放在盒子前面，拿到 null", "script 挪到 </body> 前"],
            ["图片撑爆页面", "没有 `max-width: 100%`", "全局 `img { max-width:100%; height:auto }`"],
            ["样式写了对不上", "别的选择器权重更高", "F12 Styles 里被划掉的那条就是输的"],
            ["音频 0:00 / 0:00", "文件路径错或文件不存在", "Network 看 404"],
            ["加了内容没出现", "JSON 少逗号 / 多了逗号", "Console 会报 JSON 解析错"],
            ["「加载失败」", "fetch 路径错 / 404", "catch 里已经把 err 打出来了"],
        ],
        [4.4, 7.2, 5.6],
        font_size=9,
    )

    # ================= 五、CSS 五条 =================
    h(doc, "五、CSS 只要记住这五条", 1)

    bullet(doc, "宽 = content + padding + border；`background` 只铺到 border 为止。**margin 在框外，不占宽。**", "① 盒子模型：")
    bullet(doc, "加 `* { box-sizing: border-box }` 后，写 300px 就是 300px。", "② 保命一条：")
    bullet(doc, "`display: flex` 写在**父元素**上；`justify-content` 管横、`align-items` 管纵、`gap` 管间距。", "③ 布局：")
    bullet(doc, "`img.avatar`(1-1-0) 打得过 `.avatar`(0-1-0)。**只用 class 选，别靠 id 和 !important 打架。**", "④ 权重：")
    bullet(doc, "`@media (max-width: 600px) { ... }` 写在文件末尾；手机端窄了就折行、竖排。", "⑤ 手机：")

    # ================= 六、工作流 =================
    h(doc, "六、改完一次，固定跑这四步", 1)
    code_block(doc, """1. Ctrl+S 保存
2. 浏览器 F5
3. F12 → Network：关键文件是不是 200
4. F12 → Console：有没有红字""", size=9)

    para(doc, "**上线（三条命令）：**", size=10, space_after=2)
    code_block(doc, """cd D:\\my-site
git add .
git commit -m "改了什么"
git push          # 约 5 秒，不输密码（SSH 已配好）""", size=8.5)

    bullet(doc, "推完打开 `https://small-handsome001.github.io/mysite/` 看，**Actions 页面 Queued 就等，别连推三次**。", "验证：")

    # ================= 七、Python ↔ JS =================
    h(doc, "七、你会的 Python 换到 JS 长什么样", 1)

    make_table(
        doc,
        ["想做", "Python", "JavaScript"],
        [
            ["列表 / 字典", "`lst = [1,2]`", "`const lst = [1,2]`"],
            ["循环处理每个", "`[f(x) for x in lst]`", "`lst.map(x => f(x))`"],
            ["拼成一个字符串", "`\"\".join(parts)`", "`parts.join(\"\")`"],
            ["定义函数", "`def f(a): return a`", "`function f(a) { return a; }`"],
            ["打印 / 调试", "`print(x)`", "`console.log(x)`"],
            ["出错停止", "`raise` / 报错行号", "红字 + 文件名:行号（Console）"],
        ],
        [3.2, 6.6, 7.4],
        font_size=9,
    )

    hrule(doc)
    para(doc, "卡住的时候只问一句：", size=9, color=GREY, space_after=2)
    para(doc, "「现在走到第几步了？」—— 而不是「那行代码长什么样」。", size=11, bold=True, color=ACCENT)
    para(doc, "网页不会报错，所以你要自己知道「正常长什么样」。这就是这张卡的全部作用。", size=9, color=GREY)

    doc.save(path)
    print("saved", path)


if __name__ == "__main__":
    build(r"D:\my-site\网页开发速查卡.docx")

