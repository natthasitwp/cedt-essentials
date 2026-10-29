# Autograded exercises

The learner fills in stubs; pytest tells them when they are right. Reference solutions
exist only in your scratchpad.

## Layout

```
pyproject.toml           uv project: the libraries the course needs + pytest
                         [tool.pytest.ini_options] testpaths = ["exercises"], addopts = "--tb=short"
exercises/conftest.py    copy of assets/exercises/conftest.py (data_dir and no_loops fixtures)
exercises/w01/ex1_topic.py           stub the learner edits
exercises/w01/test_w01_ex1_topic.py  grader (learner must not edit)
data/                    synthetic data from tools/make_data.py with a fixed seed
```

Test file names must be unique across weeks (`test_w01_...`), because pytest imports them
by basename.

## Stubs

- A module docstring in the learner's language: the task, the data file, and the exact
  command to run its grader.
- Real signatures with type hints. Each body is `raise NotImplementedError`. The docstring
  is the full spec: inputs, outputs, ordering, rounding, edge cases, what to raise.
- Use small, realistic data from the learner's mission domain (log lines, benchmark
  tables, prices) rather than toy examples. Label invented numbers as synthetic.

## Graders

- Hard-code expected values, computed once by running your reference solution on the
  seeded data. Never compute the expected value with the same code you are testing.
- Test the edge cases from the docstring (empty input, unsorted input, units, bounds).
- For "no loops" tasks use the `no_loops` fixture. For "use SQL" or "use a window
  function", inspect the source. Every structural check must also fail while the stub
  still says `NotImplementedError`, so nothing is green before the learner starts.
- Shell exercises run with `subprocess` against temp files; use `file://` URLs instead of
  the network.
- To teach testing, use the mutation grader (`assets/exercises/target.py`,
  `make_mutants.py`, `test_grader.py`): the learner's tests must pass on `impl.py` and
  fail on each hidden, encoded mutant.
- A step's project gets a checker script (`check_project.py <repo>`) that prints a ✓/✗
  list the learner pastes into the course page.

## GPU weeks

Keep a CPU-runnable grader for the concept (shapes, arithmetic, small tensors, a stub
server) and put the GPU part in a Colab or Kaggle notebook whose measured numbers the
learner submits. Say what hardware each part needs.

## Verify before publishing

1. Run the graders on the stubs: everything fails or errors except tests that only
   exercise provided example code.
2. Copy `exercises/`, `data/` and `pyproject.toml` to a scratch folder, overlay your
   reference solutions, run pytest there: everything passes.
3. Write the real pass count ("K passed") into the lesson's submission checklist.
4. Delete `__pycache__`, `.pytest_cache` and `out/` from the workspace.
