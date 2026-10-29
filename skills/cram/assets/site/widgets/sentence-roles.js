/* sentence-roles: the learner decides whether the relative word is the subject or the object
   of its clause, then sees why and whether it can be left out.

   Config
     sentence    the whole sentence
     clause      the adjective clause inside it (underlined)
     connector   the relative word to judge (who / whom / which / that)
     role        "subject" or "object"
     reduced     optional: the sentence with the connector left out (object only)

   @example {"sentence": "The course that you took was hard.", "clause": "that you took", "connector": "that", "role": "object", "reduced": "The course you took was hard."}
*/
CramWidgets.register("sentence-roles", {
  defaults: { role: "object" },
  mount(el, cfg, kit) {
    const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c]);
    const i = cfg.sentence.indexOf(cfg.clause);
    if (i < 0) throw new Error("clause is not part of sentence");
    const j = cfg.clause.indexOf(cfg.connector);
    if (j < 0) throw new Error("connector is not part of clause");
    const pre = cfg.sentence.slice(0, i), post = cfg.sentence.slice(i + cfg.clause.length);
    const c0 = cfg.clause.slice(0, j), c1 = cfg.clause.slice(j + cfg.connector.length);
    const box = kit.el("p", { class: "sr-sentence", html:
      `${esc(pre)}<span class="sr-clause">${esc(c0)}<b class="sr-conn">${esc(cfg.connector)}</b>${esc(c1)}</span>${esc(post)}` }, el);
    box.style.fontSize = "1.15rem";
    box.querySelector(".sr-clause").style.cssText = `text-decoration: underline 2px ${kit.css("blue")}; text-underline-offset: 5px`;
    box.querySelector(".sr-conn").style.color = kit.css("brown");

    kit.el("p", { html: `ใน clause ที่ขีดเส้นใต้ คำว่า <b>${esc(cfg.connector)}</b> เป็นอะไร?` }, el);
    const row = kit.el("div", { class: "q-row" }, el);
    const fb = kit.el("div", { class: "readout" }, el);
    const rest = c1.trim();
    const why = cfg.role === "object"
      ? `หลัง <b>${esc(cfg.connector)}</b> มีประธาน (<i>${esc(rest.split(" ")[0])}</i>) อยู่แล้ว ${esc(cfg.connector)} จึงเป็น<b>กรรม</b> ละได้` +
        (cfg.reduced ? `<br>→ <b>${esc(cfg.reduced)}</b>` : "")
      : `หลัง <b>${esc(cfg.connector)}</b> เป็นกริยาเลย (<i>${esc(rest.split(" ")[0])}</i>) ${esc(cfg.connector)} จึงเป็น<b>ประธาน</b> ละไม่ได้`;
    for (const [role, label] of [["subject", "ประธาน"], ["object", "กรรม"]]) {
      const b = kit.el("button", { type: "button", text: label }, row);
      b.addEventListener("click", () => {
        const ok = role === cfg.role;
        fb.style.color = kit.css(ok ? "ok" : "bad");
        fb.innerHTML = (ok ? "ถูกต้อง ✓ " : "ยังไม่ใช่ ") + `<span style="color:${kit.css("ink")}">${why}</span>`;
      });
    }
  },
});
