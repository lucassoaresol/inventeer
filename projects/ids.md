# IDS Project Entry Point

## Identidade

- Produto: Inventeer Delivery System
- Issue raiz: `INV-88`
- Domínios: `IDS`, `DAP`, `EPP`, `DEP`, `EE`
- Repositório local esperado: `repos/ids`

## Papel

O IDS é o sistema interno que governa o ciclo de entrega da entrada do cliente até o pacote de
evidências. Ele é fonte canônica para contratos DAP, EPP e DEP consumidos pelos produtos.

## Pontos de entrada

Leia em `repos/ids`, apenas conforme a necessidade:

1. `CLAUDE.md` — contexto operacional específico do spoke.
2. `README.md` — pipeline, domínios e mapa do repositório.
3. `artifacts/IDS_Operating_System_Overview.md` — regras de fonte única e operação.
4. `artifacts/` — standards e templates DAP/EPP/DEP/EE.
5. `clients/` — workspaces e contratos canônicos dos produtos/clientes.

## Limites

- Consulte contratos no IDS; não copie seus corpos para este workspace.
- Mudanças em standards ou contratos exigem seguir as regras de aprovação do próprio IDS.
- O IDS governa execução; não substitui código, testes ou specs dos produtos.
