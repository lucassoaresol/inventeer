---
name: apex-eng-docs-bootstrap
description: "APEX · Generate or refresh repository architectural documentation by consuming gaps reported by doc-audit. Templates live in framework/stack-profiles/{stack}/doc-minimum/. Writes via per-edit consent UX. Refreshes via \"open for review\" suggestion. Wrapper gerado: lê e executa apex://framework/workflows/eng-docs-bootstrap. Requer o servidor MCP apex."
---

# APEX · eng-docs-bootstrap

Generate or refresh repository architectural documentation by consuming gaps reported by doc-audit. Templates live in framework/stack-profiles/{stack}/doc-minimum/. Writes via per-edit consent UX. Refreshes via "open for review" suggestion.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/eng-docs-bootstrap`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
