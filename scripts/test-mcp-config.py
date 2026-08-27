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
EXPECTED_GITHUB_URL = "https://api.githubcopilot.com/mcp/"
EXPECTED_GITHUB_TOOLSETS = "pull_requests,repos,actions,git"
EXPECTED_FIGMA_URL = "https://mcp.figma.com/mcp"
EXPECTED_FIGMA_LOCAL = {
    "command": "npx",
    "args": [
        "-y",
        "@alvinindra/figma-mcp-rust@0.2.0",
        "--ip",
        "127.0.0.1",
        "--port",
        "1994",
    ],
}
FORBIDDEN_PROVIDER_SERVERS = {"cloudflare", "cloudflare-docs", "aws", "aws-docs"}


def ok(number: int, message: str) -> None:
    print(f"ok {number} - {message}")


with (ROOT / ".mcp.json").open(encoding="utf-8") as file:
    claude_servers = json.load(file)["mcpServers"]

with (ROOT / ".codex/config.toml").open("rb") as file:
    codex_servers = tomllib.load(file)["mcp_servers"]

assert codex_servers["apex"]["default_tools_approval_mode"] == "writes"
ok(1, "Codex approval remains mandatory for APEX writes")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    context7 = servers.get("context7")
    assert context7 is not None, f"{label} omits Context7"
    assert context7["command"] == EXPECTED_CONTEXT7["command"]
    assert context7["args"] == EXPECTED_CONTEXT7["args"]
ok(2, "Codex and Claude use the same credential-free Context7 command")

shadcn_targets = []
for label, servers, cwd_base, expected_cwd in (
    ("Claude", claude_servers, ROOT, "repos/portal-web"),
    ("Codex", codex_servers, ROOT, "repos/portal-web"),
):
    shadcn = servers.get("shadcn")
    assert shadcn is not None, f"{label} omits shadcn"
    assert shadcn["command"] == EXPECTED_SHADCN["command"]
    assert shadcn["args"] == EXPECTED_SHADCN["args"]
    assert shadcn["cwd"] == expected_cwd
    shadcn_targets.append((cwd_base / shadcn["cwd"] / "components.json").resolve(strict=True))
assert shadcn_targets[0] == shadcn_targets[1]
assert shadcn_targets[0] == (ROOT / "repos/portal-web/components.json").resolve(strict=True)
ok(3, "shadcn commands use the same workspace-relative cwd")
ok(4, "both shadcn cwd values resolve to the Portal Web components.json")

assert codex_servers["shadcn"]["default_tools_approval_mode"] == "writes"
ok(5, "Codex approval remains mandatory for shadcn writes")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    github = servers.get("github")
    assert github is not None, f"{label} omits GitHub"
    assert github["url"] == EXPECTED_GITHUB_URL
    headers = github.get("headers", github.get("http_headers"))
    assert headers["X-MCP-Toolsets"] == EXPECTED_GITHUB_TOOLSETS
    assert headers["X-MCP-Readonly"] == "true"
assert claude_servers["github"]["headers"]["Authorization"] == "Bearer ${GITHUB_PAT_TOKEN}"
assert codex_servers["github"]["bearer_token_env_var"] == "GITHUB_PAT_TOKEN"
ok(6, "Codex and Claude use the same scoped read-only GitHub MCP")

assert codex_servers["github"]["default_tools_approval_mode"] == "writes"
ok(7, "GitHub is server-side read-only with Codex write approval as defense in depth")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    figma = servers.get("figma")
    assert figma is not None, f"{label} omits Figma"
    assert figma["url"] == EXPECTED_FIGMA_URL
    assert "headers" not in figma
    assert "http_headers" not in figma
    assert "bearer_token_env_var" not in figma
ok(8, "Codex and Claude use the same credential-free Figma OAuth endpoint")

assert codex_servers["figma"]["default_tools_approval_mode"] == "writes"
ok(9, "Codex approval remains mandatory for Figma writes")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    figma_local = servers.get("figma-local")
    assert figma_local is not None, f"{label} omits figma-local"
    assert figma_local["command"] == EXPECTED_FIGMA_LOCAL["command"]
    assert figma_local["args"] == EXPECTED_FIGMA_LOCAL["args"]
    assert all("latest" not in argument for argument in figma_local["args"])
assert codex_servers["figma-local"]["enabled"] is False
assert codex_servers["figma-local"]["default_tools_approval_mode"] == "prompt"
claude_settings = json.loads((ROOT / ".claude/settings.json").read_text(encoding="utf-8"))
assert "figma-local" not in claude_settings.get("enabledMcpjsonServers", [])
ok(10, "local Figma pilot is pinned, loopback-only, and not auto-enabled")

for label, servers in (("Claude", claude_servers), ("Codex", codex_servers)):
    forbidden = FORBIDDEN_PROVIDER_SERVERS.intersection(servers)
    assert not forbidden, f"{label} config contains provider servers: {sorted(forbidden)}"
ok(11, "Cloudflare and AWS MCPs remain deferred")

serialized_configs = json.dumps(claude_servers) + json.dumps(codex_servers)
for secret_marker in ("ghp_", "github_pat_", "API_KEY=", "ACCESS_KEY=", "SECRET_KEY="):
    assert secret_marker not in serialized_configs
assert serialized_configs.count("GITHUB_PAT_TOKEN") == 2
ok(12, "versioned MCP definitions contain only the GitHub token variable name")

readme = (ROOT / "README.md").read_text(encoding="utf-8")
for phrase in (
    "Context7",
    "código e documentação local continuam tendo precedência",
    "`github` é compartilhado pelos dois engines",
    "`X-MCP-Readonly: true` remove operações mutáveis",
    "Linear permanece canônico para issues",
    "`shadcn` pertence ao `portal-web`",
    "servidor shadcn opera com cwd em `repos/portal-web`",
    "Ferramentas de escrita do shadcn exigem aprovação",
    "`figma` também é compartilhado pelos dois engines",
    "OAuth em runtime, sem token versionado",
    "ferramentas de escrita do Figma exigem aprovação pelo modo `writes`",
    "`codex mcp login figma`",
    "`figma-local` é um piloto manual e opt-in",
    "arquivo Figma descartável",
    "plugin Desktop estiver ausente ou desconectado",
    "`127.0.0.1:1994`",
    "Essas ferramentas exigem aprovação pelo modo `writes`",
    "migração do Portal para AWS",
):
    assert phrase in readme, f"README omits boundary: {phrase}"
ok(13, "README documents MCP approval, routing, and provider boundaries")

agents = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
for phrase in (
    "Use o MCP shadcn somente para trabalho em `repos/portal-web`",
    "Use o MCP Figma autenticado por OAuth",
    "Antes de qualquer ferramenta de escrita do Figma",
    "O MCP `figma-local` é um piloto manual e opt-in",
    "arquivo Figma descartável",
    "plugin Desktop estiver ausente ou desconectado",
    "Use o MCP GitHub read-only para evidência de PRs",
    "Mantenha o MCP GitHub restrito aos toolsets `pull_requests,repos,actions,git`",
    "Sua disponibilidade não autoriza comentários, approvals, merges",
    "revalide ambos antes do parecer",
    "verifique o worktree e obtenha a aprovação exigida pelo engine",
    "não transfere ownership nem autoriza mudanças de produto",
    "mantenha ferramentas de escrita do MCP `apex` sujeitas a aprovação",
):
    assert phrase in agents, f"AGENTS.md omits shadcn guardrail: {phrase}"
ok(14, "workspace instructions preserve MCP ownership and write approval")

state = (ROOT / ".specs/STATE.md").read_text(encoding="utf-8")
for decision in ("AD-028", "AD-030", "AD-032", "AD-037", "AD-043", "AD-051"):
    section = state.split(f"### {decision}", 1)[1].split("### ", 1)[0]
    assert "**Status**: active" in section, f"{decision} is not active"
ad_029 = state.split("### AD-029", 1)[1].split("### ", 1)[0]
assert "**Status**: superseded by AD-030" in ad_029
ad_037 = state.split("### AD-037", 1)[1].split("## Handoff", 1)[0]
for phrase in ("GITHUB_PAT_TOKEN", "X-MCP-Readonly: true", "não altera GitHub"):
    assert phrase in ad_037, f"AD-037 omits GitHub MCP boundary: {phrase}"
ad_043 = state.split("### AD-043", 1)[1].split("## Handoff", 1)[0]
for phrase in ("OAuth em runtime", "ferramentas de escrita sujeitas à aprovação", "não autoriza mudanças"):
    assert phrase in ad_043, f"AD-043 omits Figma MCP boundary: {phrase}"
ad_051 = state.split("### AD-051", 1)[1].split("## Handoff", 1)[0]
for phrase in ("figma-local", "127.0.0.1:1994", "desabilitado por padrão", "inventeer-ops"):
    assert phrase in ad_051, f"AD-051 omits pilot boundary: {phrase}"
ok(15, "workspace decisions record resource preflight and MCP boundaries")

tlc = (ROOT / ".agents/skills/tlc-spec-driven/SKILL.md").read_text(encoding="utf-8")
assert "Step 1: Codebase" in tlc
assert "Step 2: Project docs" in tlc
assert "Step 3: Context7 MCP" in tlc
ok(16, "Context7 remains behind canonical codebase and project documentation")

print("\n16 teste(s) passaram.")
