# 第 3 课 · CSS：把样式抽出来

## 一、CSS 是什么

```css
h1 {
  color: #1a1a1a;
  font-size: 40px;
}
```

人话：**页面上所有 `h1`，颜色 `#1a1a1a`，字号 40 像素。**

不写 CSS 时 `<h1>` 也是大标题——那是浏览器的**默认样式**。CSS 就是覆盖默认值。

## 二、三种写法，只用外部文件

```html
<link rel="stylesheet" href="03-my-style.css" />
```

必须放 `<head>` 里。`rel="stylesheet"` 固定、`href` 是路径、自闭合无结束标签。

行内 `style="..."` 和内部 `<style>` 都不该用：**样式和内容混在一起，改一处要改几十处。**

## 三、选择器

```css
h1 { }        /* 标签：所有 h1 */
.intro { }    /* class：class="intro" 的元素 */
#main { }     /* id：id="main" 的元素 */
```

| | `class` | `id` |
|---|---|---|
| 写法 | `.名字` | `#名字` |
| 能重复 | ✅ 能 | ❌ 全页唯一 |
| 用途 | **批量套样式（99% 用这个）** | 锚点跳转、单独特例 |

**优先级：标签 < class < id。** 样式一律用 `class`——`id` 太强，覆盖它只能上 `!important`，最后会失控。

## 四、常用属性

```css
color: #333;              background-color: #f5f5f5;
font-size: 18px;          font-weight: 700;
font-family: sans-serif;  line-height: 1.6;
text-align: center;       text-decoration: none;
margin: 20px;   /* 外边距：和外面其他元素的距离 */
padding: 16px;  /* 内边距：自己内部内容到边界的距离 */
```

颜色：`#333`（缩写）等于 `#333333`。记住 `#333` 深灰 / `#fff` 白 / `#000` 黑 / `#f5f5f5` 浅灰。

## 五、特别注意

**CSS 写错浏览器不报错，直接静默忽略。** 写 `backgroud-color` 少个 n，页面不变，控制台一片安静。

排查靠：**F12 → Elements → 选中元素 → Styles**，那是"最终生效的样式表"，被划掉的属性就是写错的。

| 坑 | 原因 |
|---|---|
| 完全没生效 | `<link>` 的 href 路径错了，看 Network 是不是 404 |
| 部分没生效 | 选择器拼错，`class="intro"` 对应 `.intro` |
| 忘了分号 | 漏 `;` 后面整块可能失效 |
| 中文冒号 | `color：red` 不认，必须英文 `:` |

## 六、实验

把 HTML 上的 `class="card"` 临时删掉 → 卡片样式消失 → 加回来又出现。

**结论：CSS 不修改 HTML，它只是拿选择器找目标，找到就套样式。**
