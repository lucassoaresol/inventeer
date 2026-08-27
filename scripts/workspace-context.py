#!/usr/bin/env python3
"""Plan, measure, and check deterministic workspace context routes."""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Sequence


ROUTE_NAMES = (
    "portal-task",
    "assistants-task",
    "pr-review",
    "cycle-triage",
    "delivery-front",
    "project-discovery",
)
ESTIMATOR = {
    "unit": "unicode-code-points",
    "code_points_per_estimated_token": 4,
}
HEADING_RE = re.compile(r"^(#{1,6}) .+")


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
        raise ContextError(f"{location} is unsafe")
    return path


def resolve_file(root: pathlib.Path, value: Any, location: str) -> pathlib.Path:
    relative = safe_relative_path(value, location)
    try:
        resolved = root.joinpath(*relative.parts).resolve(strict=True)
        resolved.relative_to(root.resolve(strict=True))
    except (OSError, ValueError) as error:
        raise ContextError(f"{location} escapes or is missing") from error
    if not resolved.is_file():
        raise ContextError(f"{location} is not a regular file")
    return resolved


def read_source(path: pathlib.Path, location: str) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as error:
        raise ContextError(f"{location} is not readable UTF-8 text") from error


def heading_level(line: str) -> int | None:
    match = HEADING_RE.fullmatch(line)
    return len(match.group(1)) if match else None


def select_headings(text: str, headings: Sequence[str], location: str) -> str:
    if not headings:
        return text
    lines = text.splitlines(keepends=True)
    selected: list[str] = []
    for heading in headings:
        indexes = [index for index, line in enumerate(lines) if line.rstrip("\r\n") == heading]
        if len(indexes) != 1:
            raise ContextError(f"{location} heading must exist exactly once")
        start = indexes[0]
        level = heading_level(heading)
        if level is None:
            raise ContextError(f"{location} heading is malformed")
        end = len(lines)
        for index in range(start + 1, len(lines)):
            candidate_level = heading_level(lines[index].rstrip("\r\n"))
            if candidate_level is not None and candidate_level <= level:
                end = index
                break
        selected.extend(lines[start:end])
    return "".join(selected)


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
    exact_keys(manifest, {"version", "estimator", "routes"}, "manifest")
    if manifest["version"] != 2:
        raise ContextError("manifest.version must be 2")
    if manifest["estimator"] != ESTIMATOR:
        raise ContextError("manifest.estimator must match the approved estimator")
    routes = manifest["routes"]
    if not isinstance(routes, list):
        raise ContextError("manifest.routes must be an array")
    names = tuple(route.get("name") for route in routes if isinstance(route, dict))
    if names != ROUTE_NAMES or len(routes) != len(ROUTE_NAMES):
        raise ContextError("routes must use the approved order")

    for route_index, route in enumerate(routes):
        location = f"routes[{route_index}]"
        if not isinstance(route, dict):
            raise ContextError(f"{location} must be an object")
        exact_keys(route, {"name", "budget_estimated_tokens", "references"}, location)
        budget = route["budget_estimated_tokens"]
        if not isinstance(budget, int) or isinstance(budget, bool) or budget <= 0:
            raise ContextError(f"{location}.budget_estimated_tokens must be a positive integer")
        references = route["references"]
        if not isinstance(references, list) or not references:
            raise ContextError(f"{location}.references must be a non-empty array")
        seen_sources: set[str] = set()
        for reference_index, reference in enumerate(references):
            reference_location = f"{location}.references[{reference_index}]"
            if not isinstance(reference, dict):
                raise ContextError(f"{reference_location} must be an object")
            exact_keys(reference, {"source", "headings", "reason", "gate"}, reference_location)
            source = reference["source"]
            if source in seen_sources:
                raise ContextError(f"{reference_location}.source is duplicated")
            seen_sources.add(source)
            source_path = resolve_file(root, source, f"{reference_location}.source")
            headings = reference["headings"]
            if (
                not isinstance(headings, list)
                or len(headings) != len(set(headings))
                or any(not isinstance(heading, str) or heading_level(heading) is None for heading in headings)
                or (headings and not source.endswith(".md"))
            ):
                raise ContextError(f"{reference_location}.headings are invalid")
            selected = select_headings(
                read_source(source_path, f"{reference_location}.source"),
                headings,
                reference_location,
            )
            if headings and not selected:
                raise ContextError(f"{reference_location}.headings select no content")
            for field in ("reason", "gate"):
                if not isinstance(reference[field], str) or not reference[field].strip():
                    raise ContextError(f"{reference_location}.{field} must be non-empty")


def route_by_name(manifest: dict[str, Any], route_name: str) -> dict[str, Any]:
    routes = {route["name"]: route for route in manifest["routes"]}
    try:
        return routes[route_name]
    except KeyError as error:
        raise ContextError(f"unknown route: {route_name}") from error


def plan_route(manifest: dict[str, Any], route_name: str) -> dict[str, Any]:
    route = route_by_name(manifest, route_name)
    return {
        "route": route["name"],
        "estimator": manifest["estimator"],
        "budget_estimated_tokens": route["budget_estimated_tokens"],
        "references": route["references"],
    }


def estimate_tokens(characters: int, ratio: int) -> int:
    return (characters + ratio - 1) // ratio


def measure_route(root: pathlib.Path, manifest: dict[str, Any], route_name: str) -> dict[str, Any]:
    route = route_by_name(manifest, route_name)
    ratio = manifest["estimator"]["code_points_per_estimated_token"]
    sources: list[dict[str, Any]] = []
    total_characters = 0
    for index, reference in enumerate(route["references"]):
        source_path = resolve_file(root, reference["source"], f"references[{index}].source")
        selected = select_headings(
            read_source(source_path, f"references[{index}].source"),
            reference["headings"],
            f"references[{index}]",
        )
        characters = len(selected)
        total_characters += characters
        sources.append(
            {
                "source": reference["source"],
                "headings": reference["headings"],
                "characters": characters,
                "estimated_tokens": estimate_tokens(characters, ratio),
            }
        )
    estimated_tokens = estimate_tokens(total_characters, ratio)
    budget = route["budget_estimated_tokens"]
    return {
        "route": route["name"],
        "estimator": manifest["estimator"],
        "budget_estimated_tokens": budget,
        "sources": sources,
        "total_characters": total_characters,
        "estimated_tokens": estimated_tokens,
        "status": "pass" if estimated_tokens <= budget else "fail",
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=pathlib.Path, default=pathlib.Path(__file__).resolve().parents[1])
    parser.add_argument("--manifest", default=".specs/context/routes.json")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("audit")
    for command in ("plan", "measure"):
        subcommand = commands.add_parser(command)
        subcommand.add_argument("--route", required=True)
    commands.add_parser("check")
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
    if args.command == "plan":
        print(json.dumps(plan_route(manifest, args.route), indent=2))
        return 0
    if args.command == "measure":
        report = measure_route(root, manifest, args.route)
        print(json.dumps(report, indent=2))
        return 0 if report["status"] == "pass" else 1

    reports = [measure_route(root, manifest, route_name) for route_name in ROUTE_NAMES]
    status = "pass" if all(report["status"] == "pass" for report in reports) else "fail"
    print(json.dumps({"status": status, "routes": reports}, indent=2))
    return 0 if status == "pass" else 1


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except ContextError as error:
        print(f"workspace-context: {error}", file=sys.stderr)
        raise SystemExit(2)
