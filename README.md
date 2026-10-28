# CEDT Essentials

Agent skills for Claude Code, Cursor, Codex and other agents that support `SKILL.md`.

## Install

```bash
# all skills
npx skills add natthasitwp/cedt-essentials

# one skill
npx skills add natthasitwp/cedt-essentials --skill notebook-exercises
```

Or copy a folder from `skills/` into `~/.claude/skills/` by hand.

## Skills

| Skill | What it does |
|---|---|
| [notebook-exercises](skills/notebook-exercises/SKILL.md) | Adds self-checking exercises after each topic in Jupyter lesson notebooks. Answers are stored as hashes, so solutions stay hidden. |

## Usage

In Claude Code, type `/notebook-exercises`, or ask:

> Add self-checking exercises after each topic in the notebooks under `code/Week03_ML/`.

## Checks

Every push runs [gitleaks](https://github.com/gitleaks/gitleaks) for secrets and `scripts/check_skills.py` for personal info (emails, home paths, Thai ID/phone numbers, real answer hashes) and valid `SKILL.md` frontmatter. Run it locally before pushing:

```bash
python scripts/check_skills.py
```
