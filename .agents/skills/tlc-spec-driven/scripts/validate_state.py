#!/usr/bin/env python3
"""
validate_state.py - deterministic completion gate for a feature.

The skill's strongest invariant is "the Verifier is always-on, never prompted;
Execute is not done until validation.md reports PASS." That is prose the model
must remember. This turns it into a checkable pass/fail the closing step runs
automatically, so declaring a feature done without a real Verifier report fails
loudly instead of slipping through.

It does NOT merely check that validation.md exists - a report that exists but is
empty, still holds the template placeholder, or has no evidence would pass a
shallow existence check while proving nothing. This gate requires a real,
filled verdict plus at least one file:line evidence citation.

Operates only on the .specs/ markdown artifacts (stack- and tool-agnostic). No
dependencies. Run from the project root (the dir that contains .specs), or pass
--root. Meant to be invoked by the skill as the closing gate of Execute, the
same way lessons.py is invoked at distillation - not a manual step.

Usage:
  python3 <skill-dir>/scripts/validate_state.py [feature]
  python3 <skill-dir>/scripts/validate_state.py

  Invoke from the skill directory that ships this script (not the project root).
  Pass --root when cwd is not the project that contains .specs/.

Exit codes: 0 ok, 1 a completed feature is missing a real PASS report,
            2 usage error.
"""

import argparse
import os
import re
import sys

# A file:line citation: a path with an extension, then :<line>. e.g. src/a.ts:42
EVIDENCE_RE = re.compile(r"[\w./-]+\.[A-Za-z0-9]+:\d+")
PROVENANCE_MODES = frozenset({"independent-agent", "standalone-fallback"})
PLACEHOLDER_RE = re.compile(r"(?:^[-–—]?$|\b(?:todo|tbd|none|placeholder)\b|\[[^]]*\]|<[^>]*>)", re.IGNORECASE)


def _feature_dirs(root):
    base = os.path.join(root, ".specs", "features")
    if not os.path.isdir(base):
        return base, []
    dirs = [
        d for d in sorted(os.listdir(base))
        if os.path.isdir(os.path.join(base, d))
    ]
    return base, dirs


def _verdict(text):
    """Return 'pass', 'fail', 'unfilled', or None from a validation report."""
    lines = text.splitlines()

    def outcome(candidates):
        hay = " ".join(candidates)
        has_pass = re.search(r"\bPASS\b", hay, re.IGNORECASE) is not None
        has_fail = re.search(r"\bFAIL\b", hay, re.IGNORECASE) is not None
        if has_pass and has_fail:
            return "unfilled"
        if has_pass:
            return "pass"
        if has_fail:
            return "fail"
        return None

    explicit = []
    fallback = []
    for line in lines:
        stripped = line.strip()
        plain = re.sub(r"[*_`]", "", stripped)
        if re.search(r"^#{1,4}\s*validation\b", plain, re.IGNORECASE):
            if outcome([plain]) is not None:
                explicit.append(plain)
            continue
        if re.search(r"^(?:overall|verdict|validation status)\s*:", plain, re.IGNORECASE):
            explicit.append(plain)
            continue
        if re.search(r"^result\s*:", plain, re.IGNORECASE):
            fallback.append(plain)

    selected = explicit if explicit else fallback
    if selected:
        return outcome(selected)

    has_pass = re.search(r"\bPASS\b", text, re.IGNORECASE) is not None
    has_fail = re.search(r"\bFAIL\b", text, re.IGNORECASE) is not None
    if has_pass and has_fail:
        # Both present on the verdict line = unfilled template "[PASS | FAIL]".
        return "unfilled"
    if has_pass:
        return "pass"
    if has_fail:
        return "fail"
    return None


def _appears_complete(fdir):
    """Conservative completeness heuristic for the cross-check mode.

    A feature 'appears complete' if it already has a validation.md, or if it has
    a tasks.md with at least one task and no unchecked '- [ ]' boxes left. When
    the signal is ambiguous (no tasks.md, Tasks phase skipped), returns False so
    an in-flight feature is never falsely flagged.
    """
    if os.path.exists(os.path.join(fdir, "validation.md")):
        return True
    tasks = os.path.join(fdir, "tasks.md")
    if not os.path.exists(tasks):
        return False
    body = open(tasks, encoding="utf-8", errors="replace").read()
    if not re.search(r"^#{2,4}\s+T\d+\s*:", body, re.MULTILINE):
        return False
    if re.search(r"^\s*-\s*\[\s\]", body, re.MULTILINE):
        return False  # unchecked box remains -> still in progress
    return True


def _field(text, label):
    """Return a Markdown metadata field with emphasis/backticks removed."""
    for line in text.splitlines():
        plain = re.sub(r"[*_`]", "", line.strip())
        match = re.match(rf"^{re.escape(label)}\s*:\s*(.*)$", plain, re.IGNORECASE)
        if match:
            return match.group(1).strip()
    return None


def _real_value(value):
    return bool(value and len(value) >= 12 and not PLACEHOLDER_RE.search(value))


def _provenance_errors(text, name):
    errors = []
    mode = _field(text, "Verifier mode")
    evidence = _field(text, "Verifier evidence")
    fallback_reason = _field(text, "Fallback reason")
    if mode not in PROVENANCE_MODES:
        errors.append(
            f"{name}: Verifier mode must be one of {sorted(PROVENANCE_MODES)}, got {mode!r}"
        )
        return errors
    if not _real_value(evidence):
        errors.append(
            f"{name}: Verifier evidence is missing or placeholder; record the independent execution evidence"
        )
    if mode == "standalone-fallback" and not _real_value(fallback_reason):
        errors.append(
            f"{name}: Fallback reason is required for standalone-fallback and must name the unavailable capability"
        )
    return errors


def _check_feature(fdir, name, *, require_provenance=False):
    """Return list of error strings for one feature (empty = pass)."""
    errors = []
    vpath = os.path.join(fdir, "validation.md")
    if not os.path.exists(vpath):
        errors.append(
            f"{name}: no validation.md - Execute is not done until the Verifier "
            f"writes it (author != verifier). Dispatch validation before marking done."
        )
        return errors
    text = open(vpath, encoding="utf-8", errors="replace").read()
    verdict = _verdict(text)
    if verdict is None:
        errors.append(f"{name}: validation.md has no PASS/FAIL verdict (a prose-only report does not count)")
    elif verdict == "unfilled":
        errors.append(f"{name}: validation.md verdict is still the template placeholder '[PASS | FAIL]' - not filled")
    elif verdict == "fail":
        errors.append(f"{name}: validation.md verdict is FAIL - route the ranked gaps to fix tasks, then re-verify (feature is not done)")
    if verdict == "pass" and not EVIDENCE_RE.search(text):
        errors.append(f"{name}: validation.md is PASS but cites no file:line evidence - evidence-or-zero not satisfied")
    if verdict == "pass" and require_provenance:
        errors.extend(_provenance_errors(text, name))
    return errors


def _resolve(root, feature):
    base, dirs = _feature_dirs(root)
    if not os.path.isdir(base):
        print(f"validate_state: no {base} directory - nothing to check.")
        return []
    if feature:
        fdir = feature if os.path.isdir(feature) else os.path.join(base, feature)
        if not os.path.isdir(fdir):
            print(f"validate_state: feature not found: {feature}", file=sys.stderr)
            raise SystemExit(2)
        return [(fdir, os.path.basename(fdir.rstrip("/")))]
    if len(dirs) == 1:
        return [(os.path.join(base, dirs[0]), dirs[0])]
    if not dirs:
        print("validate_state: no features under .specs/features/ - nothing to check.")
        return []
    # Cross-check mode: only features that appear complete.
    picked = [(os.path.join(base, d), d) for d in dirs if _appears_complete(os.path.join(base, d))]
    if not picked:
        print("validate_state: no completed feature detected (all in progress) - nothing to gate.")
    return picked


def main(argv=None):
    p = argparse.ArgumentParser(prog="validate_state.py", description="Deterministic completion gate: a done feature must have a real PASS validation report.")
    p.add_argument("feature", nargs="?", default=None, help="Feature dir or name (default: sole feature, else cross-check all completed)")
    p.add_argument("--root", default=".", help="Project root containing .specs/ (default: current dir)")
    args = p.parse_args(argv)
    root = os.path.abspath(args.root)

    targets = _resolve(root, args.feature)
    all_errors = []
    for fdir, name in targets:
        all_errors += _check_feature(
            fdir, name, require_provenance=args.feature is not None
        )

    for e in all_errors:
        print(f"  ERROR {e}")
    n = len(all_errors)
    checked = ", ".join(name for _, name in targets) or "(none)"
    print(f"\nvalidate_state: {n} error(s) across [{checked}]")
    return 1 if n else 0


if __name__ == "__main__":
    raise SystemExit(main())
