"""Build public, synthetic skill examples. Run: python3 scripts/build_examples.py."""
from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'examples'
CRAM = ROOT / 'skills/cram/assets/site'
SEM = ROOT / 'skills/semester/assets'


def write(path, content):
    p = OUT / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content)


def chrome(text, prefix):
    """Shared demo navigation; keep the skills' original page styling."""
    extra = f'<link rel="stylesheet" href="{prefix}assets/demo.css"><script defer src="{prefix}assets/demo.js"></script>'
    text = text.replace('</head>', extra + '</head>') if '</head>' in text else extra + text
    nav = f'<aside class="demo-bar"><a href="{prefix}index.html">← CEDT Essentials / Examples</a><span>ตัวอย่างสาธิต · ข้อมูลสมมติ</span><button type="button" id="demo-theme">สลับธีม</button><button type="button" id="demo-reset">ล้างข้อมูลทดลอง</button></aside>'
    return text.replace('<main>', nav + '<main>', 1)


def page(title, body, depth=0):
    prefix = '../' * depth
    return chrome(f'''<!doctype html><html lang="th"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Jost:wght@400;500;600&family=IBM+Plex+Sans+Thai:wght@400;500;600&family=Mali:wght@500;600&family=IBM+Plex+Mono:wght@400;500&display=swap"><meta name="description" content="ตัวอย่างผลลัพธ์จาก cram และ semester — CEDT Essentials"><title>{title} · CEDT Essentials</title><link rel="stylesheet" href="{prefix}cram/assets/style.css"><script defer src="{prefix}cram/assets/site.js"></script></head><body data-site="cedt-demo-cram-v1"><main>{body}</main></body></html>''', prefix)


shutil.copytree(CRAM / 'assets', OUT / 'cram/assets', dirs_exist_ok=True)
write('assets/demo.css', '''.demo-bar{max-width:62rem;margin:20px auto;padding:12px 18px;display:flex;gap:12px;align-items:center;flex-wrap:wrap;border:1px dashed var(--rule);font:13px/1.6 system-ui;color:var(--ink-soft)}.demo-bar a{margin-right:auto}.demo-bar button{font:inherit;color:var(--ink);background:var(--card);border:1px solid var(--rule);border-radius:5px;padding:5px 10px;cursor:pointer}.demo-hero{width:100%;border-radius:8px;margin:16px 0 28px}.demo-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin:28px 0}.demo-card{border:1px solid var(--rule);background:var(--card);padding:24px;border-radius:4px 15px 5px 12px}.demo-card h2{margin-top:0}.demo-card a{font-weight:600}.demo-label{font:13px var(--mono);color:var(--blue);letter-spacing:.08em}.demo-footer{margin-top:48px;padding-top:18px;border-top:1px solid var(--rule);font-size:14px}.slide img{width:100%}@media(max-width:600px){.demo-grid{grid-template-columns:1fr}.demo-bar{margin:16px}.demo-bar span{width:100%}}''')
write('assets/demo.js', '''(() => {
  try { const theme = localStorage.getItem('cedt-demo-theme'); if(theme) document.documentElement.dataset.theme = theme; } catch {}
  document.getElementById('demo-theme')?.addEventListener('click', () => {
    const dark = document.documentElement.dataset.theme === 'dark';
    const theme = dark ? 'light' : 'dark'; document.documentElement.dataset.theme = theme;
    try { localStorage.setItem('cedt-demo-theme', theme); } catch {}
  });
  document.getElementById('demo-reset')?.addEventListener('click', () => {
    try { Object.keys(localStorage).filter(k => k.startsWith('cedt-demo-') && k !== 'cedt-demo-theme').forEach(k => localStorage.removeItem(k)); location.reload(); } catch { alert('เบราว์เซอร์ไม่อนุญาตให้ล้างข้อมูล'); }
  });
})();''')
write('index.html', page('ลองเรียนก่อนติดตั้ง', '''<p class="kicker">OPEN STUDY TOOLKIT / LIVE EXAMPLES</p><img class="demo-hero" src="assets/banner.png" alt="CEDT Essentials — Study smarter. Keep learning."><h1>เรียนให้เข้าใจ<br>แล้วไปต่อด้วยตัวเอง</h1><p class="meta">ลองดูสิ่งที่ agent สร้างให้คุณได้ จากสองสกิลใน CEDT Essentials</p><div class="goal">เลือกอ่านบทสั้นก่อนสอบ หรือวางเส้นทางเรียนระยะยาว ทุกตัวอย่างใช้ธีมสมุดโน้ตเดียวกับสกิลจริง</div><div class="demo-grid"><section class="demo-card"><p class="demo-label">01 / CRAM · 15 MIN</p><h2>จากสไลด์<br>สู่ความเข้าใจ</h2><p>บทเรียน Probability สั้น ๆ พร้อมสไลด์ตัวอย่าง คำถามให้คิดก่อนเปิดเฉลย และโจทย์ตรวจคำตอบทันที</p><a href="cram/index.html">เปิดตัวอย่าง cram →</a><p class="meta">2 บทเรียน · 6 คำถาม · Cheat sheet</p></section><section class="demo-card"><p class="demo-label">02 / SEMESTER · 6 WEEKS</p><h2>เปลี่ยนเป้าหมาย<br>เป็นตารางเรียน</h2><p>คอร์ส Python สำหรับงานข้อมูล มี roadmap กำหนดส่งวันอาทิตย์ งานประจำสัปดาห์ และ handbook สองบทแรก</p><a href="semester/course.html">เปิดตัวอย่าง semester →</a><p class="meta">Syllabus · Progress · Handbook</p></section></div><h2>ลองกดอะไรได้บ้าง?</h2><ol><li>ตอบคำถามใน cram แล้วกลับมาดูความคืบหน้าที่สารบัญ</li><li>เปิดแผนรายสัปดาห์ใน semester และทดลองส่งบันทึกงาน</li><li>สลับ light / dark mode หรือเปิดบนมือถือ</li></ol><div class="note"><b>เกี่ยวกับ demo:</b> เนื้อหาและสไลด์สร้างขึ้นใหม่เพื่อสาธิต ไม่มีสไลด์ คลิป หรือข้อมูลผู้เรียนจริง ระบบสอบ AI ของ semester ต้องใช้ Claude artifact จึงไม่เปิดในเว็บสาธิตนี้ ข้อมูลทดลองเก็บเฉพาะเบราว์เซอร์ของคุณ ไม่มีการส่งงานไปหาอาจารย์</div><footer class="demo-footer"><a href="https://github.com/natthasitwp/cedt-essentials">ดู repo และวิธีติดตั้ง ↗</a> · MIT License</footer>'''))

# Cram: real starter assets and quiz format, with an explicitly authored mini-lecture.
lessons = [
    ('01', 'sample-space', 'เริ่มจาก Sample space', 'นับผลลัพธ์ก่อนแทนสูตร',
     'เมื่อทอยลูกเต๋ายุติธรรมหนึ่งลูก Sample space คือ {1, 2, 3, 4, 5, 6} ส่วน Event คือผลลัพธ์บางส่วนที่เราสนใจ เช่น “แต้มเป็นเลขคู่” คือ {2, 4, 6}',
     'P(A) = จำนวนผลลัพธ์ใน A / จำนวนผลลัพธ์ทั้งหมด เมื่อทุกผลลัพธ์มีโอกาสเท่ากัน',
     'ถ้าเปลี่ยนเป็น “แต้มมากกว่า 4” จะมีผลลัพธ์กี่แบบ?', 'มี 2 แบบ คือ 5 และ 6 ดังนั้น P(A) = 2/6 = 1/3',
     'อย่าใช้สูตรนับจำนวนหากผลลัพธ์มีโอกาสเกิดไม่เท่ากัน เช่น ลูกเต๋าถ่วงน้ำหนัก',
     'เลขคู่มี 3 แบบจากทั้งหมด 6 แบบ ดังนั้น P(เลขคู่) = 3/6 = 0.5',
     [dict(id='01-1', type='num', q='ทอยลูกเต๋ายุติธรรมหนึ่งลูก โอกาสได้เลขคู่เท่ากับเท่าไร?', answer='0.5', hint='นับ 2, 4, 6', sol='มี 3 แบบจาก 6 แบบ: 3/6 = 0.5'), dict(id='01-2', type='mc', q='ชุดใดคือ Event “แต้มมากกว่า 4”?', choices=['{1, 2, 3, 4}', '{4, 5, 6}', '{5, 6}', '{6}'], answer=2, sol='มากกว่า 4 ไม่รวม 4 จึงเหลือ 5 และ 6'), dict(id='01-3', type='think', q='ทำไมลูกเต๋าถ่วงน้ำหนักจึงใช้การนับหารตรง ๆ ไม่ได้?', sol='สูตรนี้ต้องให้แต่ละผลลัพธ์มีโอกาสเท่ากัน หากไม่เท่ากัน ต้องรวมความน่าจะเป็นของแต่ละผลลัพธ์ใน Event')]),
    ('02', 'conditional', 'เมื่อรู้ข้อมูลเพิ่ม: Conditional probability', 'จำกัด Sample space แล้วนับใหม่',
     'เมื่อรู้ว่าผลทอยเป็นเลขคู่ ผลลัพธ์ที่ยังเป็นไปได้เหลือ {2, 4, 6} ถ้าถามต่อว่าแต้มมากกว่า 3 หรือไม่ ผลลัพธ์ที่ผ่านทั้งสองเงื่อนไขคือ {4, 6}',
     'P(A | B) = P(A ∩ B) / P(B) โดย P(B) > 0',
     'P(แต้มมากกว่า 3 | เลขคู่) จะเท่ากับ P(เลขคู่ | แต้มมากกว่า 3) เสมอไหม?', 'ไม่เสมอ แม้ตัวอย่างนี้เท่ากันที่ 2/3 แต่เมื่อเปลี่ยนเป็น “มากกว่า 4” จะได้ 1/3 กับ 1/2 ตามลำดับ',
     'ตัวหารคือเงื่อนไขที่รู้แล้ว B ไม่ใช่ Event A ที่กำลังถามหา',
     'ในเลขคู่ {2, 4, 6} มี 2 ผลลัพธ์ที่มากกว่า 3 ดังนั้น P(มากกว่า 3 | เลขคู่) = 2/3',
     [dict(id='02-1', type='num', q='รู้แล้วว่าแต้มเป็นเลขคู่ โอกาสได้แต้มมากกว่า 3 เท่าไร? ตอบเป็นเศษส่วนได้', answer='2/3', hint='พิจารณาเฉพาะ {2, 4, 6}', sol='ผลลัพธ์ที่ผ่านคือ {4, 6} จึงได้ 2/3'), dict(id='02-2', type='mc', q='ใน P(A | B) เรารู้อะไรแล้ว?', choices=['A เกิดขึ้นแล้ว', 'B เกิดขึ้นแล้ว', 'A และ B ไม่เกิด', 'A และ B อิสระกัน'], answer=1, sol='ด้านขวาของ | คือเงื่อนไขที่ทราบแล้ว'), dict(id='02-3', type='think', q='อธิบายว่าทำไม P(A | B) กับ P(B | A) จึงอาจไม่เท่ากัน', sol='ใช้พื้นที่อ้างอิงคนละชุด ตัวหาร P(B) กับ P(A) อาจต่างกัน แม้ตัวเศษ P(A ∩ B) เท่ากัน')])]
source = ROOT / 'examples-source/cram/lessons'
source.mkdir(parents=True, exist_ok=True)
index_source = source / 'index.md'
if not index_source.exists():
    index_source.write_text('''---
title: Probability ก่อนวันสอบ
code: CRAM / PROBABILITY BASICS
site: cedt-demo-cram-v1
purpose: mini-lecture สร้างขึ้นใหม่เพื่อสาธิต ไม่มีคลิปจึงไม่มี timestamp
---
:::note
คำตอบที่ทำได้เก็บเฉพาะเบราว์เซอร์นี้ เนื้อหาและสไลด์เป็นตัวอย่างสมมติ ไม่มีข้อมูลผู้เรียนจริง
:::
''')
for nn, slug, title, sub, intro, formula, predict, reveal, warning, worked, qs in lessons:
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="500" viewBox="0 0 1000 500"><rect width="1000" height="500" fill="#f4f3ef"/><path d="M50 100H950M50 425H950" stroke="#dcd8d0"/><text x="55" y="65" font-family="sans-serif" font-size="21" fill="#4e7184">CEDT / ORIGINAL DEMO SLIDE {int(nn):02d}</text><text x="55" y="160" font-family="sans-serif" font-size="34" fill="#45403c">{'Sample space &amp; events' if nn == '01' else 'Conditional probability'}</text><text x="55" y="225" font-family="monospace" font-size="26" fill="#45403c">{'S = {1, 2, 3, 4, 5, 6}' if nn == '01' else 'B = {2, 4, 6}, A = {4, 5, 6}'}</text><rect x="48" y="270" width="900" height="100" rx="8" fill="#d4e2d0"/><text x="70" y="330" font-family="monospace" font-size="29" fill="#45403c">{'P(even) = 3 / 6 = 0.5' if nn == '01' else 'P(A | B) = 2 / 3'}</text><text x="55" y="463" font-family="sans-serif" font-size="18" fill="#6c6661">Synthetic teaching material / fair six-sided die</text></svg>'''
    write(f'cram/slides/demo-{nn}.svg', svg)
    path = source / f'{nn}-{slug}.md'
    if not path.exists():
        text = f'''---
title: {title}
minutes: 15
src: สไลด์สาธิตที่สร้างขึ้นใหม่
oneline: {sub}
goal: {sub} และอธิบายคำตอบได้
cheat:
  - "{formula}"
---
## แนวคิด

{intro}

::slide demo-{nn}.svg | {formula} | สไลด์สาธิต {int(nn)} สร้างขึ้นสำหรับตัวอย่างนี้

:::def นิยาม
{formula}
:::

:::predict {predict}
{reveal}
:::

:::warn
{warning}
:::

## ลองดูตัวอย่าง

{worked}

## ลองทำด้วยตัวเอง

:::quiz
'''
        for q in qs:
            text += f"? {q['type']} | {q['q']}\n"
            if q['type'] == 'mc':
                text += ''.join(f"- {'[x] ' if i == q['answer'] else ''}{c}\n" for i, c in enumerate(q['choices']))
            elif q['type'] == 'num':
                text += f"answer: {q['answer']}\n"
            if q.get('hint'):
                text += f"hint: {q['hint']}\n"
            text += f"sol: {q['sol']}\n\n"
        path.write_text(text + ':::\n')
# Run the skill's real Markdown compiler against the editable example sources.
import importlib.util
spec = importlib.util.spec_from_file_location('cram_builder', ROOT / 'skills/cram/scripts/build.py')
builder = importlib.util.module_from_spec(spec)
spec.loader.exec_module(builder)
builder.ROOT = source.parent
builder.SRC = source
builder.SITE = OUT / 'cram'
if builder.main():
    raise SystemExit('Cram example build failed')
for path in (OUT / 'cram').rglob('*.html'):
    prefix = '../' if path.parent == OUT / 'cram' else '../../'
    path.write_text(chrome(path.read_text(), prefix))

# Semester: populate the actual course template; use a local-only demo adapter.
course = dict(code='PY 101', title='PY 101 · Python for Data', topbar='PY 101 · ตัวอย่าง semester', heading='เส้นทาง Python for Data', subject='Python', missionLabel='งานข้อมูล', start='2026-11-02', credits='Demo · 4 ชม./สัปดาห์', goal='อ่านข้อมูล คำนวณสถิติเบื้องต้น และส่งรายงานที่รันซ้ำได้', credit='คอร์สและผลงานตัวอย่างสมมติ สร้างเพื่อแสดงรูปแบบผลลัพธ์ของ semester', capstone='วิเคราะห์ข้อมูลจำลอง พร้อมอธิบายข้อจำกัดและส่งโค้ดที่รันซ้ำได้', handbookUrl='handbook.html', courseUrl='course.html', handbookReady=['w01','w02'], hardware={'cpu':'CPU / Mac / Windows'}, stages=[dict(id='basics', label='Stage 1', title='Python foundations', bufferAfter=False),dict(id='data', label='Stage 2', title='Data workflow', bufferAfter=False)], steps=[])
for i, (title, topics, project) in enumerate([
    ('Python: lists & functions', ['List, loop และผลรวม', 'Function และ edge cases'], 'เขียนฟังก์ชันสรุปชุดข้อมูลและทดสอบกรณี list ว่าง'),
    ('Data cleaning', ['Missing values', 'การตรวจข้อมูลก่อนคำนวณ'], 'ล้างข้อมูลจำลองและรายงานจำนวนแถวก่อนและหลัง'),
    ('Descriptive statistics', ['Mean และ median', 'Outlier และการเลือกสถิติ'], 'เปรียบเทียบค่าเฉลี่ยกับมัธยฐานก่อนและหลังเพิ่ม outlier'),
    ('Reproducible report', ['แยก input / computation / output', 'บันทึกข้อจำกัดและวิธีรันซ้ำ'], 'ส่งสคริปต์และรายงานที่อีกคนรันแล้วได้ผลเดิม')]):
    course['steps'].append(dict(id=f'step-{i+1}', stage='basics' if i < 2 else 'data', title=title, short=title, desc='ตัวอย่างแผนเรียนที่เชื่อมกับเป้าหมายการทำงานข้อมูล', diff='beginner', weeks=1, hw='cpu', opt=False, topics=topics, project=project))
write('semester/course.json', json.dumps(course, ensure_ascii=False, indent=2) + '\n')
tpl = (SEM / 'course-page.html').read_text()
for key, val in {'COURSE':json.dumps(course, ensure_ascii=False).replace('</','<\\/'), 'TITLE':course['title'], 'TOPBAR':course['topbar'], 'HEADING':course['heading'], 'CREDITS':course['credits'], 'GOAL':course['goal'], 'CREDIT':course['credit'], 'START':course['start']}.items():
    tpl = tpl.replace('__'+key+'__', val)
# Leave production skill templates untouched. Public demos have no Claude service.
a = tpl.index('(async () => {\n  if (!window.claude?.use)')
b = tpl.index('})();', a) + len('})();')
tpl = tpl[:a] + '''showNotice("DEMO · ทดลองส่งบันทึกงานได้ ข้อมูลอยู่เฉพาะเบราว์เซอร์นี้ คะแนนเริ่มต้นเป็นข้อมูลสมมติ ระบบสอบ AI ไม่เปิดบนเว็บสาธิต");''' + tpl[b:]
tpl = tpl.replace('const progress = {};', '''let demoState = {};
try { demoState = JSON.parse(localStorage.getItem('cedt-demo-semester-v1') || '{}'); } catch {}
const progress = demoState.progress || { 'step-1.w1': { workDone: true, workNote: 'ผลงานสมมติ: ทดสอบ list ว่างและคำนวณผลรวมของ [2, 4, 6] ได้ 12', workAt: '2026-11-08T12:00:00+07:00', best: 85, tries: 1, passedAt: '2026-11-08T12:00:00+07:00', lastFeedback: 'ตัวอย่าง feedback สมมติ: แยกฟังก์ชันได้ชัดเจน ควรเพิ่มการทดสอบกรณีข้อมูลว่าง' } };
if (demoState.start) start = demoState.start;
function persistDemo() { try { localStorage.setItem('cedt-demo-semester-v1', JSON.stringify({progress, start})); } catch { showNotice('เบราว์เซอร์ไม่อนุญาตบันทึก ข้อมูลจะหายเมื่อรีโหลด'); } }''')
tpl = tpl.replace('  if (!db) return;', '  persistDemo();\n  if (!db) return;')
tpl = tpl.replace('  start = v; render();', '  start = v; persistDemo(); render(); m.textContent = "บันทึกในเบราว์เซอร์นี้แล้ว";')
tpl = tpl.replace('ระบบสอบใช้ได้เมื่อเปิดหน้านี้บน claude.ai และอนุญาตให้ใช้ Claude', 'Demo นี้ไม่เรียก AI · สกิลจริงสร้างและตรวจข้อสอบใหม่ผ่าน Claude artifact')
tpl = tpl.replace('ระบบสอบเรียกใช้ Claude ผ่านบัญชีของคุณ ครั้งแรกจะมีหน้าต่างขออนุญาตขึ้นมา คะแนนและงานที่ส่งจะบันทึกไว้ในหน้านี้ และ Claude อ่านย้อนหลังได้', 'เว็บนี้เป็นตัวอย่างสาธารณะ: การส่งงานเป็นการทดลองในเบราว์เซอร์เท่านั้น ไม่มีผู้สอนตรวจ และไม่มีการเรียกใช้ Claude หรือบันทึกข้อมูลบนเซิร์ฟเวอร์')
tpl = tpl.replace('uv run pytest exercises/${hb}', 'python -m unittest test_practice.py')
write('semester/course.html', '<!doctype html><html lang="th"><meta name="viewport" content="width=device-width, initial-scale=1">' + chrome(tpl, '../') + '</html>')

fragments = []
for nn, title, sub, text, code, question, answer in [
    ('01','Lists & functions','Python foundations · สัปดาห์ 1','เริ่มจากชุดข้อมูลเล็ก ๆ แล้วแยกการคำนวณเป็นฟังก์ชันที่ทดสอบได้ รายการ [2, 4, 6] มีผลรวม 12 และมีสมาชิก 3 ตัว','def total(values):\n    return sum(values)\n\nprint(total([2, 4, 6]))  # 12','ถ้าส่ง list ว่างเข้า total จะได้อะไร?','ได้ 0 เพราะ sum ของ list ว่างเริ่มจากค่า 0'),
    ('02','Clean before you calculate','Python foundations · สัปดาห์ 2','ข้อมูลจำลอง [2, None, 4, 6] มีค่าที่หายไปหนึ่งรายการ ก่อนคำนวณให้ตัดสินใจว่าจะจัดการอย่างไรและบันทึกจำนวนที่ถูกตัดออก','values = [2, None, 4, 6]\nclean = [x for x in values if x is not None]\nprint(sum(clean) / len(clean))  # 4.0','ถ้าใช้ if x แทน if x is not None จะเกิดปัญหาอะไร?','ค่า 0 จะถูกตัดออกด้วย ทั้งที่เป็นข้อมูลที่ใช้คำนวณได้')]:
    fragments.append(f'''<article class="lesson" id="w{nn}" data-week="W{nn}" data-title="{title}" data-sub="{sub}" hidden><p class="kicker">W{nn} / ~4 ชั่วโมง</p><h1>{title}</h1><div class="goal">เป้าหมาย: อ่านโค้ด อธิบายผล และลองเปลี่ยนข้อมูลได้</div><h2><span class="num">1</span>แนวคิด</h2><p>{text}</p><pre><code data-lang="python">{html.escape(code)}</code></pre><details class="predict"><summary>{question}</summary><p>{answer}</p></details><div class="link-infer">การแยกขั้นตอนให้ชัดเจนช่วยให้รายงานข้อมูลตรวจสอบและรันซ้ำได้</div><h2><span class="num">2</span>ฝึกและส่งหลักฐาน</h2><div class="exercise"><p>ดาวน์โหลด <a href="exercises/practice.py" download>practice.py</a> และ <a href="exercises/test_practice.py" download>test_practice.py</a> ไว้ในโฟลเดอร์เดียวกัน เติมฟังก์ชัน แล้วรันคำสั่งด้านล่าง</p><pre><code data-lang="bash">python -m unittest test_practice.py</code></pre></div><p>ส่งโค้ด ผลลัพธ์ที่คำนวณได้ และอธิบาย edge case อย่างน้อยหนึ่งกรณีในหน้าคอร์ส งานใน demo นี้เก็บเฉพาะเบราว์เซอร์</p></article>''')
shell = (SEM / 'handbook-shell.html').read_text().replace('__LESSONS__','\n'.join(fragments)).replace('__CODE__','PY 101').replace('__MISSION_LABEL__','งานข้อมูล').replace('__COURSE_URL__','course.html')
shell = shell.replace('ให้ <code>uv run pytest</code> ขึ้นเขียวทั้งหมด', 'ด้วยคำสั่งที่ให้ไว้ในบทเรียน').replace('แล้วไปส่งงานกับสอบย่อยที่หน้าคอร์ส', 'แล้วทดลองส่งบันทึกงานที่หน้าคอร์ส (ระบบสอบ AI ไม่เปิดใน demo)')
write('semester/handbook.html', '<!doctype html><html lang="th"><meta name="viewport" content="width=device-width, initial-scale=1">' + chrome(shell, '../') + '</html>')
write('semester/exercises/practice.py', '''"""Synthetic demo exercise. Complete both functions, then run the tests."""
def total(values):
    """Return the sum, or 0 for an empty list."""
    raise NotImplementedError


def clean_mean(values):
    """Ignore None, keep zero, return None if no values remain."""
    raise NotImplementedError
''')
write('semester/exercises/test_practice.py', '''import unittest
from practice import total, clean_mean


class PracticeTests(unittest.TestCase):
    def test_total(self):
        self.assertEqual(total([2, 4, 6]), 12)
        self.assertEqual(total([]), 0)
        self.assertEqual(total([-2, 2]), 0)

    def test_clean_mean(self):
        self.assertEqual(clean_mean([2, None, 4, 6]), 4.0)
        self.assertEqual(clean_mean([0, None, 4]), 2.0)
        self.assertIsNone(clean_mean([None]))
        self.assertIsNone(clean_mean([]))


if __name__ == '__main__':
    unittest.main()
''')
write('_headers', '''/*
  X-Content-Type-Options: nosniff
  Referrer-Policy: strict-origin-when-cross-origin
  Permissions-Policy: camera=(), microphone=(), geolocation=()
''')
print('Built examples/ from cram and semester templates.')
