#!/usr/bin/env python3

import pathlib


REFERENCES = pathlib.Path(__file__).parents[1] / "references"
ENTRY_POINTS = ("implement.md", "sub-agents.md", "validate.md")

for name in ENTRY_POINTS:
    guidance = (REFERENCES / name).read_text(encoding="utf-8")
    assert "git stash or temp copy" not in guidance
    assert "disposable" in guidance
    assert "worktree" in guidance
    assert "copy" in guidance

print("ok 1 - requires disposable-only discrimination sensor state at every verifier entry point")
