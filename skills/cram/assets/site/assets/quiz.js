/* quiz.js: self-check questions with instant feedback.

   A lesson declares its questions as JSON and gives them a place to appear:
     <div class="quiz" data-quiz="01"></div>
     <script type="application/json" id="problems-01">[ ... ]</script>

   Question fields:
     id      unique, e.g. "01-1"
     type    "num" (typed number) | "mc" (choices) | "think" (reveal, then rate yourself)
     q       question text (HTML allowed; math as \( … \))
     answer  num: the number as a string ("0.5", "1/3"); mc: index of the right choice
     tol     num only: allowed absolute error (default 1e-3 relative to the size of the answer)
     choices mc only: list of strings, about the same length each
     hint    optional
     sol     worked solution shown after an attempt
     slide   optional slide number the question comes from

   Progress is kept per browser in localStorage, so a solved question stays solved. */
(function () {
  const site = document.body.dataset.site || "cram";
  const key = (lesson) => `${site}-done-${lesson}`;
  const load = (lesson) => { try { return new Set(JSON.parse(localStorage.getItem(key(lesson))) || []); } catch { return new Set(); } };
  const save = (lesson, set) => { try { localStorage.setItem(key(lesson), JSON.stringify([...set])); } catch {} };

  const toNum = (s) => {
    s = String(s).trim().replace(/,/g, "").replace(/−/g, "-");
    const frac = s.match(/^(-?\d+(?:\.\d+)?)\s*\/\s*(-?\d+(?:\.\d+)?)$/);
    if (frac) return +frac[1] / +frac[2];
    return s === "" ? NaN : Number(s);
  };

  function mount(box) {
    const lesson = box.dataset.quiz;
    const data = document.getElementById("problems-" + lesson);
    if (!data) return;
    const problems = JSON.parse(data.textContent);
    const done = load(lesson);

    problems.forEach((p, i) => {
      const el = document.createElement("div");
      el.className = "q" + (done.has(p.id) ? " done" : "");
      const tag = { num: "ตอบเป็นตัวเลข", mc: "เลือกคำตอบ", think: "คิดแล้วเทียบเฉลย" }[p.type];
      el.innerHTML = `<div class="q-head">ข้อ ${i + 1} · <span class="tag">${tag}</span>${p.slide ? ` · สไลด์ ${p.slide}` : ""}</div>
        <div class="q-body">${p.q}</div><div class="q-ans"></div><div class="fb" aria-live="polite"></div>`;
      const ans = el.querySelector(".q-ans"), fb = el.querySelector(".fb");

      const reveal = () => {
        if (el.querySelector(".q-sol")) return;
        const s = document.createElement("div");
        s.className = "q-sol"; s.innerHTML = "<b>เฉลย</b> " + p.sol;
        el.append(s); window.renderMath && window.renderMath(s);
      };
      const solved = () => { done.add(p.id); save(lesson, done); el.classList.add("done"); };
      const hintBtn = () => {
        if (!p.hint) return "";
        return `<button type="button" data-hint>คำใบ้</button>`;
      };

      if (p.type === "num") {
        ans.innerHTML = `<div class="q-row"><input type="text" inputmode="decimal" aria-label="คำตอบข้อ ${i + 1}">
          <button type="button" class="primary" data-check>ตรวจ</button>${hintBtn()}<button type="button" data-show>ดูเฉลย</button></div>`;
        const input = ans.querySelector("input");
        const check = () => {
          const got = toNum(input.value), want = toNum(p.answer);
          const tol = p.tol ?? Math.max(1e-9, Math.abs(want) * 1e-3);
          if (Number.isNaN(got)) { fb.className = "fb no"; fb.textContent = "พิมพ์เป็นตัวเลข เช่น 0.5 หรือ 1/3"; return; }
          if (Math.abs(got - want) <= tol) { fb.className = "fb ok"; fb.textContent = "ถูกต้อง ✓"; solved(); reveal(); }
          else { fb.className = "fb no"; fb.textContent = "ยังไม่ถูก ลองใหม่หรือเปิดคำใบ้"; }
        };
        ans.querySelector("[data-check]").addEventListener("click", check);
        input.addEventListener("keydown", (e) => { if (e.key === "Enter") check(); });
      } else if (p.type === "mc") {
        ans.innerHTML = `<div class="choices">${p.choices.map((c, ci) => `<button type="button" data-c="${ci}">${c}</button>`).join("")}</div>
          <div class="q-row" style="margin-top:8px">${hintBtn()}</div>`;
        ans.querySelectorAll("[data-c]").forEach((b) => b.addEventListener("click", () => {
          const right = +b.dataset.c === +p.answer;
          b.classList.add(right ? "right" : "wrong");
          fb.className = "fb " + (right ? "ok" : "no");
          fb.textContent = right ? "ถูกต้อง ✓" : "ยังไม่ใช่ ลองข้ออื่น";
          if (right) { solved(); reveal(); }
        }));
      } else {
        ans.innerHTML = `<div class="q-row">${hintBtn()}<button type="button" class="primary" data-show>เทียบเฉลย</button></div>`;
      }

      ans.querySelector("[data-hint]")?.addEventListener("click", (e) => {
        if (el.querySelector(".q-hint")) return;
        const h = document.createElement("div");
        h.className = "q-hint"; h.innerHTML = "<b>คำใบ้</b> " + p.hint;
        e.target.closest(".q-ans").after(h); window.renderMath && window.renderMath(h);
      });
      ans.querySelector("[data-show]")?.addEventListener("click", () => {
        reveal();
        if (p.type === "think" && !el.querySelector(".selfrate")) {
          const r = document.createElement("div");
          r.className = "q-row selfrate"; r.style.marginTop = "8px";
          r.innerHTML = `<span class="hint">ตอบได้แบบนี้ไหม</span><button type="button" data-ok>ได้</button><button type="button" data-no>ยังไม่ได้</button>`;
          r.querySelector("[data-ok]").addEventListener("click", () => { solved(); fb.className = "fb ok"; fb.textContent = "บันทึกว่าทำได้แล้ว"; });
          r.querySelector("[data-no]").addEventListener("click", () => { fb.className = "fb no"; fb.textContent = "กลับไปอ่านส่วนที่เกี่ยวข้องแล้วลองอีกรอบ"; });
          el.append(r);
        }
      });
      box.append(el);
    });
    window.renderMath && window.renderMath(box);
  }

  document.querySelectorAll(".quiz[data-quiz]").forEach(mount);
})();
