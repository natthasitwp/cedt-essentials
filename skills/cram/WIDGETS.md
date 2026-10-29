# Widgets

Interactive figures inside a lesson: drag a signal, move a slider, click a word. A lesson
asks for one by name with a JSON config; the code lives in one `.js` file and is reused by
every lesson that needs it.

```markdown
::widget convolution {"x": "rect(0,1)", "h": "exp(1)", "range": [-2, 5], "t": 0.5}
```

## Which widgets exist

The skill ships these in `assets/site/widgets/`. Open `site/widgets.html` after a build to
see every widget with its example config.

| Widget | For | Config |
|---|---|---|
| `convolution` | continuous-time convolution: drag \(t\), overlap shaded, \(y(t)\) drawn | `x`, `h` (signals), `range`, `t`, `preview` |
| `sentence-roles` | is the relative word the subject or object of its clause? | `sentence`, `clause`, `connector`, `role`, `reduced` |

Reuse one before writing a new one: a different config usually covers the next lesson.

## Writing a new widget

When no widget fits, write one file in the workspace: `widgets/<name>.js` (not in `site/`).
The build copies it into the site and it wins over a skill widget of the same name.

```js
/* <name>: one line saying what the learner does with it.

   Config
     key     what it means

   @example {"key": "value"}
*/
CramWidgets.register("<name>", {
  defaults: { key: "value" },
  mount(el, cfg, kit) {
    // draw into el; cfg = defaults + the lesson's JSON
  },
});
```

The `@example` line is required: `site/widgets.html` uses it to show the widget.

### Rules

- **Classic script, no `import`/`export`.** Pages must open straight from disk (`file://`),
  where ES modules do not load.
- **No libraries** unless the figure truly needs one; then load it from a CDN with an exact
  version and say in the lesson that it needs internet.
- **Config is data.** Never `eval` or `new Function` a string from the config. For signals
  use `kit.signal("rect(0,1)")`, which only accepts known names and numbers.
- **Theme colours only:** `kit.css("blue")` etc. (tokens: `ink`, `ink-soft`, `muted`, `rule`,
  `paper`, `card`, `blue`, `brown`, `slate`, `sage-ink`, `ok`, `bad`). Never hard-code colours,
  so light and dark both work.
- **Touch and mouse:** use `kit.drag` / `kit.slider` (pointer events). Keep text at least 14px.
- **Math labels:** write `\\( … \\)` in strings and call `kit.renderMath(node)` after
  changing them.
- **About 50–120 lines.** If it grows past that, split it into two widgets.

### kit

| Helper | What it does |
|---|---|
| `kit.plot(parent, {x:[a,b], y:[c,d], height, label})` | responsive SVG in data units; returns `p` |
| `p.axes({xlabel, ylabel})`, `p.curve(f or points, {color, dash, fill, width})`, `p.vline(x)`, `p.dot(x,y)`, `p.text(x,y,s)`, `p.clear()`, `p.range([a,b],[c,d])` | drawing; all chainable |
| `kit.drag(p, x => …)` | drag across a plot; gives x in data units |
| `kit.slider(parent, {min,max,step,value,label}, v => …)` | labelled slider; returns `{input, set(v)}` |
| `kit.signal("2*rect(0,1)")` | function of t: `rect(a,b)`, `tri(a,b)`, `step(a)`, `exp(a[,start])`, `ramp(a)`, `sin(f)`, `cos(f)`, `sinc(a)`, `delta(a[,w])` |
| `kit.integrate(f, a, b, n)` | midpoint rule; use n ≥ 4000 for a value you print |
| `kit.el(tag, attrs, parent)` | create an element (`"svg:path"` for SVG); `text`/`html` attrs set content |
| `kit.css(token)`, `kit.renderMath(node)` | theme colour; render LaTeX inside node |

### Check before using it

1. `python3 <skill>/scripts/build.py`, then look at `site/widgets.html` in the browser:
   the widget draws, has no console errors, and works with a drag or tap at phone width.
2. **Check the numbers.** Compare at least one value the widget shows with one you compute
   separately (a short Python run), e.g. `rect(0,1) * rect(0,1)` at \(t=1.5\) must be 0.5.
   A figure that teaches the wrong number is worse than no figure.
3. A widget that is useful beyond this course can be offered to the skill: tell the user it
   could go into `cedt-essentials` as a pull request.
