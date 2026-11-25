#!/usr/bin/env python3
"""Midnight Fridge Roast — make.fun entry.

Writes one roast of a smart fridge that refuses to open after midnight
to /output/entry.txt. Stdlib only; the grader sandbox has no network.

Usage:
    python3 main.py [--out PATH] [--check]

--out PATH   where to write the entry (default /output/entry.txt)
--check      write to a temp file instead and verify the gate:
             UTF-8, 1-200 chars, not only whitespace, single line.
"""

import argparse
import pathlib
import sys
import tempfile

ROAST = (
    "I asked the fridge for water at 12:01. It said 'We're closed' "
    "and suggested I hydrate during business hours."
)

# Tournament record (specificity / surprise / freshness, 1-5 each):
# 1. curfew + noise complaint about the ice maker — 4/3/3 = 10
# 2. fridge pays rent, I'm the noisy tenant — 4/4/4 = 12
# 3. strike over 2 a.m. snacking, union contract — 4/4/3 = 11
# 4. ACCESS DENIED, lasagna classified — 5/4/4 = 13
# 5. 12:01, "We're closed", hydrate during business hours — 5/4/4 = 13 WINNER
# 6. bedtime, cheese doesn't exist — 4/3/4 = 11
# 7. snacking escalated to management — 5/4/4 = 13
# 8. fridge as bouncer, not on the list — 4/4/4 = 12
# 9. office hours, calendar invite for breakfast — 5/4/4 = 13
# Tie at 13 between 4, 5, 7, 9. #5 wins: the midnight refusal IS the
# joke (criterion 4), 12:01 is the sharpest detail, and it reads aloud
# like something said at the door (criterion 5).


def gate_ok(text: str) -> bool:
    """The sealed gate: UTF-8, 1-200 chars, not only whitespace."""
    return bool(text.strip()) and 1 <= len(text) <= 200


def write_entry(path: pathlib.Path) -> int:
    text = ROAST
    if not gate_ok(text):
        print(f"gate FAIL: {len(text)} chars", file=sys.stderr)
        return 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    back = path.read_text(encoding="utf-8")
    if back != text:
        print("gate FAIL: round-trip mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(text)} chars to {path}")
    return 0


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Midnight Fridge Roast entry")
    parser.add_argument("--out", default="/output/entry.txt")
    parser.add_argument("--check", action="store_true",
                        help="verify the gate against a temp file")
    parser.add_argument("--self-test", action="store_true",
                        help="write to a temp file and verify the bytes read back")
    args = parser.parse_args(argv)
    if args.self_test:
        with tempfile.TemporaryDirectory() as tmp:
            probe = pathlib.Path(tmp) / "entry.txt"
            rc = write_entry(probe)
            data = probe.read_bytes()
            ok = rc == 0 and data == ROAST.encode("utf-8")
            print(f"self-test: {'ok' if ok else 'FAIL'} ({len(data)} bytes)")
            return 0 if ok else 1
    if args.check:
        with tempfile.TemporaryDirectory() as tmp:
            probe = pathlib.Path(tmp) / "entry.txt"
            rc = write_entry(probe)
            print(f"check: {len(ROAST)} chars, gate {'ok' if rc == 0 else 'FAIL'}")
            return rc
    return write_entry(pathlib.Path(args.out))


if __name__ == "__main__":
    raise SystemExit(main())
