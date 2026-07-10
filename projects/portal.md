# Portal Project Entry Point

## Identidade

- Produto: Inventeer Client Portal
- Issue raiz: `INV-254`
- Domínio: `PORTAL`
- Repositórios locais esperados:
  - `repos/portal` — produto, artifacts e planejamento.
  - `repos/portal-api` — backend, contratos públicos e persistência.
  - `repos/portal-web` — frontend client-rendered.
- Dependência contextual: `repos/ids` — standards canônicos do pipeline, carregados sob demanda.

## Topologia

```text
repos/portal
    ├── define produto, artifacts e contexto governado
    ├── repos/portal-api implementa API e contratos compartilhados
    └── repos/portal-web consome contratos e implementa a experiência web
```

## Pontos de entrada

### Produto — `repos/portal`

1. `CLAUDE.md` — contexto operacional do spoke.
2. `README.md` — identidade, status e mapa de artifacts.
3. `artifacts/PORTAL_Base_Overview.md` — definição canônica do produto no repo.
4. `artifacts/PORTAL_Authority_Model.md` — autoridade e permissões.
5. `artifacts/PORTAL_Execution_Plan.md` — planejamento histórico; Linear governa progresso atual.

### Backend — `repos/portal-api`

1. `AGENTS.md` — regras operacionais, arquitetura e gates obrigatórios.
2. `README.md` — setup, runtime e comandos.
3. `docs/adr/` e `docs/architecture/` — decisões e notas arquiteturais, quando existirem.
4. `specs/` — specs locais do backend.

### Frontend — `repos/portal-web`

1. `AGENTS.md` — ownership, stack e invariantes do frontend.
2. `README.md` — setup, comandos e deploy.
3. `CLAUDE.md` — regras adicionais existentes no repo.
4. `specs/` — specs locais do frontend.

## Limites entre repos

- `portal-api` é owner dos contratos públicos compartilhados e das regras de negócio do backend.
- `portal-web` consome esses contratos e não deve redefinir regras centrais localmente.
- `portal` mantém o contexto de produto; não substitui implementação e testes dos dois repos de código.
- Antes de uma mudança cross-repo, identifique explicitamente quais repos precisam ser modificados.
- Quando a task tocar intake, DAP/EPP/DEP, Gates, aprovação, rigor ou handoff, consulte o standard
  correspondente em `repos/ids` antes de especificar o comportamento.
- `repos/ids` é contexto read-only para tasks de Portal; uma task de Portal não altera contratos IDS.

## Skills recomendadas

1. `portal-task-context` prepara a issue, carrega o entendimento do produto e determina ownership.
2. `tlc-spec-driven` especifica, implementa e verifica nos repos identificados quando necessário.
