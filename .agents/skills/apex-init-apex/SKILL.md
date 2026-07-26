---
name: apex-init-apex
description: "APEX · Initialize APEX in any repository — creates ENV.md and AGENTS.md at the repo root, validates required MCPs, and checks org integration credentials. The only command that runs without ENV.md. Wrapper gerado: lê e executa apex://framework/workflows/init-apex. Requer o servidor MCP apex."
---

# APEX · init-apex

Initialize APEX in any repository — creates ENV.md and AGENTS.md at the repo root, validates required MCPs, and checks org integration credentials. The only command that runs without ENV.md.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/init-apex`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
