---
name: apex-eng-monitor
description: "APEX · Post-deploy monitoring — reads Sentry for release errors and generates bug reports Wrapper experimental: inspeciona apex://framework/workflows/eng-monitor no Codex; não use como executor de entrega."
---

# APEX · eng-monitor

Post-deploy monitoring — reads Sentry for release errors and generates bug reports

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-monitor` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
