#!/usr/bin/env python3
"""Reject high-confidence sensitive or unsuitable blobs in the staged Git index."""

from __future__ import annotations

import argparse
import pathlib
import re
import subprocess
import sys


MAX_BLOB_SIZE = 5 * 1024 * 1024
PRIVATE_KEY = re.compile(br"-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----")
CREDENTIAL_TOKENS = (
    re.compile(br"github_pat_[A-Za-z0-9_]{30,}"),
    re.compile(br"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(br"AKIA[0-9A-Z]{16}"),
    re.compile(br"xox[baprs]-[A-Za-z0-9-]{20,}"),
    re.compile(br"sk_live_[A-Za-z0-9]{20,}"),
)
FORBIDDEN_NAMES = {"id_rsa", "id_ed25519", "credentials.json", "secrets.json"}
FORBIDDEN_SUFFIXES = {".pem", ".key", ".p12", ".pfx", ".dump"}
ENV_TEMPLATES = (".example", ".sample", ".template")


class GuardError(RuntimeError):
    """Git index inspection failed before a safe result could be produced."""


def run_git(repo: pathlib.Path, *args: str) -> subprocess.CompletedProcess[bytes]:
    return subprocess.run(
        ["git", *args],
        cwd=repo,
        capture_output=True,
        check=False,
    )


def staged_paths(repo: pathlib.Path) -> list[str]:
    result = run_git(repo, "diff", "--cached", "--name-only", "--diff-filter=ACMR", "-z")
    if result.returncode != 0:
        raise GuardError
    paths = []
    for encoded in result.stdout.rstrip(b"\0").split(b"\0") if result.stdout else []:
        try:
            path = encoded.decode("utf-8", errors="strict")
        except UnicodeDecodeError as error:
            raise GuardError("unsafe-path") from error
        if any(ord(character) < 32 or ord(character) == 127 for character in path):
            raise GuardError("unsafe-path")
        paths.append(path)
    return paths


def staged_blob(repo: pathlib.Path, path: str) -> bytes:
    entry = run_git(repo, "ls-files", "--stage", "-z", "--", path)
    if entry.returncode != 0 or not entry.stdout:
        raise GuardError
    record = entry.stdout.split(b"\0", 1)[0]
    try:
        metadata, encoded_path = record.split(b"\t", 1)
        mode, object_id, stage = metadata.split(b" ")
    except ValueError as error:
        raise GuardError from error
    if stage != b"0" or encoded_path.decode("utf-8", errors="strict") != path or not mode:
        raise GuardError
    blob = run_git(repo, "cat-file", "blob", object_id.decode("ascii"))
    if blob.returncode != 0:
        raise GuardError
    return blob.stdout


def forbidden_path(path: str) -> bool:
    name = pathlib.PurePosixPath(path).name.lower()
    if name == ".env" or (name.startswith(".env.") and not name.endswith(ENV_TEMPLATES)):
        return True
    return name in FORBIDDEN_NAMES or any(name.endswith(suffix) for suffix in FORBIDDEN_SUFFIXES)


def violation(path: str, blob: bytes) -> str | None:
    if forbidden_path(path):
        return "forbidden-path"
    if len(blob) > MAX_BLOB_SIZE:
        return "oversized"
    if b"\0" in blob:
        return "binary"
    if PRIVATE_KEY.search(blob):
        return "private-key"
    if any(pattern.search(blob) for pattern in CREDENTIAL_TOKENS):
        return "credential-token"
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    repo = parse_args().repo.resolve()
    try:
        paths = staged_paths(repo)
        violations = []
        for path in paths:
            reason = violation(path, staged_blob(repo, path))
            if reason:
                violations.append((path, reason))
    except GuardError as error:
        if error.args == ("unsafe-path",):
            print("staged-content: staged path is unsafe [unsafe-path]", file=sys.stderr)
        else:
            print("staged-content: could not inspect Git index [git-error]", file=sys.stderr)
        return 1

    if violations:
        for path, reason in violations:
            print(f"staged-content: {path} [{reason}]", file=sys.stderr)
        return 1
    noun = "file" if len(paths) == 1 else "files"
    print(f"staged-content: PASS ({len(paths)} {noun})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
