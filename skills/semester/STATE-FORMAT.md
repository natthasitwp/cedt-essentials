# Learner state files

Adapted from the formats in Matt Pocock's `teach` skill (https://github.com/mattpocock/skills).

## MISSION.md

```md
# Mission: {topic}

## Why
{1–3 sentences: the concrete outcome. "Ship X", "get a job doing Y", "start a company that Z".}

## Success looks like
- {observable things the user will be able to do}

## Constraints
- {hours per week, term dates, exam months, hardware, budget, language}

## Out of scope
- {adjacent topics deliberately left out}
```

One mission per workspace. Keep it to one screen. Confirm with the user before changing it,
and write a learning record when it changes.

## RESOURCES.md

Two groups, every entry with one line on what it is for:

```md
## Knowledge
- [Book or paper or docs](https://...) What it covers. Use for: ...

## Wisdom (communities)
- [Meetup, forum or server](https://...) Why it is worth joining.

## Gaps
- {topics the mission needs that have no good source yet}
```

High-trust sources only: primary sources, recognised experts, official docs. Prune what
turns out shallow or wrong. Note it here if the user does not want to join communities.

## GLOSSARY.md

`**Term**:` then a one or two sentence definition, then `_Avoid_:` with synonyms the course
does not use. Add a term only after the user has used it correctly. Lessons and exams
follow the glossary's wording.

## NOTES.md

Short bullets of the user's stated preferences: language, pace, what to skip, how they like
feedback. Read it before writing any lesson.

## learning-records/NNNN-slug.md

```md
# {What is now known}

{1–3 sentences: what the user showed they understand (or stated they already know, or a
misconception that got corrected), and what that changes about what to teach next.}

Evidence: {exam W05 attempt 2: 90%, short answers on KV cache sizing correct}
```

Write one only with evidence: a passed exam on a hard topic, feedback that exposed a
misconception, stated prior knowledge, or a mission change. Not for material that was
merely covered. When understanding changes, mark the old record
`Status: superseded by NNNN` instead of deleting it.
