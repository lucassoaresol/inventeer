---
name: apex-init-apex
description: "APEX · Initialize APEX in any repository — creates ENV.md and AGENTS.md at the repo root, validates required MCPs, and checks org integration credentials. The only command that runs without ENV.md. Wrapper experimental: inspeciona apex://framework/workflows/init-apex no Codex; não use como executor de entrega."
---

# APEX · init-apex

Initialize APEX in any repository — creates ENV.md and AGENTS.md at the repo root, validates required MCPs, and checks org integration credentials. The only command that runs without ENV.md.

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/init-apex` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
