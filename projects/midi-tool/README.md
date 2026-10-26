# midi-tool

批量处理 MIDI 文件的命令行小工具。写它的原因：手改太蠢。

## 能做什么

```bash
# 1. 统计：目录里每首曲子的时长、轨道数、音符数、音域、BPM
python midi_tool.py scan "D:\音乐创作"

# 2. 存成 JSON（方便接到了网站或脚本里）
python midi_tool.py scan "D:\音乐创作" --json result.json

# 3. 批量移调：全部升 2 个半音，结果写到 out/
python midi_tool.py transpose "D:\音乐创作" -s 2

# 4. 降 3 个半音，自定义输出目录
python midi_tool.py transpose "D:\音乐创作" -s -3 -o 降调版
```

`scan` 输出示例：

```
文件                            时长  轨  音符  音域
--------------------------------------------------------------
demo_drums.mid                  3:05   7  5264  C1–G#5
demo_final.mid                  3:05   6  4886  C1–G5
seg_final.mid                   0:10   7   301  A1–B5
```

## 安装

```bash
pip install mido
```

只需要 `mido` 一个依赖（纯 Python，不需要编译器）。

## 两个它已经处理掉的坑

**① 鼓轨不能移调。**
MIDI 第 10 通道（`channel == 9`）是打击乐，音符编号表示「哪个鼓」——
把 42（闭合踩镲）升 2 个半音变成 44，出来的是完全不同的乐器。工具里整轨跳过。

**② 移调不能越界。**
音符编号是 0–127，超出范围的音符写进去就是非法文件。
遇到越界的单个音符直接跳过，不中断整批处理。

## 已知限制

- `scan` 的 BPM 取第一处 `set_tempo`，走速度变化的曲子（渐变、变速）显示的不准
- 移调是「全曲统一移半音数」，不识别调号、不做智能转调
- 只处理 `.mid` / `.midi`，不读 MusicXML（`.mscx` 得先导出）

## 结构

```
midi_tool.py    全部逻辑，约 200 行
```

用到的都是标准库 + mido 的基础 API：`MidiFile` / `track` / `msg.type` / `msg.note`。
没有框架，没有抽象层——这个规模不需要。
