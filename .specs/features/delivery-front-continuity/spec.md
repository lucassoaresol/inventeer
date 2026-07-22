# Delivery Front Continuity Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** Portuguese

## Problem Statement

Tasks concluídas no código permanecem aguardando CI, review e aprovação antes do merge em uma branch
de integração como `develop`. Sem um fluxo explícito para esse intervalo, o ciclo fica ocioso ou a
próxima task começa sobre uma base inadequada, mistura escopos, cria stacks profundos ou exige uma
reconstrução arriscada depois do squash merge.

O workspace precisa coordenar a frente ativa de entrega entre várias tasks sem substituir a triagem,
o contexto de task única ou a execução TLC. A primeira entrega deve ser read-only: observar Linear,
GitHub e Git local, classificar a próxima task merge-safe e produzir um plano verificável antes de
qualquer mutação.

## Goals

- [ ] Manter o fluxo do ciclo enquanto uma PR aguarda review, com limite explícito de trabalho em
  progresso.
- [ ] Selecionar a próxima task pela segurança de merge, além de prioridade e readiness.
- [ ] Distinguir trabalho independente, dependente, conflitante e bloqueado com evidência.
- [ ] Preservar um diff por task e planejar corretamente a reconciliação após squash merge.
- [ ] Criar o contrato para uma futura skill `advance-delivery-front` inicialmente read-only.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Criar agora a skill `advance-delivery-front` | Esta fase especifica e aprova o comportamento antes da implementação. |
| Criar branches ou worktrees | O MVP planejado é read-only e não recebeu autorização de mutação. |
| Abrir, editar, promover, fechar ou mergear PRs | Ações GitHub serão avaliadas somente após o piloto read-only. |
| Rebase, merge local, reset ou force push | Operações frágeis exigem script determinístico, dry-run e aprovação futura. |
| Alterar estados ou relações no Linear | Linear permanece canônico e read-only nesta fase. |
| Modificar `tlc-spec-driven` | A TLC continua responsável apenas por especificar, implementar e validar uma task. |
| Mudar convenções Git dos repositórios de produto | A skill deve consumir as regras locais, não substituí-las. |
| Permitir stacks com mais de uma dependência pendente | A profundidade maior aumenta exponencialmente o custo de reconciliação. |

## Approved Workspace Decision

Aprovação registrada em 2026-07-22 e decisão adicionada a `.specs/STATE.md`:

### AD-022

- **Decision**: Coordenar frentes contínuas de entrega com no máximo uma PR pronta para review e uma
  próxima task em implementação ou PR draft por repositório; priorizar tasks independentes e
  permitir no máximo um nível de PR dependente com boundary SHA registrado, mantendo-a draft até a
  reconciliação com a branch de integração.
- **Reason**: Review e aprovação são esperas externas; o ciclo deve continuar sem misturar escopos,
  esconder dependências ou criar stacks difíceis de recuperar após squash merge.
- **Trade-off**: O fluxo adiciona classificação, metadados e uma etapa de reconciliação; algumas
  tasks conflitantes ainda precisarão aguardar quando não houver trabalho independente seguro.
- **Alternatives considered**: Parar até cada merge; abrir várias PRs prontas sem ordem; manter stacks
  ilimitados; embutir toda a coordenação na TLC; tratar cada transição informalmente.
- **Scope**: Seleção, preparação, review e reconciliação de tasks consecutivas nos repositórios
  registrados neste workspace.
- **Date**: 2026-07-22
- **Status**: active

Esta decisão está ativa enquanto não for supersedida por outra decisão transversal.

## Assumptions and Decisions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Limite de WIP | Uma PR pronta + uma task ativa ou PR draft por repo | Mantém fluxo sem criar fila profunda de branches dependentes. | Yes |
| Preferência de continuidade | Escolher trabalho independente antes de empilhar | Reduz conflitos, restacks e dependência de um review ainda instável. | Yes |
| Profundidade do stack | No máximo uma PR dependente | Permite continuidade sem formar uma cadeia A → B → C. | Yes |
| Estado Linear de uma PR draft dependente | Manter a task `In Progress` | Draft dependente ainda não está revisável contra a integração. | Yes |
| Estado Linear de uma PR pronta | Usar `In Review` | Representa que base, diff e gates já permitem review útil. | Yes |
| Primeiro incremento | Observação e plano read-only | Permite validar classificação e transições antes de automatizar mutações. | Yes |
| Mutação futura | Sempre exigir autorização explícita | Branches, PRs, Linear, rebase e force push alteram estado compartilhado. | Yes |
| Isolamento local | Recomendar worktree quando duas tasks do mesmo repo precisarem de manutenção simultânea; permitir branch switching somente com worktree limpo | Worktree é isolamento, não autorização para paralelismo de CPU ou sessões. | Yes |
| Metadado durável de stack | Planejar marker estruturado na PR draft, sujeito a aprovação da fase mutável | Config local e `session-context/` não são portáveis; a PR acompanha a dependência operacional. | No — validate in pilot |

**Open questions:** somente o formato do metadado durável será validado no piloto; ele não bloqueia o
MVP read-only.

## Evidence Model

Toda conclusão deve usar uma destas classes:

- `FORMAL`: relações, estados, ciclo ou hierarquia no Linear; base, draft, review, CI ou merge no
  GitHub.
- `INHERITED`: convenções locais de Git, branch protection, merge order ou decisões ativas.
- `CODE`: sobreposição confirmada em arquivos, contratos, símbolos, testes ou migrations.
- `INFERENCE`: risco de colisão ou ordem sugerida sem relação formal.
- `QUESTION`: informação ausente que muda a base, o estado ou a segurança da próxima task.

Uma colisão de código não deve ser apresentada como dependência formal. Uma posição próxima no ciclo
não deve ser tratada como dependência sem evidência.

## User Stories

### P1: Assess the Active Delivery Front

**User Story**: Como engenheiro com uma PR aguardando review, quero ver o estado combinado do ciclo,
das PRs e dos repos para continuar trabalhando sem perder rastreabilidade.

**Why P1**: Nenhuma transição segura pode ser recomendada sem uma fotografia coerente das três
fontes operacionais.

**Acceptance Criteria**:

1. **DFC-01** — WHEN o usuário pedir continuidade de uma frente THEN o sistema SHALL consultar, sem
   mutar, as issues relevantes do Linear, as PRs ativas e o estado Git dos repos prováveis.
2. **DFC-02** — WHEN fontes forem consultadas THEN o sistema SHALL registrar timestamp, freshness,
   branch de integração, PR/branch/head/base, draft, review, CI, issue, estado e relações conhecidas.
3. **DFC-03** — WHEN GitHub, Linear ou um repo necessário estiver indisponível THEN o sistema SHALL
   declarar a evidência ausente e não recomendar uma transição que dependa dela como segura.
4. **DFC-04** — WHEN o worktree estiver sujo THEN o sistema SHALL identificar os caminhos sem
   alterá-los e impedir qualquer recomendação que pressuponha branch switching naquele worktree.

**Independent Test**: Fornecer um snapshot com uma PR pronta e um repo sujo; o relatório identifica
ambos, não altera estado e bloqueia somente as transições afetadas.

### P1: Select the Next Merge-Safe Task

**User Story**: Como engenheiro seguindo um ciclo, quero que a próxima task seja classificada pela
relação com as PRs pendentes para evitar espera desnecessária e stacks artificiais.

**Why P1**: A continuidade depende de selecionar trabalho que possa ser integrado com risco
controlado, não apenas a próxima issue por prioridade.

**Acceptance Criteria**:

1. **DFC-05** — WHEN houver candidatas prontas THEN o sistema SHALL classificar cada candidata como
   `independent`, `dependent`, `conflicting` ou `blocked`, citando evidência e nível de confiança.
2. **DFC-06** — WHEN existir uma candidata independente compatível com a ordem do ciclo THEN o
   sistema SHALL preferi-la a criar um stack dependente.
3. **DFC-07** — WHEN houver colisão sem dependência funcional THEN o sistema SHALL recomendar outra
   candidata independente ou espera explícita, sem inventar relação formal.
4. **DFC-08** — WHEN já existirem uma PR pronta e uma segunda task ativa/draft no mesmo repo THEN o
   sistema SHALL recusar iniciar uma terceira frente dependente e recomendar concluir ou promover a
   frente existente.
5. **DFC-09** — WHEN a seleção envolver mais de um repo THEN o sistema SHALL declarar o merge order
   herdado e manter branches, PRs e gates separados por repo.

**Independent Test**: Dadas quatro candidatas, uma de cada classe, o relatório escolhe a independente
e explica por que as demais não são a primeira ação.

### P1: Produce a Delivery Contract

**User Story**: Como engenheiro iniciando a próxima task, quero um contrato de branch e PR antes da
implementação para saber como o trabalho será entregue após o merge anterior.

**Why P1**: A base errada só costuma aparecer no final, quando o custo de separar commits e diffs já
é alto.

**Acceptance Criteria**:

1. **DFC-10** — WHEN uma task independente for selecionada THEN o sistema SHALL recomendar branch a
   partir da integração atual, PR final contra a integração e estado draft apenas quando a ordem de
   entrega exigir.
2. **DFC-11** — WHEN uma task realmente dependente for selecionada THEN o sistema SHALL recomendar
   branch a partir do head exato da PR-base, PR draft contra a branch-base e registro do boundary
   SHA e do destino final.
3. **DFC-12** — WHEN produzir o contrato THEN o sistema SHALL incluir issue, repo, branch de trabalho,
   base SHA, PR-base, base inicial, base final, estado Linear, estado PR, escopo de arquivos esperado,
   gates e condições para promoção.
4. **DFC-13** — WHEN o contrato for entregue THEN o sistema SHALL recomendar exatamente uma próxima
   ação e indicar quais ações futuras exigem aprovação.

**Independent Test**: Gerar contratos para uma task independente e uma dependente; cada um contém
bases, estados e condição de promoção distintos.

### P2: Plan Post-Merge Reconciliation

**User Story**: Como engenheiro com uma PR draft, quero um plano preciso para reconciliá-la depois do
merge da PR-base sem carregar os commits ou o escopo da task anterior.

**Why P2**: O Portal usa squash merge; uma atualização genérica pode reaplicar a task-base ou produzir
um diff enganoso.

**Acceptance Criteria**:

1. **DFC-14** — WHEN a PR-base de uma branch independente mergear THEN o sistema SHALL planejar a
   atualização sobre a integração, revalidação do diff e gates antes de promover a PR draft.
2. **DFC-15** — WHEN a PR-base de um stack mergear por squash THEN o sistema SHALL usar o boundary SHA
   para planejar a reaplicação exclusiva dos commits da task dependente sobre a integração.
3. **DFC-16** — WHEN a PR-base receber novos commits antes do merge THEN o sistema SHALL marcar o
   plano anterior como stale e exigir nova avaliação de impacto e novo boundary antes da promoção.
4. **DFC-17** — WHEN a PR-base for fechada sem merge THEN o sistema SHALL bloquear promoção automática
   e exigir replanejamento da dependência contra a integração.
5. **DFC-18** — WHEN a reconciliação for planejada THEN o sistema SHALL exigir comparação antes/depois,
   diff somente da task, gates aplicáveis e CI verde antes de `Ready for review` / `In Review`.
6. **DFC-19** — WHEN uma futura operação exigir reescrever branch publicada THEN o sistema SHALL
   limitar a ação a branch draft de propriedade do usuário, usar `--force-with-lease` e pedir
   autorização explícita; o MVP read-only somente descreve essa condição.

**Independent Test**: Simular squash merge, atualização da PR-base e fechamento sem merge; cada caso
produz uma transição diferente e nenhuma mutação.

### P2: Preserve Task-Only Delivery

**User Story**: Como revisor, quero que cada PR contenha apenas o trabalho da sua task para poder
avaliar escopo, gates e contrato sem ruído da task anterior.

**Why P2**: Continuidade só agrega valor se não degradar a superfície de review.

**Acceptance Criteria**:

1. **DFC-20** — WHEN uma PR draft estiver pronta para promoção THEN o sistema SHALL comparar a
   superfície final com o contrato de entrega e listar arquivos inesperados.
2. **DFC-21** — WHEN commits ou arquivos da task-base permanecerem na superfície final THEN o sistema
   SHALL bloquear a recomendação de promoção.
3. **DFC-22** — WHEN artefatos locais ou de validação não pertencerem ao contrato do produto THEN o
   sistema SHALL mantê-los fora do commit e da PR sem apagá-los automaticamente.

**Independent Test**: Introduzir um arquivo da task-base e um artefato local no snapshot; a promoção
é bloqueada e nenhum arquivo é removido.

## State Model

| Delivery state | Linear | Pull request | Allowed next transition |
| --- | --- | --- | --- |
| `ready` | Ready to Start | none | Start selected task |
| `active` | In Progress | none or draft | Implement or validate |
| `waiting-base` | In Progress | draft against dependency | Refresh plan or wait for base |
| `reconciling` | In Progress | draft | Update base, diff and gates |
| `reviewable` | In Review | ready against final integration | Review or changes requested |
| `changes-requested` | In Progress or In Review per local policy | ready/draft | Correct and revalidate |
| `merged` | Done through canonical workflow | merged | Select next task |
| `abandoned-base` | In Progress or Blocked | draft | Replan or cancel |

Invalid transitions include `waiting-base → reviewable` without reconciliation, `active → merged`
without a reviewable PR, and any transition that creates a third dependent front in the same repo.

## Implicit-Requirement Dimensions

| Dimension | Resolution |
| --- | --- |
| Input validation and bounds | Require registered project/repo, identifiable cycle or issue set, resolvable integration branch, WIP ≤ 2 and stack depth ≤ 1. |
| Failure and partial failure | Missing Linear, GitHub or Git evidence produces a partial report and blocks only conclusions that require the missing source. No rollback is needed in the read-only MVP. |
| Idempotency and retry | Repeating an assessment against the same snapshot SHALL produce the same classification and SHALL not create external state. |
| Auth boundaries and rate limits | Use existing read-only credentials; never print tokens. Handle API denial or throttling as unavailable evidence. |
| Concurrency and ordering | Timestamp every source; detect changed PR head/base/status before relying on an earlier plan. Prefer one ready + one active/draft per repo. |
| Data lifecycle and expiry | Chat reports are ephemeral. Proposed stack metadata must have a durable, non-secret destination validated during the pilot; `session-context/` alone is insufficient across machines. |
| Observability | Report consulted sources, snapshot time, evidence class, selected candidate, rejected candidates and exact reason for every blocked transition. |
| External dependency failure | GitHub or Linear failure must degrade to an explicitly incomplete plan, never an inferred safe transition. |
| Operational enablement | MVP needs read access to Git, GitHub and Linear. Future mutation needs authenticated write access, clean worktree, protected-branch awareness and explicit approval. |
| State-transition integrity | Enforce the state table, WIP cap, stack-depth cap, reconciliation gate and task-only diff gate. |

## Future Skill Contract

Planned name: `advance-delivery-front`.

Candidate triggering description:

> Coordinate continuity across Inventeer tasks when one or more PRs await review or merge by
> inspecting the active delivery front, selecting the next merge-safe issue, distinguishing
> independent from stacked work, producing branch/PR contracts, and planning post-merge
> reconciliation. Use when the user wants to continue a cycle without waiting for a PR, prepare a
> dependent draft PR, resume after an upstream merge, or verify that a promoted PR contains only its
> own task. Start read-only; require explicit authorization for GitHub, Linear, or Git mutations.

Planned reusable contents:

```text
.agents/skills/advance-delivery-front/
├── SKILL.md
├── agents/openai.yaml
├── references/
│   └── continuity-policy.md
└── scripts/
    └── inspect-git-front.sh
```

- `SKILL.md`: concise orchestration, evidence model, boundaries and handoffs.
- `continuity-policy.md`: state model, classification rules, squash-stack reconciliation and future
  mutation protocol.
- `inspect-git-front.sh`: deterministic read-only capture of refs, worktrees, branch ancestry,
  merge bases and changed paths. It must not fetch, checkout, branch, rebase, push or edit files.
- Mutation scripts are excluded from the MVP and require a separate approved revision.

## Handoffs

```text
triage-project-cycle
    -> selects and classifies the next merge-safe task

advance-delivery-front
    -> owns the active PR/task topology and delivery contract

portal-task-context | assistants-task-context
    -> prepares the selected single issue with the delivery contract attached

tlc-spec-driven
    -> specifies, implements and validates only that issue

advance-delivery-front
    -> reassesses promotion after review or merge events
```

The continuity skill must not duplicate full issue context or TLC execution.

## Requirement Traceability

| Requirement | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| DFC-01..04 | Assess front | ISSUE | User request and observed PR wait | Specify | Approved |
| DFC-05..09 | Select next | DECISION | Approved WIP and merge-safe model | Specify | Approved |
| DFC-10..13 | Delivery contract | DECISION | Approved read-only-first recommendation | Specify | Approved |
| DFC-14..19 | Reconciliation | INHERITED | Portal squash merge plus safety requirements | Specify | Approved |
| DFC-20..22 | Task-only delivery | ISSUE | Repeated requirement that PR contain only task work | Specify | Approved |

**Coverage:** 22 requirements; all mapped to independently testable stories; no implementation tasks
created in this phase.

## Success Criteria

- [ ] Given one ready PR and at least two candidate issues, the MVP identifies a merge-safe next task
  or explains why none is safe without mutating state.
- [ ] Independent and dependent candidates receive different branch/PR contracts.
- [ ] A squash-merged dependency produces a boundary-aware reconciliation plan.
- [ ] Stale, dirty, unavailable and abandoned-base cases never produce a false-safe recommendation.
- [ ] No plan permits more than one ready PR plus one active/draft task per repo.
- [x] The user approved AD-022 without needing implementation details from the future skill.

## Approval Record

Approved by the user on 2026-07-22. This approval authorizes:

1. keeping `Status` as `Approved`;
2. keeping AD-022 in `.specs/STATE.md` as `active`;
3. designing and tasking the read-only MVP of `advance-delivery-front`.

It does not authorize branch, worktree, PR, Linear, rebase, push or force-push operations.
