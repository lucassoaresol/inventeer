---
name: apex-eng-review
description: "APEX · Engineering workflow to solution review or PR Wrapper gerado: lê e executa apex://framework/workflows/eng-review. Requer o servidor MCP apex."
---

# APEX · eng-review

Engineering workflow to solution review or PR

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/eng-review`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
