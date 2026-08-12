#!/usr/bin/env python3
"""Validate and print deterministic reference-only workspace context plans."""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
from typing import Any


ROUTE_NAMES = (
    "portal-task",
    "assistants-task",
    "pr-review",
    "cycle-triage",
    "delivery-front",
)


class ContextError(ValueError):
    """The manifest or requested route violates the context contract."""


def exact_keys(value: dict[str, Any], expected: set[str], location: str) -> None:
    if set(value) != expected:
        raise ContextError(f"{location} has unknown or missing fields")


def safe_relative_path(value: Any, location: str) -> pathlib.PurePosixPath:
    if not isinstance(value, str) or not value:
        raise ContextError(f"{location} must be a non-empty relative path")
    path = pathlib.PurePosixPath(value)
    if (
        path.is_absolute()
        or value != path.as_posix()
        or any(part in {"", ".", ".."} for part in path.parts)
        or any(character in value for character in "*?[]\\")
    ):
        raise ContextError(f"{location} is unsafe: {value}")
    return path


def resolve_file(root: pathlib.Path, value: Any, location: str) -> None:
    relative = safe_relative_path(value, location)
    try:
        resolved = root.joinpath(*relative.parts).resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise ContextError(f"{location} escapes or is missing: {value}") from error
    if not resolved.is_file():
        raise ContextError(f"{location} is not a regular file: {value}")


def load_manifest(root: pathlib.Path, relative_manifest: str) -> dict[str, Any]:
    relative = safe_relative_path(relative_manifest, "manifest")
    path = root.joinpath(*relative.parts)
    try:
        resolved = path.resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
        manifest = json.loads(resolved.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as error:
        raise ContextError("manifest is unavailable or invalid JSON") from error
    if not isinstance(manifest, dict):
        raise ContextError("manifest must be an object")
    return manifest


def validate_manifest(root: pathlib.Path, manifest: dict[str, Any]) -> None:
    exact_keys(manifest, {"version", "routes"}, "manifest")
    if manifest["version"] != 1:
        raise ContextError("manifest.version must be 1")
    routes = manifest["routes"]
    if not isinstance(routes, list):
        raise ContextError("manifest.routes must be an array")
    names = tuple(route.get("name") for route in routes if isinstance(route, dict))
    if names != ROUTE_NAMES or len(routes) != len(ROUTE_NAMES):
        raise ContextError(f"routes must be ordered exactly as {ROUTE_NAMES}")

    for route_index, route in enumerate(routes):
        location = f"routes[{route_index}]"
        if not isinstance(route, dict):
            raise ContextError(f"{location} must be an object")
        exact_keys(route, {"name", "references"}, location)
        references = route["references"]
        if not isinstance(references, list) or not references:
            raise ContextError(f"{location}.references must be a non-empty array")
        seen_sources: set[str] = set()
        for reference_index, reference in enumerate(references):
            reference_location = f"{location}.references[{reference_index}]"
            if not isinstance(reference, dict):
                raise ContextError(f"{reference_location} must be an object")
            exact_keys(reference, {"source", "section", "reason", "gate"}, reference_location)
            source = reference["source"]
            if source in seen_sources:
                raise ContextError(f"{reference_location}.source is duplicated: {source}")
            seen_sources.add(source)
            resolve_file(root, source, f"{reference_location}.source")
            section = reference["section"]
            if section is not None and (not isinstance(section, str) or not section.startswith("#")):
                raise ContextError(f"{reference_location}.section must be null or a Markdown heading")
            for field in ("reason", "gate"):
                if not isinstance(reference[field], str) or not reference[field].strip():
                    raise ContextError(f"{reference_location}.{field} must be non-empty")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", default=".specs/context/routes.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("audit")
    plan = commands.add_parser("plan")
    plan.add_argument("--route", required=True)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve(strict=True)
    manifest = load_manifest(root, args.manifest)
    validate_manifest(root, manifest)
    if args.command == "audit":
        reference_count = sum(len(route["references"]) for route in manifest["routes"])
        print(f"ok - {len(manifest['routes'])} routes, {reference_count} references")
        return 0

    routes = {route["name"]: route for route in manifest["routes"]}
    if args.route not in routes:
        raise ContextError(f"unknown route: {args.route}")
    route = routes[args.route]
    print(json.dumps({"route": route["name"], "references": route["references"]}, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContextError as error:
        print(f"workspace-context: {error}", file=sys.stderr)
        raise SystemExit(2)
