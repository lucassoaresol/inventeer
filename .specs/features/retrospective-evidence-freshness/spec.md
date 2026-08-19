# Retrospective Evidence Freshness Specification

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** Portuguese

## Problem Statement

O auditor de sessões mistura sessões físicas e continuations sob `primary_sessions`, informa
exclusões solicitadas como se tivessem sido aplicadas e não transporta proveniência suficiente para
comparar cohorts coletados em máquinas diferentes. O Handoff versionado também pode continuar
descrevendo ações transitórias depois que o Git já invalidou esse estado.

## Goals

- [x] Produzir um relatório retrospectivo sanitizado, inequívoco, reproduzível e portátil.
- [x] Tornar o Handoff do workspace verificável contra o SHA e o estado de publicação registrados.
- [x] Distinguir validação de contrato de comprovação operacional nos relatórios aplicáveis.

## Out of Scope

| Feature | Reason |
| --- | --- |
| Alterar histories locais de Codex ou Claude | O auditor permanece estritamente read-only. |
| Persistir transcripts, IDs de sessão ou paths absolutos | A evidência deve continuar sanitizada e portátil. |
| Alterar Linear, GitHub ou repositórios sob `repos/` | Esta é uma melhoria do workspace pessoal. |
| Adotar Value Increments na TLC | Essa mudança permanece na próxima frente independente. |
| Comprovar operação dual-engine do Portal | Essa comprovação pertence ao piloto posterior. |
| Instrumentar execução APEX end-to-end | O critério da AD-034 permanece inalterado. |

## Assumptions & Open Questions

| Assumption / decision | Chosen default | Rationale | Confirmed? |
| --- | --- | --- | --- |
| Compatibilidade do relatório v2 | O contrato v3 remove nomes ambíguos em vez de preservar aliases silenciosos. | Um alias manteria o risco de interpretação que motivou a mudança; consumidores locais serão atualizados no mesmo outcome. | y |
| Identidade portátil do workspace | O receipt recebe um identificador lógico explícito e representa o cwd como `<workspace-root>`. | Um nome lógico permite comparar máquinas sem persistir paths locais. | y |
| Comando reproduzível sem IDs | O receipt registra argumentos normalizados e contagens de exclusão, nunca os IDs fornecidos. | Preserva os parâmetros semanticamente relevantes sem expor identificadores de sessão. | y |
| Checksum do resultado | O receipt calcula SHA-256 sobre o relatório canônico sem o próprio envelope de proveniência. | Evita autorreferência e permite verificar bytes reproduzíveis. | y |
| Freshness do Handoff | Um helper local valida e substitui somente `## Handoff`, registrando SHA comportamental, publicação e invalidação. Descendants limitados a Handoff, spec, index e validation não invalidam o SHA comportamental. | Comparar literalmente com o commit que contém o próprio Handoff criaria uma referência autorrecursiva impossível; a allowlist preserva apenas fechamento de evidência. | y |
| Veredictos existentes | Somente relatórios criados ou materialmente revisados por esta feature recebem os dois eixos. | A AD-040 proíbe revalidar retroativamente todo o histórico. | y |

**Open questions:** none - all resolved or logged above.

## User Stories

### P1: Emitir evidência retrospectiva inequívoca e portátil

**User Story:** Como mantenedor do workspace, quero comparar retrospectivas entre máquinas sem
confundir sessões, continuations ou exclusões para tomar decisões sobre o fluxo com cohorts válidos.

**Why P1:** As decisões AD-041 e AD-045 dependem dessas contagens, e o contrato atual admite
interpretações diferentes para a mesma saída.

**Acceptance Criteria:**

1. WHEN o auditor produzir um relatório THEN ele SHALL identificar o contrato como versão 3 e SHALL omitir o campo `primary_sessions`. `REF-01`
2. WHEN sessões Codex forem agregadas THEN o relatório SHALL separar `session_instances`, `continuations` e `logical_work_streams` com valores exatos. `REF-02`
3. WHEN sessões Claude forem agregadas THEN o relatório SHALL separar `session_instances`, `sidechains` e `logical_sessions` com valores exatos. `REF-03`
4. WHEN IDs forem fornecidos para exclusão THEN o relatório SHALL separar `exclusions_requested`, `exclusions_matched` e `exclusions_unmatched`. `REF-04`
5. IF um ID solicitado não pertencer ao cwd ou à janela THEN o auditor SHALL contá-lo como não encontrado e SHALL preservar as contagens do cohort. `REF-05`
6. WHEN o modo receipt for solicitado THEN o auditor SHALL emitir o relatório, seu SHA-256 e a proveniência sanitizada do auditor, da janela, do workspace lógico e dos argumentos normalizados. `REF-06`
7. The receipt SHALL representar a raiz como `<workspace-root>` e SHALL omitir cwd absoluto, IDs de sessão, paths de transcript, prompts e respostas. `REF-07`
8. WHEN o mesmo cohort e o mesmo auditor forem executados em roots físicos diferentes THEN os campos portáteis e o checksum do relatório SHALL permanecer iguais. `REF-08`

**Independent Test:** Fixtures Codex e Claude equivalentes executadas em dois roots temporários
produzem o mesmo receipt portátil e discriminam todas as contagens e exclusões.

### P1: Tornar o Handoff autoconsciente de sua validade

**User Story:** Como mantenedor do workspace, quero que o Handoff declare o estado Git que ele
descreve para não executar instruções transitórias depois que commits ou publicação mudarem.

**Why P1:** O Handoff atual ainda solicita review e push de commits que já estão em `origin/main`.

**Acceptance Criteria:**

1. WHEN o helper gravar um Handoff THEN ele SHALL registrar `Recorded at`, `Valid at SHA`, `Publication state` e `Invalidated by`. `REF-09`
2. WHEN o helper gravar um Handoff THEN ele SHALL substituir somente a seção `## Handoff` e SHALL preservar decisões e bytes fora dessa seção. `REF-10`
3. IF o SHA atual não descender de `Valid at SHA` ou o delta descendant alterar uma superfície não documental de fechamento THEN a consulta SHALL retornar estado `stale` e razão `sha-changed`. `REF-11`
4. IF o estado upstream observado divergir de `Publication state` THEN a consulta SHALL retornar estado `stale` e razão `publication-changed`. `REF-12`
5. IF o Handoff contiver uma instrução transitória de push, PR ou publicação THEN o helper SHALL rejeitar a gravação antes de alterar o arquivo. `REF-13`
6. IF o arquivo estiver ausente, malformado, linkado ou fora da raiz permitida THEN o helper SHALL falhar sem alterar estado existente. `REF-14`

**Independent Test:** Um repositório temporário comprova escrita isolada, consulta válida,
invalidação por SHA/publicação, rejeição de ação transitória e preservação após falha.

### P2: Separar contrato validado de operação comprovada

**User Story:** Como mantenedor do workspace, quero ver separadamente o que os testes de contrato
provaram e o que um piloto real provou para não promover uma política acima de sua evidência.

**Why P2:** A validação da AD-045 passou estruturalmente, mas ainda não executou o piloto dual-engine.

**Acceptance Criteria:**

1. WHEN um relatório de validação de workflow for criado ou materialmente revisado THEN ele SHALL declarar `Contract status` e `Operational status` separadamente. `REF-15`
2. IF não existir piloto real aplicável THEN o relatório SHALL usar `Operational status: UNPROVEN` e SHALL listar a evidência operacional ausente. `REF-16`

**Independent Test:** O relatório desta feature e o contrato documental revisado falham no gate se
um único PASS tentar representar simultaneamente contrato e operação não comprovada.

## Edge Cases

- WHEN uma retrospectiva antiga entrar posteriormente na mesma janela THEN o receipt SHALL alterar o checksum e SHALL manter explícitos a janela e os outcomes de exclusão. `REF-17`
- IF o mesmo ID aparecer nos histories Codex e Claude THEN `exclusions_matched` SHALL contá-lo uma vez no total e SHALL preservar a decomposição por engine. `REF-18`
- IF o período for inválido ou o workspace lógico estiver vazio THEN o auditor SHALL falhar antes de emitir um receipt. `REF-19`
- IF a consulta do Handoff não puder resolver o upstream THEN ela SHALL retornar estado `indeterminate` sem afirmar freshness. `REF-20`

## Implicit-Requirement Dimensions

| Dimension | Resolution |
| --- | --- |
| Input validation & bounds | Janela, workspace lógico, enums de publicação e payload do Handoff falham fechados. |
| Compatibility & representation | Contrato v3 é uma quebra explícita; consumidores e fixtures locais migram juntos. |
| Failure / partial-failure states | Escritas são atômicas e falhas preservam o Handoff anterior. |
| Idempotency / retry / duplicate handling | Mesmo input produz mesmo relatório; exclusões repetidas são deduplicadas. |
| Auth boundaries & rate limits | N/A porque toda operação é local e read-only, exceto a escrita explícita do Handoff local. |
| Concurrency / ordering | Single-writer; substituição atômica impede estado parcial. |
| Data lifecycle / expiry | Receipts permanecem locais por padrão; só agregados sanitizados podem ser promovidos deliberadamente. |
| Observability | Estados e razões estruturados explicam freshness, invalidação e falhas. |
| External-dependency failure | Git upstream ausente ou inacessível produz `indeterminate`. |
| Operational enablement | CLIs raiz, documentação e gate agregado tornam o fluxo reproduzível nas duas engines. |
| State-transition integrity | Handoff só é válido para o SHA comportamental e publicação registrados; descendants limitados à evidência de fechamento permanecem válidos. |

## Requirement Traceability

| Requirement ID | Story | Provenance | Evidence | Phase | Status |
| --- | --- | --- | --- | --- | --- |
| REF-01 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-02 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-03 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-04 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-05 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-06 | Evidência retrospectiva | DECISION | Contrato aprovado; AD-027, AD-033 e AD-041 | Execute | Implemented |
| REF-07 | Evidência retrospectiva | SAFETY | Contrato aprovado; política de segurança do workspace | Execute | Implemented |
| REF-08 | Evidência retrospectiva | DECISION | Contrato aprovado; comparação cross-machine | Execute | Implemented |
| REF-09 | Freshness de Handoff | DECISION | Contrato aprovado; Handoff stale observado em `STATE.md` | Execute | Implemented |
| REF-10 | Freshness de Handoff | INHERITED | AD-023 e contrato TLC de memória | Execute | Implemented |
| REF-11 | Freshness de Handoff | SAFETY | Handoff stale observado em `STATE.md` | Execute | Implemented |
| REF-12 | Freshness de Handoff | SAFETY | Publicação divergente observada em `STATE.md` | Execute | Implemented |
| REF-13 | Freshness de Handoff | DECISION | Contrato aprovado; separação de ação transitória | Execute | Implemented |
| REF-14 | Freshness de Handoff | SAFETY | Política fail-closed do workspace | Execute | Implemented |
| REF-15 | Dois eixos de validação | INHERITED | AD-023 e validação AD-045 | Execute | Implemented |
| REF-16 | Dois eixos de validação | DECISION | Contrato aprovado; piloto ainda ausente | Execute | Implemented |
| REF-17 | Edge cases | SAFETY | Drift de cohort observado | Execute | Implemented |
| REF-18 | Edge cases | SAFETY | Deduplicação cross-engine | Execute | Implemented |
| REF-19 | Edge cases | SAFETY | Input inválido | Execute | Implemented |
| REF-20 | Edge cases | SAFETY | Falha de upstream Git | Execute | Implemented |

**Coverage:** 20 total, 20 mapped to Execute, 0 unmapped.

## Success Criteria

- [ ] Fixtures comportamentais discriminam todos os 20 requisitos.
- [ ] O gate agregado da raiz passa sem alterar os dois arquivos de lessons preexistentes.
- [ ] Uma coleta local gera receipt portátil sem cwd ou IDs de sessão.
- [ ] O Handoff final consulta como `fresh` no SHA e estado de publicação registrados.
- [ ] O relatório final declara contrato e operação em eixos separados.
