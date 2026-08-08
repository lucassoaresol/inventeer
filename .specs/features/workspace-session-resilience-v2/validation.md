# Validação de Workspace Session Resilience v2

**Verdict:** FAIL
**Data:** 2026-08-08
**Spec:** `.specs/features/workspace-session-resilience-v2/spec.md`
**Range do diff:** `152b2de9d8948320152f0f972ec07da8771edfe5..923b7861ed5e07b6f0e11d5e47199a773ae1563d`
**Verifier:** subagente independente (autor != verifier)

## Evidência de Entrega

- **Estado da validação:** `fail`
- **Vínculo da evidência:** base `152b2de9d8948320152f0f972ec07da8771edfe5`, head/work SHA `923b7861ed5e07b6f0e11d5e47199a773ae1563d`
- **Contrato de requisitos:** `.specs/features/workspace-session-resilience-v2/spec.md` no head da evidência
- **Estado dos gates:** verde. Testes focais passaram 25/25; build passou 20/20 suites; integridade do diff no range passou.
- **Condições pendentes:** corrigir WSR-09 e adicionar assertions exatas para WSR-11, WSR-14 e WSR-15; depois repetir a validação independente.
- **Paths de alto risco:** `scripts/audit-session-history.py`, `scripts/test-session-history-audit.py`, `scripts/test-session-resilience-contract.sh`

## Conclusão das Tasks

| Task | Status | Evidência |
| --- | --- | --- |
| T1 | Concluída | `c0c910c`; contrato focal de segredo passou 11/11 |
| T2 | Concluída | `cebac21`; teste focal do auditor passou 14/14 |
| T3 | Concluída | `923b786`; build gate passou 20/20 suites |

## Requisitos Ancorados na Spec

Evidence-or-zero foi aplicado aos 15 requisitos. Uma assertion parcial não aprova o requisito.

| Requisito | Outcome definido pela spec | Evidência de assertion exata | Resultado |
| --- | --- | --- | --- |
| WSR-01 | Um valor com aparência de segredo fornecido no chat não é repetido; referências necessárias usam `[REDACTED]`. | `scripts/test-session-resilience-contract.sh:21` - `grep -Fq 'não repita o valor'`; `scripts/test-session-resilience-contract.sh:23` - `grep -Fq 'use \`[REDACTED]\`'` | PASS |
| WSR-02 | O valor é proibido em comandos exibidos, logs, commits, checkpoints e artifacts versionados. | `scripts/test-session-resilience-contract.sh:31` - `grep -Fq` exato sobre as cinco superfícies | PASS |
| WSR-03 | O uso local prefere `.env` ignorado ou entrada interativa. | `scripts/test-session-resilience-contract.sh:35` - `grep -Fq '\`.env\` ignorado ou entrada interativa'` | PASS |
| WSR-04 | A orientação de rotação é condicional e não afirma que a credencial continua ativa. | `scripts/test-session-resilience-contract.sh:39` e `scripts/test-session-resilience-contract.sh:41` exigem as duas frases exatas | PASS |
| WSR-05 | Origens Codex e Claude são selecionadas no intervalo normalizado `[since, until)`. | `scripts/test-session-history-audit.py:242` e `scripts/test-session-history-audit.py:290` colocam os dois engines exatamente em `until`; `scripts/test-session-history-audit.py:328` e `scripts/test-session-history-audit.py:353` afirmam relatórios completos que os excluem | PASS |
| WSR-06 | `until` inválido e janelas não crescentes falham com código não zero e os dois diagnósticos exatos. | `scripts/test-session-history-audit.py:473`-`474` e `scripts/test-session-history-audit.py:489`-`490` afirmam código não zero e stderr exato | PASS |
| WSR-07 | O relatório emite contract version inteiro 2, limites normalizados e quantidade de exclusões. | `scripts/test-session-history-audit.py:316`-`327` afirma schema e valores top-level exatos | PASS |
| WSR-08 | Totais de interrupção são deduplicados; counts afetados, percentuais com duas casas e máximos por primary são exatos. | `scripts/test-session-history-audit.py:328`-`345` afirma o relatório Codex completo, inclusive totais `8/8`, counts `2/2`, máximos `2/2` e percentuais `66.67/66.67` | PASS |
| WSR-09 | Eventos de cópias e subagentes não afetam counts, percentuais ou máximos das primárias. | A exclusão de subagentes é exata em `scripts/test-session-history-audit.py:457`-`466`. A exclusão copy-only não tem assertion discriminante. `scripts/audit-session-history.py:187`-`208` agrega interrupções de arquivos duplicados com `max`; um probe do verifier com arquivo canônico sem eventos e cópia interrompida retornou counts e máximos iguais a 1. | FAIL |
| WSR-10 | Successes, failures, denials e unresolved APEX existentes mantêm significados separados. | Valores Codex exatos: `scripts/test-session-history-audit.py:348`-`351`. Valores Claude exatos: `scripts/test-session-history-audit.py:363`-`366`. Os quatro outcomes são afirmados separadamente. | PASS |
| WSR-11 | Roots ausentes e roots disponíveis sem matches são distinguíveis e retornam todas as métricas de interrupção em zero. | Disponibilidade é exata em `scripts/test-session-history-audit.py:400`-`405` e `scripts/test-session-history-audit.py:428`-`431`. Somente `max_aborts_per_session` e `sessions_with_aborts_percent` são afirmados como zero; os demais totais, counts, máximos e percentual não têm assertion exata. | GAP |
| WSR-12 | JSON e texto omitem conteúdo, IDs, paths de history/workspace e valores sentinela semelhantes a credenciais. | `scripts/test-session-history-audit.py:312`-`313` e `scripts/test-session-history-audit.py:379`-`381` rejeitam o sentinela, IDs representativos, workspace path exato e scratch history path nos dois formatos | PASS |
| WSR-13 | AD-041 registra compatibilidade, privacidade, cohort fechado e piloto limitado. | `scripts/test-session-resilience-contract.sh:45`-`55` seleciona AD-041 e exige cada frase da decisão | PASS |
| WSR-14 | O piloto ativo contém somente metadados de contrato, agregados sanitizados, regras de elegibilidade, medidas de sucesso e thresholds explícitos. | `scripts/test-session-resilience-contract.sh:63`-`80` afirma metadados e agregados; `scripts/test-session-resilience-contract.sh:94`-`97` rejeita padrões de UUID/history path. Nenhuma assertion exige regras de elegibilidade ou medidas de sucesso presentes em `.specs/features/workspace-session-resilience-v2/pilot.md:52` e `.specs/features/workspace-session-resilience-v2/pilot.md:66`. | GAP |
| WSR-15 | Após dez primárias elegíveis ou a próxima feature longa, uma comparação final é obrigatória antes de propor runner. | `scripts/test-session-resilience-contract.sh:82`-`92` afirma o gatilho e os thresholds. Nenhuma assertion exige os passos de comparação ou o limite pré-automação em `.specs/features/workspace-session-resilience-v2/pilot.md:90`-`100`. | GAP |

**Estado spec-anchored:** 11/15 requisitos passam; 1 falha comportamental; 3 gaps de evidência; 0 gaps de precisão da spec.

## Compatibilidade APEX

Os quatro outcomes permanecem requisitos explícitos com assertions exatas:

| Outcome | Assertion Codex | Assertion Claude | Resultado |
| --- | --- | --- | --- |
| `apex_tool_successes` | `scripts/test-session-history-audit.py:348` | `scripts/test-session-history-audit.py:363` | PASS |
| `apex_tool_failures` | `scripts/test-session-history-audit.py:349` | `scripts/test-session-history-audit.py:364` | PASS |
| `apex_tool_denials` | `scripts/test-session-history-audit.py:350` | `scripts/test-session-history-audit.py:365` | PASS |
| `apex_tool_unresolved` | `scripts/test-session-history-audit.py:351` | `scripts/test-session-history-audit.py:366` | PASS |

## Edge Cases

| Edge case | Evidência de assertion exata | Resultado |
| --- | --- | --- |
| Origem igual a `until` é excluída. | Fixtures de limite em `scripts/test-session-history-audit.py:242` e `scripts/test-session-history-audit.py:290`; relatórios exatos em `scripts/test-session-history-audit.py:328` e `scripts/test-session-history-audit.py:353` | PASS |
| Timestamp malformado é ignorado sem vazar conteúdo. | Fixture malformada em `scripts/test-session-history-audit.py:245`-`250`; exclusão do sentinela em `scripts/test-session-history-audit.py:312`-`313`; relatório exato em `scripts/test-session-history-audit.py:328` | PASS |
| ID primário duplicado conta concentração de interrupção e APEX uma vez. | Fixture Codex duplicada em `scripts/test-session-history-audit.py:192`-`200`, fixture Claude duplicada em `scripts/test-session-history-audit.py:281`-`286` e counts exatos em `scripts/test-session-history-audit.py:328`-`366` | PASS |
| Nenhuma primária Codex correspondente produz counts, percentuais e máximos afetados iguais a zero. | `scripts/test-session-history-audit.py:457`-`466` afirma cada métrica affected-primary como zero | PASS |
| Omissão de `until` preserva o comportamento não limitado após `since`. | `scripts/test-session-history-audit.py:492`-`499` afirma `until is None` e inclusão do arquivo Codex adicional | PASS |

## Gate Check

- **Comandos focais:** `python3 scripts/test-session-history-audit.py`; `bash scripts/test-session-resilience-contract.sh`
- **Resultado focal:** 14/14 testes do auditor e 11/11 testes de contrato passaram; 0 falhas; 0 skips.
- **Comando de build:** `bash scripts/test-workspace.sh`
- **Resultado do build:** 20/20 suites passaram; 0 falhas; 0 skips.
- **Comando de integridade:** `git diff --check 152b2de9d8948320152f0f972ec07da8771edfe5..923b7861ed5e07b6f0e11d5e47199a773ae1563d`
- **Resultado de integridade:** limpo.
- **Gate estrutural da TLC:** `validate_state.py workspace-session-resilience-v2` saiu 1 e recusou corretamente o veredito FAIL; a feature não está concluída.
- **Testes focais antes da feature:** 9 testes do auditor; contrato de session resilience ausente.
- **Testes focais depois da feature:** 25 testes.
- **Delta:** +16 testes. As statements `assert` do auditor aumentaram de 15 para 45.
- **Integridade dos testes:** assertions removidas do sentinela foram fortalecidas em loops com múltiplos valores. Duas assertions antigas `files == 0` foram substituídas pelas de disponibilidade; isso não enfraquece um outcome preciso de interrupção v2, mas WSR-11 ainda carece das assertions completas de métricas zero descritas acima.

## Discrimination Sensor

Todas as mutações rodaram somente em uma cópia `mktemp` sob `/tmp`; o scratch foi removido. Nenhum stash foi usado.

| Mutação | Alvo | Falha comportamental | Resultado |
| --- | --- | --- | --- |
| 1 | `scripts/audit-session-history.py:169` | Alterou o limite Codex de `timestamp >= until` para `timestamp > until` | KILLED: `scripts/test-session-history-audit.py:328` falhou |
| 2 | `scripts/audit-session-history.py:210` | Incluiu subagentes na população de concentração primária | KILLED: `scripts/test-session-history-audit.py:328` falhou |
| 3 | `AGENTS.md:160` | Substituiu o marcador canônico `[REDACTED]` por `[MASKED]` | KILLED: `scripts/test-session-resilience-contract.sh:23` falhou |

**Profundidade:** lightweight, 3 mutações comportamentais.
**Resultado:** 3/3 mortas.
**Isolamento:** `git status --porcelain` da árvore real estava vazio antes; permaneceu vazio após o cleanup; a igualdade exata passou.

## Qualidade de Código

| Princípio | Status | Evidência |
| --- | --- | --- |
| Código mínimo; sem abstrações alheias | PASS | Nove arquivos alterados correspondem ao escopo T1-T3; `git diff --name-status` não contém repo de produto nem workflow alheio. |
| Mudanças cirúrgicas; estilo existente | PASS | O range contém os três commits atômicos planejados e o commit da spec aprovada. |
| Sem scope creep | PASS | Todos os paths alterados são nomeados pelas tasks ou são artifacts aprovados de spec/tasks. |
| Quantidade de testes não caiu | PASS | Testes focais passaram de 9 para 25; assertions do auditor passaram de 15 para 45. |
| Outcome check ancorado na spec | FAIL | O comportamento WSR-09 falha; WSR-11, WSR-14 e WSR-15 não têm assertions exatas completas. |
| Expectativa de cobertura por camada | FAIL | A exclusão de cópias no auditor e os contratos de lifecycle documental estão incompletos. |
| Todo teste em escopo está reivindicado | PASS | Assertions do auditor e shell mapeiam a requisito, edge case ou done-when de task. |
| Diretrizes de qualidade do workspace | PASS | O build gate exigido por `AGENTS.md:153` passou; a validação seguiu evidence-or-zero e sensor descartável da TLC vendorizada. |

UAT interativo não se aplica a este auditor read-only de metadados e contrato de instruções do repositório.

## Gaps Ranqueados e Planos de Correção

1. **Major: vazamento copy-only em WSR-09.** `scripts/audit-session-history.py:187`-`208` agrega interrupções de arquivos duplicados com `max`; uma cópia derivada pode tornar uma primária afetada e elevar seus máximos. Preserve uma observação primária canônica determinística para concentração, exclua eventos de arquivos duplicados dessas métricas e adicione fixture em que somente a cópia tem aborts/compactions.
2. **Major: contrato incompleto de métricas zero em WSR-11.** Estenda `scripts/test-session-history-audit.py` para afirmar todos os totais, counts afetados, percentuais e máximos como zero para roots ausentes e roots disponíveis sem matches.
3. **Major: eligibility e success measures de WSR-14 não são enforced.** Estenda `scripts/test-session-resilience-contract.sh` com assertions exatas para cada limite de elegibilidade e medida de sucesso, mantendo a rejeição de UUID/history path.
4. **Major: closing comparison de WSR-15 não é enforced.** Afirme os passos da comparação final e a regra de que nenhum runner é proposto ou implementado antes da comparação e do outcome no decision log.

## Resumo

**Overall:** FAIL. Os gates estão verdes e os três mutantes foram mortos, mas a implementação viola WSR-09 para interrupções copy-only. Outros três requisitos não têm assertions evidence-or-zero completas. Os status dos requisitos permanecem inalterados porque esta validação não modifica spec, tasks, STATE ou implementação.
