# CEDT Essentials

Agent skills that help university students learn faster and keep learning on their own.
They work in Claude Code, Cursor, Codex and other agents that support `SKILL.md`.

## Why this exists

These skills started in [CEDT](https://www.cp.eng.chula.ac.th/cedt) (Computer Engineering
and Digital Technology) at Chulalongkorn University. The program packs 124 credits into
three and a half years: a summer internship after each of years 1–3, a two-semester capstone
project from year 3, and a co-op semester in year 4. It also expects graduates to be able to
learn on their own for the rest of their careers.

That combination leaves students with four problems, and the same is true in most Thai
engineering programs:

- **Too little time.** Between classes, internships and projects there are few hours left
  for anything outside the syllabus, and they come in small pieces.
- **Self-learning is expected but not taught.** Nobody shows you how to keep studying a
  subject for months without a teacher, deadlines or grades.
- **Industry moves faster than courses.** Fields like AI and LLM serving change every few
  months; a curriculum cannot keep up, so students fill the gap themselves.
- **Lectures are long.** Catching up from two-hour recordings and dense slides before an
  exam is slow.

Each skill below takes one of these problems and turns an AI agent into a study partner
that follows sound teaching practice instead of just giving answers.

## Skills

| Skill | Use it when | What you get |
|---|---|---|
| [semester](skills/semester/SKILL.md) | You want to learn a subject outside the curriculum seriously, over months | A university-style course from a goal or public roadmap: a dated weekly syllabus with Sunday deadlines, a course page that tracks your submissions and grades you with Claude-written exams, a handbook that stays two weeks ahead, and autograded coding exercises |
| [cram](skills/cram/SKILL.md) | You need to learn a lecture or a course quickly from your own class materials | Short lessons built from your slides, notes and lecture transcripts: real slide images, buttons that jump to the right minute of the recording, self-check questions and a one-page cheat sheet |
| [notebook-exercises](skills/notebook-exercises/SKILL.md) | Your class teaches with Jupyter notebooks and you want practice | Self-checking exercises after each topic of a lesson notebook, with answers stored as hashes so solutions stay hidden |

`semester` and `cram` share one look: a paper-notebook theme with Thai and English fonts that
is comfortable to read for a long time. Pages are light by default; dark mode is opt-in.

## Install

```bash
# all skills
npx skills add natthasitwp/cedt-essentials

# one skill
npx skills add natthasitwp/cedt-essentials --skill cram
```

Or copy a folder from `skills/` into `~/.claude/skills/` by hand.

## Usage

In Claude Code, type the skill name as a slash command, or just ask.

**semester**: run it in an empty folder.

> /semester Teach me inference engineering as a semester-long course, following this roadmap: https://...

**cram**: point it at your class files.

> /cram Make quick lessons from `materials/L03.pdf` and the lecture transcript `materials/L03.vtt`. The midterm is next Friday.

**notebook-exercises**:

> Add self-checking exercises after each topic in the notebooks under `code/Week03_ML/`.

## Credits

The teaching approach in `semester` (mission, zone of proximal development, retrieval
practice, learning records) is adapted from Matt Pocock's
[`teach`](https://github.com/mattpocock/skills) skill.

## Checks

Every push runs [gitleaks](https://github.com/gitleaks/gitleaks) for secrets and
`scripts/check_skills.py` for personal info (emails, home paths, Thai ID and phone numbers,
real answer hashes) and valid `SKILL.md` frontmatter. Run it locally before pushing:

```bash
python scripts/check_skills.py
```
