#!/usr/bin/env python3

import importlib.util
import json
import pathlib
import tempfile
import unittest


ROOT = pathlib.Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "scripts/pr-review-pilot.py"


def load_module():
    spec = importlib.util.spec_from_file_location("pr_review_pilot", MODULE_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


BASE_SHA = "a" * 40
HEAD_SHA = "b" * 40


def valid_record(**overrides):
    record = {
        "schema_version": 1,
        "repository": "inventeer/portal-api",
        "pr": 280,
        "observed_at": "2026-08-07T12:00:00Z",
        "base_sha": BASE_SHA,
        "head_sha": HEAD_SHA,
        "final_base_sha": BASE_SHA,
        "final_head_sha": HEAD_SHA,
        "verdict": "no-actionable-findings",
        "github_review_evidence": "threads",
        "linear": {
            "target_issue": "INV-3145",
            "target_updated_at": "2026-08-07T10:00:00Z",
            "scope": "target-only",
            "reads": 1,
            "expansions": [],
        },
        "checks": {"remote": "passed", "local": "unbound"},
        "findings": [],
        "post_merge": {"status": "not-observed", "cutoff": None},
    }
    record.update(overrides)
    return record


class PilotLedgerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.module = load_module()

    def test_base_change_requires_stale_verdict(self):
        record = valid_record(final_base_sha="c" * 40)
        with self.assertRaisesRegex(ValueError, "verdict must be stale"):
            self.module.validate_record(record)
        record["verdict"] = "stale"
        self.assertEqual(self.module.validate_record(record)["verdict"], "stale")

    def test_head_change_requires_stale_verdict(self):
        record = valid_record(final_head_sha="d" * 40)
        with self.assertRaisesRegex(ValueError, "verdict must be stale"):
            self.module.validate_record(record)

    def test_stale_identity_overrides_unresolved_finding_verdict(self):
        record = valid_record(
            final_base_sha="c" * 40,
            verdict="stale",
            findings=[{"id": "F1", "severity": "P1", "outcome": "unresolved"}],
        )
        self.assertEqual(self.module.validate_record(record)["verdict"], "stale")

    def test_unresolved_p2_requires_block(self):
        record = valid_record(
            findings=[{"id": "F1", "severity": "P2", "outcome": "unresolved"}]
        )
        with self.assertRaisesRegex(ValueError, "require a block verdict"):
            self.module.validate_record(record)
        record["verdict"] = "block"
        self.assertEqual(self.module.validate_record(record)["verdict"], "block")

    def test_unknown_and_sensitive_fields_are_rejected(self):
        for field in ("comment", "diff", "token"):
            record = valid_record()
            record[field] = "must not persist"
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, "unknown fields"):
                self.module.validate_record(record)

    def test_record_is_canonical_and_append_only(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = pathlib.Path(temp_dir)
            ledger = self.module.record_review(workspace, valid_record())
            first_bytes = ledger.read_bytes()
            self.module.record_review(workspace, valid_record(pr=281))
            lines = ledger.read_text(encoding="utf-8").splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(json.loads(lines[0])["pr"], 280)
            self.assertTrue(first_bytes.endswith(b"\n"))
            self.assertEqual(list(workspace.rglob("*.jsonl")), [ledger])

    def test_summary_uses_decided_denominator(self):
        records = [
            valid_record(
                findings=[
                    {"id": "F1", "severity": "P1", "outcome": "accepted-fixed"},
                    {"id": "F2", "severity": "P2", "outcome": "withdrawn-false-positive"},
                    {"id": "F3", "severity": "P3", "outcome": "indeterminate"},
                ]
            )
        ]
        summary = self.module.summarize(records)
        self.assertEqual(summary["reviewed_prs"], 1)
        self.assertEqual(summary["decided_findings"], 2)
        self.assertEqual(summary["acceptance_rate"], 0.5)
        self.assertEqual(summary["false_positive_rate"], 0.5)
        self.assertEqual(summary["indeterminate_findings"], 1)
        self.assertEqual(summary["github_review_evidence"]["threads"], 1)
        self.assertEqual(summary["remote_checks"]["passed"], 1)
        self.assertEqual(summary["local_validations"]["unbound"], 1)

    def test_zero_decided_findings_has_null_rates(self):
        summary = self.module.summarize([valid_record()])
        self.assertIsNone(summary["acceptance_rate"])
        self.assertIsNone(summary["false_positive_rate"])

    def test_summary_separates_stale_inputs_and_expansion_reasons(self):
        linear = valid_record()["linear"]
        linear.update(
            scope="expanded",
            reads=3,
            expansions=[
                {"issue": "INV-2228", "reason": "inherited-dod"},
                {"issue": "INV-254", "reason": "ownership"},
            ],
        )
        summary = self.module.summarize(
            [
                valid_record(
                    final_base_sha="c" * 40,
                    verdict="stale",
                    github_review_evidence="approval-only",
                    linear=linear,
                )
            ]
        )
        self.assertEqual(summary["stale_reviews"], 1)
        self.assertEqual(summary["stale_base_changes"], 1)
        self.assertEqual(summary["stale_head_changes"], 0)
        self.assertEqual(summary["linear_expansion_reasons"]["inherited-dod"], 1)
        self.assertEqual(summary["linear_expansion_reasons"]["ownership"], 1)
        self.assertEqual(summary["github_review_evidence"]["approval-only"], 1)

    def test_ledger_path_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            workspace = pathlib.Path(temp_dir)
            outside = workspace.parent / "outside.jsonl"
            with self.assertRaisesRegex(ValueError, "session-context/review-pilot"):
                self.module.record_review(workspace, valid_record(), outside)

    def test_symlinked_pilot_root_cannot_escape_workspace(self):
        with tempfile.TemporaryDirectory() as temp_dir, tempfile.TemporaryDirectory() as outside_dir:
            workspace = pathlib.Path(temp_dir)
            session_context = workspace / "session-context"
            session_context.mkdir()
            (session_context / "review-pilot").symlink_to(outside_dir, target_is_directory=True)
            with self.assertRaisesRegex(ValueError, "resolves outside workspace"):
                self.module.record_review(workspace, valid_record())


if __name__ == "__main__":
    unittest.main(verbosity=2)
