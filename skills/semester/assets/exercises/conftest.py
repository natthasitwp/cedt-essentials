"""Shared helpers for the autograder."""
from __future__ import annotations

import ast
import inspect
import textwrap
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]

LOOP_NODES = (ast.For, ast.While, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp, ast.AsyncFor)


@pytest.fixture
def data_dir() -> Path:
    return ROOT / "data"


@pytest.fixture
def no_loops():
    """Fail if a function body contains a Python-level loop or comprehension."""
    def check(fn) -> None:
        src = textwrap.dedent(inspect.getsource(fn))
        assert "NotImplementedError" not in src, f"{fn.__name__} ยังไม่ได้เขียน"
        tree = ast.parse(src)
        loops = [type(n).__name__ for n in ast.walk(tree) if isinstance(n, LOOP_NODES)]
        assert not loops, f"{fn.__name__} ต้องไม่มี loop แต่เจอ {loops} ให้ใช้ vectorized operation แทน"
    return check
