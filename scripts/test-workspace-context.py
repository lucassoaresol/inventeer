#!/usr/bin/env python3
"""Exercise bounded, closed-schema workspace context plans and measurements."""

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
    "project-discovery",
)
FORBIDDEN_CONTENT = "CONTENT_MUST_NOT_APPEAR"


def run(*args: str, root: pathlib.Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(PLANNER), "--root", str(root), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def write_manifest(root: pathlib.Path, manifest: dict[str, object]) -> pathlib.Path:
    path = root / "routes.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    for route in manifest.get("routes", []):
        for reference in route.get("references", []):
            source = reference.get("source")
            if not isinstance(source, str) or source.startswith(("/", "..")):
                continue
            target = root / source
            target.parent.mkdir(parents=True, exist_ok=True)
            headings = reference.get("headings", [])
            if headings:
                text = "# Fixture\n" + "".join(
                    f"{heading}\n{FORBIDDEN_CONTENT}_{index}\n"
                    for index, heading in enumerate(headings)
                )
            else:
                text = f"{FORBIDDEN_CONTENT}\n"
            target.write_text(text, encoding="utf-8")
    return path


def tree_fingerprint(root: pathlib.Path) -> list[tuple[str, bytes]]:
    return [
        (path.relative_to(root).as_posix(), path.read_bytes())
        for path in sorted(root.rglob("*"))
        if path.is_file() and not path.is_symlink()
    ]


base = json.loads(MANIFEST.read_text(encoding="utf-8"))
assert set(base) == {"version", "estimator", "routes"}
assert base["version"] == 2
assert base["estimator"] == {
    "unit": "unicode-code-points",
    "code_points_per_estimated_token": 4,
}
assert tuple(route["name"] for route in base["routes"]) == ROUTES
assert all(route["budget_estimated_tokens"] == 20_000 for route in base["routes"])
assert all(
    isinstance(reference["headings"], list)
    for route in base["routes"]
    for reference in route["references"]
)
print("ok 1 - canonical manifest declares the exact estimator, budgets, routes, and heading lists")

audit = run("audit")
assert audit.returncode == 0, audit.stderr
assert audit.stdout.startswith("ok - 6 routes, "), audit.stdout
print("ok 2 - canonical manifest audits exactly six routes")

for route in ROUTES:
    first = run("plan", "--route", route)
    second = run("plan", "--route", route)
    assert first.returncode == second.returncode == 0, first.stderr
    assert first.stdout == second.stdout
    payload = json.loads(first.stdout)
    assert set(payload) == {"route", "estimator", "budget_estimated_tokens", "references"}
    assert payload["route"] == route
    assert payload["budget_estimated_tokens"] == 20_000
    assert payload["estimator"] == base["estimator"]
    assert payload["references"]
    assert FORBIDDEN_CONTENT not in first.stdout
    assert str(ROOT) not in first.stdout
print("ok 3 - every route emits byte-stable plan metadata without content or physical paths")

canonical_check = run("check")
assert canonical_check.returncode == 0, canonical_check.stderr
canonical_report = json.loads(canonical_check.stdout)
assert canonical_report["status"] == "pass"
assert [route["route"] for route in canonical_report["routes"]] == list(ROUTES)
assert all(route["status"] == "pass" for route in canonical_report["routes"])
assert FORBIDDEN_CONTENT not in canonical_check.stdout
assert str(ROOT) not in canonical_check.stdout
print("ok 4 - all six canonical routes measure within budget without disclosing content")

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    measured = copy.deepcopy(base)
    measured["routes"][0]["references"] = [
        {
            "source": "selected.md",
            "headings": ["## First", "## Last"],
            "reason": "measure exact selected sections",
            "gate": "fixture",
        },
        {
            "source": "whole.md",
            "headings": [],
            "reason": "measure exact whole file",
            "gate": "fixture",
        },
    ]
    write_manifest(fixture_root, measured)
    source = fixture_root / "selected.md"
    source_text = (
        "# Fixture\n"
        "## First\n"
        "alpha\n"
        "### Child\n"
        "beta\n"
        "## Middle\n"
        f"{FORBIDDEN_CONTENT}\n"
        "## Last\n"
        "omega\n"
    )
    source.write_text(source_text, encoding="utf-8")
    whole = fixture_root / "whole.md"
    whole_text = "whole\nfile\n"
    whole.write_text(whole_text, encoding="utf-8")
    selected = "## First\nalpha\n### Child\nbeta\n## Last\nomega\n"
    expected_characters = len(selected) + len(whole_text)
    expected_tokens = (expected_characters + 3) // 4

    report = run("--manifest", "routes.json", "measure", "--route", ROUTES[0], root=fixture_root)
    assert report.returncode == 0, report.stderr
    payload = json.loads(report.stdout)
    assert payload["total_characters"] == expected_characters
    assert payload["estimated_tokens"] == expected_tokens
    assert payload["sources"] == [
        {
            "source": "selected.md",
            "headings": ["## First", "## Last"],
            "characters": len(selected),
            "estimated_tokens": (len(selected) + 3) // 4,
        },
        {
            "source": "whole.md",
            "headings": [],
            "characters": len(whole_text),
            "estimated_tokens": (len(whole_text) + 3) // 4,
        },
    ]
    assert payload["status"] == "pass"
    assert FORBIDDEN_CONTENT not in report.stdout

    measured["routes"][0]["budget_estimated_tokens"] = expected_tokens
    write_manifest(fixture_root, measured)
    source.write_text(source_text, encoding="utf-8")
    whole.write_text(whole_text, encoding="utf-8")
    boundary_pass = run("--manifest", "routes.json", "check", root=fixture_root)
    assert boundary_pass.returncode == 0
    assert json.loads(boundary_pass.stdout)["routes"][0]["status"] == "pass"

    measured["routes"][0]["budget_estimated_tokens"] = expected_tokens - 1
    write_manifest(fixture_root, measured)
    source.write_text(source_text, encoding="utf-8")
    whole.write_text(whole_text, encoding="utf-8")
    before = tree_fingerprint(fixture_root)
    boundary_fail = run("--manifest", "routes.json", "check", root=fixture_root)
    assert boundary_fail.returncode == 1
    failed_payload = json.loads(boundary_fail.stdout)
    assert failed_payload["status"] == "fail"
    assert [route["route"] for route in failed_payload["routes"]] == list(ROUTES)
    assert failed_payload["routes"][0]["status"] == "fail"
    assert all(route["status"] == "pass" for route in failed_payload["routes"][1:])
    assert FORBIDDEN_CONTENT not in boundary_fail.stdout + boundary_fail.stderr
    assert str(fixture_root) not in boundary_fail.stdout + boundary_fail.stderr
    assert tree_fingerprint(fixture_root) == before

    selected_fail = run(
        "--manifest", "routes.json", "measure", "--route", ROUTES[0], root=fixture_root
    )
    assert selected_fail.returncode == 1
    selected_fail_payload = json.loads(selected_fail.stdout)
    assert selected_fail_payload["status"] == "fail"
    assert selected_fail_payload["estimated_tokens"] == expected_tokens
    assert selected_fail_payload["budget_estimated_tokens"] == expected_tokens - 1
    assert FORBIDDEN_CONTENT not in selected_fail.stdout + selected_fail.stderr
    assert str(fixture_root) not in selected_fail.stdout + selected_fail.stderr
    assert tree_fingerprint(fixture_root) == before
print("ok 5 - selected and all-route adjacent budget boundaries discriminate pass from fail")

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    adjacent = copy.deepcopy(base)
    adjacent["routes"][0]["references"] = [
        {
            "source": "adjacent.md",
            "headings": ["## One", "## Two"],
            "reason": "measure adjacent selected headings",
            "gate": "fixture",
        }
    ]
    write_manifest(fixture_root, adjacent)
    adjacent_text = "# Fixture\n## One\n## Two\n"
    (fixture_root / "adjacent.md").write_text(adjacent_text, encoding="utf-8")
    report = run("--manifest", "routes.json", "measure", "--route", ROUTES[0], root=fixture_root)
    assert report.returncode == 0, report.stderr
    payload = json.loads(report.stdout)
    selected_adjacent = "## One\n## Two\n"
    assert payload["total_characters"] == len(selected_adjacent)
    assert payload["sources"][0]["characters"] == len(selected_adjacent)
    assert payload["estimated_tokens"] == (len(selected_adjacent) + 3) // 4
    assert "Fixture" not in report.stdout
print("ok 6 - adjacent selected headings are measured without content or synthetic separators")

unknown = run("plan", "--route", "unknown")
assert unknown.returncode == 2
assert "unknown route" in unknown.stderr
print("ok 7 - unknown routes fail closed")

invalid_cases: list[tuple[str, dict[str, object]]] = []

case = copy.deepcopy(base)
case["unexpected"] = True
invalid_cases.append(("unknown top-level field", case))

case = copy.deepcopy(base)
case["version"] = 1
invalid_cases.append(("invalid version", case))

for label, estimator in (
    ("invalid estimator unit", {"unit": "bytes", "code_points_per_estimated_token": 4}),
    ("invalid estimator ratio", {"unit": "unicode-code-points", "code_points_per_estimated_token": 0}),
):
    case = copy.deepcopy(base)
    case["estimator"] = estimator
    invalid_cases.append((label, case))

case = copy.deepcopy(base)
case["routes"][0]["budget_estimated_tokens"] = 0
invalid_cases.append(("invalid budget", case))

case = copy.deepcopy(base)
case["routes"] = list(reversed(case["routes"]))
invalid_cases.append(("invalid route order", case))

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

case = copy.deepcopy(base)
case["routes"][0]["references"][0]["headings"] = ["not a heading"]
invalid_cases.append(("malformed heading", case))

case = copy.deepcopy(base)
heading = case["routes"][0]["references"][0]["headings"][0]
case["routes"][0]["references"][0]["headings"] = [heading, heading]
invalid_cases.append(("repeated configured heading", case))

case = copy.deepcopy(base)
case["routes"][0]["references"][0]["source"] = "source.py"
case["routes"][0]["references"][0]["headings"] = ["## Heading"]
invalid_cases.append(("heading on non-Markdown source", case))

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    for label, manifest in invalid_cases:
        write_manifest(fixture_root, manifest)
        if label == "missing source":
            (fixture_root / "missing.md").unlink()
        before = tree_fingerprint(fixture_root)
        result = run("--manifest", "routes.json", "audit", root=fixture_root)
        assert result.returncode == 2, (label, result.stdout, result.stderr)
        assert FORBIDDEN_CONTENT not in result.stderr
        assert str(fixture_root) not in result.stderr
        assert tree_fingerprint(fixture_root) == before
print(f"ok 8 - {len(invalid_cases)} malformed manifest cases fail closed without mutation")

heading_failures: list[tuple[str, str]] = []
case = copy.deepcopy(base)
case["routes"][0]["references"] = [
    {"source": "heading.md", "headings": ["## Target"], "reason": "fixture", "gate": "fixture"}
]
heading_failures.append(("missing heading", "# Fixture\n## Different\n"))
heading_failures.append(("duplicate heading", "# Fixture\n## Target\none\n## Target\ntwo\n"))

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    for label, text in heading_failures:
        write_manifest(fixture_root, case)
        (fixture_root / "heading.md").write_text(text + FORBIDDEN_CONTENT, encoding="utf-8")
        before = tree_fingerprint(fixture_root)
        result = run("--manifest", "routes.json", "audit", root=fixture_root)
        assert result.returncode == 2, label
        assert FORBIDDEN_CONTENT not in result.stderr
        assert tree_fingerprint(fixture_root) == before
print("ok 9 - absent and duplicated Markdown headings fail closed")

with tempfile.TemporaryDirectory() as temporary:
    fixture_root = pathlib.Path(temporary)
    write_manifest(fixture_root, base)
    outside = fixture_root.parent / "outside-context-source"
    outside.write_text(FORBIDDEN_CONTENT + "\n", encoding="utf-8")
    target = fixture_root / base["routes"][0]["references"][0]["source"]
    target.unlink()
    target.symlink_to(outside)
    before = tree_fingerprint(fixture_root)
    result = run("--manifest", "routes.json", "audit", root=fixture_root)
    assert result.returncode == 2
    assert FORBIDDEN_CONTENT not in result.stderr
    assert str(fixture_root) not in result.stderr
    assert tree_fingerprint(fixture_root) == before
    outside.unlink()
print("ok 10 - symlink escapes fail closed without source content or mutation")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
readme = (ROOT / "README.md").read_text(encoding="utf-8")
for command in (
    "workspace-context.py check",
    "workspace-context.py plan --route <rota>",
    "measure --route <rota>",
):
    assert command in agents
for command in (
    "workspace-context.py check",
    "workspace-context.py plan --route portal-task",
    "workspace-context.py measure --route portal-task",
):
    assert command in readme
for outcome in ("exit `1`", "exit `2`", "metadata"):
    assert outcome in agents and outcome in readme
print("ok 11 - operator contracts require bounded metadata-only planning with exact exit semantics")


# --- Preflight declarado dentro de cada skill roteada ------------------------
# A regra ambiental alcançava 2 de 27 sessões Claude: uma engine lê AGENTS.md uma vez por sessão,
# mas lê o corpo da skill no momento em que o trabalho começa. O passo declarado é a unidade
# aplicável; este bloco garante que ele exista, aponte para a própria rota e venha primeiro.

VENDORED = set(json.loads((ROOT / ".agents/vendor.json").read_text(encoding="utf-8")))


def first_workflow_step(body: str) -> str:
    marker = "## Workflow\n"
    if marker not in body:
        return ""
    rest = body.split(marker, 1)[1].lstrip("\n")
    steps = rest.split("\n2. ", 1)
    return steps[0]


def preflight_violation(skill: str, route: str, body: str) -> str | None:
    """Return why a routed skill fails the preflight contract, or None when it passes."""
    step = first_workflow_step(body)
    if not step:
        return f"{skill} has no numbered workflow"
    if not step.lstrip().startswith("1. "):
        return f"{skill} does not open its workflow with step 1"
    for command in ("workspace-context.py check", "workspace-context.py plan --route"):
        if command not in step:
            return f"{skill} omits `{command}` from its first workflow step"
    if f"plan --route {route}" not in step:
        return f"{skill} must plan route {route} in its first step"
    return None


routed_skills: dict[str, str] = {}
for route in json.loads(MANIFEST.read_text(encoding="utf-8"))["routes"]:
    for reference in route["references"]:
        source = reference["source"]
        if not source.startswith(".agents/skills/"):
            continue
        skill = pathlib.PurePosixPath(source).parts[2]
        if skill in VENDORED:
            # Vendored content is replaced wholesale on update; a local step would not survive.
            continue
        assert routed_skills.setdefault(skill, route["name"]) == route["name"], (
            f"{skill} is referenced by more than one route"
        )

assert routed_skills, "no routed skills derived from the manifest"
assert set(routed_skills) == {
    "portal-task-context",
    "assistants-task-context",
    "review-pull-request",
    "triage-project-cycle",
    "advance-delivery-front",
    "discover-project-context",
}, sorted(routed_skills)

for skill, route in sorted(routed_skills.items()):
    body = (ROOT / ".agents/skills" / skill / "SKILL.md").read_text(encoding="utf-8")
    violation = preflight_violation(skill, route, body)
    assert violation is None, violation
    step = first_workflow_step(body)
    assert "non-zero" in step, f"{skill} does not tell the reader to stop on a non-zero result"
    assert "metadata only" in step, f"{skill} does not state the metadata-only bound"

# Uma skill sem rota não ganha preflight: o passo mediria um orçamento que não existe.
for unrouted in ("create-review-bundle",):
    body = (ROOT / ".agents/skills" / unrouted / "SKILL.md").read_text(encoding="utf-8")
    assert "workspace-context.py" not in body, f"{unrouted} has no route and must not preflight"

# Casos de falha exercitados contra o detector, para que ele não passe por vacuidade.
GOOD_STEP = (
    "## Workflow\n\n1. Run `python3 scripts/workspace-context.py check` and\n"
    "   `python3 scripts/workspace-context.py plan --route pr-review`. Stop on a non-zero result;\n"
    "   these commands emit metadata only and do not replace reading the selected sources.\n"
    "2. Do the work.\n"
)
assert preflight_violation("probe", "pr-review", GOOD_STEP) is None
for label, mutated, expected in (
    ("comando ausente", GOOD_STEP.replace("scripts/workspace-context.py check` and\n", "nothing` and\n"), "omits"),
    ("rota trocada", GOOD_STEP.replace("--route pr-review", "--route cycle-triage"), "must plan route"),
    ("passo demovido", GOOD_STEP.replace("\n\n1. Run", "\n\n1. Do something else.\n2. Run"), "omits"),
    ("sem workflow", "## Other\n\n1. Run `python3 scripts/workspace-context.py check`\n", "no numbered workflow"),
):
    violation = preflight_violation("probe", "pr-review", mutated)
    assert violation is not None, f"detector missed: {label}"
    assert expected in violation, f"{label}: unexpected message {violation!r}"

print(f"ok 12 - {len(routed_skills)} routed skills declare their own preflight as step 1")
