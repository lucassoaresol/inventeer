---
name: apex-qa-unit-test
description: "APEX · Design and implement focused unit tests for the current change set Wrapper gerado: lê e executa apex://framework/workflows/qa-unit-test. Requer o servidor MCP apex."
---

# APEX · qa-unit-test

Design and implement focused unit tests for the current change set

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/qa-unit-test`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
