# Lesson format

Start every lesson from `site/lessons/00-template.html`. File name `NN-slug.html` (two-digit
number, short English slug). Fill every `{{…}}`; delete blocks that do not apply.

## Page header

- `<body data-site="…">`: one short id for the whole site (progress is stored under it).
- `data-video` / `data-captions`: paths to the recording and its captions relative to the
  page. Remove both if the video is not on the user's machine; the jump buttons then hide.
- Keep the KaTeX tags only on pages with math. Write math as `\( … \)` and `\[ … \]`.

## Order inside a lesson

1. Kicker (`Lesson NN · L01 · ~20 นาที`), `h1` title, meta line with the slide range.
2. `goal`: one thing the learner can do after this lesson.
3. `clips`: the 1–5 moments in the recording where this lesson's idea is taught.
4. One `h2` per idea, each with some of:
   - `figure.slide` with the slide image, alt text, and a caption naming what to look at
   - `.lecture[data-t]`: the lecturer's point in one or two sentences, with its timestamp
   - `.def[data-label]`: definition or formula exactly in the slides' notation
   - `details.predict`: a question to answer before reading on, answer with the reason
   - `.warn`: the mistake people make here
   - `.link-infer`: where this is used later in the course or in practice
5. A worked example from the slides or homework, solved step by step.
6. `ลองทำ`: the quiz block (below).
7. `sources`: 1–3 trusted links that add what the lecture skipped (textbook chapter,
   university notes, official docs, a well-known video). Say what each adds.
8. A one-line reminder that the user can ask Claude about anything unclear, then the pager.

## Questions

```html
<div class="quiz" data-quiz="03"></div>
<script type="application/json" id="problems-03">
[
  { "id": "03-1", "type": "num", "slide": 19, "q": "หา \\(E\\) ของ \\(x(t)=e^{-t}u(t)\\)", "answer": "1/2", "hint": "…", "sol": "…" },
  { "id": "03-2", "type": "mc", "q": "…", "choices": ["…", "…", "…", "…"], "answer": 1, "sol": "…" },
  { "id": "03-3", "type": "think", "q": "อธิบายด้วยคำของตัวเองว่า …", "sol": "คำตอบตัวอย่าง …" }
]
</script>
```

- The JSON must parse: escape backslashes in math (`\\(`), use straight quotes.
- `num` accepts decimals and fractions; set `tol` when rounding is expected (e.g. `0.01`).
- Mix types: about half `num`, the rest `mc` and `think`. Tie questions to slide numbers.
- Compute every numeric answer with code before writing it down.
- Update the lesson's `data-total` on the index to the number of questions.

## Writing

- Short paragraphs; one idea per paragraph; plain words before notation.
- Explain why a step is done, not only what is done.
- Use the lecture's examples first, then one new example so the learner transfers the idea.
- A lesson longer than about 30 minutes of reading is two lessons.
