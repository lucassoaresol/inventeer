---
name: apex-eng-build-tech-spec
description: "APEX · Tech Spec creation from Tracker story Wrapper experimental: inspeciona apex://framework/workflows/eng-build-tech-spec no Codex; não use como executor de entrega."
---

# APEX · eng-build-tech-spec

Tech Spec creation from Tracker story

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Limite operacional

1. Use este wrapper somente quando o usuário pedir inspeção ou diagnóstico explícito da integração
   APEX no Codex.
2. Leia o recurso MCP `apex://framework/workflows/eng-build-tech-spec` e pare se o servidor, recurso ou conteúdo não estiver
   disponível.
3. Não execute o workflow como entrega no Codex: leitura do recurso não cria prompt nativo,
   contexto de sessão, artifacts nem tools obrigatórias. Use `tlc-spec-driven` como executor.
