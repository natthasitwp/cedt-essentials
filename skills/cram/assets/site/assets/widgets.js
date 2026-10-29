/* widgets.js: interactive figures inside lessons.

   A lesson asks for one with   ::widget convolution {"x": "rect(0,1)", "h": "exp(1)"}
   build.py turns that into     <div class="widget" data-widget="convolution" data-config="{…}">
   and loads this file plus widgets/convolution.js, which registers itself:

     CramWidgets.register("convolution", {
       defaults: { … },                 // merged under the lesson's config
       mount(el, cfg, kit) { … },       // draw into el; kit has the helpers below
     });

   Classic scripts, not ES modules, so pages still open straight from disk (file://).
   See WIDGETS.md for the full contract. */
(function () {
  const defs = {};
  const NS = "http://www.w3.org/2000/svg";

  const css = (name) => getComputedStyle(document.documentElement).getPropertyValue("--" + name).trim();
  const el = (tag, attrs = {}, parent) => {
    const n = tag.startsWith("svg:") ? document.createElementNS(NS, tag.slice(4)) : document.createElement(tag);
    for (const [k, v] of Object.entries(attrs)) {
      if (k === "text") n.textContent = v;
      else if (k === "html") n.innerHTML = v;
      else n.setAttribute(k, v);
    }
    if (parent) parent.append(n);
    return n;
  };

  /* Signals by name: "rect(a,b)", "tri(a,b)", "step(a)", "exp(a)", "ramp(a)", "sin(f)", "cos(f)",
     "sinc(a)", "delta(a)" (narrow pulse) with numeric arguments only; prefix "k*" scales,
     e.g. "2*rect(0,1)". No eval: lesson config can never run code. */
  const SIG = {
    rect: (a = 0, b = 1) => (t) => (t >= a && t < b ? 1 : 0),
    tri: (a = 0, b = 2) => (t) => { const m = (a + b) / 2, w = (b - a) / 2; return Math.max(0, 1 - Math.abs(t - m) / w); },
    step: (a = 0) => (t) => (t >= a ? 1 : 0),
    exp: (a = 1, s = 0) => (t) => (t >= s ? Math.exp(-a * (t - s)) : 0),
    ramp: (a = 0) => (t) => (t >= a ? t - a : 0),
    sin: (f = 1) => (t) => Math.sin(2 * Math.PI * f * t),
    cos: (f = 1) => (t) => Math.cos(2 * Math.PI * f * t),
    sinc: (a = 1) => (t) => (t === 0 ? 1 : Math.sin(Math.PI * a * t) / (Math.PI * a * t)),
    delta: (a = 0, w = 0.05) => (t) => (Math.abs(t - a) < w / 2 ? 1 / w : 0),
  };
  function signal(spec) {
    const m = String(spec).replace(/\s+/g, "").match(/^(-?[\d.]+\*)?([a-z]+)(?:\(([-\d.,]*)\))?$/);
    if (!m || !SIG[m[2]]) throw new Error(`unknown signal "${spec}" (use ${Object.keys(SIG).join(", ")})`);
    const k = m[1] ? parseFloat(m[1]) : 1;
    const args = m[3] ? m[3].split(",").filter(Boolean).map(Number) : [];
    const f = SIG[m[2]](...args);
    return (t) => k * f(t);
  }

  /* A responsive SVG plot in data coordinates. */
  function plot(parent, o = {}) {
    const W = o.width || 640, H = o.height || 220, P = { l: 36, r: 12, t: 12, b: 26 };
    let [x0, x1] = o.x || [-1, 1], [y0, y1] = o.y || [-0.2, 1.2];
    const svg = el("svg:svg", { viewBox: `0 0 ${W} ${H}`, class: "kit-plot", role: "img", "aria-label": o.label || "" }, parent);
    const X = (x) => P.l + ((x - x0) / (x1 - x0)) * (W - P.l - P.r);
    const Y = (y) => H - P.b - ((y - y0) / (y1 - y0)) * (H - P.t - P.b);
    const toX = (px) => x0 + ((px - P.l) / (W - P.l - P.r)) * (x1 - x0);
    const layer = el("svg:g", {}, svg);
    const api = {
      svg, X, Y, toX, layer,
      clear() { layer.replaceChildren(); return api; },
      axes({ xlabel = "", ylabel = "", ticks = true } = {}) {
        const g = el("svg:g", { class: "kit-axes" }, layer);
        el("svg:line", { x1: P.l, x2: W - P.r, y1: Y(0), y2: Y(0) }, g);
        el("svg:line", { x1: X(0), x2: X(0), y1: P.t, y2: H - P.b }, g);
        if (ticks) for (let v = Math.ceil(x0); v <= x1; v++) {
          el("svg:line", { x1: X(v), x2: X(v), y1: Y(0) - 3, y2: Y(0) + 3 }, g);
          el("svg:text", { x: X(v), y: Math.min(H - 6, Y(0) + 16), "text-anchor": "middle", text: v }, g);
        }
        if (xlabel) el("svg:text", { x: W - P.r, y: Y(0) - 6, "text-anchor": "end", class: "kit-label", text: xlabel }, g);
        if (ylabel) el("svg:text", { x: X(0) + 6, y: P.t + 10, class: "kit-label", text: ylabel }, g);
        return api;
      },
      /* f: function of x, or [[x,y],…]. opts: color (token name), width, dash, fill (shade to y=0), n */
      curve(f, { color = "ink", width = 2, dash = "", fill = false, n = 400, from = x0, to = x1 } = {}) {
        const pts = Array.isArray(f) ? f : Array.from({ length: n + 1 }, (_, i) => { const x = from + ((to - from) * i) / n; return [x, f(x)]; });
        const d = pts.map(([x, y], i) => `${i ? "L" : "M"}${X(x).toFixed(1)},${Y(y).toFixed(1)}`).join("");
        if (fill && pts.length) {
          const a = `${d}L${X(pts[pts.length - 1][0]).toFixed(1)},${Y(0)}L${X(pts[0][0]).toFixed(1)},${Y(0)}Z`;
          el("svg:path", { d: a, fill: css(color), "fill-opacity": 0.28, stroke: "none" }, layer);
        }
        el("svg:path", { d, fill: "none", stroke: css(color), "stroke-width": width, "stroke-dasharray": dash, "stroke-linejoin": "round" }, layer);
        return api;
      },
      vline(x, { color = "brown", dash = "4 4" } = {}) {
        el("svg:line", { x1: X(x), x2: X(x), y1: P.t, y2: H - P.b, stroke: css(color), "stroke-dasharray": dash }, layer);
        return api;
      },
      dot(x, y, { color = "brown", r = 5 } = {}) {
        el("svg:circle", { cx: X(x), cy: Y(y), r, fill: css(color) }, layer);
        return api;
      },
      text(x, y, s, { color = "ink-soft", anchor = "start" } = {}) {
        el("svg:text", { x: X(x), y: Y(y), fill: css(color), "text-anchor": anchor, class: "kit-label", text: s }, layer);
        return api;
      },
      range(x, y) { if (x) [x0, x1] = x; if (y) [y0, y1] = y; return api; },
    };
    return api;
  }

  /* Drag across a plot (mouse, pen or finger); calls onMove(x in data units). */
  function drag(p, onMove) {
    const svg = p.svg;
    svg.style.touchAction = "none";
    svg.style.cursor = "ew-resize";
    const at = (e) => {
      const r = svg.getBoundingClientRect(), vb = svg.viewBox.baseVal;
      onMove(p.toX(((e.clientX - r.left) / r.width) * vb.width));
    };
    svg.addEventListener("pointerdown", (e) => { svg.setPointerCapture(e.pointerId); at(e); });
    svg.addEventListener("pointermove", (e) => { if (svg.hasPointerCapture(e.pointerId)) at(e); });
  }

  function slider(parent, { min = 0, max = 1, step = 0.01, value = 0, label = "" } = {}, onInput) {
    const wrap = el("label", { class: "kit-slider" }, parent);
    if (label) el("span", { html: label }, wrap);
    const input = el("input", { type: "range", min, max, step, value }, wrap);
    const out = el("output", { text: (+value).toFixed(2) }, wrap);
    input.addEventListener("input", () => { out.textContent = (+input.value).toFixed(2); onInput(+input.value); });
    return { input, set(v) { input.value = v; out.textContent = (+v).toFixed(2); } };
  }

  /* Midpoint rule. Error is at most about (b-a)/n times the jump at a discontinuity, so
     use a large n (4000+) for a value you print and a smaller one for curves you draw. */
  function integrate(f, a, b, n = 2000) {
    if (b <= a) return 0;
    const h = (b - a) / n;
    let s = 0;
    for (let i = 0; i < n; i++) s += f(a + (i + 0.5) * h);
    return s * h;
  }

  const kit = { css, el, plot, drag, slider, signal, integrate,
    renderMath: (node) => window.renderMath && window.renderMath(node) };

  function mount(node) {
    const name = node.dataset.widget, def = defs[name];
    if (!def) { node.textContent = `ไม่พบ widget “${name}”`; return; }
    if (node.dataset.mounted) return;
    node.dataset.mounted = "1";
    let cfg = {};
    try { cfg = JSON.parse(node.dataset.config || "{}"); } catch { /* build.py already checked */ }
    node.replaceChildren();
    try { def.mount(node, Object.assign({}, def.defaults || {}, cfg), kit); }
    catch (e) { node.textContent = `widget “${name}” error: ${e.message}`; console.error(e); }
    kit.renderMath(node);
  }

  window.CramWidgets = {
    register(name, def) {
      defs[name] = def;
      if (document.readyState !== "loading") document.querySelectorAll(`.widget[data-widget="${name}"]`).forEach(mount);
    },
    kit,
  };
  document.addEventListener("DOMContentLoaded", () =>
    document.querySelectorAll(".widget[data-widget]").forEach((n) => defs[n.dataset.widget] && mount(n)));
  /* KaTeX loads with defer too: re-render widget labels once it is there. */
  addEventListener("load", () => document.querySelectorAll(".widget").forEach((n) => kit.renderMath(n)));
})();
