"""Fail if a tracked file leaks personal info, or a skill has broken frontmatter.

Usage: python scripts/check_skills.py
"""
import re
import subprocess
import sys
from pathlib import Path

ALLOWED_EMAILS = re.compile(r"noreply@anthropic\.com|@users\.noreply\.github\.com$")

CHECKS = [
    # the domain must end in letters, so package pins like katex@0.16.11 are not emails
    ("email address", re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)*\.[A-Za-z]{2,}\b")),
    ("absolute home path", re.compile(r"(/Users/|/home/)(?!<)[\w.-]+|C:\\Users\\[\w.-]+")),
    ("Thai national ID", re.compile(r"\b\d-?\d{4}-?\d{5}-?\d{2}-?\d\b")),
    ("Thai phone number", re.compile(r"(?<!\d)0[689]\d-?\d{3}-?\d{4}(?!\d)")),
    ("real answer hash", re.compile(r"\"q\d+\":\s*\"[0-9a-f]{16}\"")),
]

SKIP = {"LICENSE", "scripts/check_skills.py"}


def tracked_files():
    out = subprocess.run(["git", "ls-files"], capture_output=True, text=True, check=True).stdout
    return [Path(p) for p in out.splitlines() if p not in SKIP]


def check_leaks(path, text):
    errors = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for label, pattern in CHECKS:
            for m in pattern.finditer(line):
                if label == "email address" and ALLOWED_EMAILS.search(m.group()):
                    continue
                errors.append(f"{path}:{lineno}: {label}: {m.group()}")
    return errors


def check_frontmatter(path, text):
    m = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not m:
        return [f"{path}: missing --- frontmatter --- block"]
    fields = dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M))
    errors = []
    for key in ("name", "description"):
        if not fields.get(key, "").strip():
            errors.append(f"{path}: frontmatter is missing '{key}'")
    if fields.get("name") and fields["name"] != path.parent.name:
        errors.append(f"{path}: name '{fields['name']}' does not match folder '{path.parent.name}'")
    return errors


def main():
    errors = []
    for path in tracked_files():
        try:
            text = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, FileNotFoundError):
            continue
        errors += check_leaks(path, text)
        if path.name == "SKILL.md":
            errors += check_frontmatter(path, text)
    if not list(Path("skills").glob("*/SKILL.md")):
        errors.append("no skills/*/SKILL.md found")
    for e in errors:
        print(e)
    print(f"{len(errors)} problem(s) found" if errors else "✅ no leaks, all skills valid")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
