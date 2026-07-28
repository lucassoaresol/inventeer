---
name: apex-eng-pre-pr
description: "APEX · Pre-PR validation — deterministic gate pipeline producing pre-pr-verdict.json (ADR 0011) Wrapper experimental: inspeciona apex://framework/workflows/eng-pre-pr no Codex; não use como executor de entrega."
---

# APEX · eng-pre-pr

Pre-PR validation — deterministic gate pipeline producing pre-pr-verdict.json (ADR 0011)

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-pre-pr` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
