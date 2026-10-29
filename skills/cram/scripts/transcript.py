"""Turn a lecture transcript into timed chunks you can read, search and cite.

Accepts WebVTT (.vtt), SubRip (.srt), or plain text with [h:mm:ss] / h:mm:ss at line starts.

    python transcript.py materials/L01.vtt chunks --minutes 3     # condensed text per 3-minute window
    python transcript.py materials/L01.vtt search "energy" "power" # every line that mentions a term
    python transcript.py materials/L01.vtt json > L01-transcript.json

Auto-captions repeat lines and break sentences; chunks merges the repeats so a whole
lecture fits in a few thousand words with its timestamps.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

TIME = r"(?:(\d+):)?(\d{1,2}):(\d{2})(?:[.,](\d{1,3}))?"
CUE = re.compile(rf"^\s*{TIME}\s*-->\s*{TIME}")
PLAIN = re.compile(rf"^\s*\[?{TIME}\]?\s*[-–:]?\s*(.*)$")


def to_sec(h, m, s, ms=None) -> float:
    return int(h or 0) * 3600 + int(m) * 60 + int(s) + (int(ms.ljust(3, "0")) / 1000 if ms else 0)


def fmt(sec: float) -> str:
    sec = int(sec)
    return f"{sec // 3600}:{sec // 60 % 60:02d}:{sec % 60:02d}"


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)          # vtt styling and word timings
    text = re.sub(r"\{[^}]+\}", "", text)
    return " ".join(text.split())


def parse(path: Path) -> list[dict]:
    lines = path.read_text(encoding="utf-8-sig", errors="replace").splitlines()
    cues: list[dict] = []
    if any(CUE.match(l) for l in lines):
        cur = None
        for l in lines:
            m = CUE.match(l)
            if m:
                cur = {"start": to_sec(*m.groups()[:4]), "text": ""}
                cues.append(cur)
            elif cur is not None and l.strip() and not l.strip().isdigit():
                cur["text"] = (cur["text"] + " " + clean(l)).strip()
            elif not l.strip():
                cur = None
    else:
        for l in lines:
            m = PLAIN.match(l)
            if m and m.group(5).strip():
                cues.append({"start": to_sec(*m.groups()[:4]), "text": clean(m.group(5))})
    # drop the rolling duplicates auto-captions produce
    out: list[dict] = []
    for c in cues:
        if not c["text"]:
            continue
        if out and (c["text"] == out[-1]["text"] or c["text"].startswith(out[-1]["text"])):
            out[-1]["text"] = c["text"]
            continue
        if out and out[-1]["text"].endswith(c["text"]):
            continue
        out.append(c)
    return out


def chunks(cues: list[dict], minutes: float) -> list[dict]:
    size = minutes * 60
    groups: list[dict] = []
    for c in cues:
        if not groups or c["start"] - groups[-1]["start"] >= size:
            groups.append({"start": c["start"], "text": []})
        words = groups[-1]["text"]
        if not words or c["text"] != words[-1]:
            words.append(c["text"])
    return [{"t": fmt(g["start"]), "text": " ".join(g["text"])} for g in groups]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file")
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("chunks"); c.add_argument("--minutes", type=float, default=3)
    s = sub.add_parser("search"); s.add_argument("terms", nargs="+")
    sub.add_parser("json")
    args = ap.parse_args()

    cues = parse(Path(args.file))
    if not cues:
        sys.exit("no timed lines found: is this a .vtt, .srt, or text with timestamps?")
    if args.cmd == "chunks":
        for g in chunks(cues, args.minutes):
            print(f"[{g['t']}] {g['text']}\n")
    elif args.cmd == "search":
        terms = [t.lower() for t in args.terms]
        for cue in cues:
            if any(t in cue["text"].lower() for t in terms):
                print(f"{fmt(cue['start'])}  {cue['text']}")
    else:
        json.dump([{"t": fmt(c["start"]), "text": c["text"]} for c in cues], sys.stdout, ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
