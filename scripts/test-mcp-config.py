#!/usr/bin/env python3

import json
import pathlib
import tomllib


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_CONTEXT7 = {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
}
EXPECTED_SHADCN = {
    "command": "npx",
    "args": ["shadcn@latest", "mcp"],
}
FORBIDDEN_PROVIDER_SERVERS = {"cloudflare", "cloudflare-docs", "aws", "aws-docs"}


def ok(number: int, message: str) -> None:
    print(f"ok {number} - {message}")


with (ROOT / ".mcp.json").open(encoding="utf-8") as file:
    claude_servers = json.load(file)["mcpServers"]

with (ROOT / ".codex/config.toml").open("rb") as file:
    codex_servers = tomllib.load(file)["mcp_servers"]

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    context7 = servers.get("context7")
    assert context7 is not None, f"{label} omits Context7"
    assert context7["command"] == EXPECTED_CONTEXT7["command"]
    assert context7["args"] == EXPECTED_CONTEXT7["args"]
ok(1, "Codex and Claude use the same credential-free Context7 command")

shadcn_targets = []
for label, servers, cwd_base, expected_cwd in (
    ("Claude", claude_servers, ROOT, "repos/portal-web"),
    ("Codex", codex_servers, ROOT / ".codex", "../repos/portal-web"),
):
    shadcn = servers.get("shadcn")
    assert shadcn is not None, f"{label} omits shadcn"
    assert shadcn["command"] == EXPECTED_SHADCN["command"]
    assert shadcn["args"] == EXPECTED_SHADCN["args"]
    assert shadcn["cwd"] == expected_cwd
    shadcn_targets.append((cwd_base / shadcn["cwd"] / "components.json").resolve(strict=True))
assert shadcn_targets[0] == shadcn_targets[1]
assert shadcn_targets[0] == (ROOT / "repos/portal-web/components.json").resolve(strict=True)
ok(2, "shadcn commands use engine-specific cwd values")
ok(3, "both shadcn cwd values resolve to the Portal Web components.json")

assert codex_servers["shadcn"]["default_tools_approval_mode"] == "writes"
ok(4, "Codex approval remains mandatory for shadcn writes")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    forbidden = FORBIDDEN_PROVIDER_SERVERS.intersection(servers)
    assert not forbidden, f"{label} config contains provider servers: {sorted(forbidden)}"
ok(5, "Cloudflare and AWS MCPs remain deferred")

serialized_configs = json.dumps(claude_servers) + json.dumps(codex_servers)
for secret_marker in ("API_KEY", "ACCESS_KEY", "SECRET_KEY", "TOKEN"):
    assert secret_marker not in serialized_configs
ok(6, "versioned MCP definitions contain no credential markers")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in (
    "Context7",
    "código e documentação local continuam tendo precedência",
    "`shadcn` pertence ao `portal-web`",
    "servidor shadcn opera com cwd em `repos/portal-web`",
    "Ferramentas de escrita do shadcn exigem aprovação",
    "migração do Portal para AWS",
):
    assert phrase in readme, f"README omits boundary: {phrase}"
ok(7, "README documents source precedence, shadcn routing, and provider boundaries")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
for phrase in (
    "Use o MCP shadcn somente para trabalho em `repos/portal-web`",
    "verifique o worktree e obtenha a aprovação exigida pelo engine",
    "não transfere ownership nem autoriza mudanças de produto",
):
    assert phrase in agents, f"AGENTS.md omits shadcn guardrail: {phrase}"
ok(8, "workspace instructions preserve Portal Web ownership and write approval")

state = (ROOT / ".specs/STATE.md").read_text(encoding="utf-8")
for decision in ("AD-028", "AD-030"):
    section = state.split(f"### {decision}", 1)[1].split("### ", 1)[0]
    assert "**Status**: active" in section, f"{decision} is not active"
ad_029 = state.split("### AD-029", 1)[1].split("### ", 1)[0]
assert "**Status**: superseded by AD-030" in ad_029
ok(9, "workspace decisions record resource preflight and shadcn adoption")

tlc = (ROOT / ".agents/skills/tlc-spec-driven/SKILL.md").read_text(encoding="utf-8")
assert "Step 1: Codebase" in tlc
assert "Step 2: Project docs" in tlc
assert "Step 3: Context7 MCP" in tlc
ok(10, "Context7 remains behind canonical codebase and project documentation")

print("\n10 teste(s) passaram.")
