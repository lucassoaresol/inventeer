---
name: apex-eng-ard-from-code
description: "APEX · Engineering workflow for creating or iterating an ARD based on repository code Wrapper experimental: inspeciona apex://framework/workflows/eng-ard-from-code no Codex; não use como executor de entrega."
---

# APEX · eng-ard-from-code

Engineering workflow for creating or iterating an ARD based on repository code

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-ard-from-code` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
