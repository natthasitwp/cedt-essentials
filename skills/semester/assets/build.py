"""Build the course page and the handbook from the teaching workspace.

    course/course.json + course/template.html      -> dist/course.html
    handbook/shell.html + handbook/lessons/w*.html  -> dist/handbook.html

Run from the workspace root:  python tools/build.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ["code", "title", "heading", "subject", "start", "stages", "steps"]


def load_course() -> dict:
    c = json.loads((ROOT / "course" / "course.json").read_text())
    missing = [k for k in REQUIRED if not c.get(k)]
    if missing:
        sys.exit(f"course.json is missing: {', '.join(missing)}")
    stage_ids = {g["id"] for g in c["stages"]}
    for s in c["steps"]:
        for k in ("id", "stage", "title", "weeks"):
            if k not in s:
                sys.exit(f"step {s.get('id', '?')} is missing '{k}'")
        if s["stage"] not in stage_ids:
            sys.exit(f"step {s['id']} has unknown stage '{s['stage']}'")
    return c


def build_course(c: dict) -> Path:
    tpl = (ROOT / "course" / "template.html").read_text()
    data = json.dumps(c, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    out = (tpl.replace("__COURSE__", data)
              .replace("__TITLE__", c["title"])
              .replace("__TOPBAR__", c.get("topbar", c["title"]))
              .replace("__HEADING__", c["heading"])
              .replace("__CREDITS__", c.get("credits", "3(2-2-5)"))
              .replace("__GOAL__", c.get("goal", ""))
              .replace("__CREDIT__", c.get("credit", ""))
              .replace("__START__", c["start"]))
    path = ROOT / "dist" / "course.html"
    path.write_text(out)
    return path


def build_handbook(c: dict) -> Path:
    shell = (ROOT / "handbook" / "shell.html").read_text()
    lessons = sorted((ROOT / "handbook" / "lessons").glob("w*.html"))
    out = (shell.replace("__LESSONS__", "\n".join(p.read_text() for p in lessons))
                .replace("__CODE__", c["code"])
                .replace("__MISSION_LABEL__", c.get("missionLabel", c["subject"]))
                .replace("__COURSE_URL__", c.get("courseUrl") or "#"))
    path = ROOT / "dist" / "handbook.html"
    path.write_text(out)
    print(f"handbook lessons: {', '.join(p.stem for p in lessons) or 'none'}")
    return path


def main() -> None:
    c = load_course()
    (ROOT / "dist").mkdir(exist_ok=True)
    print("built", build_course(c).relative_to(ROOT))
    if (ROOT / "handbook" / "shell.html").exists():
        print("built", build_handbook(c).relative_to(ROOT))


if __name__ == "__main__":
    main()
