#!/usr/bin/env python3

import json
import subprocess
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / ".agents" / "skills" / "tlc-spec-driven" / "scripts"


def run_tool(name: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(TOOLS / name), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )


def spec_fixture(heading: str, criterion: str = "WHEN the gate runs THEN the tool SHALL pass") -> str:
    return textwrap.dedent(
        f"""\
        # Gate Specification

        ## Problem Statement

        Exercise the deterministic gate.

        ## Out of Scope

        - Product behavior.

        ## Assumptions & Open Questions

        | Assumption | Chosen default | Rationale |
        | --- | --- | --- |
        | Runtime | Python 3 | The tool ships as Python. |

        **Open questions:** none

        ## User Stories

        ### P1: Validate the artifact

        {heading}

        1. **GATE-01** — {criterion}

        ## Requirement Traceability

        | Requirement ID | Story | Status |
        | --- | --- | --- |
        | GATE-01 | Validate the artifact | Pending |
        """
    )


def tasks_fixture(*, dependency: str = "T1") -> str:
    return textwrap.dedent(
        f"""\
        # Gate Tasks

        ## Test Coverage Matrix

        | Layer | Required test |
        | --- | --- |
        | CLI | behavior |

        ## Gate Check Commands

        | Gate | Command |
        | --- | --- |
        | Quick | test command |

        ## Execution Plan

        ```mermaid
        graph LR
          T1 --> T2
        ```

        ## Task Breakdown

        ### Phase 1

        #### T1: Create fixture

        - **Depends on:** none
        - **Where:** `fixture.md`
        - **Tests:** unit
        - **Gate:** quick

        #### T2: Validate fixture

        - **Depends on:** {dependency}
        - **Where:** `validator.py`
        - **Tests:** unit
        - **Gate:** quick
        """
    )


class SpecGateTests(unittest.TestCase):
    def assert_spec_result(
        self,
        heading: str,
        expected: int,
        criterion: str = "WHEN the gate runs THEN the tool SHALL pass",
    ) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="tlc-spec-gate-") as directory:
            path = Path(directory) / "spec.md"
            path.write_text(spec_fixture(heading, criterion), encoding="utf-8")
            result = run_tool("validate_spec.py", str(path))
        self.assertEqual(expected, result.returncode, result.stdout + result.stderr)
        return result

    def test_accepts_colon_inside_markdown_emphasis(self) -> None:
        self.assert_spec_result("**Acceptance Criteria:**", 0)
        self.assert_spec_result("**Acceptance Criteria:**", 1, "WHEN the gate runs THEN the tool passes")

    def test_accepts_colon_outside_markdown_emphasis(self) -> None:
        self.assert_spec_result("**Acceptance Criteria**:", 0)
        self.assert_spec_result("**Acceptance Criteria**:", 1, "WHEN the gate runs THEN the tool passes")

    def test_accepts_wrapped_acceptance_criterion(self) -> None:
        self.assert_spec_result(
            "**Acceptance Criteria**:",
            0,
            "WHEN the gate runs THEN the tool\n           SHALL evaluate the complete criterion",
        )

    def test_rejects_missing_required_section(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tlc-spec-gate-") as directory:
            path = Path(directory) / "spec.md"
            path.write_text(spec_fixture("**Acceptance Criteria**:").replace("## User Stories", "## Stories"), encoding="utf-8")
            result = run_tool("validate_spec.py", str(path))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("missing required section: ## User Stories", result.stdout)

    def test_rejects_acceptance_criterion_without_shall(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tlc-spec-gate-") as directory:
            path = Path(directory) / "spec.md"
            path.write_text(spec_fixture("**Acceptance Criteria**:", "WHEN the gate runs THEN the tool passes"), encoding="utf-8")
            result = run_tool("validate_spec.py", str(path))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("acceptance criterion has no SHALL", result.stdout)


class StateGateTests(unittest.TestCase):
    def run_validation(self, report: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="tlc-state-gate-") as directory:
            feature = Path(directory) / ".specs" / "features" / "gate"
            feature.mkdir(parents=True)
            (feature / "validation.md").write_text(report, encoding="utf-8")
            return run_tool("validate_state.py", "gate", "--root", directory)

    def test_overall_pass_outranks_subordinate_fail(self) -> None:
        result = self.run_validation("## Validation: PASS\n\n**Sensor result:** FAIL\n\nEvidence: `src/gate.py:12`\n")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_overall_fail_outranks_subordinate_pass(self) -> None:
        result = self.run_validation("**Overall:** FAIL\n\n**Sensor result:** PASS\n\nEvidence: `src/gate.py:12`\n")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("verdict is FAIL", result.stdout)
        self.assertNotIn("template placeholder", result.stdout)

    def test_pass_without_file_line_evidence_fails_closed(self) -> None:
        result = self.run_validation("**Verdict:** PASS\n\nAll checks completed.\n")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("cites no file:line evidence", result.stdout)


class TaskGateTests(unittest.TestCase):
    def run_tasks(self, body: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix="tlc-task-gate-") as directory:
            path = Path(directory) / "tasks.md"
            path.write_text(body, encoding="utf-8")
            return run_tool("validate_tasks.py", str(path))

    def test_matching_mermaid_and_dependency_fields_pass(self) -> None:
        result = self.run_tasks(tasks_fixture())
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_mismatched_mermaid_and_dependency_fields_fail(self) -> None:
        result = self.run_tasks(tasks_fixture(dependency="none"))
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("diagram shows T1 -> T2", result.stdout)


class CommitGateTests(unittest.TestCase):
    def test_accepts_supported_conventional_commit(self) -> None:
        result = run_tool("check_commit.py", "--message", "test(tlc): harden deterministic gates")
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_rejects_non_conventional_commit(self) -> None:
        result = run_tool("check_commit.py", "--message", "Added validators.")
        self.assertEqual(1, result.returncode, result.stdout + result.stderr)
        self.assertIn("header does not match", result.stdout)


class WorkspaceAdoptionTests(unittest.TestCase):
    def test_local_extensions_are_retained(self) -> None:
        manifest = json.loads((ROOT / ".agents" / "vendor.json").read_text(encoding="utf-8"))["tlc-spec-driven"]
        expected_customizations = [
            "review contract and artifact lifecycle",
            "orientation before decision questions",
            "operational enablement discovery",
            "requirement provenance",
            "resource-aware execution preflight",
            "deterministic gate compatibility and prospective adoption",
        ]
        self.assertEqual(expected_customizations, manifest["local_customizations"])

        anchors = {
            ROOT / ".agents" / "skills" / "tlc-spec-driven" / "references" / "specify.md": [
                "Establish the Review Contract",
                "Operational enablement",
                "Preserve Requirement Provenance",
            ],
            ROOT / ".agents" / "skills" / "tlc-spec-driven" / "references" / "implement.md": [
                "Resource preflight before heavy work",
            ],
            ROOT / ".agents" / "skills" / "tlc-spec-driven" / "references" / "validate.md": [
                "Delivery Evidence",
            ],
        }
        for path, expected_anchors in anchors.items():
            body = path.read_text(encoding="utf-8")
            for anchor in expected_anchors:
                self.assertIn(anchor, body, f"missing retained extension {anchor!r} in {path}")

    def test_version_metadata_is_synchronized(self) -> None:
        manifest = json.loads((ROOT / ".agents" / "vendor.json").read_text(encoding="utf-8"))["tlc-spec-driven"]
        skill = (ROOT / ".agents" / "skills" / "tlc-spec-driven" / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")

        self.assertEqual("3.3.0", manifest["upstream_version"])
        self.assertEqual("fe318be656b315d5b6f45cf7ea23946b2d0241b0", manifest["base_ref"])
        self.assertIn("  version: 3.3.0", skill)
        self.assertIn("| `tlc-spec-driven` | Tech Lead's Club | 3.3.0 |", readme)

    def test_adoption_is_prospective_and_root_gate_uses_fixtures(self) -> None:
        state = (ROOT / ".specs" / "STATE.md").read_text(encoding="utf-8")
        root_gate = (ROOT / "scripts" / "test-workspace.sh").read_text(encoding="utf-8")
        normalized_state = " ".join(state.split()).casefold()

        self.assertIn("### AD-040", state)
        self.assertIn("artefatos criados ou materialmente revisados sob a tlc 3.3.0", normalized_state)
        self.assertIn("não varrer nem revalidar retroativamente", normalized_state)
        self.assertIn("scripts/test-tlc-deterministic-gates.py", root_gate)
        self.assertNotIn("validate_spec.py .specs/features", root_gate)

    def test_transition_gates_are_explicit(self) -> None:
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        state = (ROOT / ".specs" / "STATE.md").read_text(encoding="utf-8")
        normalized_state = " ".join(state.split()).casefold()

        for gate in ("validate_spec.py", "validate_tasks.py", "check_commit.py", "validate_state.py"):
            self.assertIn(gate, readme)
        self.assertIn("antes de confirmar spec, aprovar tasks, criar commit ou encerrar validation", normalized_state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
