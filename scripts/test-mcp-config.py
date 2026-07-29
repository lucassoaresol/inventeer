#!/usr/bin/env python3

import json
import pathlib
import tomllib


ROOT = pathlib.Path(__file__).resolve().parents[1]
EXPECTED_CONTEXT7 = {
    "command": "npx",
    "args": ["-y", "@upstash/context7-mcp"],
}
FORBIDDEN_ROOT_SERVERS = {"shadcn", "cloudflare", "cloudflare-docs", "aws", "aws-docs"}


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

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    forbidden = FORBIDDEN_ROOT_SERVERS.intersection(servers)
    assert not forbidden, f"{label} config contains root-scoped servers: {sorted(forbidden)}"
ok(2, "cwd-sensitive and provider-specific MCPs stay out of the workspace root")

serialized_configs = json.dumps(claude_servers) + json.dumps(codex_servers)
for secret_marker in ("API_KEY", "ACCESS_KEY", "SECRET_KEY", "TOKEN"):
    assert secret_marker not in serialized_configs
ok(3, "versioned MCP definitions contain no credential markers")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in (
    "Context7",
    "código e documentação local continuam tendo precedência",
    "`shadcn` pertence ao `portal-web`",
    "migração do Portal para AWS",
):
    assert phrase in readme, f"README omits boundary: {phrase}"
ok(4, "README documents source precedence and deferred MCP boundaries")

state = (ROOT / ".specs/STATE.md").read_text(encoding="utf-8")
for decision in ("AD-028", "AD-029"):
    section = state.split(f"### {decision}", 1)[1].split("### ", 1)[0]
    assert "**Status**: active" in section, f"{decision} is not active"
ok(5, "workspace decisions record resource preflight and Context7 adoption")

tlc = (ROOT / ".agents/skills/tlc-spec-driven/SKILL.md").read_text(encoding="utf-8")
assert "Step 1: Codebase" in tlc
assert "Step 2: Project docs" in tlc
assert "Step 3: Context7 MCP" in tlc
ok(6, "Context7 remains behind canonical codebase and project documentation")

print("\n6 teste(s) passaram.")

