# Assistants Project Entry Point

## Identidade

- Produto: Inventeer Assistants
- Issue raiz: `INV-2228`
- Domínio: `AST`
- Repositório local esperado: `repos/assistants`
- Dependência contextual: `repos/ids` — contratos DAP/EPP/DEP e standards, carregados sob demanda.
- Hierarquia Linear: `PROD → INIT → PROJ → MILE → TASK → SUBTASK`

## Fontes canônicas

- Linear: hierarquia e estado operacional das issues.
- `repos/ids`: contratos DAP, EPP e DEP.
- `repos/assistants`: runtime, testes, configuração, infraestrutura, artifacts derivados e specs.
- `repos/inventeer-hub`: padrões organizacionais referenciados pelo produto.

## Pontos de entrada do repositório

Leia em `repos/assistants`, apenas conforme a necessidade:

1. `AGENTS.md` e `CLAUDE.md` — instruções e realidade construída, quando existirem.
2. `PROJECT.md` — identidade e contexto interno.
3. `README.md` — visão geral e execução local.
4. `artifacts/ASSIST_Pending_Decisions.md` — decisões abertas, resolvidas e superseded.
5. `artifacts/ASSIST_Architecture.md` — arquitetura lógica.
6. `artifacts/adrs/` — decisões arquiteturais duradouras.
7. `.specs/` — specs de features, quando existir no projeto.

## Skills recomendadas

1. `assistants-task-context` prepara a issue e seu contexto herdado.
2. `tlc-spec-driven` especifica, implementa e verifica quando necessário.

## Dependência IDS

- Consulte `repos/ids/clients/Inventeer-Internal/Inventeer-Assistants/` quando a task tocar escopo,
  DoDs, arquitetura ou constraints de EPP, Gates, rigor, go-live ou evidências DEP.
- Para mudanças internas sem impacto de contrato, registre IDS como não aplicável com o motivo.
- Contratos no IDS são read-only durante tasks de Assistants e não devem ser copiados para este repo.
