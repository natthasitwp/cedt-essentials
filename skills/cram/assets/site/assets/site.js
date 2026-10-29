/* site.js: shared page behaviour.
   - wraps <pre><code data-lang="..."> in a box with a language tag and a copy button
   - renders \( … \), \[ … \] and $$ … $$ math when KaTeX is loaded on the page
   - marks finished lessons on the index (<li data-lesson="01">) from localStorage */
(function () {
  document.querySelectorAll("pre > code").forEach((code) => {
    const pre = code.parentElement, wrap = document.createElement("div");
    wrap.className = "code";
    pre.replaceWith(wrap);
    wrap.append(pre);
    if (code.dataset.lang) {
      const l = document.createElement("span");
      l.className = "lang"; l.textContent = code.dataset.lang; wrap.prepend(l);
    }
    const b = document.createElement("button");
    b.type = "button"; b.textContent = "คัดลอก";
    b.addEventListener("click", () => {
      const done = () => { b.textContent = "คัดลอกแล้ว"; setTimeout(() => (b.textContent = "คัดลอก"), 1500); };
      (navigator.clipboard ? navigator.clipboard.writeText(code.textContent) : Promise.reject()).then(done, () => {
        const r = document.createRange(); r.selectNodeContents(code);
        const s = getSelection(); s.removeAllRanges(); s.addRange(r); b.textContent = "เลือกข้อความแล้ว";
      });
    });
    wrap.append(b);
  });

  window.renderMath = (el) => {
    if (window.renderMathInElement) {
      renderMathInElement(el || document.body, {
        delimiters: [{ left: "$$", right: "$$", display: true }, { left: "\\[", right: "\\]", display: true }, { left: "\\(", right: "\\)", display: false }],
        throwOnError: false,
      });
    }
  };
  addEventListener("load", () => window.renderMath());

  const site = document.body.dataset.site || "cram";
  document.querySelectorAll("[data-lesson-status]").forEach((el) => {
    let done = [];
    try { done = JSON.parse(localStorage.getItem(`${site}-done-${el.dataset.lessonStatus}`)) || []; } catch {}
    const total = +el.dataset.total || 0;
    if (total && done.length >= total) { el.textContent = "ทำครบแล้ว ✓"; el.classList.add("done"); }
    else if (done.length) el.textContent = `ทำแล้ว ${done.length}/${total || "?"}`;
  });
})();
