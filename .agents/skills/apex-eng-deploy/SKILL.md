---
name: apex-eng-deploy
description: "APEX · Deploy and operate a release — environment promotion, gradual rollout, health verification, and rollback on regression. Wrapper experimental: inspeciona apex://framework/workflows/eng-deploy no Codex; não use como executor de entrega."
---

# APEX · eng-deploy

Deploy and operate a release — environment promotion, gradual rollout, health verification, and rollback on regression.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-deploy` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
