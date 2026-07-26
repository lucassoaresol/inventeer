---
name: apex-taxonomy
description: "APEX · Manages the organizational taxonomy securely via the cloud gateway (Organizational Options CRUD) Wrapper gerado: lê e executa apex://framework/workflows/taxonomy. Requer o servidor MCP apex."
---

# APEX · taxonomy

Manages the organizational taxonomy securely via the cloud gateway (Organizational Options CRUD)

Arquivo gerado por `scripts/sync-apex-commands.sh` a partir de `apex_framework_index`. Não edite
manualmente: o próximo sync sobrescreve. A fonte canônica do workflow é o recurso MCP, não este
arquivo.

## Execução

1. Leia o recurso MCP `apex://framework/workflows/taxonomy`.
2. Pare e relate indisponibilidade se o servidor MCP `apex` não estiver conectado, se o recurso
   não existir ou se o conteúdo retornado estiver vazio. Não improvise um substituto nem troque
   por outra skill.
3. Siga integralmente o workflow retornado, incluindo suas próprias regras, gates e handoffs.
