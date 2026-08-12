#!/usr/bin/env python3
"""Run and query sanitized same-state evidence for the root workspace gate."""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import pathlib
import re
import stat
import subprocess
import sys
import tempfile
import time
from collections.abc import Callable, Sequence
from typing import Any


SCHEMA = 1
PROFILE = "workspace"
STORE_RELATIVE = pathlib.Path("session-context/runtime/workspace-gate-evidence-v1.json")
GATE_RELATIVE = pathlib.Path("scripts/test-workspace.sh")
RECEIPT_FIELDS = {
    "schema",
    "profile",
    "result",
    "exit_code",
    "duration_ms",
    "completed_at",
    "state_sha256",
    "contract_sha256",
}
RESULTS = {"passed", "failed", "interrupted", "state-changed"}
HASH = re.compile(r"[0-9a-f]{64}")


class EvidenceError(RuntimeError):
    """Evidence storage or content violates the closed local contract."""


class RepositoryUnavailable(EvidenceError):
    """A complete stable workspace identity cannot be captured."""


def run_git(root: pathlib.Path, *args: str) -> bytes:
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=root,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            check=False,
        )
    except OSError as error:
        raise RepositoryUnavailable from error
    if result.returncode != 0:
        raise RepositoryUnavailable
    return result.stdout


def resolve_root(value: pathlib.Path | str) -> pathlib.Path:
    try:
        root = pathlib.Path(value).resolve(strict=True)
    except OSError as error:
        raise RepositoryUnavailable from error
    if not root.is_dir():
        raise RepositoryUnavailable
    observed = pathlib.Path(os.fsdecode(run_git(root, "rev-parse", "--show-toplevel").strip())).resolve()
    if observed != root:
        raise RepositoryUnavailable
    return root


def filesystem_entry(root: pathlib.Path, raw_path: bytes) -> bytes:
    relative = pathlib.PurePath(os.fsdecode(raw_path))
    if relative.is_absolute() or ".." in relative.parts:
        raise RepositoryUnavailable
    path = root.joinpath(*relative.parts)
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return b"missing"
    except OSError as error:
        raise RepositoryUnavailable from error
    mode = stat.S_IMODE(metadata.st_mode).to_bytes(4, "big")
    if stat.S_ISREG(metadata.st_mode):
        try:
            content = path.read_bytes()
        except OSError as error:
            raise RepositoryUnavailable from error
        kind = b"file"
    elif stat.S_ISLNK(metadata.st_mode):
        try:
            content = os.fsencode(os.readlink(path))
        except OSError as error:
            raise RepositoryUnavailable from error
        kind = b"symlink"
    else:
        raise RepositoryUnavailable
    return b"".join((kind, mode, len(content).to_bytes(8, "big"), content))


def frame(*parts: bytes) -> bytes:
    return b"".join(len(part).to_bytes(8, "big") + part for part in parts)


def capture_once(root: pathlib.Path) -> bytes:
    head = run_git(root, "rev-parse", "--verify", "HEAD").strip()
    staged = run_git(root, "ls-files", "--stage", "-z")
    tracked_entries = []
    for record in sorted(filter(None, staged.split(b"\0"))):
        try:
            metadata, raw_path = record.split(b"\t", 1)
            _mode, _object_id, stage = metadata.split(b" ")
        except ValueError as error:
            raise RepositoryUnavailable from error
        if stage != b"0":
            raise RepositoryUnavailable
        tracked_entries.append(frame(record, filesystem_entry(root, raw_path)))

    untracked_entries = []
    untracked = run_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    for raw_path in sorted(filter(None, untracked.split(b"\0"))):
        untracked_entries.append(frame(raw_path, filesystem_entry(root, raw_path)))
    return frame(head, b"".join(tracked_entries), b"".join(untracked_entries))


def state_identity(root: pathlib.Path | str) -> str:
    resolved = resolve_root(root)
    first = capture_once(resolved)
    second = capture_once(resolved)
    if first != second:
        raise RepositoryUnavailable
    return hashlib.sha256(first).hexdigest()


def contract_identity(root: pathlib.Path | str) -> str:
    resolved = resolve_root(root)
    gate = resolved / GATE_RELATIVE
    try:
        gate_content = gate.read_bytes()
        module_content = pathlib.Path(__file__).read_bytes()
    except OSError as error:
        raise RepositoryUnavailable from error
    metadata = json.dumps(
        {"schema": SCHEMA, "profile": PROFILE, "argv": ["bash", GATE_RELATIVE.as_posix()]},
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(frame(metadata, module_content, gate_content)).hexdigest()


def store_path(root: pathlib.Path) -> pathlib.Path:
    return root / STORE_RELATIVE


def ensure_store_directory(root: pathlib.Path) -> pathlib.Path:
    current = root
    for part in STORE_RELATIVE.parent.parts:
        current = current / part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            try:
                current.mkdir(mode=0o700)
            except OSError as error:
                raise EvidenceError from error
            metadata = current.lstat()
        except OSError as error:
            raise EvidenceError from error
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise EvidenceError
    return current


def validate_receipt(value: Any) -> dict[str, Any]:
    if not isinstance(value, dict) or set(value) != RECEIPT_FIELDS:
        raise EvidenceError
    if value["schema"] != SCHEMA or value["profile"] != PROFILE or value["result"] not in RESULTS:
        raise EvidenceError
    exit_code = value["exit_code"]
    duration = value["duration_ms"]
    if (
        not isinstance(exit_code, int)
        or isinstance(exit_code, bool)
        or not 0 <= exit_code <= 255
        or not isinstance(duration, int)
        or isinstance(duration, bool)
        or duration < 0
    ):
        raise EvidenceError
    if (value["result"] == "passed") != (exit_code == 0):
        raise EvidenceError
    if value["result"] == "state-changed" and exit_code != 1:
        raise EvidenceError
    completed = value["completed_at"]
    if not isinstance(completed, str) or not completed.endswith("Z"):
        raise EvidenceError
    try:
        parsed = dt.datetime.fromisoformat(completed.removesuffix("Z") + "+00:00")
    except ValueError as error:
        raise EvidenceError from error
    if parsed.utcoffset() != dt.timedelta(0):
        raise EvidenceError
    for field in ("state_sha256", "contract_sha256"):
        if not isinstance(value[field], str) or HASH.fullmatch(value[field]) is None:
            raise EvidenceError
    return value


def write_receipt(root: pathlib.Path, receipt: dict[str, Any]) -> None:
    validate_receipt(receipt)
    directory = ensure_store_directory(root)
    target = store_path(root)
    try:
        if target.is_symlink():
            raise EvidenceError
        descriptor, temporary_name = tempfile.mkstemp(
            prefix=".workspace-gate-evidence.",
            dir=directory,
        )
    except OSError as error:
        raise EvidenceError from error
    temporary = pathlib.Path(temporary_name)
    try:
        os.fchmod(descriptor, 0o600)
        payload = (json.dumps(receipt, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
        with os.fdopen(descriptor, "wb") as stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, target)
        target.chmod(0o600)
    except OSError as error:
        raise EvidenceError from error
    finally:
        temporary.unlink(missing_ok=True)


def read_receipt(root: pathlib.Path) -> dict[str, Any] | None:
    target = store_path(root)
    current = root
    for part in STORE_RELATIVE.parent.parts:
        current = current / part
        try:
            parent_metadata = current.lstat()
        except FileNotFoundError:
            return None
        except OSError as error:
            raise EvidenceError from error
        if stat.S_ISLNK(parent_metadata.st_mode) or not stat.S_ISDIR(parent_metadata.st_mode):
            raise EvidenceError
    try:
        flags = os.O_RDONLY
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        descriptor = os.open(target, flags)
    except FileNotFoundError:
        return None
    except OSError as error:
        raise EvidenceError from error
    try:
        metadata = os.fstat(descriptor)
        if (
            not stat.S_ISREG(metadata.st_mode)
            or stat.S_IMODE(metadata.st_mode) != 0o600
            or metadata.st_size > 65536
        ):
            raise EvidenceError
        with os.fdopen(descriptor, "rb") as stream:
            descriptor = -1
            payload = stream.read()
        value = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        raise EvidenceError from error
    finally:
        if descriptor >= 0:
            os.close(descriptor)
    return validate_receipt(value)


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def default_child(root: pathlib.Path) -> int:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        ["bash", GATE_RELATIVE.as_posix()],
        cwd=root,
        env=environment,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    return result.returncode


def execute_gate(
    root: pathlib.Path | str,
    *,
    run_child: Callable[[pathlib.Path], int] = default_child,
) -> int:
    resolved = resolve_root(root)
    before = state_identity(resolved)
    contract = contract_identity(resolved)
    started = time.monotonic_ns()
    try:
        child_code = run_child(resolved)
        if not isinstance(child_code, int) or isinstance(child_code, bool):
            child_code = 1
        if child_code < 0:
            result = "interrupted"
            exit_code = 128 + min(abs(child_code), 127)
        else:
            exit_code = min(child_code, 255)
            result = "passed" if exit_code == 0 else "failed"
    except KeyboardInterrupt:
        result = "interrupted"
        exit_code = 130

    try:
        after = state_identity(resolved)
    except RepositoryUnavailable:
        after = before
        result = "state-changed"
        exit_code = 1
    if after != before:
        result = "state-changed"
        exit_code = 1

    duration_ms = max(0, (time.monotonic_ns() - started) // 1_000_000)
    receipt = {
        "schema": SCHEMA,
        "profile": PROFILE,
        "result": result,
        "exit_code": exit_code,
        "duration_ms": duration_ms,
        "completed_at": utc_now(),
        "state_sha256": after,
        "contract_sha256": contract,
    }
    write_receipt(resolved, receipt)
    return exit_code


def status(root: pathlib.Path | str, *, require_fresh: bool = False) -> tuple[str, str, int]:
    try:
        resolved = resolve_root(root)
        current = read_receipt(resolved)
    except RepositoryUnavailable:
        return "rerun-required", "repository-unavailable", 2
    except EvidenceError:
        return "rerun-required", "evidence-invalid", 2
    if current is None:
        return "rerun-required", "evidence-missing", 1
    try:
        contract = contract_identity(resolved)
        if current["contract_sha256"] != contract:
            return "rerun-required", "contract-changed", 1
        state_hash = state_identity(resolved)
        if current["state_sha256"] != state_hash:
            return "rerun-required", "state-changed", 1
    except RepositoryUnavailable:
        return "rerun-required", "repository-unavailable", 2
    if current["result"] != "passed":
        return "rerun-required", "latest-not-passed", 1
    if require_fresh:
        return "rerun-required", "fresh-required", 1
    return "reusable", "match", 0


def print_json(value: dict[str, Any]) -> None:
    print(json.dumps(value, sort_keys=True, separators=(",", ":")))


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run")
    run.add_argument("--profile", choices=(PROFILE,), required=True)
    query = commands.add_parser("status")
    query.add_argument("--profile", choices=(PROFILE,), required=True)
    query.add_argument("--require-fresh", action="store_true")
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    if args.command == "status":
        state, reason, exit_code = status(args.root, require_fresh=args.require_fresh)
        print_json({"schema": SCHEMA, "profile": PROFILE, "state": state, "reason": reason})
        return exit_code
    try:
        exit_code = execute_gate(args.root)
        result = read_receipt(resolve_root(args.root))["result"]
    except RepositoryUnavailable:
        print("workspace-gate-evidence: repository-unavailable", file=sys.stderr)
        return 2
    except EvidenceError:
        print("workspace-gate-evidence: evidence-write-failed", file=sys.stderr)
        return 2
    print_json({"schema": SCHEMA, "profile": PROFILE, "result": result})
    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
