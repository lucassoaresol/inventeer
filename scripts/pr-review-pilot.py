#!/usr/bin/env python3
"""Validate, append, and summarize sanitized pull-request pilot records."""

import argparse
import datetime as dt
import json
import os
import pathlib
import re
import sys
from collections import Counter


TOP_FIELDS = {
    "schema_version",
    "repository",
    "pr",
    "observed_at",
    "base_sha",
    "head_sha",
    "final_base_sha",
    "final_head_sha",
    "verdict",
    "github_review_evidence",
    "linear",
    "checks",
    "findings",
    "post_merge",
}
LINEAR_FIELDS = {"target_issue", "target_updated_at", "scope", "reads", "expansions"}
EXPANSION_FIELDS = {"issue", "reason"}
CHECK_FIELDS = {"remote", "local"}
FINDING_FIELDS = {"id", "severity", "outcome"}
POST_MERGE_FIELDS = {"status", "cutoff"}

VERDICTS = {"block", "non-blocking-findings", "no-actionable-findings", "inconclusive", "stale"}
GITHUB_REVIEW_EVIDENCE = {"threads", "approval-only", "none", "unavailable"}
LINEAR_SCOPES = {"none", "target-only", "expanded", "reused", "unavailable"}
EXPANSION_REASONS = {"inherited-dod", "dependency", "ids", "hierarchy", "ownership"}
REMOTE_CHECKS = {"passed", "failed", "pending", "unavailable"}
LOCAL_CHECKS = {"passed", "failed", "not-run", "unbound"}
SEVERITIES = {"P0", "P1", "P2", "P3"}
OUTCOMES = {
    "accepted-fixed",
    "accepted-by-contract",
    "rejected-with-evidence",
    "withdrawn-false-positive",
    "unresolved",
    "indeterminate",
}
POST_MERGE_STATUSES = {"confirmed-escape", "no-confirmed-escape", "not-observed"}
DECIDED_OUTCOMES = {
    "accepted-fixed",
    "accepted-by-contract",
    "rejected-with-evidence",
    "withdrawn-false-positive",
}
ACCEPTED_OUTCOMES = {"accepted-fixed", "accepted-by-contract"}

SHA_RE = re.compile(r"[0-9a-f]{40}")
REPOSITORY_RE = re.compile(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+")
ISSUE_RE = re.compile(r"INV-[1-9][0-9]*")
FINDING_RE = re.compile(r"F[1-9][0-9]*")


def _require_object(value, label):
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be an object")


def _require_exact_fields(value, allowed, label):
    _require_object(value, label)
    unknown = set(value) - allowed
    missing = allowed - set(value)
    if unknown:
        raise ValueError(f"{label} has unknown fields: {', '.join(sorted(unknown))}")
    if missing:
        raise ValueError(f"{label} is missing fields: {', '.join(sorted(missing))}")


def _require_enum(value, allowed, label):
    if value not in allowed:
        raise ValueError(f"{label} must be one of: {', '.join(sorted(allowed))}")


def _require_timestamp(value, label, nullable=False):
    if nullable and value is None:
        return
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError(f"{label} must be an RFC3339 UTC timestamp ending in Z")
    try:
        dt.datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise ValueError(f"{label} must be a valid timestamp") from error


def validate_record(record):
    """Return a validated record without adding or dropping fields."""
    _require_exact_fields(record, TOP_FIELDS, "record")
    if record["schema_version"] != 1:
        raise ValueError("schema_version must be 1")
    if not isinstance(record["repository"], str) or not REPOSITORY_RE.fullmatch(
        record["repository"]
    ):
        raise ValueError("repository must use owner/name")
    if not isinstance(record["pr"], int) or isinstance(record["pr"], bool) or record["pr"] < 1:
        raise ValueError("pr must be a positive integer")
    _require_timestamp(record["observed_at"], "observed_at")
    for field in ("base_sha", "head_sha", "final_base_sha", "final_head_sha"):
        if not isinstance(record[field], str) or not SHA_RE.fullmatch(record[field]):
            raise ValueError(f"{field} must be a lowercase full SHA")
    _require_enum(record["verdict"], VERDICTS, "verdict")
    _require_enum(
        record["github_review_evidence"],
        GITHUB_REVIEW_EVIDENCE,
        "github_review_evidence",
    )

    linear = record["linear"]
    _require_exact_fields(linear, LINEAR_FIELDS, "linear")
    target_issue = linear["target_issue"]
    if target_issue is not None and (
        not isinstance(target_issue, str) or not ISSUE_RE.fullmatch(target_issue)
    ):
        raise ValueError("linear.target_issue must be null or an INV identifier")
    _require_timestamp(linear["target_updated_at"], "linear.target_updated_at", nullable=True)
    _require_enum(linear["scope"], LINEAR_SCOPES, "linear.scope")
    if (
        not isinstance(linear["reads"], int)
        or isinstance(linear["reads"], bool)
        or linear["reads"] < 0
    ):
        raise ValueError("linear.reads must be a non-negative integer")
    if not isinstance(linear["expansions"], list):
        raise ValueError("linear.expansions must be an array")
    for index, expansion in enumerate(linear["expansions"]):
        label = f"linear.expansions[{index}]"
        _require_exact_fields(expansion, EXPANSION_FIELDS, label)
        if not isinstance(expansion["issue"], str) or not ISSUE_RE.fullmatch(expansion["issue"]):
            raise ValueError(f"{label}.issue must be an INV identifier")
        _require_enum(expansion["reason"], EXPANSION_REASONS, f"{label}.reason")
    if linear["scope"] == "expanded" and not linear["expansions"]:
        raise ValueError("expanded Linear scope requires at least one expansion")
    if linear["scope"] in {"none", "unavailable"} and linear["reads"] != 0:
        raise ValueError("none or unavailable Linear scope requires zero reads")

    checks = record["checks"]
    _require_exact_fields(checks, CHECK_FIELDS, "checks")
    _require_enum(checks["remote"], REMOTE_CHECKS, "checks.remote")
    _require_enum(checks["local"], LOCAL_CHECKS, "checks.local")

    if not isinstance(record["findings"], list):
        raise ValueError("findings must be an array")
    finding_ids = set()
    unresolved_blockers = False
    for index, finding in enumerate(record["findings"]):
        label = f"findings[{index}]"
        _require_exact_fields(finding, FINDING_FIELDS, label)
        if not isinstance(finding["id"], str) or not FINDING_RE.fullmatch(finding["id"]):
            raise ValueError(f"{label}.id must use F<number>")
        if finding["id"] in finding_ids:
            raise ValueError("finding ids must be unique within a review")
        finding_ids.add(finding["id"])
        _require_enum(finding["severity"], SEVERITIES, f"{label}.severity")
        _require_enum(finding["outcome"], OUTCOMES, f"{label}.outcome")
        unresolved_blockers |= (
            finding["outcome"] == "unresolved" and finding["severity"] in {"P0", "P1", "P2"}
        )

    post_merge = record["post_merge"]
    _require_exact_fields(post_merge, POST_MERGE_FIELDS, "post_merge")
    _require_enum(post_merge["status"], POST_MERGE_STATUSES, "post_merge.status")
    _require_timestamp(post_merge["cutoff"], "post_merge.cutoff", nullable=True)
    if post_merge["status"] != "not-observed" and post_merge["cutoff"] is None:
        raise ValueError("an observed post-merge status requires a cutoff")

    changed_identity = (
        record["base_sha"] != record["final_base_sha"]
        or record["head_sha"] != record["final_head_sha"]
    )
    if changed_identity and record["verdict"] != "stale":
        raise ValueError("verdict must be stale when base or head changed")
    if not changed_identity and record["verdict"] == "stale":
        raise ValueError("stale verdict requires a changed base or head")
    if not changed_identity and unresolved_blockers and record["verdict"] != "block":
        raise ValueError("unresolved P0, P1, or P2 findings require a block verdict")
    return record


def _pilot_root(workspace):
    return pathlib.Path(workspace).resolve() / "session-context" / "review-pilot"


def record_review(workspace, record, ledger=None):
    """Append one validated canonical JSON record below the ignored pilot root."""
    validated = validate_record(record)
    workspace_root = pathlib.Path(workspace).resolve()
    pilot_root = _pilot_root(workspace)
    resolved_pilot_root = pilot_root.resolve()
    if resolved_pilot_root != workspace_root and workspace_root not in resolved_pilot_root.parents:
        raise ValueError("session-context/review-pilot resolves outside workspace")
    target = (
        pathlib.Path(ledger).resolve()
        if ledger is not None
        else (resolved_pilot_root / "reviews.jsonl").resolve()
    )
    if target != resolved_pilot_root / "reviews.jsonl" and resolved_pilot_root not in target.parents:
        raise ValueError("ledger must remain below session-context/review-pilot")
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(validated, sort_keys=True, separators=(",", ":"), ensure_ascii=True) + "\n"
    with target.open("a", encoding="utf-8", newline="\n") as stream:
        stream.write(payload)
        stream.flush()
        os.fsync(stream.fileno())
    return target


def load_ledger(path):
    records = []
    with pathlib.Path(path).open(encoding="utf-8") as stream:
        for line_number, line in enumerate(stream, 1):
            if not line.strip():
                continue
            try:
                records.append(validate_record(json.loads(line)))
            except (json.JSONDecodeError, ValueError) as error:
                raise ValueError(f"invalid ledger line {line_number}: {error}") from error
    return records


def summarize(records):
    validated = [validate_record(record) for record in records]
    findings = [finding for record in validated for finding in record["findings"]]
    outcome_counts = Counter(finding["outcome"] for finding in findings)
    severity_counts = Counter(finding["severity"] for finding in findings)
    review_evidence_counts = Counter(record["github_review_evidence"] for record in validated)
    remote_check_counts = Counter(record["checks"]["remote"] for record in validated)
    local_check_counts = Counter(record["checks"]["local"] for record in validated)
    expansion_reason_counts = Counter(
        expansion["reason"]
        for record in validated
        for expansion in record["linear"]["expansions"]
    )
    decided = sum(outcome_counts[outcome] for outcome in DECIDED_OUTCOMES)
    accepted = sum(outcome_counts[outcome] for outcome in ACCEPTED_OUTCOMES)
    false_positives = outcome_counts["withdrawn-false-positive"]
    return {
        "reviewed_prs": len(validated),
        "repositories": sorted({record["repository"] for record in validated}),
        "github_review_evidence": {
            state: review_evidence_counts[state] for state in sorted(GITHUB_REVIEW_EVIDENCE)
        },
        "findings_by_severity": {severity: severity_counts[severity] for severity in sorted(SEVERITIES)},
        "decided_findings": decided,
        "accepted_findings": accepted,
        "false_positive_findings": false_positives,
        "acceptance_rate": accepted / decided if decided else None,
        "false_positive_rate": false_positives / decided if decided else None,
        "unresolved_findings": outcome_counts["unresolved"],
        "indeterminate_findings": outcome_counts["indeterminate"],
        "confirmed_escapes": sum(
            record["post_merge"]["status"] == "confirmed-escape" for record in validated
        ),
        "stale_reviews": sum(record["verdict"] == "stale" for record in validated),
        "stale_base_changes": sum(
            record["base_sha"] != record["final_base_sha"] for record in validated
        ),
        "stale_head_changes": sum(
            record["head_sha"] != record["final_head_sha"] for record in validated
        ),
        "linear_reads": sum(record["linear"]["reads"] for record in validated),
        "linear_target_only_reviews": sum(
            record["linear"]["scope"] == "target-only" for record in validated
        ),
        "linear_expanded_reviews": sum(
            record["linear"]["scope"] == "expanded" for record in validated
        ),
        "linear_expansion_reasons": {
            reason: expansion_reason_counts[reason] for reason in sorted(EXPANSION_REASONS)
        },
        "remote_checks": {state: remote_check_counts[state] for state in sorted(REMOTE_CHECKS)},
        "local_validations": {state: local_check_counts[state] for state in sorted(LOCAL_CHECKS)},
        "head_bound_local_validations": sum(
            record["checks"]["local"] in {"passed", "failed"} for record in validated
        ),
    }


def _read_json(path):
    if path == "-":
        return json.load(sys.stdin)
    with pathlib.Path(path).open(encoding="utf-8") as stream:
        return json.load(stream)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    record_parser = subparsers.add_parser("record", help="validate and append one review record")
    record_parser.add_argument("--workspace", default=str(pathlib.Path(__file__).resolve().parents[1]))
    record_parser.add_argument("--input", required=True, help="JSON file or - for stdin")
    record_parser.add_argument("--ledger")

    summary_parser = subparsers.add_parser("summary", help="summarize an existing ledger")
    summary_parser.add_argument("--workspace", default=str(pathlib.Path(__file__).resolve().parents[1]))
    summary_parser.add_argument("--ledger")

    validate_parser = subparsers.add_parser("validate", help="validate one record without writing")
    validate_parser.add_argument("--input", required=True, help="JSON file or - for stdin")

    args = parser.parse_args(argv)
    try:
        if args.command == "record":
            target = record_review(args.workspace, _read_json(args.input), args.ledger)
            print(target)
        elif args.command == "summary":
            ledger = pathlib.Path(args.ledger) if args.ledger else _pilot_root(args.workspace) / "reviews.jsonl"
            print(json.dumps(summarize(load_ledger(ledger)), indent=2, sort_keys=True))
        else:
            validate_record(_read_json(args.input))
            print("valid")
    except (OSError, ValueError, json.JSONDecodeError) as error:
        parser.error(str(error))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
