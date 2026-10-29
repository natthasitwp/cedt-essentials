# Theme: lesson notebook with a sketched route map

The course page and the handbook share one look. The templates already contain it; use
these tokens for anything new.

## Look

- **Page:** warm paper with a faint 28px grid, a thin brown frame around the viewport, one
  reading column about 44–46rem wide. Comfortable reading: 17px body, line-height 1.8.
- **Headings:** the `h1` sits on a sage block. `h2` is uppercase with a thin rule under it
  and a blue hand-written number for lesson sections.
- **Route map:** stage labels on a slightly rotated blue tag; step cards with uneven
  "hand-drawn" corners, a blue numbered circle, and red hand-written arrows between them.
  Card fill shows status: blue-soft dashed = this week, sage = passed, brown-soft = overdue.
- **Components:** `goal` (sage left rule), `def` (slate band with a label), `note`
  (slate-soft), `warn` (brown), `link-infer` (blue, labelled with the mission),
  `predict` (dashed box), `exercise` (sketch-border card), `paper-ref`, `pill` statuses,
  `chip` tags, code blocks on `--code-bg` with a copy button.

## Tokens (light / dark)

| token | light | dark | use |
|---|---|---|---|
| `--paper` | `#F4F3EF` | `#1A1917` | page |
| `--card` | `#FBFAF7` | `#211F1C` | boxes |
| `--ink` | `#45403C` | `#E6E0D8` | text |
| `--ink-soft` / `--muted` | `#6C6661` / `#9A948D` | `#B9B1A8` / `#8C857D` | secondary text |
| `--rule` | `#DCD8D0` | `#3A3631` | borders |
| `--sage` / `--sage-ink` | `#D4E2D0` / `#4F7A4A` | `#2E3B2B` / `#9CC394` | h1, goals, passed |
| `--slate` / `--slate-soft` | `#4E7184` / `#E2EAEE` | `#93B6C9` / `#233039` | links, definitions |
| `--brown` / `--brown-soft` | `#7A3D1C` / `#F1E6DF` | `#A8603A` / `#3A2A20` | frame, warnings, late |
| `--blue` / `--blue-soft` | `#1668B8` / `#E3EEF9` | `#74AAF0` / `#1D2A3B` | map, current week, mission box |
| `--arrow` | `#C8402F` | `#E07A68` | map arrows |

Every token is defined on bare `:root`, redefined under
`@media (prefers-color-scheme: dark) { :root:not([data-theme="light"]) {...} }` and again
under `:root[data-theme="dark"]`. `body` always sets its own background.

## Type

- Body: **Jost** with **IBM Plex Sans Thai** for Thai glyphs.
- Hand-written accents (map cards, numbers, tags, pills): **Mali**, which covers Thai.
- Data and code: **IBM Plex Mono** with tabular numbers.

All four come from Google Fonts with system fallbacks. Use the hand face sparingly: labels
and numbers, never paragraphs.

## Rules

- Keep the 16px side gutter at phone width with the `max(16px, env(safe-area-inset-*))`
  padding, and no horizontal page scroll (tables and code scroll in their own box).
- Respect `prefers-reduced-motion`. No print buttons (the artifact viewer blocks them).
- If the user asks for a different palette, change the tokens in both templates together.
