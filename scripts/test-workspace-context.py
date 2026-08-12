#!/usr/bin/env python3
"""Exercise the closed-schema, reference-only workspace context planner."""

from __future__ import annotations

import copy
import json
import pathlib
import subprocess
import tempfile


ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANNER = ROOT / "scripts/workspace-context.py"
MANIFEST = ROOT / ".specs/context/routes.json"
ROUTES = (
    "portal-task",
    "assistants-task",
    "pr-review",
    "cycle-triage",
    "delivery-front",
)


def run(*args: str, root: pathlib.Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(PLANNER), "--root", str(root), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_manifest(root: pathlib.Path, manifest: dict[str, object]) -> None:
    path = root / "routes.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    for route in manifest.get("routes", []):
        for reference in route.get("references", []):
            source = reference.get("source")
            if isinstance(source, str) and not source.startswith(("/", "..")):
                target = root / source
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("CONTENT_MUST_NOT_APPEAR\n", encoding="utf-8")


def tree_fingerprint(root: pathlib.Path) -> list[tuple[str, bytes]]:
    return [
        (path.relative_to(root).as_posix(), path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    ]


audit = run("audit")
assert audit.returncode == 0, audit.stderr
assert audit.stdout.startswith("ok - 5 routes, "), audit.stdout
print("ok 1 - canonical manifest audits exactly five routes")

for route in ROUTES:
    first = run("plan", "--route", route)
    second = run("plan", "--route", route)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert set(payload) == {"route", "references"}
    assert payload["route"] == route
    assert payload["references"]
    assert "CONTENT_MUST_NOT_APPEAR" not in first.stdout
print("ok 2 - every supported route emits byte-stable metadata only")

unknown = run("plan", "--route", "unknown")
assert unknown.returncode == 2
assert "unknown route" in unknown.stderr
print("ok 3 - unknown routes fail closed")

base = json.loads(MANIFEST.read_text(encoding="utf-8"))
invalid_cases: list[tuple[str, dict[str, object]]] = []

case = copy.deepcopy(base)
case["unexpected"] = True
invalid_cases.append(("unknown top-level field", case))

case = copy.deepcopy(base)
case["routes"][0]["unexpected"] = True
invalid_cases.append(("unknown route field", case))

case = copy.deepcopy(base)
case["routes"][0]["references"][0]["unexpected"] = True
invalid_cases.append(("unknown reference field", case))

case = copy.deepcopy(base)
case["routes"][0]["references"].append(copy.deepcopy(case["routes"][0]["references"][0]))
invalid_cases.append(("duplicate reference", case))

for label, unsafe in (("absolute path", "/tmp/source"), ("path traversal", "../source")):
    case = copy.deepcopy(base)
    case["routes"][0]["references"][0]["source"] = unsafe
    invalid_cases.append((label, case))

case = copy.deepcopy(base)
case["routes"][0]["references"][0]["source"] = "missing.md"
invalid_cases.append(("missing source", case))

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    for label, manifest in invalid_cases:
        write_manifest(fixture_root, manifest)
        if label == "missing source":
            (fixture_root / "missing.md").unlink()
        before = tree_fingerprint(fixture_root)
        result = run("--manifest", "routes.json", "audit", root=fixture_root)
        assert result.returncode == 2, (label, result.stdout, result.stderr)
        assert "CONTENT_MUST_NOT_APPEAR" not in result.stderr
        assert tree_fingerprint(fixture_root) == before
print(f"ok 4 - {len(invalid_cases)} malformed manifest cases fail closed")

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    write_manifest(fixture_root, base)
    outside = fixture_root.parent / "outside-context-source"
    outside.write_text("CONTENT_MUST_NOT_APPEAR\n", encoding="utf-8")
    target = fixture_root / base["routes"][0]["references"][0]["source"]
    target.unlink()
    target.symlink_to(outside)
    result = run("--manifest", "routes.json", "audit", root=fixture_root)
    assert result.returncode == 2
    assert "CONTENT_MUST_NOT_APPEAR" not in result.stderr
    outside.unlink()
print("ok 5 - symlink escapes fail closed without source content")
