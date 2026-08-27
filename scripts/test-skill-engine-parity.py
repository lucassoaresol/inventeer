#!/usr/bin/env python3
"""Assert that every local skill is reachable and executable from both engines.

AD-024 declares this workspace dual-engine, but nothing verified it: the Codex surface is
`.agents/skills/<name>/` plus `agents/openai.yaml`, while the Claude surface is the relative symlink
under `.claude/skills/`. A skill can lose one surface, or declare a tool dependency that only one
engine configures, and no existing suite notices - five of the eight skills had never run under
Claude at all when this check was written.
"""

import json
import pathlib
import re
import sys
import tomllib

try:
    import yaml
except ModuleNotFoundError:  # pragma: no cover - environment guard
    # The manifests are YAML by the Codex skill contract, so this suite needs a real parser rather
    # than a regex that would silently accept a malformed file.
    sys.exit("skill-engine-parity: PyYAML is required; install it with 'pip install pyyaml'")

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILL_ROOT = ROOT / ".agents/skills"
CLAUDE_ROOT = ROOT / ".claude/skills"
VENDOR = ROOT / ".agents/vendor.json"
ROUTES = ROOT / ".specs/context/routes.json"
MCP_CLAUDE = ROOT / ".mcp.json"
MCP_CODEX = ROOT / ".codex/config.toml"
CLAUDE_DOC = ROOT / "CLAUDE.md"

passed = 0


def ok(message: str) -> None:
    global passed
    passed += 1
    print(f"ok {passed} - {message}")


def fail(message: str) -> None:
    raise AssertionError(message)


vendored = set(json.loads(VENDOR.read_text(encoding="utf-8")))
local_skills = sorted(
    path.name
    for path in SKILL_ROOT.iterdir()
    if path.is_dir() and not path.name.startswith("apex-")
)
authored = [name for name in local_skills if name not in vendored]
if not authored:
    fail("no authored skills found; the parity check would pass vacuously")

# --- Superfície das duas engines ---------------------------------------------

for name in authored:
    manifest = SKILL_ROOT / name / "agents/openai.yaml"
    if not manifest.is_file():
        fail(f"{name} has no agents/openai.yaml, so the Codex surface is missing")
    link = CLAUDE_ROOT / name
    if not link.is_symlink():
        fail(f"{name} has no .claude/skills symlink, so the Claude surface is missing")
for name in vendored:
    if (SKILL_ROOT / name / "agents/openai.yaml").exists():
        fail(f"{name} is vendored and must not carry a workspace-authored openai.yaml")
ok(f"{len(authored)} authored skills expose both engine surfaces")

# --- Contrato da metadata do Codex -------------------------------------------

for name in authored:
    manifest = SKILL_ROOT / name / "agents/openai.yaml"
    document = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    if not isinstance(document, dict):
        fail(f"{name}: openai.yaml must parse to a mapping")
    interface = document.get("interface")
    if not isinstance(interface, dict):
        fail(f"{name}: openai.yaml has no interface block")
    for field in ("display_name", "short_description", "default_prompt"):
        value = interface.get(field)
        if not isinstance(value, str) or not value.strip():
            fail(f"{name}: interface.{field} is missing or empty")
    # A copied manifest that still invokes another skill routes the user to the wrong workflow.
    if f"${name}" not in interface["default_prompt"]:
        fail(f"{name}: default_prompt does not invoke ${name}")
ok(f"{len(authored)} Codex manifests declare a complete interface naming their own skill")

# --- Dependências de tool resolvem nas duas engines --------------------------

claude_servers = json.loads(MCP_CLAUDE.read_text(encoding="utf-8")).get("mcpServers", {})
codex_servers = tomllib.loads(MCP_CODEX.read_text(encoding="utf-8")).get("mcp_servers", {})

declared = 0
for name in authored:
    document = yaml.safe_load((SKILL_ROOT / name / "agents/openai.yaml").read_text(encoding="utf-8"))
    for dependency in (document.get("dependencies") or {}).get("tools") or []:
        if dependency.get("type") != "mcp":
            continue
        server = dependency.get("value")
        declared += 1
        if server not in claude_servers:
            fail(f"{name} depends on MCP {server}, absent from .mcp.json")
        if server not in codex_servers:
            fail(f"{name} depends on MCP {server}, absent from .codex/config.toml")
        expected = dependency.get("url")
        if expected:
            for label, config in (("Claude", claude_servers[server]), ("Codex", codex_servers[server])):
                if config.get("url") != expected:
                    fail(
                        f"{name} declares MCP {server} at {expected} but {label} configures "
                        f"{config.get('url')!r}"
                    )
ok(f"{declared} declared MCP dependencies resolve identically in both engines")

# --- Assimetrias de MCP precisam ser declaradas, não silenciosas -------------

# Matched case-insensitively: the prose names the server as a proper noun ("Linear"), the
# configuration keys it in lowercase.
claude_doc = CLAUDE_DOC.read_text(encoding="utf-8").casefold()
for server in sorted(set(codex_servers) - set(claude_servers)):
    if server.casefold() not in claude_doc:
        fail(
            f"MCP {server} is configured for Codex but not for Claude, and CLAUDE.md does not "
            f"explain the asymmetry"
        )
for server in sorted(set(claude_servers) - set(codex_servers)):
    fail(f"MCP {server} is configured for Claude but not for Codex")
ok("every MCP asymmetry between the engines is documented in CLAUDE.md")

# --- Rotas de contexto apontam para skills reais -----------------------------

routes = json.loads(ROUTES.read_text(encoding="utf-8"))["routes"]
routed = set()
for route in routes:
    for reference in route["references"]:
        source = reference["source"]
        if not source.startswith(".agents/skills/"):
            continue
        if not (ROOT / source).is_file():
            fail(f"route {route['name']} references {source}, which does not exist")
        skill = pathlib.PurePosixPath(source).parts[2]
        if skill not in vendored:
            routed.add(skill)
ok(f"{len(routes)} context routes reference {len(routed)} existing authored skills")

# --- Caminhos citados pelas skills existem -----------------------------------

pattern = re.compile(r"\bscripts/[A-Za-z0-9._-]+\.(?:py|sh)\b")
checked = 0
for name in local_skills:
    body = (SKILL_ROOT / name / "SKILL.md").read_text(encoding="utf-8")
    for reference in sorted(set(pattern.findall(body))):
        # A skill may cite a workspace script or one it ships itself; both spellings are relative.
        if (ROOT / reference).is_file() or (SKILL_ROOT / name / reference).is_file():
            checked += 1
            continue
        fail(f"{name}/SKILL.md cites {reference}, which exists in neither the workspace nor the skill")
ok(f"{checked} script references cited by skills resolve")

print(f"\n{passed} suite(s) passed.")
