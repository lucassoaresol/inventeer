#!/usr/bin/env python3
"""Validate root-workspace syntax, Markdown links, and Claude skill parity."""

import ast
import pathlib
import re


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXCLUDED_PARTS = {".git", "repos", "session-context"}
LINK_RE = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def workspace_files(pattern):
    return sorted(
        path
        for path in ROOT.rglob(pattern)
        if not EXCLUDED_PARTS.intersection(path.relative_to(ROOT).parts)
    )


python_files = workspace_files("*.py")
for path in python_files:
    ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
print(f"ok 1 - {len(python_files)} Python files parse successfully")

markdown_links = 0
for path in workspace_files("*.md"):
    for raw_target in LINK_RE.findall(path.read_text(encoding="utf-8")):
        target = raw_target.strip().strip("<>").split("#", 1)[0]
        if not target or "://" in target or target.startswith(("mailto:", "/")):
            continue
        markdown_links += 1
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            raise AssertionError(f"broken Markdown link in {path.relative_to(ROOT)}: {raw_target}")
print(f"ok 2 - {markdown_links} relative Markdown links resolve")

skill_root = ROOT / ".agents/skills"
claude_root = ROOT / ".claude/skills"
local_skills = sorted(
    path.name
    for path in skill_root.iterdir()
    if path.is_dir() and not path.name.startswith("apex-")
)
claude_skills = sorted(path.name for path in claude_root.iterdir() if path.is_symlink())
if local_skills != claude_skills:
    raise AssertionError(f"Claude skill parity mismatch: local={local_skills}, claude={claude_skills}")
for name in local_skills:
    link = claude_root / name
    if link.resolve(strict=True) != (skill_root / name).resolve(strict=True):
        raise AssertionError(f"Claude skill link resolves to the wrong source: {name}")
    if link.readlink().is_absolute():
        raise AssertionError(f"Claude skill link must be relative: {name}")
print(f"ok 3 - {len(local_skills)} local skills have exact relative Claude symlinks")
