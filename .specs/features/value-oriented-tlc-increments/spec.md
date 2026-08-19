# Incrementos de Valor na TLC

**Status:** Implemented
**Review language:** Portuguese
**Canonical language:** Portuguese

## Problem Statement

A TLC vendorizada mantém tarefas pequenas e verificáveis, mas associa cada tarefa a um commit. Esse
acoplamento transforma atividades mecânicas e checkpoints de sessão em unidades permanentes do
histórico, separando código, testes, documentação e rastreabilidade que entregam o mesmo resultado.

O workspace precisa preservar a granularidade das tarefas e seus gates, mas registrar no Git apenas
incrementos completos, verificáveis e reversíveis de valor. A customização deve funcionar nos dois
engines previstos pela AD-045 e portar somente a capacidade comprovada no EDREN.

## Goals

- [x] Definir `Value Increment` como a unidade planejada e validada de commit da TLC.
- [x] Manter tarefas atômicas, gates por tarefa, traceability e checkpoints recuperáveis.
- [x] Impedir deterministicamente a volta do contrato task-to-commit.
- [x] Preservar o Verifier, a delegação opt-in e a compatibilidade Codex/Claude deste workspace.
- [x] Registrar a customização sobre a skill vendorizada sem migrar artifacts históricos concluídos.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Executar o piloto operacional dual-engine | É a Frente 3 e depende desta capacidade já adotada. |
| Alterar Linear, GitHub ou repositórios em `repos/` | Esta é uma melhoria do fluxo local do workspace. |
| Importar a política Codex-only, single-agent ou de modelos do EDREN | Essas decisões conflitam com a AD-045 e não são necessárias ao commit por valor. |
| Reescrever ou consolidar o histórico Git existente | A mudança governa entregas futuras; história publicada não será alterada. |
| Migrar todos os `tasks.md` concluídos | Artifacts históricos preservam o contrato sob o qual foram executados. |
| Definir um número ideal fixo de tarefas ou commits | A fronteira é outcome, gate e rollback, não contagem. |

---

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Unidade de commit | Um `Value Increment` completo, verificável e reversível | Representa valor revisável sem usar Git como checkpoint de tarefa. | y |
| Unidade de execução | Tarefas permanecem atômicas e verificadas individualmente | Granularidade reduz risco e conserva traceability. | y |
| Checkpoint intermediário | Handoff section-scoped enquanto o incremento estiver aberto | Recupera quedas sem publicar valor incompleto. | y |
| Correção antes da publicação | Incorporar ao incremento ainda aberto ou ao fechamento documental imediatamente associado | Evita commits corretivos mecânicos antes de existir uma entrega publicada. | y |
| Correção depois da publicação | Criar novo incremento e commit auditável | História remota não deve ser reescrita implicitamente. | y |
| Compatibilidade histórica | Não alterar artifacts concluídos; planos novos ou materialmente revisados usam o schema novo | Evita backfill sem enfraquecer o contrato futuro. | y |
| Compatibilidade de engines | Preservar delegação opt-in, Verifier por subagente quando autorizado e fallback standalone | Mantém a AD-045 e não importa decisões locais do EDREN. | y |
| Customização vendorizada | Registrar capacidade e sensor em `.agents/vendor.json` | Uma atualização upstream precisa tornar o merge e a regressão explícitos. | y |

**Open questions:** none - o planejamento foi aprovado na sessão de retrospectiva e retomado nesta
sessão.

---

## User Stories

### P1: Planejar entregas por incremento verificável de valor

**User Story:** Como mantenedor do workspace, quero agrupar tarefas que produzem o mesmo outcome para
que o plano declare antecipadamente a unidade real de revisão e rollback.

**Why P1:** Sem uma fronteira explícita, o executor volta naturalmente a confundir tarefa com commit.

**Acceptance Criteria:**

1. The TLC workflow SHALL definir `Value Increment` como um outcome completo, verificável e reversível que contém uma ou mais tarefas atômicas. `VIC-01`
2. WHEN um `tasks.md` novo ou materialmente revisado for apresentado THEN o plano SHALL conter `Value Increment Plan` com ID `VI-NNN`, outcome, requisitos, tarefas, gate terminal, fronteira de rollback e Conventional Commit proposto. `VIC-02`
3. WHEN tarefas formais forem planejadas THEN cada tarefa SHALL pertencer exatamente a um `VI-NNN` existente e aparecer exatamente uma vez no `Value Increment Plan`. `VIC-03`
4. WHERE um outcome exigir várias tarefas sequenciais, o plano SHALL permitir agrupá-las no mesmo incremento sem reduzir a verificação individual. `VIC-04`
5. WHERE uma tarefa já representar todo o outcome verificável, o plano SHALL permitir um incremento com uma única tarefa. `VIC-05`
6. IF conjuntos de tarefas possuírem gates terminais ou fronteiras de rollback independentes THEN o plano SHALL representá-los como incrementos separados. `VIC-06`

**Independent Test:** Validar fixtures com uma e várias tarefas, ownership duplicado, referência
desconhecida e campos vazios no plano de incrementos.

### P1: Executar e commitar somente valor completo

**User Story:** Como mantenedor do workspace, quero que cada commit carregue o outcome completo e
verde para revisar, bisectar e reverter entregas sem reconstruir microcommits mecânicos.

**Why P1:** O histórico deve representar entregas, enquanto tarefas e Handoff representam progresso.

**Acceptance Criteria:**

1. WHEN uma tarefa terminar THEN o executor SHALL executar seu gate, atualizar status e traceability e manter o incremento aberto sem commit se ainda houver tarefas nele. `VIC-07`
2. WHILE um incremento permanecer aberto, o executor SHALL usar o Handoff section-scoped como checkpoint recuperável com tarefas verificadas e próximo passo exato. `VIC-08`
3. WHEN a última tarefa de um incremento estiver verde THEN o executor SHALL executar o gate terminal declarado antes de criar seu único commit. `VIC-09`
4. WHEN o commit do incremento for criado THEN ele SHALL incluir código, testes, status de tarefas, traceability e documentação necessários ao mesmo outcome. `VIC-10`
5. WHEN o commit do incremento for criado THEN sua mensagem SHALL passar por `check_commit.py` e descrever o outcome predominante. `VIC-11`
6. IF qualquer gate de tarefa ou terminal falhar THEN o executor SHALL manter o incremento não concluído e não criar seu commit. `VIC-12`
7. IF uma correção for descoberta antes da publicação do incremento THEN o executor SHALL incorporá-la ao incremento aberto ou ao fechamento documental inseparável do mesmo outcome. `VIC-13`
8. IF uma correção for necessária depois que o incremento estiver publicado THEN o executor SHALL criar um novo incremento auditável sem reescrever a história remota. `VIC-14`
9. IF a segurança ou o alvo de uma consolidação local forem incertos THEN o executor SHALL solicitar direção antes de reescrever a história. `VIC-15`

**Independent Test:** Inspecionar o contrato Execute e simular gates verdes/falhos, correções antes e
depois da publicação e mensagens Conventional Commit.

### P1: Preservar verificação, delegação e evolução vendorizada

**User Story:** Como operador Codex e Claude do workspace, quero que a mudança de commits não altere
as fronteiras de qualidade, engines ou ownership existentes.

**Why P1:** A capacidade só é portável se não importar decisões EDREN-only nem enfraquecer o Verifier.

**Acceptance Criteria:**

1. WHEN fases forem empacotadas para execução delegada THEN um `Value Increment` SHALL permanecer inteiro em um único batch e nunca ser dividido entre workers. `VIC-16`
2. WHEN o último incremento da feature for commitado THEN o workflow SHALL executar o Verifier obrigatório com outcome check e discrimination sensor. `VIC-17`
3. WHERE subagentes não estiverem disponíveis ou autorizados, o workflow SHALL executar o fallback standalone fresh-eyes sem reduzir evidence-or-zero ou o discrimination sensor. `VIC-18`
4. The vendored skill SHALL preservar suporte operacional a Codex e Claude e SHALL omitir políticas Codex-only, single-agent ou de modelo fixo copiadas do EDREN. `VIC-19`
5. WHEN a customização for adotada THEN `.agents/vendor.json` SHALL registrar `value-oriented increments` e seu sensor de regressão task-to-commit. `VIC-20`
6. WHEN o contrato da skill for testado THEN um sensor determinístico SHALL rejeitar instruções vivas que exijam um commit por tarefa ou permitam commit antes do gate terminal. `VIC-21`
7. WHEN o validador receber um plano novo sem schema de incremento ou com ownership inconsistente THEN ele SHALL falhar fechado com erros específicos. `VIC-22`
8. WHILE artifacts históricos concluídos permanecerem inalterados, a adoção SHALL preservá-los sem backfill e SHALL exigir o schema novo somente quando um plano for criado ou materialmente revisado. `VIC-23`

**Independent Test:** Executar o sensor contra skill, referências, validador e registry; provar que o
contrato de subagentes e o fallback standalone continuam presentes e que um artifact histórico não é
reescrito.

## Edge Cases

- IF uma feature pequena combinar código, testes e documentação no mesmo outcome THEN o workflow SHALL usar o tipo Conventional Commit predominante sem fragmentar por tipo de arquivo. `VIC-24`
- IF o Verifier encontrar gap antes da publicação THEN o workflow SHALL manter ou reabrir o incremento relevante e repetir o ciclo fix-to-reverify limitado. `VIC-25`
- IF o Verifier encontrar gap depois da publicação THEN o workflow SHALL registrar a correção em novo incremento auditável. `VIC-26`
- WHEN uma atualização upstream tocar as mesmas superfícies da customização THEN o merge SHALL preservar ou substituir explicitamente o contrato e o sensor de Value Increment. `VIC-27`

## Implicit-Requirement Dimensions

| Dimension | Resolution |
| --- | --- |
| Compatibility & representation | Schema novo governa planos novos/revisados; artifacts concluídos permanecem históricos sem backfill. |
| Failure / partial-failure states | Gate falho mantém incremento aberto e sem commit; Handoff registra o próximo passo. |
| Concurrency / ordering | Tarefas continuam ordenadas e um incremento não pode atravessar batches. |
| Observability | Plano registra outcome, requisitos, tarefas, gate terminal, rollback e mensagem proposta. |
| State-transition integrity | Task gate fecha tarefa; terminal gate fecha incremento; publicação decide se correção pode integrar ou exige novo incremento. |
| Remaining dimensions | N/A porque não há persistência de produto, chamada externa, autenticação, pagamento, TTL ou protocolo de rede nesta mudança de workflow local. |

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| VIC-01 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-02 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-03 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-04 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-05 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-06 | P1: Planejamento | DECISION | Recomendação retrospectiva aprovada e evidência EDREN `47ff1fd` | Execute | Verified |
| VIC-07 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-08 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-09 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-10 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-11 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-12 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-13 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-14 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-15 | P1: Execução | DECISION | Recomendação retrospectiva aprovada e Handoff AD-046 | Execute | Verified |
| VIC-16 | P1: Compatibilidade | INHERITED | AD-045 e contrato TLC 3.3.0 atual | Execute | Verified |
| VIC-17 | P1: Compatibilidade | INHERITED | AD-045 e contrato TLC 3.3.0 atual | Execute | Verified |
| VIC-18 | P1: Compatibilidade | INHERITED | AD-045 e contrato TLC 3.3.0 atual | Execute | Verified |
| VIC-19 | P1: Compatibilidade | INHERITED | AD-045 e contrato TLC 3.3.0 atual | Execute | Verified |
| VIC-20 | P1: Vendorização | INHERITED | `.agents/vendor.json`, skill-creator e artifacts históricos | Execute | Verified |
| VIC-21 | P1: Vendorização | INHERITED | `.agents/vendor.json`, skill-creator e artifacts históricos | Execute | Verified |
| VIC-22 | P1: Vendorização | INHERITED | `.agents/vendor.json`, skill-creator e artifacts históricos | Execute | Verified |
| VIC-23 | P1: Vendorização | INHERITED | `.agents/vendor.json`, skill-creator e artifacts históricos | Execute | Verified |
| VIC-24 | Edge cases | DECISION | Retrospectiva cross-workspace e limites de publicação | Execute | Verified |
| VIC-25 | Edge cases | DECISION | Retrospectiva cross-workspace e limites de publicação | Execute | Verified |
| VIC-26 | Edge cases | DECISION | Retrospectiva cross-workspace e limites de publicação | Execute | Verified |
| VIC-27 | Edge cases | DECISION | Retrospectiva cross-workspace e limites de publicação | Execute | Verified |

**Coverage:** 27 total, 27 mapped to tasks, 0 unmapped.

## Success Criteria

- [x] O validador aceita várias tarefas em um incremento e rejeita todo ownership incompleto ou ambíguo.
- [x] Nenhuma instrução viva da TLC exige commit por tarefa.
- [x] Execute, Handoff, delegação e Verifier descrevem a mesma fronteira de incremento.
- [x] O gate agregado inclui um sensor determinístico da customização vendorizada.
- [x] A skill continua compatível com Codex e Claude, sem regras EDREN-only.
- [x] O histórico da própria feature fecha por outcomes, sem microcommit por artifact.
