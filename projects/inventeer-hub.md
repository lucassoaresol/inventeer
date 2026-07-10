# Inventeer Hub Playbook Entry Point

## Identidade

- Tipo: foundation / Playbook compartilhado.
- Repositório local esperado: `repos/inventeer-hub`.
- Uso: referência read-only para standards, frameworks, templates e skills reutilizáveis.

## Papel

O Hub contém metodologia reutilizável e tenant-neutral. Identidade, routing, specs de produtos e
histórico operacional permanecem nos spokes e repos correspondentes. Os projetos referenciam os
standards `HUB_*` por nome em vez de copiar seu conteúdo.

## Pontos de entrada

Leia em `repos/inventeer-hub`, apenas conforme a necessidade:

1. `CLAUDE.md` — operating context e protocolos do Playbook.
2. `README.md` — estrutura e relação com tenants.
3. `artifacts/identity/` — glossário e naming.
4. `artifacts/work-hierarchy/` — hierarquia, DoDs, criticidade e templates de trabalho.
5. `artifacts/workspace/` — layout de repos, integração Linear e regras de plugin.
6. `artifacts/context-and-plugins/` — disciplina de contexto, categorias e naming de skills.
7. `artifacts/onboarding/` — onboarding de teammates e workspaces.

## Limites

- Consuma o Hub como referência read-only durante trabalho nos produtos.
- Não copie standards `HUB_*` para este workspace ou para spokes.
- Só altere o Hub quando a solicitação tiver como escopo a manutenção do Playbook.
- Ao operar diretamente nele, siga seus protocolos locais de sessão, routing e aprovação.
