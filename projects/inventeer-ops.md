# Inventeer Ops Entry Point

## Identidade

- Repositório local esperado: `repos/inventeer-ops`
- Raiz Linear operacional: `INV-255`
- Papel: fonte compartilhada de contexto, documentação e plugins específicos do tenant Inventeer.

## Autoridade

- `CLAUDE.md` contém o contexto operacional do tenant.
- `artifacts/areas/` contém documentação organizada por área.
- `artifacts/products/` contém documentação organizada por produto ou sistema.
- `artifacts/products/ids/plugin/ids-delivery/` e
  `artifacts/areas/marketing/plugin/inv-marketing/` preservam as fontes dos plugins movidos.

Standards universais continuam pertencendo a `repos/inventeer-hub`. Linear continua canônico para
estado, owner e execução. Repositórios de código continuam canônicos para implementação, testes e
decisões técnicas locais.

## Rotas usadas neste workspace

| Domínio | Caminho |
| --- | --- |
| IDS | `repos/inventeer-ops/artifacts/products/ids/` |
| Portal | `repos/inventeer-ops/artifacts/products/portal/` |
| Marketing | `repos/inventeer-ops/artifacts/areas/marketing/` |
| GenAI | `repos/inventeer-ops/artifacts/areas/marketing/genai/` |

## Limites

- Leia o `CLAUDE.md` raiz e o README da subárvore aplicável antes de usar seus artifacts.
- Não trate subárvores como repos Git independentes.
- Não altere `inventeer-ops` a partir de uma task de código sem escopo documental explícito.
- Não copie contratos IDS ou standards do Hub para este workspace.
