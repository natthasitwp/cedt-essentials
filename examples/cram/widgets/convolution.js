/* convolution: drag t to slide h(t−τ) across x(τ); the overlap is shaded and y(t) is drawn
   up to the current t.

   Config
     x, h      signals by name (see kit.signal): "rect(0,1)", "exp(1)", "tri(0,2)", "2*step(0)" …
     range     [τ from, τ to] shown on both plots
     t         starting value of t
     preview   true draws the rest of y(t) faintly ahead of t

   @example {"x": "rect(0,1)", "h": "rect(0,1)", "range": [-2, 4], "t": 0.5}
*/
CramWidgets.register("convolution", {
  defaults: { x: "rect(0,1)", h: "rect(0,1)", range: [-2, 4], t: 0.5, preview: false },
  mount(el, cfg, kit) {
    const x = kit.signal(cfg.x), h = kit.signal(cfg.h);
    const [a, b] = cfg.range;
    const conv = (t, n = 1000) => kit.integrate((tau) => x(tau) * h(t - tau), a, b, n);

    const N = 240, ts = Array.from({ length: N + 1 }, (_, i) => a + ((b - a) * i) / N);
    const ys = ts.map((t) => conv(t));
    const peak = (f) => Math.max(1, ...ts.map((t) => Math.abs(f(t))));
    const top = Math.max(peak(x), peak(h)) * 1.15, yTop = Math.max(...ys.map(Math.abs), 0.1) * 1.2;

    kit.el("div", { class: "legend", html:
      `<span><i style="background:${kit.css("blue")}"></i>\\(x(\\tau)\\)</span>` +
      `<span><i style="background:${kit.css("brown")}"></i>\\(h(t-\\tau)\\)</span>` +
      `<span><i style="background:${kit.css("sage-ink")};opacity:.5"></i>\\(x(\\tau)\\,h(t-\\tau)\\) พื้นที่ = \\(y(t)\\)</span>` }, el);
    const p1 = kit.plot(el, { x: [a, b], y: [-0.15 * top, top], height: 200, label: "x(τ) and h(t−τ)" });
    const p2 = kit.plot(el, { x: [a, b], y: [-0.15 * yTop, yTop], height: 160, label: "y(t)" });
    const out = kit.el("div", { class: "readout" }, el);

    function draw(t) {
      p1.clear().axes({ xlabel: "τ" })
        .curve((tau) => x(tau) * h(t - tau), { color: "sage-ink", width: 0, fill: true, n: 600 })
        .curve(x, { color: "blue", n: 600 })
        .curve((tau) => h(t - tau), { color: "brown", dash: "6 4", n: 600 })
        .vline(t);
      p2.clear().axes({ xlabel: "t", ylabel: "y(t)" });
      if (cfg.preview) p2.curve(ts.map((s, i) => [s, ys[i]]), { color: "muted", dash: "3 4", width: 1.5 });
      const upto = ts.map((s, i) => [s, ys[i]]).filter(([s]) => s <= t);
      const yt = conv(t, 12000);
      if (upto.length) p2.curve(upto.concat([[t, yt]]), { color: "sage-ink", width: 2.5 });
      p2.vline(t).dot(t, yt);
      out.innerHTML = `\\(t = ${t.toFixed(2)}\\) &nbsp;·&nbsp; \\(y(t) = \\int x(\\tau)\\,h(t-\\tau)\\,d\\tau = ${yt.toFixed(3)}\\)`;
      kit.renderMath(out);
    }

    const s = kit.slider(el, { min: a, max: b, step: 0.01, value: cfg.t, label: "เลื่อน \\(t\\)" }, draw);
    kit.drag(p1, (t) => { t = Math.min(b, Math.max(a, t)); s.set(t); draw(t); });
    draw(cfg.t);
  },
});
