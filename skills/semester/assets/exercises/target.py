"""Load the module under test: impl.py normally, a hidden buggy copy when the grader sets IMPL.

Learner tests import from here:  from target import <function names>
"""
import importlib.util
import os
from pathlib import Path

_path = Path(os.environ.get("IMPL", Path(__file__).with_name("impl.py")))
_spec = importlib.util.spec_from_file_location("impl_under_test", _path)
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)
globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("_")})
