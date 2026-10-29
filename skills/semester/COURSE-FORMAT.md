# course.json, schedule and course page

## course.json

```json
{
  "code": "INF 4101",
  "title": "INF 4101 Inference Engineering",
  "topbar": "INF 4101 · Inference Engineer Route",
  "heading": "เส้นทาง Inference Engineer",
  "subject": "Inference Engineering",
  "missionLabel": "Inference",
  "level": "ปริญญาตรีปี 3–4",
  "credits": "3(2-2-5)",
  "start": "2026-11-02",
  "goal": "serve โมเดลขนาด 8B บนหลาย engine แล้วอธิบายตัวเลข TTFT, throughput และต้นทุนได้",
  "credit": "เนื้อหามาจาก <a href=\"https://example.org/roadmap\">ชื่อ roadmap</a> แล้วจัดเป็นตารางรายสัปดาห์",
  "capstone": "ต่อยอด project สอง step สุดท้ายเป็น demo ที่เปิดเป็น API ได้ พร้อมรายงานตัวเลข",
  "courseUrl": "",
  "handbookUrl": "",
  "handbookReady": ["w01", "w02"],
  "hardware": { "cpu": "CPU / Mac", "gpu-16gb": "GPU 16 GB · Colab / Kaggle" },
  "stages": [
    { "id": "foundations", "label": "Stage 1", "title": "Statistics & Probability", "bufferAfter": false },
    { "id": "inference", "label": "Branch A", "title": "Inference Engineer", "bufferAfter": false }
  ],
  "steps": [
    {
      "id": "foundations-1", "stage": "foundations",
      "title": "Programming prerequisites: Python, NumPy/pandas, uv, Git, shell and Jupyter",
      "short": "Python, NumPy, uv, Git",
      "desc": "What and why paragraph.",
      "diff": "beginner", "weeks": 2, "hw": "cpu", "opt": false,
      "lenses": ["fundamentals", "engineering"],
      "topics": ["...", "..."],
      "papers": [{ "t": "Title", "a": "Authors", "y": 2020, "u": "https://...", "why": "Why read it", "d": "read" }],
      "tools": [{ "n": "uv", "p": "What it is for", "u": "https://..." }],
      "res": [{ "t": "Title", "k": "book", "u": "https://..." }],
      "project": "The step's project brief.",
      "notes": ["Optional dated update."]
    }
  ]
}
```

Required: `code`, `title`, `heading`, `subject`, `start` (a Monday), `stages`, `steps`
(each with `id`, `stage`, `title`, `weeks`). Everything else is optional. `goal`, `credit`
and `capstone` may contain trusted HTML you wrote. `d` is `read`, `skim` or `replicate`.

## Schedule rules (implemented in the template)

- One item per week. Week 1 starts on `start`; every deadline is Sunday 23:59 local time.
- A step of `weeks: n` becomes `round(n)` weeks (at least 1). Its topics and papers are
  split evenly across those weeks. The last week of a step is the project hand-in.
- After each stage's required steps comes a **stage exam** week (portfolio review). The
  last stage's exam is the **capstone**.
- `bufferAfter: true` adds a buffer week after that stage's exam. Place buffers on the
  learner's real exam months.
- Steps with `opt: true` are scheduled after the final exam and never count toward the grade.
- Handbook lesson ids follow the schedule: week index 1 → `w01`.

## Grading (implemented in the template)

- A week passes when the submission is in (at least 40 characters of real content) and the
  quiz is at least 70% (stage exams: 60%).
- Three attempts per quiz, a new paper each time, best score counts.
- Late completion still passes, but that week's quiz counts ×0.8 and work 80/100.
- Finishing before the week starts shows "ผ่านก่อนกำหนด"; later deadlines do not move.
- Final weights: weekly quizzes 30%, weekly work 30%, stage exams 40% (average).
  Thai letter grades: A ≥ 80, B+ ≥ 75, B ≥ 70, C+ ≥ 65, C ≥ 60, D+ ≥ 55, D ≥ 50.

## Publishing

Publish `dist/course.html` with:

```json
{
  "db": { "rules": [
    { "path": "progress", "read": "view", "write": "admin" },
    { "path": "config", "read": "view", "write": "admin" }
  ] },
  "user": {},
  "sample": {}
}
```

`sample` writes and grades exams on the learner's own Claude account; the page asks them
the first time. Publish `dist/handbook.html` as a separate artifact with no capabilities.
Redeploys omit `capabilities` to keep them.

## The progress store

- `config/course`: `{ "start": "YYYY-MM-DD" }`, the learner's chosen start date.
- `progress/<itemId>`: `workDone`, `workNote`, `workAt`, `tries`, `best`, `lastScore`,
  `lastFeedback`, `lastAt`, `passedAt`. Item ids look like `foundations-1.w2`,
  `exam.<stageId>` and `buffer.<stageId>`.

Changing step ids after the learner has started orphans their progress. Add steps with
new ids instead of renaming old ones.
