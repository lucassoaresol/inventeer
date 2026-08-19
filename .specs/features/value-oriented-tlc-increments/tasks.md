# Incrementos de Valor na TLC — Tasks

## Execution Protocol (MANDATORY -- do not skip)

Implementar com `tlc-spec-driven`, preservando a proibição explícita de subagentes desta sessão. As
três tarefas executam serialmente e pertencem ao mesmo `Value Increment`; gates de tarefa atualizam
status e Handoff, mas nenhum commit comportamental existe antes do gate terminal do incremento.

**Design:** `.specs/features/value-oriented-tlc-increments/design.md`
**Status:** Complete

## Test Coverage Matrix

> Gerada a partir de `AGENTS.md`, AD-040, `scripts/test-workspace.sh` e das fixtures TLC existentes.

| Code Layer | Required Test Type | Coverage Expectation | Location Pattern | Run Command |
| --- | --- | --- | --- | --- |
| Parser/schema de tasks | contract | VIC-01..06, VIC-22..23; casos positivos, campos ausentes, IDs e ownership inválidos | `scripts/test-tlc-value-increments.py`, `scripts/test-tlc-deterministic-gates.py` | `python3 scripts/test-tlc-value-increments.py && python3 scripts/test-tlc-deterministic-gates.py` |
| Instruções TLC | contract | VIC-07..21, VIC-24..27; todas as superfícies vivas, batching, Verifier, fallback e frases proibidas | `scripts/test-tlc-value-increments.py` | `python3 scripts/test-tlc-value-increments.py` |
| Integração do workspace | integration | Registry, decisão, índice, links, suíte única no gate e preservação dual-engine | `scripts/test-workspace-structure.py`, `scripts/test-workspace.sh` | `python3 scripts/test-workspace-structure.py && bash scripts/test-workspace.sh` |

## Gate Check Commands

| Gate Level | When to Use | Canonical Command | Resource-Aware Equivalent (if needed) |
| --- | --- | --- | --- |
| Quick | Após parser/fixtures ou instruções/sensor | `python3 scripts/test-tlc-value-increments.py && python3 scripts/test-tlc-deterministic-gates.py` | N/A |
| Full | Após integração da raiz | `bash scripts/test-workspace.sh` | Runner sequencial já canônico. |
| Build | Fechamento do VI-001 | `python3 scripts/workspace-gate-evidence.py run --profile workspace` | Runner sequencial já canônico; executar preflight antes. |
| Diff integrity | Validação da feature | `git diff --check 1032d1e..<evidence-head>` | N/A |

## Value Increment Plan

| Value Increment | Outcome | Requirements | Tasks | Terminal Gate | Rollback Boundary | Proposed Commit |
| --- | --- | --- | --- | --- | --- | --- |
| VI-001 | A TLC planeja, executa e valida commits por outcome completo sem perder granularidade, checkpoints, dual-engine ou Verifier. | VIC-01..27 | T1, T2, T3, T4 | Build | Reverter a customização vendorizada, seu sensor e a adoção local sem alterar histories ou repos de produto. | `feat(workflow): adopt value-oriented increments` |

## Execution Plan

### Phase 1: Capacidade e adoção

```text
T1 -> T2 -> T3 -> T4
```

## Task Breakdown

### T1: Tornar o schema de Value Increment determinístico

**What:** Estender o validador de tasks e suas fixtures prospectivas para exigir o plano `VI-NNN` e ownership exato de cada tarefa.
**Where:** `.agents/skills/tlc-spec-driven/scripts/`
**Depends on:** None
**Reuses:** `validate_tasks.py`, `check_commit.py`, AD-040 e fixtures existentes
**Requirement:** VIC-01..06, VIC-11, VIC-22..23
**Value Increment:** VI-001

**Done when:**

- [x] `Value Increment Plan` e seus sete campos são obrigatórios para planos novos/revisados.
- [x] Uma ou várias tarefas válidas podem pertencer ao mesmo incremento.
- [x] Task sem owner, owner desconhecido, ownership duplicado, task desconhecida e campo vazio falham com erro específico.
- [x] A mensagem proposta segue o mesmo contrato de `check_commit.py`.
- [x] Fixtures prospectivas da TLC usam o schema novo; artifacts históricos não são alterados.
- [x] O gate Quick passa sem warnings.

**Tests:** contract
**Gate:** quick

### T2: Alinhar Planning, Execute, Handoff, batching e Verifier

**What:** Substituir toda instrução task-to-commit viva pela máquina de estados de Value Increment e adicionar o sensor de regressão vendorizada.
**Where:** `.agents/skills/tlc-spec-driven/`
**Depends on:** T1
**Reuses:** implementação EDREN `47ff1fd`, contratos locais de subagentes, memory e validation
**Requirement:** VIC-07..21, VIC-24..27
**Value Increment:** VI-001

**Done when:**

- [x] `SKILL.md`, Tasks, Execute, Memory, Sub-agents e Validate descrevem a mesma fronteira de incremento.
- [x] Task gate fecha tarefa; Handoff cobre incremento aberto; terminal gate autoriza o commit único.
- [x] Batch nunca divide um `Value Increment`; Verifier roda após o último incremento e fallback standalone permanece completo.
- [x] Correções pré/pós-publicação e history rewrite incerto possuem outcomes explícitos.
- [x] `.agents/vendor.json` registra a customização e o sensor task-to-commit.
- [x] O sensor rejeita frases antigas, commit prematuro e marcadores EDREN-only, preservando Codex/Claude.
- [x] O gate Quick passa sem warnings.

**Tests:** contract
**Gate:** quick

### T3: Adotar o contrato no workspace e fechar o incremento

**What:** Integrar a nova suíte ao gate agregado, registrar AD-047, indexar a feature e fechar spec/tasks/traceability no mesmo outcome comportamental.
**Where:** `workspace contract surfaces`
**Depends on:** T2
**Reuses:** `scripts/test-workspace.sh`, feature index, decision index e Handoff freshness
**Requirement:** VIC-01..27
**Value Increment:** VI-001

**Done when:**

- [x] A suíte de Value Increment aparece exatamente uma vez no gate agregado.
- [x] AD-047 governa features futuras sem superseder AD-040, AD-045 ou AD-046.
- [x] Feature index, spec e tasks refletem cobertura completa e status do incremento.
- [x] Os dois arquivos de lessons preexistentes permanecem fora do incremento.
- [x] Preflight de recursos aprova a estratégia sequencial.
- [x] O gate Build terminal passa e gera receipt fresco antes do commit proposto.
- [x] `check_commit.py` aprova `feat(workflow): adopt value-oriented increments`.

**Tests:** integration
**Gate:** build

### T4: Fechar gaps do discrimination sensor

**What:** Fortalecer o sensor para rejeitar ID malformado, task omitida do plano e inversão da semântica de publicação encontrada pelo Verifier standalone.
**Where:** `scripts/test-tlc-value-increments.py`
**Depends on:** T3
**Reuses:** fixtures isoladas, `required_contracts` e o ciclo fix-to-reverify da TLC
**Requirement:** VIC-02..03, VIC-13..15, VIC-22, VIC-25..26
**Value Increment:** VI-001

**Done when:**

- [x] `VI-1` falha com o erro específico de ID inválido.
- [x] Uma task existente fora da tabela falha com o erro específico de ownership ausente.
- [x] A inversão das regras antes/depois da publicação falha no contrato textual.
- [x] As três mutações isoladas são mortas e o worktree real preserva seu porcelain inicial.
- [x] O gate Quick passa sem warnings.

**Tests:** contract
**Gate:** quick

## Phase Execution Map

```text
Phase 1
T1 -> T2 -> T3 -> T4
```

## Task Granularity Check

| Task | Semantic scope | Revert/verification unit | Status |
| --- | --- | --- | --- |
| T1 | Um schema/parser de planejamento | Fixtures do parser + revert do parser | PASS |
| T2 | Uma máquina de estados da skill | Sensor de instruções + revert da customização | PASS |
| T3 | Uma adoção de workspace | Gate agregado + decisão/índice/spec | PASS |
| T4 | Uma correção de sensor | Três mutações reproduzidas + revert do teste | PASS |

## Diagram-Definition Cross-Check

| Task | Depends On | Diagram Shows | Status |
| --- | --- | --- | --- |
| T1 | None | Start | PASS |
| T2 | T1 | T1 -> T2 | PASS |
| T3 | T2 | T2 -> T3 | PASS |
| T4 | T3 | T3 -> T4 | PASS |

## Test Co-location Validation

| Task | Code Layer Created/Modified | Matrix Requires | Task Says | Status |
| --- | --- | --- | --- | --- |
| T1 | Parser/schema de tasks | contract | contract | PASS |
| T2 | Instruções TLC e sensor | contract | contract | PASS |
| T3 | Integração do workspace | integration | integration | PASS |
| T4 | Sensor de regressão | contract | contract | PASS |
