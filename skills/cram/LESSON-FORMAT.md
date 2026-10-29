# Lesson format

Write lessons as Markdown in `lessons/NN-slug.md` (two-digit number, short English slug).
Never write HTML pages by hand: `python3 <skill>/scripts/build.py` turns the Markdown into
the site, adds the page shell, navigation, index and cheat sheet, and checks everything.
[assets/lessons/01-example.md](assets/lessons/01-example.md) is a complete example.

## Course file: `lessons/index.md`

```markdown
---
title: Signals & Systems
code: 2102xxx · L05–L06
site: ss-2026          # short id; progress is stored under it
purpose: one line under the title on the index
theme: light           # or dark, only when the user asks for it
---
Optional Markdown shown above the lesson list.
```

## Lesson front matter

```markdown
---
title: Convolution integral และวิธี flip-and-shift
src: L05                     # lecture id shown in the kicker
minutes: 25
slides: 2–4                  # shown as "โยงกับสไลด์ 2–4" (or write meta: for your own line)
deck: L05                    # ::slide 3 then means site/slides/L05-p003.png
goal: one thing the learner can do after this lesson
oneline: short description for the index
video: ../../materials/L05.mp4      # optional, relative to site/lessons/
captions: ../../materials/L05.vtt   # optional
cheat:
  - "\( y(t)=\int x(\tau)h(t-\tau)\,d\tau \)"
  - "rect * rect = triangle, width = sum of widths"
sources:
  - "[MIT OCW 6.003](https://ocw.mit.edu/…) what it adds beyond the lecture"
---
```

`cheat:` items go to the cheat sheet (required: one or more per lesson). `sources:` become
the "อ่านเพิ่ม / ที่มา" box at the end.

## Body

Plain Markdown: `## heading` (numbered automatically), `### sub-heading`, paragraphs,
`**bold**`, `*italic*`, `` `code` ``, `[link](url)`, `- lists`, `1. lists`, `| tables |`,
`> quotes`, fenced code with a language. A line that starts with an HTML tag passes through.

Math is LaTeX: `\( … \)` inline, `\[ … \]` or `$$ … $$` on its own line. Single `$` is never
math, so prices are safe. Markdown is not applied inside math or code.

### Blocks (`:::name` … `:::`)

| Block | Becomes |
|---|---|
| `:::def label` | definition / formula box with the label on top |
| `:::warn` | common-mistake box |
| `:::predict question` | "ทายก่อน" fold: question on the line, answer and reason inside |
| `:::lecture 1:23:14` | the lecturer's point with a play-from-here button (timestamp optional) |
| `:::note`, `:::link` | side note; "ใช้ตรงไหน" link to later topics |
| `:::example title` | worked-example card |
| `:::quiz` | self-check questions (below) |
| `:::widget name` + JSON lines | interactive figure (see WIDGETS.md) |
| `:::html` | raw HTML/JS kept as is, for a one-off figure |

### Lines (`::name args`)

- `::slide 12 | what the slide shows (alt text) | what to look at` — the slide image from
  `deck`. Use a file name instead of the number for crops: `::slide L05-p004-crop.png | … | …`.
- `::clip 0:42:10 | what is taught there` — listed in the clips box at the top.
- `::widget convolution {"x": "rect(0,1)", "h": "exp(1)"}` — one-line widget.

## Order inside a lesson

1. Front matter (goal, clips) → 2. one `##` per idea with slide, lecture point, plain
explanation, `:::def`, `:::predict`, `:::warn` → 3. a worked example from the slides or
homework → 4. `## ลองทำ` with `:::quiz`. Sources and the pager are added for you.

## Questions

```markdown
:::quiz
? num | slide 4 | หา \( y(1.5) \) ของ rect * rect
answer: 1/2
tol: 0.01
hint: ดูช่วงที่ซ้อนกัน
sol: ซ้อนกันบน \( [0.5, 1] \) จึงได้ 0.5

? mc | ผลของ rect * rect มีรูปร่างแบบใด
- สี่เหลี่ยม
- [x] สามเหลี่ยม
- เอกซ์โพเนนเชียล
sol: ขึ้นแล้วลงเป็นเส้นตรง กว้างรวม 2

? think | อธิบายด้วยคำของตัวเองว่าทำไมต้องพลิก \( h \)
sol: คำตอบตัวอย่าง …
:::
```

- `? type | [slide N |] question` starts a question; types are `num`, `mc`, `think`.
- `num`: `answer:` a number or fraction (`0.5`, `1/3`), optional `tol:`.
- `mc`: `- choice` lines, exactly one `- [x]`. Keep choices about the same length and move
  the right one around.
- Every question needs `sol:`. A line that does not start a new field continues the one
  above; a blank line inside a field becomes a line break.
- No escaping: write `\(` in questions exactly as in the text.
- Mix types: about half `num` in calculation courses. Compute every numeric answer with code
  before writing it down.

## Writing

- Short paragraphs; one idea per paragraph; plain words before notation.
- Explain why a step is done, not only what is done.
- Use the lecture's examples first, then one new example so the learner transfers the idea.
- A lesson longer than about 30 minutes of reading is two lessons.
- To change a lesson later, edit its `.md` and rebuild. Never edit files in `site/`.
