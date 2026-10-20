"""生成《JS 学习手册：看懂 ≠ 会写》PDF 的 DOCX 源文件。

内容来源：D:\\my-site 第 1-11 课的真实学习记录与踩坑。
"""

import re

from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

FONT_CN = "微软雅黑"
FONT_MONO = "Consolas"
ACCENT = RGBColor(0x2F, 0x6B, 0xFF)
GREY = RGBColor(0x66, 0x66, 0x66)
DARK = RGBColor(0x22, 0x22, 0x22)
RED = RGBColor(0xC0, 0x39, 0x2B)


def set_run_font(run, size=None, bold=None, color=None, mono=False):
    name = FONT_MONO if mono else "Segoe UI"
    run.font.name = name
    run._element.rPr.rFonts.set(qn("w:eastAsia"), FONT_MONO if mono else FONT_CN)
    if size is not None:
        run.font.size = Pt(size)
    if bold is not None:
        run.font.bold = bold
    if color is not None:
        run.font.color.rgb = color


def style_base(document):
    normal = document.styles["Normal"]
    normal.font.name = "Segoe UI"
    normal.font.size = Pt(10)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
    normal.paragraph_format.line_spacing = 1.4
    normal.paragraph_format.space_after = Pt(5)

    for lvl, size in ((1, 15), (2, 12), (3, 10.5)):
        st = document.styles[f"Heading {lvl}"]
        st.font.name = "Segoe UI"
        st.font.size = Pt(size)
        st.font.bold = True
        st.font.color.rgb = DARK
        st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT_CN)
        st.paragraph_format.space_before = Pt(14 if lvl == 1 else 10)
        st.paragraph_format.space_after = Pt(6)
        st.font.underline = False


def add_rich(p, text, size=10, bold=False, color=None):
    """支持 `代码` 和 **加粗** 两种行内标记。"""
    pos = 0
    pattern = re.compile(r"`([^`]+)`|\*\*([^*]+)\*\*")
    for m in pattern.finditer(text):
        if m.start() > pos:
            r = p.add_run(text[pos:m.start()])
            set_run_font(r, size=size, bold=bold, color=color)
        if m.group(1) is not None:
            r = p.add_run(m.group(1))
            set_run_font(r, size=size - 0.5, bold=bold, color=color, mono=True)
        else:
            r = p.add_run(m.group(2))
            set_run_font(r, size=size, bold=True, color=color)
        pos = m.end()
    if pos < len(text):
        r = p.add_run(text[pos:])
        set_run_font(r, size=size, bold=bold, color=color)


def para(document, text="", size=10, bold=False, color=None, space_after=None,
         indent=None, mono=False):
    p = document.add_paragraph()
    if space_after is not None:
        p.paragraph_format.space_after = Pt(space_after)
    if indent is not None:
        p.paragraph_format.left_indent = Cm(indent)
    if mono:
        r = p.add_run(text)
        set_run_font(r, size=size, bold=bold, color=color, mono=True)
    else:
        add_rich(p, text, size=size, bold=bold, color=color)
    return p


def h(doc, text, level=1):
    """不用 Word 的 Heading 样式（会和模板里的下划线打架），自己造。"""
    para_ = doc.add_paragraph()
    pf = para_.paragraph_format
    pf.space_before = Pt(16 if level == 1 else 11)
    pf.space_after = Pt(6 if level == 1 else 4)
    pf.keep_with_next = True
    r = para_.add_run(text)
    set_run_font(r, size=15 if level == 1 else 11.5, bold=True, color=DARK)
    return para_


def bullet(document, text, bold_prefix="", size=10):
    p = document.add_paragraph(style="List Bullet")
    p.paragraph_format.space_after = Pt(3)
    if bold_prefix:
        r0 = p.add_run(bold_prefix)
        set_run_font(r0, size=size, bold=True)
    add_rich(p, text, size=size)
    return p


def num_item(document, num, text, size=10):
    p = document.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.85)
    p.paragraph_format.first_line_indent = Cm(-0.5)
    p.paragraph_format.space_after = Pt(3)
    r0 = p.add_run(f"{num}. ")
    set_run_font(r0, size=size, bold=True)
    add_rich(p, text, size=size)
    return p


def shade_paragraph(p, hex_color="F4F6F9"):
    pPr = p._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    pPr.append(shd)


def code_block(document, code, size=8.5):
    p = document.add_paragraph()
    p.paragraph_format.left_indent = Cm(0.3)
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_together = True
    shade_paragraph(p)
    lines = code.strip("\n").split("\n")
    for i, line in enumerate(lines):
        r = p.add_run(line)
        set_run_font(r, size=size, mono=True, color=DARK)
        if i < len(lines) - 1:
            r.add_break()
    return p


def hrule(document):
    p = document.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)
    pPr = p._p.get_or_add_pPr()
    borders = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), "6")
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), "D8DCE3")
    borders.append(bottom)
    pPr.append(borders)
    return p


def shade_cell(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def make_table(document, headers, rows, widths, font_size=8.8, header_fill="EAEFF7",
               mono_cols=()):
    table = document.add_table(rows=1, cols=len(headers))
    table.style = "Table Grid"
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    for i, w in enumerate(widths):
        table.columns[i].width = Cm(w)

    hdr = table.rows[0].cells
    for i, h in enumerate(headers):
        shade_cell(hdr[i], header_fill)
        p = hdr[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(2)
        r = p.add_run(h)
        set_run_font(r, size=font_size, bold=True, color=DARK)

    for row in rows:
        cells = table.add_row().cells
        for i, val in enumerate(row):
            p = cells[i].paragraphs[0]
            p.paragraph_format.space_before = Pt(2)
            p.paragraph_format.space_after = Pt(2)
            if i in mono_cols:
                r = p.add_run(str(val))
                set_run_font(r, size=font_size, mono=True)
            else:
                add_rich(p, str(val), size=font_size)

    for row in table.rows:
        row._tr.get_or_add_trPr().append(OxmlElement("w:cantSplit"))
        for i, w in enumerate(widths):
            row.cells[i].width = Cm(w)
    table.rows[0]._tr.get_or_add_trPr().append(OxmlElement("w:tblHeader"))
    return table


def build(path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.left_margin = Cm(2.0)
    sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(1.8)
    sec.bottom_margin = Cm(1.8)
    style_base(doc)

    # ================= 封面 =================
    para(doc, "看懂 ≠ 会写", size=22, bold=True, color=ACCENT, space_after=2)
    para(doc, "JS 学习手册：零件、骨架、错题", size=13, bold=True, color=DARK, space_after=4)
    para(doc, "幽林 · 2026-10-21 · 整理自第 1—11 课的真实记录", size=9, color=GREY, space_after=2)
    hrule(doc)

    para(doc, "这份手册不按课程顺序写，按「你卡在哪」写。", size=10, color=DARK)
    para(doc, "三部分：① 为什么看懂却写不出；② 七个零件 + 三个骨架；③ 错题本与自测。", size=9, color=GREY)

    # ================= 一、看懂与写出 =================
    h(doc, "一、看懂和写出，是两种不同的能力", 1)
    para(doc, "这不是智力问题，是训练类型不同。", color=GREY)

    make_table(
        doc,
        ["能力", "你做的时候在干什么", "有没有练过"],
        [
            ("看懂（识别）", "别人写好的代码，你逐行读，能说出它大概在干嘛", "练了很多，因为每天都在读"),
            ("写出（生成）", "从空白开始，自己决定先写哪行、变量叫什么", "几乎没练，因为一直在读"),
            ("改（修改）", "在已有代码上动一两个地方", "练过一点（改 CSS、改 JSON）"),
        ],
        widths=[2.9, 9.3, 4.4],
    )

    para(doc, "读代码是「认出熟悉的东西」，写代码是「从记忆里取出并组装」。", size=10, space_after=2)
    para(doc, "前者靠见过就行，后者必须动手输出过一次。你没输出过，写不出是必然结果，不是笨。", size=10, bold=True)

    h(doc, "破法：四步输出训练（每个骨架都这么做）", 2)
    num_item(doc, 1, "照着抄一遍（不许改任何字符）—— 让手指熟悉形状。")
    num_item(doc, 2, "关掉原文，默写一遍 —— 写不出来就回去看，最多重复 3 次。")
    num_item(doc, 3, "改一个参数（把 3 首改成 2 首、把 title 改成 name）—— 确认你懂每个零件的作用。")
    num_item(doc, 4, "换一个场景（曲子列表 → 笔记列表）—— 这一步过了，才算真的会。")

    para(doc, "目标不是「能背出整段代码」，是「记得有哪几个零件、顺序大概怎样、每步在干嘛」。", size=9.5, color=GREY)

    # ================= 二、你现在会什么 =================
    h(doc, "二、你现在真正拥有的能力（不是学过的课，是能做的事）", 1)
    num_item(doc, 1, "打开 `assets/music.json`，加一首曲子，刷新页面就多一张卡片 —— 不碰 HTML、不碰 JS。")
    num_item(doc, 2, "看一眼网页，能用 F12 的 Elements / Network / Console 找到「哪里不对」。")
    num_item(doc, 3, "用 CSS 改字号、间距、颜色、圆角、布局（flex），并知道改完先按 Ctrl+S 再 F5。")
    num_item(doc, 4, "写标签结构，知道 head 和 body 各放什么，知道多用了一个括号会整页崩。")
    num_item(doc, 5, "用 git 保存版本，用 SSH 把代码推到 GitHub，用 Pages 发布成公网网址。")
    num_item(doc, 6, "在手机上检查自己的页面有没有溢出、字号是否过大。")
    num_item(doc, 7, "把「加载失败」做成用户看得懂的提示，而不是一片空白。")

    para(doc, "上面每一条，都是能在 10 分钟内演示出来的。这就是你一个月前的空白和别人现在看到的差别。",
         size=9.5, color=GREY)

    # ================= 三、七个零件 =================
    h(doc, "三、JS 的七个零件（每个都只要记住「干什么用」）", 1)
    para(doc, "不要背语法细节，先记住每个零件解决什么问题。写的时候忘了细节，按用途就能想起来。", color=GREY)

    h(doc, "零件 1：const —— 给一个东西起名字", 2)
    code_block(doc, 'const tracks = [...];      // 「tracks」这个名字，指向右边那堆数据')
    bullet(doc, "把数据存起来，后面反复用。", "干什么：")
    bullet(doc, "`let` 用于后面要改的值（比如计数器 count），`const` 用于不再整体替换的值。")
    bullet(doc, "起名要能看出是什么：`tracks`（数组，复数）、`track`（单个）、`listEl`（元素，El 结尾）。")

    h(doc, "零件 2：数组 + 对象 —— 描述「一堆东西」", 2)
    code_block(doc,
               'const tracks = [\n'
               '  { title: "断らなかった", meta: "原创 · 2026", file: "assets/audio/track-01.mp3" },\n'
               '  { title: "人声小样", meta: "术曲 · 0:28", file: "assets/audio/track-02.mp3" }\n'
               '];')
    bullet(doc, "`[ ]` 里装很多个，`{ }` 里装一个东西的各个属性。", "干什么：")
    bullet(doc, "`tracks` = 整个数组；`tracks[0]` = 第一首；`tracks[0].title` = 第一首的标题。")
    bullet(doc, "你 C++ 学过结构体数组、Python 学过 list[dict]，这是同一个东西换了写法。", "对照：")

    h(doc, "零件 3：function —— 把一串动作打包，起个名字", 2)
    code_block(doc,
               'function renderTracks(list) {\n'
               '  // 括号里是「入口」，外面的东西从这里进来\n'
               '  return "结果";   // return 是「出口」\n'
               '}')
    bullet(doc, "入口（参数）→ 干活 → 出口（return）。三段缺一段，函数就没用。", "干什么：")
    bullet(doc, "`renderTracks(tracks)`。**写了函数不会自动执行，必须调用。**", "调用：")
    bullet(doc, "函数写了没调用（或者调用没接住 return），页面就什么都不变。", "最常见错：")

    h(doc, "零件 4：map —— 让每一项都变一次", 2)
    code_block(doc,
               'tracks.map(function (track) {\n'
               '  return `<div>${track.title}</div>`.trim();\n'
               '});\n'
               '// 结果：["<div>断らなかった</div>", "<div>人声小样</div>"]  ← 还是数组')
    bullet(doc, "把数组里的每一项，都送进函数处理一次，收集返回值组成新数组。", "干什么：")
    bullet(doc, "**进出都是数组**。进去 3 项，出来 3 项（每项可能变长变短，但个数不变）。", "关键：")
    bullet(doc, "结果必须接住：`const parts = tracks.map(...)`。不接就等于扔了。", "必错点：")

    h(doc, "零件 5：join —— 把数组粘成一个字符串", 2)
    code_block(doc,
               'parts.join("");     // 括号里是「用什么粘」，空字符串 = 什么都不要')
    bullet(doc, "map 出来的是数组，`innerHTML` 要的是字符串，中间必须用 join 转一次。", "干什么：")
    bullet(doc, "`parts.join(\"\")` 把数组拼成一整段 HTML。", "写法：")
    bullet(doc, "`map` 是数组的方法，`join` 也是。**函数（方法）上没有 join** —— 所以 `tracks.map.join(\"\")` 必错。", "必错点：")

    h(doc, "零件 6：模板字符串 —— 在字符串里插变量", 2)
    code_block(doc,
               'const name = "断らなかった";\n'
               '\n'
               '`<h3>${name}</h3>`        // ✅ 反引号 + ${}，能换行\n'
               '"<h3>" + name + "</h3>"   // 老写法，用 + 拼接，不能换行')
    bullet(doc, "反引号 `` ` ``（键盘左上角，英文输入法），不是单引号，也不是中文引号。", "怎么打：")
    bullet(doc, "反引号里可以换行、可以写 `${变量}`，普通引号不行。", "要点：")

    h(doc, "零件 7：innerHTML —— 把内容塞进页面", 2)
    code_block(doc,
               'const listEl = document.querySelector("#track-list");   // 先找到盒子\n'
               'listEl.innerHTML = parts.join("");                      // 再用 HTML 填满它')
    bullet(doc, "把某个元素「里面」的内容整个换掉。", "干什么：")
    bullet(doc, "**是替换不是追加**。第二次执行会清掉上一次的内容，这正是想要的行为。", "关键：")
    bullet(doc, "数据是你自己写的，可以放心用；**哪天要显示别人输入的内容，必须换成 `textContent`**（防 XSS）。", "安全：")

    # ================= 四、三个骨架 =================
    h(doc, "四、三个骨架：背会这三个，就能从零写出来", 1)
    para(doc, "写不出来的时候，不要想「代码长什么样」，想「有几步」。下面每个骨架都是固定顺序，把空填上就是程序。",
         color=GREY)

    h(doc, "骨架 A：一堆数据 → 页面上一堆卡片（最常用）", 2)
    code_block(doc,
               '// 第 1 步：数据在哪\n'
               'const tracks = [ { title: "A", meta: "m", file: "f.mp3" } ];\n'
               '\n'
               '// 第 2 步：先找到要放内容的盒子\n'
               'const listEl = document.querySelector("#track-list");\n'
               '\n'
               '// 第 3 步：写一个函数，把数据变成字符串\n'
               'function renderTracks(list) {\n'
               '  const parts = list.map(function (item) {        // 每个都变一次\n'
               '    return `\n'
               '      <div class="track">\n'
               '        <h3>${item.title}</h3>\n'
               '        <p class="meta">${item.meta}</p>\n'
               '        <audio controls src="${item.file}"></audio>\n'
               '      </div>\n'
               '    `;\n'
               '  });\n'
               '  return parts.join("");                          // 粘成一个字符串\n'
               '}\n'
               '\n'
               '// 第 4 步：塞进页面\n'
               'listEl.innerHTML = renderTracks(tracks);')
    para(doc, "四步：数据 → 找盒子 → map 变字符串并 join → innerHTML。少了第 4 步就是白屏。", size=9.5, bold=True)

    h(doc, "骨架 B：从文件读数据（fetch）", 2)
    code_block(doc,
               'const listEl = document.querySelector("#track-list");\n'
               '\n'
               'fetch("assets/music.json")            // 第 1 步：发出请求（不等结果）\n'
               '  .then(function (res) {               // 第 2 步：拿到响应\n'
               '    if (!res.ok) throw new Error("HTTP " + res.status);\n'
               '    return res.json();                 // 解析成数据（也是异步）\n'
               '  })\n'
               '  .then(function (tracks) {            // 第 3 步：这里才是数据\n'
               '    listEl.innerHTML = tracks.map(function (t) {\n'
               '      return `<div class="track"><h3>${t.title}</h3></div>`;\n'
               '    }).join("");\n'
               '  })\n'
               '  .catch(function (err) {              // 第 4 步：出错也要有界面\n'
               '    listEl.innerHTML = `<p class="meta">加载失败：${err.message}</p>`;\n'
               '  });')
    bullet(doc, "数据在第二个 `then` 里，**不在 fetch 下一行**。", "记住：")
    bullet(doc, "两层 then：第一个处理「响应」，第二个处理「数据」。", "为什么两层：")
    bullet(doc, "`.catch` 的括号里那个 `err`，只在这个函数内部存在。抄代码不能只抄里面。", "作用域：")

    h(doc, "骨架 C：点击做一件事", 2)
    code_block(doc,
               'const btn = document.querySelector("#toggle");\n'
               '\n'
               'btn.addEventListener("click", function () {\n'
               '  document.body.classList.toggle("dark");\n'
               '});')
    bullet(doc, "拿到元素 → `addEventListener(\"click\", 函数)`。函数在**被点击时**才执行。", "结构：")
    bullet(doc, "`querySelector` 只接受**一个**选择器参数；要选多个用 `querySelectorAll`。", "易错：")

    # ================= 五、错题本 =================
    h(doc, "五、错题本：现象 → 原因 → 怎么查", 1)
    para(doc, "按「你看到什么」查，不要按「我学了什么」查。这是这套表唯一的用法。", color=GREY)

    h(doc, "JS 与数据", 2)
    make_table(
        doc,
        ["你看到的", "真正的原因", "怎么查 / 怎么修"],
        [
            ("页面空白，Console 没红字", "then 里没写渲染代码，或函数调用了但没用返回值", "Network 看 JSON 是否 200；确认 innerHTML 那行执行了"),
            ("页面空白，Console 有红字", "语法错 / 变量未定义 / 函数不存在", "点红字看行号，从最上面第一条错误读起"),
            ("`map.join is not a function`", "map 是方法，不是数组", "先把 map 结果存变量：const parts = ..."),
            ("`err is not defined`", "把 .catch(function(err){}) 的壳删了，只留内容", "把语句放回 catch 的括号里"),
            ("`null` 的 innerHTML 报错", "querySelector 没找到元素（id 拼错 / script 在元素前面）", "确认 id 一致；script 放 body 末尾"),
            ("播放器显示 0:00 / 0:00", "音频文件路径错，浏览器读不到", "看 Network 是否有 404；路径前面该不该带 ../"),
            ("加了内容没出现", "JSON 少逗号 / 多项之间没逗号 / 最后一项多了逗号", "保守写法：每项后面都写逗号会报错，只有最后一项不写"),
            ("改了 JSON 页面没变", "没保存，或浏览器缓存", "看 VSCode 标签页圆点；Ctrl+F5 强刷"),
        ],
        widths=[4.6, 6.4, 5.6],
    )

    h(doc, "HTML / CSS", 2)
    make_table(
        doc,
        ["你看到的", "真正的原因", "怎么查 / 怎么修"],
        [
            ("页面顶部多一个字符", "head 里出现普通文字（如多余的 \\ 或 >）", "多余字符会让 head 提前结束，F12 Elements 看 head/body 分界"),
            ("图片跑到最上面、页面乱", "<img> 写进了 <head>", "head 只放 charset / viewport / title / meta / link"),
            ("整段样式失效", "注释少了闭合 */", "数一数 /* 和 */ 是否一样多"),
            ("写了 width 不生效", "另一条选择器权重更高（img.avatar 打赢 .avatar）", "F12 Styles 里被划掉的那条就是输掉的"),
            ("卡片被图撑爆", "图片没限制宽度", "全局 img { max-width: 100%; height: auto }"),
            ("手机上有横向滚动", "某个元素比屏幕宽", "用 iframe 摆 320/390/768 三档，或 F12 切设备模式"),
            ("字号在手机上太大", "固定 px", "用 clamp(24px, 6vw, 36px)"),
        ],
        widths=[4.4, 6.6, 5.6],
    )

    h(doc, "Git 与部署", 2)
    make_table(
        doc,
        ["你看到的", "真正的原因", "怎么查 / 怎么修"],
        [
            ("push 报 upstream 错误", "本地分支没记住远程", "git push -u origin main（只需一次）"),
            ("推送成功但线上没变", "Pages 构建在排队（Queued）", "看 Actions 页面状态：Queued 就等，红叉才修"),
            ("以为没部署成功", "curl 读到 CDN 缓存", "看 Last-Modified，或加 -H \"Cache-Control: no-cache\""),
            ("SSH: accepts key 又 denied", "私钥打不开（有密码但没提供）", "ssh-keygen -y -f 私钥：卡住=有密码，直接打印=正常"),
            ("双击 bat 窗口一闪就没", ".bat 是 LF 换行，cmd 只认 CRLF", "换行符必须 CRLF；HTTP 服务只需要开一个"),
        ],
        widths=[4.6, 6.4, 5.6],
    )

    # ================= 六、自测 =================
    h(doc, "六、自测：能答对 7 题，就算真的会了", 1)
    para(doc, "先自己写答案，再看下一页。写不出来就回去看零件那一节。", color=GREY)

    quiz = [
        "有一个数组 `tracks`，怎么取第一首的标题？",
        "`tracks.map(...)` 和 `tracks.join(\"\")` 各自返回什么类型？",
        "为什么 `map` 之后必须 `join` 才能塞进 `innerHTML`？",
        "模板字符串用哪种引号？里面的变量怎么写？",
        "`fetch` 之后的数据在 `.then` 的第几个回调里？为什么不在下一行？",
        "「白屏 + Console 没红字」优先查什么？",
        "「白屏 + Console 有红字」优先查什么？",
        "`querySelector` 写错了 id 会怎样？会在哪一步报错？",
        "把 `.catch(function (err) {...})` 里的语句搬到函数外面，会发生什么？",
        "要让页面上的卡片出现，最少需要哪四步？",
    ]
    for i, q in enumerate(quiz, 1):
        num_item(doc, i, q, size=9.5)

    doc.add_page_break()
    h(doc, "答案（先自己写）", 2)
    answers = [
        "`tracks[0].title`。方括号取第几个（从 0 开始），点取哪个字段。",
        "都是数组：`map` 返回「每项变成的结果」组成的新数组；`join` 返回**字符串**。",
        "因为 `innerHTML` 要的是一段 HTML 字符串，而 map 给的是字符串数组，join 负责把它们粘成一个。",
        "反引号 `` ` ``，变量写成 `${变量名}`。中文引号、单引号都不行。",
        "第二个 `.then`（第一个处理响应 res，要 `res.json()` 才得到数据）。因为 `fetch` 是异步的，结果只能通过回调拿到。",
        "先看 Network：请求是否 200、数据是否拿到。200 就说明「数据到了但没画」——查渲染函数有没有被调用、innerHTML 有没有执行。",
        "从**第一条**红字开始读，通常是拼写、变量未定义、函数没定义。别从中间读。",
        "`querySelector` 返回 `null`，之后对 `null` 取 `.innerHTML` 会抛 TypeError：Cannot set properties of null。",
        "`err` 是那个函数的参数，出了函数就不存在，会报 ReferenceError: err is not defined。（我犯过）",
        "①数据在哪 ②找到要放内容的元素 ③map 变字符串 + join 粘起来 ④赋给 innerHTML。",
    ]
    for i, a in enumerate(answers, 1):
        num_item(doc, i, a, size=9.5)

    # ================= 七、怎么练 =================
    h(doc, "七、接下来怎么练（三个任务，从易到难）", 1)

    h(doc, "练习 1：改动（5 分钟）", 2)
    para(doc, "打开 `assets/music.json`，给每首曲子加一个字段 `\"year\": \"2026\"`，"
              "然后把 `music.js` 里的模板改成多显示一行年份。"
              "目的：确认你知道「字段」和「模板里的位置」是一一对应的。")

    h(doc, "练习 2：默写（20 分钟）", 2)
    para(doc, "关掉所有文件，新建一个空 HTML，自己从零写出「三张卡片」，数据用最朴素的数组。"
              "卡住就回去看骨架 A，看完再关掉重写。写出来为止。")

    h(doc, "练习 3：换场景（30 分钟）", 2)
    para(doc, "把 `notes.html` 里手写的三条笔记，改成从 `assets/notes.json` 生成。"
              "这次没有现成代码可抄，只有骨架。**这一步过了，你就真的会了。**")

    hrule(doc)
    para(doc, "写不出来的时候回来看这一句：", size=9, color=GREY, space_after=2)
    para(doc, "「不是我要背下整段代码，是我要知道有几步、每步在干嘛。」", size=10.5, bold=True, color=ACCENT)
    # 末页署名省略（封面已有）

    doc.save(path)
    print("saved", path)


if __name__ == "__main__":
    build(r"D:\my-site\JS学习手册-看懂与会写.docx")

