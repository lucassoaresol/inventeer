---
name: apex-eng-monitor
description: "APEX · Post-deploy monitoring — reads Sentry for release errors and generates bug reports Wrapper gerado: lê e executa apex://framework/workflows/eng-monitor. Requer o servidor MCP apex."
---

# APEX · eng-monitor

Post-deploy monitoring — reads Sentry for release errors and generates bug reports

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/eng-monitor`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
