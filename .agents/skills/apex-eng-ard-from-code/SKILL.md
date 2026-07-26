---
name: apex-eng-ard-from-code
description: "APEX · Engineering workflow for creating or iterating an ARD based on repository code Wrapper gerado: lê e executa apex://framework/workflows/eng-ard-from-code. Requer o servidor MCP apex."
---

# APEX · eng-ard-from-code

Engineering workflow for creating or iterating an ARD based on repository code

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/eng-ard-from-code`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
