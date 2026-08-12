#!/usr/bin/env python3
"""Validate root-workspace syntax, Markdown links, and Claude skill parity."""

import ast
import pathlib
import re
import subprocess


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

feature_index = ROOT / ".specs/features/INDEX.md"
feature_index_text = feature_index.read_text(encoding="utf-8")
feature_rows = re.findall(
    r"^\| \[([^]]+)\]\(\./([^/]+)/\) \| (Active|Validated|Archived) \|$",
    feature_index_text,
    re.M,
)
indexed_features = {name: target for name, target, _status in feature_rows}
canonical_features = {path.name for path in feature_index.parent.iterdir() if path.is_dir()}
if set(indexed_features) != canonical_features or any(name != target for name, target in indexed_features.items()):
    raise AssertionError(
        f"feature index mismatch: missing={sorted(canonical_features - set(indexed_features))}, "
        f"extra={sorted(set(indexed_features) - canonical_features)}"
    )
print(f"ok 4 - feature index covers {len(canonical_features)} canonical directories")

state_at_head = subprocess.run(
    ["git", "show", "HEAD:.specs/STATE.md"],
    cwd=ROOT,
    text=True,
    capture_output=True,
    check=True,
).stdout
canonical_decisions = {}
for block in re.split(r"(?=^### AD-\d+$)", state_at_head, flags=re.M):
    decision = re.search(r"^### (AD-\d+)$", block, re.M)
    if not decision:
        continue
    status = re.search(r"^- \*\*Status\*\*: (.+)$", block, re.M)
    if not status:
        raise AssertionError(f"decision has no status: {decision.group(1)}")
    canonical_decisions[decision.group(1)] = status.group(1)
decision_index_text = (ROOT / ".specs/DECISIONS.md").read_text(encoding="utf-8")
indexed_decisions = dict(
    re.findall(r"^\| \[(AD-\d+)\]\(STATE\.md#ad-\d+\) \| ([^|]+?) \|$", decision_index_text, re.M)
)
if indexed_decisions != canonical_decisions:
    raise AssertionError(
        f"decision index mismatch: canonical={canonical_decisions}, indexed={indexed_decisions}"
    )
print(f"ok 5 - decision index classifies {len(canonical_decisions)} committed decisions")
