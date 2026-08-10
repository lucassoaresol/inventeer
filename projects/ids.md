# IDS Project Entry Point

## Identidade

- Produto: Inventeer Delivery System
- Issue raiz: `INV-88`
- Domínios: `IDS`, `DAP`, `EPP`, `DEP`, `EE`
- Repositório local esperado: `repos/inventeer-ops`
- Raiz documental: `repos/inventeer-ops/artifacts/products/ids`

## Papel

O IDS é o sistema interno que governa o ciclo de entrega da entrada do cliente até o pacote de
evidências. Ele é fonte canônica para contratos DAP, EPP e DEP consumidos pelos produtos.

## Pontos de entrada

Leia primeiro `repos/inventeer-ops/CLAUDE.md` e depois, apenas conforme a necessidade:

1. `repos/inventeer-ops/artifacts/products/ids/README.md` — pipeline, domínios e mapa da subárvore.
2. `repos/inventeer-ops/artifacts/products/ids/artifacts/IDS_Operating_System_Overview.md` — regras de fonte única e operação.
3. `repos/inventeer-ops/artifacts/products/ids/artifacts/` — standards e templates DAP/EPP/DEP/EE.
4. `repos/inventeer-ops/artifacts/products/ids/clients/` — workspaces e contratos canônicos dos produtos/clientes.
5. `repos/inventeer-ops/artifacts/products/ids/plugin/ids-delivery/` — fonte do plugin IDS.

## Limites

- Consulte contratos no IDS; não copie seus corpos para este workspace.
- A subárvore IDS não é um repo Git independente; operações Git pertencem a `repos/inventeer-ops`.
- Mudanças em standards ou contratos exigem seguir as regras de aprovação do próprio IDS.
- O IDS governa execução; não substitui código, testes ou specs dos produtos.
