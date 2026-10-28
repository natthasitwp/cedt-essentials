---
name: notebook-exercises
description: Add self-checking exercises after each topic in Jupyter lesson notebooks. Each question gets a stub cell and a check() cell that compares the answer against a stored hash, so solutions never appear in the notebook. Use when asked to "add exercises", "make practice questions", or "add self-check questions" to a .ipynb.
---

# Notebook self-check exercises

Add a short **Exercise** section after each topic of a lesson notebook. Students
replace `None` with code, run a `check(...)` cell, and get ✅ or an
`AssertionError`. Answers are stored only as truncated SHA-256 hashes.

## Rules

- **Never change lesson cells.** Only insert new cells. Tag every inserted cell
  with `"tags": ["exercise"]` in its metadata so they can be found or stripped later.
- Write questions in the same language and tone as the notebook. Keep them short:
  2–4 questions per topic, numbered `q1, q2, …` across the whole notebook.
- Each answer must be a deterministic value: a number, string, bool, list,
  tuple, dict, set, `Series` or `DataFrame`. Fix `random_state`/seeds whenever
  the answer depends on randomness. Avoid answers that depend on wall-clock
  time, file paths, or library-version-specific output formatting.
- **Notebooks that run on data in the repo** (pandas, data prep, classic ML):
  questions may use the lesson's own variables (e.g. `df`, `X_train`, `model`).
  Compute the answers by actually executing the notebook.
- **Notebooks needing GPUs, API keys, or big model downloads** (deep learning,
  LLM/LangChain, OCR): make every exercise **self-contained** — small tensors,
  toy arrays, fake/stub LLM classes, hard-coded strings — so it runs on a laptop
  CPU without network access. Test the concept the lesson taught, not the model output.
- Skip notebooks that are activity templates or that cannot run at all; say which
  ones were skipped and why.
- Add a `<details><summary>Hint</summary> … </details>` block to questions that
  are not obvious.

## Cell layout

Insert near the top (after the lesson's import cell):

1. Markdown — how the exercises work:

```markdown
## ✏️ About the exercises in this notebook
After each topic there is a short **Exercise** section.
1. Run the checker cell below once. Run it after the imports and before any exercise.
2. For each question, replace `None` with your code, then run the `check(...)` cell under it.
3. A ✅ means you are correct. An `AssertionError` tells you what is still wrong.

The exercises use the variables the lesson has created by that point, so **run the lesson cells above an exercise first**.
Answers are stored as hashes, so they don't appear in this notebook. Floats are compared after rounding to 4 decimals.
```

2. Code — the checker (copy verbatim; only `_ANSWERS` changes per notebook):

```python
# ===== Answer checker: run this cell first (do not edit) =====
import hashlib
import numpy as np
import pandas as pd

def _norm(x):
    if x is None or x is pd.NA or x is pd.NaT:
        return 'nan'
    if isinstance(x, pd.DataFrame):
        return _norm({c: x[c].to_dict() for c in x.columns})
    if isinstance(x, pd.Series):
        return _norm(x.to_dict())
    if isinstance(x, (pd.Index, np.ndarray)):
        return _norm(x.tolist())
    if isinstance(x, dict):
        return '{' + ','.join(sorted(f'{_norm(k)}:{_norm(v)}' for k, v in x.items())) + '}'
    if isinstance(x, (set, frozenset)):
        return '{' + ','.join(sorted(_norm(v) for v in x)) + '}'
    if isinstance(x, (list, tuple)):
        return '[' + ','.join(_norm(v) for v in x) + ']'
    if isinstance(x, (bool, np.bool_)):
        return str(bool(x))
    if isinstance(x, (int, np.integer)):
        return str(int(x))
    if isinstance(x, (float, np.floating)):
        x = float(x)
        if np.isnan(x):
            return 'nan'
        r = round(x, 4)
        return str(int(r)) if r.is_integer() else f'{r:.4f}'
    if isinstance(x, pd.Timestamp):
        return x.isoformat()
    return str(x).strip()

_KINDS = {
    int: ((int, np.integer), 'an integer'),
    float: ((int, float, np.integer, np.floating), 'a number'),
    str: ((str,), 'a string'),
    list: ((list,), 'a list'),
    tuple: ((tuple,), 'a tuple'),
    pd.Series: ((pd.Series,), 'a pandas Series'),
    pd.DataFrame: ((pd.DataFrame,), 'a pandas DataFrame'),
}

def check(qid, value, kind=None, columns=None, transform=None):
    """Assert that `value` is the correct answer for question `qid`.
    Floats are compared after rounding to 4 decimal places."""
    assert value is not None, f'{qid}: no answer yet - replace None with your code'
    if kind is not None:
        types, name = _KINDS.get(kind, ((kind,), kind.__name__))
        assert isinstance(value, types), f'{qid}: expected {name}, got {type(value).__name__}'
    if columns is not None:
        assert list(value.columns) == list(columns), f'{qid}: expected columns {list(columns)}, got {list(value.columns)}'
    if transform is not None:
        value = transform(value)
    digest = hashlib.sha256(_norm(value).encode()).hexdigest()[:16]
    assert digest == _ANSWERS[qid], f'{qid}: not correct yet - try again (open the hint if you are stuck)'
    print(f'✅ {qid} correct!')

_ANSWERS = {
    "q1": "<hash>",
    "q2": "<hash>",
}
```

For self-contained notebooks that don't otherwise import pandas, keep the
checker as is (pandas/numpy are assumed installed).

3. After each topic, one exercise block:

````markdown
### ✏️ Exercise: <topic name>
````

then per question, three cells:

```markdown
**Q1.** What is the **median** `Price`?

<details><summary>Hint</summary>

Use `.median()` on the column.

</details>
```

```python
# YOUR CODE HERE
q1 = None
```

```python
check('q1', q1, float)
```

`check` options:
- `kind`: `int`, `float`, `str`, `list`, `tuple`, `pd.Series`, `pd.DataFrame`, or any type.
- `columns=[...]`: require exact DataFrame columns in order.
- `transform=fn`: normalise before hashing when many forms are correct, e.g.
  `transform=sorted` for "any order", `transform=lambda s: s.lower()` for case,
  `transform=lambda df: df.reset_index(drop=True)` when the index doesn't matter.
  The same transform must be applied when computing the stored hash.

## Workflow

1. **Read the notebook** and list its topics (usually its `##` headings). Decide
   whether it can run as-is or needs self-contained exercises.
2. **Draft questions with solutions** in a scratch file (not the notebook):
   `qid`, question text, hint, solution code, `kind`, optional `transform`, and
   the index of the lesson cell after which the block goes.
3. **Compute the answers by execution.** Build a temporary copy of the notebook
   with the checker cell and the *solution* code in each stub, then execute it
   (`jupyter nbconvert --to notebook --execute --ExecutePreprocessor.timeout=600`
   or `nbclient`). In the solution copy, temporarily make the hash available by
   adding, right after each solution, a cell like:
   ```python
   print('HASH', 'q1', hashlib.sha256(_norm(TRANSFORM(q1)).encode()).hexdigest()[:16])
   ```
   Collect the printed hashes into `_ANSWERS`. Never hand-compute a hash.
4. **Write the real notebook** with Python + `json` (or `nbformat`): insert the
   intro, checker (with real `_ANSWERS`) and exercise cells, all tagged
   `exercise`, with stubs set to `qN = None`. Do not touch existing cells,
   outputs, or metadata. Clear outputs of the inserted cells.
5. **Verify** both ways:
   - Solution copy: every `check` prints ✅.
   - Student copy (stubs = `None`): the checker cell runs, and each `check`
     raises `AssertionError: qN: no answer yet` — nothing else errors.
   Delete the temporary copies afterwards.
6. **Report** per notebook: number of questions, which were self-contained,
   anything skipped. Then confirm with `git diff --stat` that only the intended
   notebooks changed.

## Removing exercises later

```python
import json, sys
p = sys.argv[1]
nb = json.load(open(p))
nb['cells'] = [c for c in nb['cells'] if 'exercise' not in c.get('metadata', {}).get('tags', [])]
json.dump(nb, open(p, 'w'), indent=1, ensure_ascii=False)
```
