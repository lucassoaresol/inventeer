---
name: apex-eng-docs-bootstrap
description: "APEX · Generate or refresh repository architectural documentation by consuming gaps reported by doc-audit. Templates live in framework/stack-profiles/{stack}/doc-minimum/. Writes via per-edit consent UX. Refreshes via \"open for review\" suggestion. Wrapper experimental: inspeciona apex://framework/workflows/eng-docs-bootstrap no Codex; não use como executor de entrega."
---

# APEX · eng-docs-bootstrap

Generate or refresh repository architectural documentation by consuming gaps reported by doc-audit. Templates live in framework/stack-profiles/{stack}/doc-minimum/. Writes via per-edit consent UX. Refreshes via "open for review" suggestion.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-docs-bootstrap` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
