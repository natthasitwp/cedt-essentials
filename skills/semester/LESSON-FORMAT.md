# Handbook lessons

One file per schedule week: `handbook/lessons/wNN.html`. Each is an HTML fragment (no
`<html>`/`<head>`), a single `<article>` that `tools/build.py` drops into the shell. The
shell shows the index by default and one lesson when the URL hash is `#wNN`, adds
prev/next links, and gives every code block a language tag and a copy button.

## Skeleton

```html
<article class="lesson" id="w03" data-week="W03" data-title="ชื่อบทสั้นๆ" data-sub="Stage 1 · Linear algebra · สัปดาห์ 1/2" hidden>
<p class="kicker">W03 · Stage 1 · Linear algebra · สัปดาห์ 1/2 · ~10 ชม.</p>
<h1>ชื่อบท</h1>
<p class="meta">หัวข้อตาม roadmap: ...</p>

<div class="goal"><b>เป้าหมายสัปดาห์นี้:</b> สิ่งที่ผู้เรียนต้องทำได้เมื่อจบสัปดาห์ เขียนเป็นความสามารถที่ตรวจได้</div>

<h2><span class="num">1</span>หัวข้อแรก</h2>
<p>คำอธิบาย ...</p>
<pre><code data-lang="python">...</code></pre>
<div class="def" data-label="นิยาม">...</div>
<details class="predict"><summary>คำถามให้ทายก่อน</summary><p>เฉลยและเหตุผล</p></details>
<div class="link-infer">หัวข้อนี้ใช้ตรงไหนใน mission ของผู้เรียน</div>
<div class="warn">กับดักที่คนพลาดบ่อย</div>

<div class="exercise"><span class="tag">แบบฝึกหัด 1</span><h4>ชื่อแบบฝึกหัด</h4>
<p>ไฟล์ <code>exercises/w03/ex1_x.py</code></p>
<pre><code data-lang="bash">uv run pytest exercises/w03/test_w03_ex1_x.py</code></pre></div>

<div class="paper-ref"><span class="lbl">Paper สัปดาห์นี้ · อ่าน</span><br><a href="...">Title</a> (Authors, Year) ทำไมต้องอ่าน</div>

<h2><span class="num">N</span>ส่งงานสัปดาห์นี้</h2>
<ul class="checklist">
<li><code>uv run pytest exercises/w03</code> ขึ้น <strong>K passed</strong></li>
<li>สิ่งที่ต้องวางในช่องส่งงานของ W03 บนหน้าคอร์ส</li>
<li>สอบย่อย W03 ที่หน้าคอร์ส</li>
</ul>
<p class="meta">อ่านเพิ่ม: ...</p>
</article>
```

## Writing rules

- Cover exactly the week's topics from `course.json`, in order; one `<h2>` per topic, each
  ending in its exercise. Keep the week within its hour budget.
- Write prose in the learner's language; keep terms of art and code in English.
- Every topic has at least one of: a worked example with real numbers, a predict box, or a
  mission box. Predict answers explain the why, not just the answer.
- Use `<sup>`, `<sub>` and Unicode symbols for simple math. Do not load a math library.
- Escape `<`, `>` and `&` inside code blocks (`&lt;`, `&gt;`, `&amp;`).
- Quote counts like "K passed" only after running the grader on the reference solution.
- The last lesson of a step restates the step's project as a checklist and says how it is
  checked (a project checker script when possible).

## Before publishing

1. `python tools/build.py`
2. Parse `dist/handbook.html` and check that every tag closes; `node --check` the script.
3. Look once at the built page through a local static server (`python -m http.server`) at
   phone and desktop width, in the default light theme (and with `data-theme="dark"` if the
   user turned dark mode on). Fix what you see, then publish.
4. Add the new ids to `handbookReady`, rebuild, and republish the course page.
