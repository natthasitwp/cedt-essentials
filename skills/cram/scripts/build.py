"""Build the cram study site from Markdown lessons. Standard library only (Python 3.9+).

    python3 <skill>/scripts/build.py            run from the workspace root

Reads
    lessons/index.md        course front matter (title, code, site, purpose) + optional intro
    lessons/NN-slug.md      one lesson each: front matter + Markdown with ::: blocks
    widgets/*.js            the user's own widgets (optional; override the skill's by name)
Writes
    site/index.html, site/lessons/NN-slug.html, site/reference/cheatsheet.html,
    site/widgets.html (every widget on one page), and refreshes site/assets + site/widgets
    from the skill. site/slides/ is left alone (scripts/slides.py writes it).

Lesson syntax is in LESSON-FORMAT.md, widgets in WIDGETS.md. Every problem found is printed
as  file:line: message  and the build exits 1, so fix and run again.
"""
from __future__ import annotations

import html
import json
import re
import shutil
import sys
from pathlib import Path
from string import Template

SKILL = Path(__file__).resolve().parents[1]
ROOT = Path.cwd()
SRC, SITE = ROOT / "lessons", ROOT / "site"
ERRORS: list[str] = []


def err(where: str, msg: str) -> None:
    ERRORS.append(f"{where}: {msg}")


# ---------------------------------------------------------------- front matter

def front_matter(text: str, where: str) -> tuple[dict, str, int]:
    """Tiny YAML subset: `key: value`, quoted or not, and `key:` followed by `- item` lines."""
    if not text.startswith("---\n"):
        return {}, text, 0
    end = text.find("\n---", 4)
    if end < 0:
        err(where, "front matter has no closing ---")
        return {}, text, 0
    head, body = text[4:end], text[end + 4:].lstrip("\n")
    meta: dict = {}
    key = None
    for i, line in enumerate(head.splitlines(), 2):
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^\s+-\s+(.*)$", line) or re.match(r"^-\s+(.*)$", line)
        if m and key:
            if not isinstance(meta[key], list):
                meta[key] = []
            meta[key].append(unquote(m.group(1)))
            continue
        m = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if not m:
            err(f"{where}:{i}", f"cannot read front matter line: {line!r}")
            continue
        key, val = m.group(1), m.group(2).strip()
        meta[key] = unquote(val) if val else []
    lines_before = text[: end + 4].count("\n") + 1
    return meta, body, lines_before


def unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        return v[1:-1]
    return v


# ---------------------------------------------------------------- inline Markdown

MATH = re.compile(r"\\\((.+?)\\\)|\\\[(.+?)\\\]|\$\$(.+?)\$\$", re.S)


class Inline:
    """Markdown inline -> HTML. Code spans and math are cut out first so * and _ inside them
    are left alone, then put back unchanged."""

    def __init__(self) -> None:
        self.has_math = False

    def __call__(self, s: str, where: str = "") -> str:
        keep: list[str] = []

        def stash(x: str) -> str:
            keep.append(x)
            return f"\x00{len(keep) - 1}\x00"

        s = re.sub(r"`([^`]+)`", lambda m: stash(f"<code>{html.escape(m.group(1))}</code>"), s)

        def math(m: re.Match) -> str:
            self.has_math = True
            # escape < > & so "\\( \\tau<t \\)" is not read as a <t> tag; KaTeX sees the plain text
            return stash(html.escape(m.group(0), quote=False))

        s = MATH.sub(math, s)
        for opener, closer in (("\\(", "\\)"), ("\\[", "\\]")):
            if s.count(opener) != s.count(closer):
                err(where, f"math {opener} … {closer} is not closed")
        if s.count("$$") % 2:
            err(where, "math $$ … $$ is not closed")
        s = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img src="\2" alt="\1" loading="lazy">', s)
        s = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", lambda m: link(m.group(1), m.group(2)), s)
        s = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", s)
        s = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", s)
        s = re.sub(r"~~(.+?)~~", r"<s>\1</s>", s)
        return re.sub(r"\x00(\d+)\x00", lambda m: keep[int(m.group(1))], s)


def link(text: str, url: str) -> str:
    ext = url.startswith(("http://", "https://"))
    return f'<a href="{url}"' + (' target="_blank" rel="noopener"' if ext else "") + f">{text}</a>"


# ---------------------------------------------------------------- block Markdown

class Page:
    """State for one lesson while its body is rendered."""

    def __init__(self, nn: str, meta: dict, where: str, offset: int) -> None:
        self.nn, self.meta, self.where, self.offset = nn, meta, where, offset
        self.inline = Inline()
        self.h2 = 0
        self.problems: list[dict] = []
        self.widgets: set[str] = set()
        self.clips: list[tuple[str, str]] = []

    def at(self, i: int) -> str:
        return f"{self.where}:{i + self.offset}"


CONTAINERS = {"def", "warn", "note", "link", "goal", "predict", "lecture", "quiz", "html", "widget", "sources", "example"}
LEAVES = {"slide", "clip", "widget"}


def render_blocks(lines: list[str], page: Page, start: int = 0) -> str:
    out: list[str] = []
    i = 0
    para: list[str] = []

    def flush() -> None:
        if para:
            out.append(f"<p>{page.inline(' '.join(para), page.at(start + i))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i]
        s = line.strip()
        ln = start + i + 1
        if not s:
            flush(); i += 1; continue

        m = re.match(r"^:::\s*([\w-]+)\s*(.*)$", s)
        if m:
            flush()
            name, arg = m.group(1), m.group(2).strip()
            depth, j = 1, i + 1
            while j < len(lines):
                t = lines[j].strip()
                if re.match(r"^:::\s*[\w-]+", t):
                    depth += 1
                elif t == ":::":
                    depth -= 1
                    if depth == 0:
                        break
                j += 1
            if j >= len(lines):
                err(page.at(ln), f":::{name} is never closed with :::")
            out.append(container(name, arg, lines[i + 1:j], page, start + i + 1))
            i = j + 1
            continue

        m = re.match(r"^::\s*([\w-]+)\s+(.*)$", s)
        if m:
            flush()
            out.append(leaf(m.group(1), m.group(2), page, ln))
            i += 1
            continue

        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            flush()
            level, text = len(m.group(1)), page.inline(m.group(2), page.at(ln))
            if level == 2:
                page.h2 += 1
                out.append(f'<h2><span class="num">{page.h2}</span>{text}</h2>')
            else:
                out.append(f"<h{level}>{text}</h{level}>")
            i += 1
            continue

        if s.startswith("```"):
            flush()
            lang = s[3:].strip()
            j = i + 1
            while j < len(lines) and not lines[j].strip().startswith("```"):
                j += 1
            code = html.escape("\n".join(lines[i + 1:j]))
            attr = f' data-lang="{lang}"' if lang else ""
            out.append(f"<pre><code{attr}>{code}</code></pre>")
            i = j + 1
            continue

        if s.startswith("|"):
            flush()
            j = i
            while j < len(lines) and lines[j].strip().startswith("|"):
                j += 1
            out.append(table(lines[i:j], page, ln))
            i = j
            continue

        if re.match(r"^([-*]|\d+\.)\s+", s):
            flush()
            ordered = bool(re.match(r"^\d+\.", s))
            items: list[str] = []
            j = i
            while j < len(lines):
                t = lines[j].strip()
                mm = re.match(r"^([-*]|\d+\.)\s+(.*)$", t)
                if mm:
                    items.append(mm.group(2))
                elif t and lines[j].startswith((" ", "\t")) and items:
                    items[-1] += " " + t
                else:
                    break
                j += 1
            tag = "ol" if ordered else "ul"
            body = "".join(f"<li>{page.inline(x, page.at(ln))}</li>" for x in items)
            out.append(f"<{tag}>{body}</{tag}>")
            i = j
            continue

        if s.startswith(">"):
            flush()
            j = i
            quote = []
            while j < len(lines) and lines[j].strip().startswith(">"):
                quote.append(lines[j].strip()[1:].strip())
                j += 1
            out.append(f"<blockquote>{render_blocks(quote, page, start + i)}</blockquote>")
            i = j
            continue

        if s.startswith("<") and not s.startswith(("<b", "<i", "<a ", "<u", "<s", "<code", "<span", "<br")):
            flush()
            j = i
            while j < len(lines) and lines[j].strip():
                j += 1
            out.append("\n".join(lines[i:j]))
            i = j
            continue

        if s == "---":
            flush(); out.append("<hr>"); i += 1; continue

        para.append(s)
        i += 1
    flush()
    return "\n".join(out)


def table(rows: list[str], page: Page, ln: int) -> str:
    cells = [[c.strip() for c in r.strip().strip("|").split("|")] for r in rows]
    if len(cells) > 1 and all(re.match(r"^:?-{2,}:?$", c) for c in cells[1]):
        head, body = cells[0], cells[2:]
    else:
        head, body = None, cells
    out = ['<div class="tbl"><table>']
    if head:
        out.append("<tr>" + "".join(f"<th>{page.inline(c, page.at(ln))}</th>" for c in head) + "</tr>")
    for r in body:
        out.append("<tr>" + "".join(f"<td>{page.inline(c, page.at(ln))}</td>" for c in r) + "</tr>")
    return "".join(out) + "</table></div>"


def container(name: str, arg: str, body: list[str], page: Page, ln: int) -> str:
    if name not in CONTAINERS:
        err(page.at(ln), f"unknown block :::{name} (known: {', '.join(sorted(CONTAINERS))})")
        return ""
    if name == "html":
        return "\n".join(body)
    if name == "quiz":
        return quiz(body, page, ln)
    if name == "widget":
        return widget(arg, "\n".join(body), page, ln)
    inner = render_blocks(body, page, ln)
    label = html.escape(arg, quote=True)
    if name == "def":
        return f'<div class="def" data-label="{label or "นิยาม"}">{inner}</div>'
    if name == "predict":
        if not arg:
            err(page.at(ln), ":::predict needs the question on the same line")
        return f'<details class="predict"><summary>{page.inline(arg, page.at(ln))}</summary>{inner}</details>'
    if name == "lecture":
        if arg and not TIME.match(arg):
            err(page.at(ln), f"timestamp {arg!r} is not h:mm:ss or m:ss")
        if arg:
            page.clips.append((arg, ""))
        return f'<div class="lecture"{f" data-t={chr(34)}{arg}{chr(34)}" if arg else ""}>{inner}</div>'
    if name == "sources":
        return f'<div class="sources"><span class="lbl">อ่านเพิ่ม / ที่มา</span>{inner}</div>'
    if name == "example":
        return f'<div class="exercise"><span class="tag">ตัวอย่าง</span>{f"<h4>{page.inline(arg)}</h4>" if arg else ""}{inner}</div>'
    cls = {"link": "link-infer"}.get(name, name)
    return f'<div class="{cls}">{inner}</div>'


TIME = re.compile(r"^\d{1,2}(:\d{2}){1,2}$")


def leaf(name: str, arg: str, page: Page, ln: int) -> str:
    if name not in LEAVES:
        err(page.at(ln), f"unknown line ::{name} (known: {', '.join(sorted(LEAVES))})")
        return ""
    if name == "widget":
        wname, _, cfg = arg.partition(" ")
        return widget(wname + " " + cfg if cfg else wname, "", page, ln)
    parts = [p.strip() for p in arg.split("|")]
    if name == "clip":
        t = parts[0]
        if not TIME.match(t):
            err(page.at(ln), f"timestamp {t!r} is not h:mm:ss or m:ss")
        page.clips.append((t, page.inline(parts[1] if len(parts) > 1 else "", page.at(ln))))
        return ""
    # slide: ::slide 12 | alt text | caption     or  ::slide L02-p012.png | alt | caption
    ref = parts[0]
    alt = parts[1] if len(parts) > 1 else ""
    cap = parts[2] if len(parts) > 2 else ""
    if not alt:
        err(page.at(ln), "::slide needs alt text: ::slide 12 | what the slide shows | caption")
    if re.fullmatch(r"\d+", ref):
        deck = page.meta.get("deck")
        if not deck:
            err(page.at(ln), "::slide with a page number needs `deck:` in the front matter")
            deck = "?"
        img, label = f"{deck}-p{int(ref):03d}.png", f"สไลด์ {int(ref)}"
    else:
        img = ref
        label = page.meta.get("slide_label", "รูป")
        mm = re.search(r"-p(\d+)", ref)
        if mm:
            label = f"สไลด์ {int(mm.group(1))}"
    if not (SITE / "slides" / img).exists():
        err(page.at(ln), f"slide image site/slides/{img} does not exist (run scripts/slides.py first)")
    return (f'<figure class="slide"><img src="../slides/{img}" alt="{html.escape(alt, quote=True)}" loading="lazy">'
            f"<figcaption><b>{label}</b>{page.inline(cap, page.at(ln))}</figcaption></figure>")


# ---------------------------------------------------------------- quiz

def quiz(body: list[str], page: Page, ln: int) -> str:
    """? type | [slide N |] question
       answer: …  (num)        - choice / - [x] right choice  (mc)
       tol: …  hint: …  sol: …   (continuation lines join the field above)"""
    items: list[dict] = []
    field = None
    for k, raw in enumerate(body):
        line, at = raw.strip(), page.at(ln + k + 1)
        if not line:
            if field and items and field in items[-1]:
                items[-1][field] += "<br>"
            continue
        m = re.match(r"^\?\s*(num|mc|think)\s*\|\s*(.*)$", line)
        if m:
            parts = [p.strip() for p in m.group(2).split("|")]
            q = {"type": m.group(1), "_at": at, "choices": [], "_right": []}
            if len(parts) > 1 and re.fullmatch(r"slide\s+\d+", parts[0]):
                q["slide"] = int(parts[0].split()[1])
                parts = parts[1:]
            q["q"] = "|".join(parts)
            items.append(q)
            field = "q"
            continue
        if line.startswith("?"):
            err(at, "question line must look like: ? num | text   (types: num, mc, think)")
            continue
        if not items:
            err(at, "text before the first ? question line")
            continue
        q = items[-1]
        m = re.match(r"^-\s+(\[[xX ]\]\s*)?(.*)$", line)
        if m:
            if m.group(1) and m.group(1).strip()[1] in "xX":
                q["_right"].append(len(q["choices"]))
            q["choices"].append(m.group(2))
            field = None
            continue
        m = re.match(r"^(answer|tol|hint|sol):\s*(.*)$", line)
        if m:
            field = m.group(1)
            q[field] = m.group(2)
            continue
        if field:
            q[field] = (q[field] + " " + line).replace("<br> ", "<br>")
        else:
            err(at, f"cannot tell what this line belongs to: {line!r}")

    out = []
    for n, q in enumerate(items, 1):
        at = q.pop("_at")
        right = q.pop("_right")
        choices = q.pop("choices")
        item: dict = {"id": f"{page.nn}-{n}", "type": q["type"]}
        if "slide" in q:
            item["slide"] = q["slide"]
        item["q"] = page.inline(q["q"].strip(), at)
        if q["type"] == "mc":
            if len(choices) < 2:
                err(at, "mc question needs at least two `- choice` lines")
            if len(right) != 1:
                err(at, "mc question needs exactly one `- [x] right choice`")
            item["choices"] = [page.inline(c, at) for c in choices]
            item["answer"] = right[0] if right else 0
        elif q["type"] == "num":
            a = str(q.get("answer", "")).strip()
            if not re.fullmatch(r"-?\d+(\.\d+)?(\s*/\s*-?\d+(\.\d+)?)?", a):
                err(at, f"num answer must be a number or fraction like 0.5 or 1/3, got {a!r}")
            item["answer"] = a
            if "tol" in q:
                try:
                    item["tol"] = float(q["tol"])
                except ValueError:
                    err(at, f"tol must be a number, got {q['tol']!r}")
        if q.get("hint"):
            item["hint"] = page.inline(q["hint"].strip(), at)
        if not q.get("sol", "").strip():
            err(at, "every question needs sol: (a worked solution)")
        item["sol"] = page.inline(q.get("sol", "").strip(), at)
        out.append(item)
    page.problems.extend(out)
    data = json.dumps(out, ensure_ascii=False, indent=1).replace("</", "<\\/")
    return (f'<div class="quiz" data-quiz="{page.nn}"></div>\n'
            f'<script type="application/json" id="problems-{page.nn}">\n{data}\n</script>')


# ---------------------------------------------------------------- widgets

def available_widgets() -> dict[str, Path]:
    found = {p.stem: p for p in sorted((SKILL / "assets" / "site" / "widgets").glob("*.js"))}
    found.update({p.stem: p for p in sorted((ROOT / "widgets").glob("*.js"))})
    return found


def widget(arg: str, body: str, page: Page, ln: int) -> str:
    name, _, cfg = arg.strip().partition(" ")
    cfg = (cfg + "\n" + body).strip() or "{}"
    if name not in available_widgets():
        err(page.at(ln), f"widget {name!r} not found in widgets/ or the skill (have: {', '.join(available_widgets()) or 'none'})")
    try:
        conf = json.loads(cfg)
    except json.JSONDecodeError as e:
        err(page.at(ln), f"widget {name} config is not valid JSON: {e.msg}")
        conf = {}
    page.widgets.add(name)
    if re.search(r"\\\(|\\\[|\$\$", cfg):
        page.inline.has_math = True
    data = html.escape(json.dumps(conf, ensure_ascii=False), quote=True)
    return f'<div class="widget" data-widget="{name}" data-config="{data}"><noscript>เปิด JavaScript เพื่อใช้ภาพโต้ตอบนี้</noscript></div>'


# ---------------------------------------------------------------- pages

KATEX = """<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.css">
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/katex.min.js"></script>
<script defer src="https://cdn.jsdelivr.net/npm/katex@0.16.11/dist/contrib/auto-render.min.js"></script>"""


def layout() -> Template:
    return Template((SKILL / "assets" / "templates" / "page.html").read_text())


def page_html(*, title: str, course: dict, root: str, body: str, nav: str, math: bool = False,
              scripts: tuple[str, ...] = (), body_attrs: str = "") -> str:
    head = [KATEX] if math else []
    head += [f'<script defer src="{root}{s}"></script>' for s in ("assets/site.js",) + scripts]
    if (ROOT / "theme.css").exists():
        head.append(f'<link rel="stylesheet" href="{root}assets/theme.css">')
    return layout().substitute(
        title=html.escape(title), root=root, head="\n".join(head),
        html_attrs=' data-theme="dark"' if course.get("theme") == "dark" else "",
        site=html.escape(course["site"], quote=True), body_attrs=body_attrs,
        course=html.escape(course["title"]), nav=nav, body=body)


def lesson_html(lesson: dict, course: dict, prev: dict | None, nxt: dict | None) -> str:
    m, page = lesson["meta"], lesson["page"]
    head = [f'<p class="kicker">Lesson {lesson["nn"]}{" · " + html.escape(m["src"]) if m.get("src") else ""}'
            f'{" · ~" + str(m["minutes"]) + " นาที" if m.get("minutes") else ""}</p>',
            f'<h1>{page.inline(m["title"])}</h1>']
    if m.get("slides") or m.get("meta"):
        meta = m.get("meta") or f'โยงกับสไลด์ {m["slides"]}'
        head.append(f'<p class="meta">{page.inline(meta)}</p>')
    if m.get("goal"):
        head.append(f'<div class="goal"><b>เป้าหมายบทนี้:</b> {page.inline(m["goal"])}</div>')
    if page.clips:
        lis = "".join(f'<li><button class="jump" data-t="{t}">{t}</button><span>{d}</span></li>'
                      for t, d in page.clips if d)
        if lis:
            head.append(f'<div class="clips"><b>คลิปบรรยายที่ตรงกับบทนี้</b><ul>{lis}</ul></div>')
    tail = []
    if m.get("sources"):
        items = "".join(f"<li>{page.inline(s)}</li>" for s in m["sources"])
        tail.append(f'<div class="sources"><span class="lbl">อ่านเพิ่ม / ที่มา</span><ul>{items}</ul></div>')
    tail.append('<p class="note">ติดตรงไหน ถาม Claude ได้เลย บอกเลขบทกับเลขข้อมาด้วย</p>')
    pl = f'<a href="{prev["file"]}">← {html.escape(prev["meta"]["title"])}</a>' if prev else '<a href="../index.html">← บทเรียนทั้งหมด</a>'
    nl = f'<a href="{nxt["file"]}">{html.escape(nxt["meta"]["title"])} →</a>' if nxt else '<a href="../reference/cheatsheet.html">Cheat sheet →</a>'
    tail.append(f'<nav class="pager">{pl}{nl}</nav>')
    scripts = ("assets/quiz.js",) if page.problems else ()
    attrs = ""
    if m.get("video"):
        attrs = f' data-video="{html.escape(m["video"], quote=True)}"'
        if m.get("captions"):
            attrs += f' data-captions="{html.escape(m["captions"], quote=True)}"'
    if m.get("video") or page.clips or "class=\"lecture\"" in lesson["body"]:
        scripts += ("assets/video.js",)
    if page.widgets:
        scripts += ("assets/widgets.js",) + tuple(f"widgets/{w}.js" for w in sorted(page.widgets))
    nav = '<a href="../index.html">บทเรียน</a><a href="../reference/cheatsheet.html">Cheat sheet</a>'
    body = "\n".join(head) + "\n" + lesson["body"] + "\n" + "\n".join(tail)
    return page_html(title=f'{lesson["nn"]} · {m["title"]}', course=course, root="../", body=body, nav=nav,
                     math=page.inline.has_math, scripts=scripts, body_attrs=attrs)


def index_html(lessons: list[dict], course: dict, intro: str) -> str:
    inline = Inline()
    rows = []
    for L in lessons:
        m = L["meta"]
        d = " · ".join(x for x in (inline(m.get("oneline", "")), f'สไลด์ {m["slides"]}' if m.get("slides") else "",
                                   f'~{m["minutes"]} นาที' if m.get("minutes") else "") if x)
        rows.append(f'<li><span class="n">{L["nn"]}</span><span class="t"><a href="lessons/{L["file"]}">'
                    f'{inline(m["title"])}</a><span class="d">{d}</span></span>'
                    f'<span class="s" data-lesson-status="{L["nn"]}" data-total="{len(L["page"].problems)}">ยังไม่เริ่ม</span></li>')
    body = (f'<p class="kicker">{html.escape(course.get("code", ""))}</p><h1>{inline(course["title"])}</h1>'
            + (f'<p class="meta">{inline(course["purpose"])}</p>' if course.get("purpose") else "")
            + '<div class="goal"><b>อ่านแบบเร็ว:</b> แต่ละบทใช้ 15–30 นาที มีรูปจากสไลด์ ช่วงคลิปที่อาจารย์สอนเรื่องนั้น และโจทย์ที่ตรวจคำตอบได้ทันที เรียงตามลำดับที่ต้องรู้ก่อนหลัง</div>'
            + intro + f'<ol class="lesson-list">{"".join(rows)}</ol>')
    return page_html(title=course["title"], course=course, root="", body=body, math=inline.has_math,
                     nav='<a href="reference/cheatsheet.html">Cheat sheet</a>')


def cheatsheet_html(lessons: list[dict], course: dict) -> str:
    inline = Inline()
    out = ['<p class="kicker">Cheat sheet · ทุกบทในหน้าเดียว</p>', f'<h1>{inline(course["title"])} Cheat sheet</h1>']
    for L in lessons:
        m = L["meta"]
        items = m.get("cheat") or []
        if isinstance(items, str):
            items = [items]
        out.append(f'<h2><span class="num">{L["nn"]}</span>{inline(m["title"])}</h2>')
        label = f'สรุป · สไลด์ {m["slides"]}' if m.get("slides") else "สรุป"
        out += [f'<div class="def" data-label="{label}">{inline(x)}</div>' for x in items]
        if not items:
            err(L["where"], "front matter has no `cheat:` items for the cheat sheet")
        out.append(f'<p class="meta"><a href="../lessons/{L["file"]}">อ่านบทเต็ม →</a></p>')
    return page_html(title=f'Cheat sheet · {course["title"]}', course=course, root="../", body="\n".join(out),
                     math=inline.has_math, nav='<a href="../index.html">บทเรียน</a>')


def gallery_html(course: dict) -> str:
    ws = available_widgets()
    out = ['<p class="kicker">Widgets</p><h1>ภาพโต้ตอบทั้งหมด</h1>',
           '<p class="meta">ทุก widget ที่ใช้ได้ พร้อมค่าตัวอย่างของมัน ใช้ตรวจว่าทำงานก่อนใส่ในบทเรียน</p>']
    for name, path in ws.items():
        m = re.search(r"@example\s+(\{.*\})", path.read_text())
        cfg = m.group(1) if m else "{}"
        out.append(f'<h2>{name}</h2><div class="widget" data-widget="{name}" data-config="{html.escape(cfg, quote=True)}"></div>')
    scripts = ("assets/widgets.js",) + tuple(f"widgets/{n}.js" for n in ws)
    return page_html(title="Widgets", course=course, root="", body="\n".join(out), math=True, scripts=scripts,
                     nav='<a href="index.html">บทเรียน</a>')


# ---------------------------------------------------------------- main

def main() -> int:
    if not SRC.is_dir():
        print("no lessons/ folder here: run from the workspace root (the folder that has lessons/)")
        return 1
    ix = SRC / "index.md"
    course, intro_md, _ = front_matter(ix.read_text(), "lessons/index.md") if ix.exists() else ({}, "", 0)
    if not course.get("title"):
        err("lessons/index.md", "needs front matter with at least `title:` (and `site:`, `code:`, `purpose:`)")
        course["title"] = "Cram"
    course.setdefault("site", re.sub(r"\W+", "-", course["title"].lower()).strip("-") or "cram")

    # refresh shared assets and widgets from the skill (user widgets/ win on name clashes)
    shutil.copytree(SKILL / "assets" / "site" / "assets", SITE / "assets", dirs_exist_ok=True)
    (SITE / "widgets").mkdir(parents=True, exist_ok=True)
    for name, path in available_widgets().items():
        shutil.copy(path, SITE / "widgets" / f"{name}.js")
    if (ROOT / "theme.css").exists():
        shutil.copy(ROOT / "theme.css", SITE / "assets" / "theme.css")
    (SITE / "lessons").mkdir(exist_ok=True)
    (SITE / "reference").mkdir(exist_ok=True)

    lessons = []
    for path in sorted(SRC.glob("[0-9][0-9]-*.md")):
        where = f"lessons/{path.name}"
        meta, body, offset = front_matter(path.read_text(), where)
        if not meta.get("title"):
            err(where, "front matter needs `title:`")
            meta["title"] = path.stem
        nn = path.name[:2]
        page = Page(nn, meta, where, offset)
        lessons.append({"nn": nn, "file": path.stem + ".html", "meta": meta, "page": page, "where": where,
                        "body": render_blocks(body.splitlines(), page)})
    if not lessons:
        err("lessons/", "no lesson files named like 01-topic.md")

    intro_page = Page("00", course, "lessons/index.md", 0)
    intro = render_blocks(intro_md.splitlines(), intro_page) if intro_md.strip() else ""

    if ERRORS:
        print("\n".join(ERRORS))
        print(f"\n{len(ERRORS)} problem(s); nothing written. Fix them and run again.")
        return 1

    for k, L in enumerate(lessons):
        prev = lessons[k - 1] if k else None
        nxt = lessons[k + 1] if k + 1 < len(lessons) else None
        (SITE / "lessons" / L["file"]).write_text(lesson_html(L, course, prev, nxt))
    keep = {L["file"] for L in lessons}
    for old in (SITE / "lessons").glob("*.html"):
        if old.name not in keep:
            old.unlink()
    (SITE / "index.html").write_text(index_html(lessons, course, intro))
    (SITE / "reference" / "cheatsheet.html").write_text(cheatsheet_html(lessons, course))
    (SITE / "widgets.html").write_text(gallery_html(course))
    if ERRORS:
        print("\n".join(ERRORS))
        return 1
    nq = sum(len(L["page"].problems) for L in lessons)
    ws = sorted(set().union(*(L["page"].widgets for L in lessons)))
    print(f"built {len(lessons)} lessons, {nq} questions" + (f", widgets: {', '.join(ws)}" if ws else "")
          + " → site/index.html")
    return 0


if __name__ == "__main__":
    sys.exit(main())
