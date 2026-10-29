"""Encode buggy copies of impl.py for the mutation grader.

Edit MUTATIONS (each is an exact (old, new) replacement in impl.py), then run:
    python make_mutants.py path/to/impl.py
and paste the printed string into BLOB in test_grader.py.
Mutants are encoded only so learners don't read them by accident.
"""
import base64
import sys
import zlib

MUTATIONS = {
    "m1": ("s = sorted(values)", "s = list(values)"),          # forgot to sort
    "m2": ("/ (latency_ms / 1000)", "/ latency_ms"),            # ms vs s
}


def main() -> None:
    src = open(sys.argv[1]).read()
    mutants = {}
    for name, (old, new) in MUTATIONS.items():
        assert src.count(old) == 1, f"{name}: '{old}' must appear exactly once"
        mutants[name] = src.replace(old, new)
    print(base64.b64encode(zlib.compress(repr(mutants).encode())).decode())


if __name__ == "__main__":
    main()
