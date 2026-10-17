# 资源放这里

## audio/ —— 音频

放到网页上的曲子：

- 格式导出为 **MP3**（128~192kbps）
- 命名：`track-01.mp3`、`track-02.mp3`（小写英文 + 连字符 + 序号）
- 禁止：空格、中文、括号、大写混用

FLAC 母带自己留着单独归档，不要放这里（Safari 播不了）。

## img/ —— 图片

- 命名：`avatar.jpg`、`project-01.png`
- 网页用图建议宽度 ≤ 1600px，体积 ≤ 500KB
- 手机拍的原图（5MB 一张）直接放上去，页面会卡

## 引用方式

从 `learning/site/music.html` 引用：

```html
<audio controls src="../../assets/audio/track-01.mp3"></audio>
<img src="../../assets/img/avatar.jpg" alt="幽林的头像" />
```

**两个 `..`**：site/ → learning/ → my-site/ → assets/
