#!/usr/bin/env python3

import json
import pathlib
import subprocess
import sys
import tempfile


def run(*args: str, expect: int = 0) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        [sys.executable, str(SUBJECT), "--root", str(ROOT), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != expect:
        raise AssertionError(
            f"expected exit {expect}, got {result.returncode}: {result.stdout}{result.stderr}"
        )
    return result


SUBJECT = pathlib.Path(__file__).with_name("lessons.py")

with tempfile.TemporaryDirectory(prefix="test-tlc-lessons.") as temp_dir:
    ROOT = pathlib.Path(temp_dir)
    run("init")
    run(
        "add",
        "--feature",
        "review-lifecycle",
        "--signal",
        "review_finding",
        "--source",
        "validation.md:confirmed-review-R1",
        "--text",
        "Bind validation evidence to the exact reviewed head before promotion.",
        "--scope",
        "delivery",
    )

    data = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(data["lessons"]) == 1
    lesson = data["lessons"][0]
    assert lesson["signal"] == "review_finding"
    assert lesson["features"] == ["review-lifecycle"]
    assert lesson["evidence"] == ["validation.md:confirmed-review-R1 (delivery)"]
    print("ok 1 - records an independently confirmed external review finding")

    run(
        "add",
        "--feature",
        "ungrounded-review",
        "--signal",
        "review_finding",
        "--source",
        "",
        "--text",
        "Do not accept an ungrounded external review opinion as a project lesson.",
        expect=2,
    )
    unchanged = json.loads((ROOT / ".specs" / "lessons.json").read_text(encoding="utf-8"))
    assert len(unchanged["lessons"]) == 1
    print("ok 2 - rejects an ungrounded external review opinion")
