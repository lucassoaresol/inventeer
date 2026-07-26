---
name: apex-eng-ready
description: "APEX · Per-task readiness gate — one cheap ✅/⚠️/❌ sweep (setup, context, connections, baseline, task) that tells you if you're ready to start, and routes to the missing step if not. Reusable standalone and as eng-start Phase 0. Wrapper gerado: lê e executa apex://framework/workflows/eng-ready. Requer o servidor MCP apex."
---

# APEX · eng-ready

Per-task readiness gate — one cheap ✅/⚠️/❌ sweep (setup, context, connections, baseline, task) that tells you if you're ready to start, and routes to the missing step if not. Reusable standalone and as eng-start Phase 0.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/eng-ready`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
