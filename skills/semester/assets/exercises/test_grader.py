"""Mutation grader: the learner's test_mine.py must pass on impl.py and fail on every hidden mutant.

Copy next to a folder <ex>/ that holds impl.py, target.py and test_mine.py; set EX_DIR and BLOB.
"""
import ast
import base64
import os
import subprocess
import sys
import zlib
from pathlib import Path

import pytest

EX_DIR = Path(__file__).parent / "ex1_testing"
BLOB = "PASTE_OUTPUT_OF_make_mutants.py"
MUTANTS = ast.literal_eval(zlib.decompress(base64.b64decode(BLOB)).decode()) if BLOB.startswith("eJ") else {}


def run_tests(impl: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-m", "pytest", str(EX_DIR / "test_mine.py"), "-q", "-p", "no:cacheprovider", "-x"],
        cwd=EX_DIR, env={**os.environ, "IMPL": str(impl)}, capture_output=True, text=True,
    )


def test_passes_on_correct_code():
    r = run_tests(EX_DIR / "impl.py")
    assert r.returncode == 0, "test ของคุณต้องผ่านกับโค้ดที่ถูก แต่มีข้อที่พัง:\n" + r.stdout[-2000:]


@pytest.mark.parametrize("name", sorted(MUTANTS))
def test_catches_bug(name, tmp_path):
    impl = tmp_path / f"{name}.py"
    impl.write_text(MUTANTS[name])
    assert run_tests(impl).returncode == 1, f"บั๊ก {name} รอดไปได้: test ของคุณยังไม่ครอบคลุมพอ"
