"""midi_tool.py —— 批量处理 MIDI 的命令行小工具

用法：
    python midi_tool.py scan   <目录>                    # 统计每首曲子的信息
    python midi_tool.py scan   <目录> --json out.json    # 存成 JSON
    python midi_tool.py transpose <目录> -s 2            # 全部升 2 个半音，写进 out/
    python midi_tool.py transpose <目录> -s -3 -o 结果/  # 降 3 个半音，自定义输出目录

依赖：mido（pip install mido）
"""

import argparse
import json
import sys
from pathlib import Path

import mido

# 音名，用来把 MIDI 音高（60）翻译成人话（C4）
NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def note_name(number):
    """60 -> 'C4'"""
    return NOTE_NAMES[number % 12] + str(number // 12 - 1)


def find_midis(directory):
    """递归找出目录下所有 .mid / .midi，按路径排序，保证每次输出顺序一致。"""
    directory = Path(directory)
    if not directory.exists():
        sys.exit(f"目录不存在：{directory}")

    files = sorted(
        [p for p in directory.rglob("*") if p.suffix.lower() in (".mid", ".midi")]
    )
    if not files:
        sys.exit(f"{directory} 里没有 .mid 文件")
    return files


def analyse(path):
    """读一个文件，返回它的基本信息。读坏了返回带 error 的字典，不中断整批。"""
    try:
        mid = mido.MidiFile(path)
    except Exception as exc:                      # noqa: BLE001 - 坏文件不该炸掉整批
        return {"file": path.name, "error": str(exc)}

    notes = 0
    pitches = []
    tempos = []
    time_signatures = []

    for track in mid.tracks:
        for msg in track:
            if msg.type == "note_on" and msg.velocity > 0:
                notes += 1
                pitches.append(msg.note)
            elif msg.type == "set_tempo":
                tempos.append(round(mido.tempo2bpm(msg.tempo), 1))
            elif msg.type == "time_signature":
                time_signatures.append(f"{msg.numerator}/{msg.denominator}")

    info = {
        "file": path.name,
        "tracks": len(mid.tracks),
        "length": round(mid.length, 2),           # 秒
    }

    # MIDI 允许把多条轨道合成一个「虚拟轨」，读音符前必须 merge
    if mid.type == 1:
        info["tracks"] = len(mid.tracks)

    if notes:
        info["notes"] = notes
        info["lowest"] = note_name(min(pitches))
        info["highest"] = note_name(max(pitches))

    if tempos:
        info["bpm"] = tempos[0]
    if time_signatures:
        info["time_signature"] = time_signatures[0]

    return info


def format_duration(seconds):
    minutes, secs = divmod(int(seconds), 60)
    return f"{minutes}:{secs:02d}"


def cmd_scan(args):
    files = find_midis(args.directory)
    results = [analyse(p) for p in files]

    if args.json:
        Path(args.json).write_text(
            json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"已写入 {args.json}（{len(results)} 个文件）")
        return

    print(f"{'文件':<28}{'时长':>7}{'轨':>4}{'音符':>6}  音域")
    print("-" * 62)
    for item in results:
        if "error" in item:
            print(f"{item['file']:<28}{'读取失败':>10}  {item['error'][:30]}")
            continue
        print(
            f"{item['file']:<28}"
            f"{format_duration(item['length']):>7}"
            f"{item['tracks']:>4}"
            f"{item.get('notes', 0):>6}"
            f"  {item.get('lowest', '-')}–{item.get('highest', '-')}"
        )


def transpose_file(src, dst, semitones):
    """整体移调。

    只改 note_on / note_off 的音高，节拍、速度、控制器原样保留。
    第 10 通道（channel 9）是打击乐，音符编号代表的是「哪个鼓」，
    移调会变成噪音，所以整轨跳过。
    """
    mid = mido.MidiFile(src)
    shifted = 0

    for track in mid.tracks:
        for msg in track:
            if msg.type in ("note_on", "note_off"):
                if msg.channel == 9:              # 鼓轨，不动
                    continue
                new_note = msg.note + semitones
                if not 0 <= new_note <= 127:
                    # 超出 MIDI 音域，跳过这个音符，避免写出非法文件
                    continue
                msg.note = new_note
                if msg.type == "note_on" and msg.velocity > 0:
                    shifted += 1

    mid.save(dst)
    return shifted


def cmd_transpose(args):
    files = find_midis(args.directory)
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)

    done = 0
    for src in files:
        # 文件名加后缀，能一眼看出动过：demo.mid -> demo_+2.mid
        sign = f"+{args.semitones}" if args.semitones > 0 else str(args.semitones)
        dst = out_dir / f"{src.stem}_{sign}{src.suffix}"
        try:
            moved = transpose_file(src, dst, args.semitones)
        except Exception as exc:                  # noqa: BLE001
            print(f"跳过 {src.name}：{exc}")
            continue
        print(f"{src.name} -> {dst.name}   改了 {moved} 个音符")
        done += 1

    print(f"\n完成 {done}/{len(files)}，输出在 {out_dir}")


def main():
    parser = argparse.ArgumentParser(description="批量处理 MIDI：统计信息 / 整体移调")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="统计目录里所有 MIDI 的信息")
    p_scan.add_argument("directory", help="要扫描的目录")
    p_scan.add_argument("--json", help="把结果存成 JSON 文件")
    p_scan.set_defaults(func=cmd_scan)

    p_tr = sub.add_parser("transpose", help="批量整体移调")
    p_tr.add_argument("directory", help="要处理的目录")
    p_tr.add_argument("-s", "--semitones", type=int, required=True, help="半音数，正数升调")
    p_tr.add_argument("-o", "--output", default="out", help="输出目录，默认 out/")
    p_tr.set_defaults(func=cmd_transpose)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
