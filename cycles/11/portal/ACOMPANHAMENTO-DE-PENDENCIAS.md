# Acompanhamento de Pendências do Portal no Ciclo 11

- **Responsável pelo recorte:** Lucas Oliveira
- **Ciclo:** 11
- **Aberto em:** 2026-08-26
- **Última revalidação:** 2026-08-28
- **Natureza:** acompanhamento histórico; não é backlog nem autorização de execução

## Relação com as outras etapas

A [entrada do Ciclo 11](./PENDENCIAS-DE-ENTRADA.md) permanece como snapshot da virada do ciclo. Este
documento acumula evidências produzidas depois dela. No fechamento, somente a disposição final e os
itens ainda materiais devem ser destilados em `PENDENCIAS-DO-FECHAMENTO.md`.

Linear continua canônico para owner, prioridade, ciclo e execução. Uma recomendação de absorver um
ajuste em uma task existente só vale quando o fence dessa task o autoriza explicitamente.

## Revalidação de 2026-08-26

Uma revisão independente no Claude Code confrontou as pendências com os repos atualizados e executou
os dois testes focais cuja disposição exigia reprodução antes de criar issue. Esta documentação
preserva resultados e limites, não o transcript da sessão.

| Item | Evidência nova | Situação após a revalidação | Próxima disposição |
| --- | --- | --- | --- |
| `FU-01` — flake de Organization Home | `organization-home.test.tsx`: 4/4 testes passaram isoladamente em Node 22, em 2,5 s | Não reproduzido nessa passada; um sucesso isolado não refuta o histórico intermitente sob carga | Manter em observação, sem issue agora; reabrir somente com reprodução sob condição comparável |
| `C11-01` — keepalive da API | `ai-engine-keepalive.spec.ts`: 5/5 testes passaram isoladamente em Node 22, em 2,9 s; LocalStack foi detectado | A falha focal de 2026-08-19 não reproduziu; isso não equivale a um novo gate completo do repo | Retirar a recomendação imediata de issue; voltar a investigar se o gate completo falhar, registrando ambiente |
| `FU-02` — catálogo manual de permissões Web | O contrato gerado possui quatro códigos ausentes da união e do catálogo locais: `ticket.manage`, `ticket_triage.view`, `ticket_triage.manage` e `ticket_interaction.manage` | O gap é maior do que o snapshot inicial descrevia e continua aberto | Incluir em `INV-3915` somente se o fence contratar sincronização do catálogo; caso contrário, criar task focal de contrato |
| `FU-03` — `portal-web/CLAUDE.md` obsoleto | Além dos achados anteriores, referencia `PROJECT_CONTEXT.md`, `code-style-guide.md` e um plano SPECKIT inexistentes; mais de cem arquivos não-teste contêm chamadas de `useQuery` ou `useMutation` | Confirmado e ampliado; instruções incorretas afetam qualquer agente no repo | Correção documental própria ou incremento de enablement explicitamente contratado antes da primeira task Web ampla |
| `FU-04` — paginação sem i18n | O componente é consumido por sete superfícies de produto — Audit Log, Products, Associated Projects, Projects, System Admin, Tickets Home e User Roles — além do Storybook | Aberto; o alcance de sete telas foi confirmado | Issue focal pequena; não absorver por proximidade em Metrics |

## Parecer sobre absorção em tasks existentes

### `FU-02`

A mudança mecânica estimada é pequena, mas tamanho não define pertencimento. A `INV-3915` retoma o
intake e pode legitimamente exigir `ticket.manage`; os três códigos de ciclo de vida pertencem a
outras superfícies. O ajuste dos quatro códigos pode entrar na mesma task somente se seu contrato
incluir explicitamente a reconciliação do catálogo Web com o contrato gerado. Sem isso, seria
expansão silenciosa de escopo.

### `FU-03`

Corrigir instruções de agente antes da frente Web é desejável, mas anexar a mudança ao primeiro
commit de `INV-3970` ou `INV-3967` sem aceite não cria vínculo funcional. A opção segura é uma task
documental curta ou um incremento de enablement explicitamente aceito na task escolhida. O commit
deve permanecer separado da mudança funcional em qualquer caso.

## Itens que continuam exigindo owner, issue ou decisão

- `C11-02`: promover Metrics v1 ainda exige ambiente, grants, mapping e smoke autorizado; merge
  não comprova rollout.
- `C11-03`: `Portal_ERD` é artifact aprovado e sua atualização ou reclassificação depende de
  governança de produto.
- `FU-05`: os grants reais de Ticket continuam operacionais e exigem pessoas e organizações
  nomeadas antes de staging/UAT.
- Infraestrutura E2E do ADR-015: restaurar ou abandonar o caminho descrito é decisão arquitetural,
  não correção documental mecânica.
- As diferenças do frame T-03 permanecem encerradas como decisão de escopo da v1 até nova decisão de
  produto.

## Limite desta atualização

Nenhum código, teste, artifact de produto, issue Linear ou repo sob `repos/` foi alterado. Os dois
resultados focais foram produzidos pela revisão independente e não foram reexecutados durante esta
atualização documental.

## Revalidação após a entrega da INV-3970

O Linear e o GitHub foram revalidados em 2026-08-26 depois da entrega da INV-3970 e da triagem dos
achados do seu QA. A INV-3970 está `Done`, e a PR
[portal-web#239](https://github.com/Inventeer/portal-web/pull/239) foi incorporada a `develop`. A
entrega fixou quatro páginas de Metrics: Activity, Delivery Flow, Quality e Velocity. A INV-3967 é
a única task restante da MILE INV-3963 e preserva o escopo residual de posicionamento dos cards e
regressão visual e comportamental.

O recorte atual atribuído a Lucas Oliveira passou a onze tasks e continua somando 20 pontos. A
mudança combina o esforço final de um ponto registrado na INV-3970 com a entrada da INV-4041, também
de um ponto. O snapshot de entrada acima permanece inalterado porque registra a composição e as
estimativas observadas na abertura do ciclo.

### Disposição dos achados do QA

| Pendência ou achado | Disposição canônica em 2026-08-26 | Relação com o Ciclo 11 |
| --- | --- | --- |
| `FU-03` — `portal-web/CLAUDE.md` obsoleto | `INV-4041`, task própria de enablement sob o catch-all INV-629 | `Prioritized` no Ciclo 11; não pertence ao roadmap do Portal |
| `FU-02` — catálogo Web divergente do contrato de permissões | `INV-4036`, sob a frente de fechamento das divergências do QA | Backlog, fora do ciclo; não será absorvida silenciosamente pela INV-3915 |
| `FU-04` — locale incompleto na paginação | `INV-4037`, junto da divergência de locale do Audit Log | Backlog, fora do ciclo |
| `C11-03` — ERD divergente do schema vivo | `INV-4039`, com decisão entre atualização e reclassificação do artifact | Backlog, fora do ciclo |
| Caminho E2E descrito pelo ADR-015 | `INV-4040`, com decisão explícita sobre restaurar ou abandonar o caminho | Backlog, fora do ciclo |
| Reidratação da navegação permissionada | `INV-4035`, separada da entrega funcional que revelou a divergência | Backlog, fora do ciclo |
| Negação integral de acesso a Metrics | `INV-4038`, distinta da negação regional do segundo tier tratada pela INV-3971 | Backlog, fora do ciclo |

A estrutura INV-4031–INV-4040 permanece fora do Ciclo 11. A documentação correspondente está na PR
[inventeer-ops#262](https://github.com/Inventeer/inventeer-ops/pull/262), ainda não incorporada a
`main` neste snapshot. Linear continua canônico para a hierarquia e o estado dessas issues.

### Itens deliberadamente sem task

- A promoção operacional de Metrics v1 continua sem issue até existir owner, ambiente e smoke
  autorizados.
- Os grants reais de Ticket continuam sem issue até existirem owner, organizações, atores e ambiente
  explícitos.
- `reportAllChanges` lendo `startTime` indefinido e os históricos de flake de
  `organization-home.test.tsx` e `ai-engine-keepalive.spec.ts` continuam sem task. Os dois testes não
  reproduziram a falha na última passada focal, e um caso isolado sem reprodução não cria backlog.

## Limite da revalidação pós-INV-3970

Esta seção registra a disposição durável dos achados. Ela não altera ciclo, estado, prioridade,
owner ou relações no Linear; não promove os artifacts da PR #262 antes do merge; e não transforma
observações sem reprodução ou owner em backlog implícito.

## Revalidação após a entrega da INV-3967 para QA

O Linear, o GitHub e os clones locais foram revalidados em 2026-08-27 depois da entrega da
INV-3967. A PR [portal-web#240](https://github.com/Inventeer/portal-web/pull/240) foi incorporada a
`develop@01bb8d4755f5c579f03bde8cf0d200b1ea37a9a2`, e a superfície foi publicada em desenvolvimento
para QA. A issue permanece `QA`, com Human Final Effort pendente. Merge e publicação em
desenvolvimento não equivalem a `Done` nem fecham a MILE INV-3963.

O [snapshot da INV-3967](./tasks/INV-3967.md) preserva a clarificação completa. A auditoria confirmou
que os dez cards da v1 já estavam nas páginas corretas. A entrega prendeu esse mapeamento em
regressão e acrescentou os filtros por grupo de Activity e Delivery Flow, sem alterar contratos da
API, chaves do Collector ou definições de métricas.

### Efeito sobre a frente de Metrics v2

| Item | Situação em 2026-08-27 | Disposição |
| --- | --- | --- |
| INV-3967 | Entrega incorporada e em `QA` | Concluir QA e registrar Human Final Effort antes de `Done` |
| INV-3963 | Continua `In Progress` | Fechar somente depois da conclusão canônica da INV-3967 |
| INV-3964, INV-3965 e INV-3966 | Continuam carregando o blocker herdado da INV-3963 | Revalidar Linear após o fechamento da INV-3963 antes de iniciar as sucessoras |

### Limites confirmados pela entrega

- A barra ampla de filtros do frame continua sem issue canônica. O rascunho local não cria backlog
  e não deve ser promovido antes das decisões de produto e contrato.
- Seletores de segmentação permanecem na INV-3969; o segundo tier de permissão, na INV-3971.
- A negação integral do grant geral e a reidratação da navegação permanecem, respectivamente, nas
  INV-4038 e INV-4035.
- Observações operacionais da sessão, estado TLC, instruções de branch, briefing de QA e identidade
  do connector não fazem parte deste registro versionado.

## Limite da revalidação pós-INV-3967

Esta atualização preserva a entrega e seus limites sem alterar Linear, GitHub, código de produto ou
artifacts canônicos. Ela não declara aprovação do QA, esforço final, fechamento da MILE, staging,
rollout ou produção.

## Revalidação após a conclusão da INV-3967

O Linear e os clones locais foram revalidados em 2026-08-28. A INV-3967 está `Done`, com Human
Final Effort de um ponto, e a MILE INV-3963 também está `Done`. Com a conclusão da MILE, foram
satisfeitos os blockers formais das sucessoras INV-3964, INV-3965 e INV-3966. As relações históricas
continuam visíveis no Linear, que deve ser revalidado antes do início de qualquer sucessora.

O recorte atual do Ciclo 11 contém onze tasks e soma 19 pontos. Duas tasks, INV-3970 e INV-3967,
estão concluídas e representam dois pontos; restam nove tasks e 17 pontos. A INV-4041 permanece
`Prioritized`, mas foi reclassificada da referência catch-all observada anteriormente para o projeto
Portal Engineering Operations, sob a MILE INV-4057.

O [snapshot da INV-3967](./tasks/INV-3967.md) continua preservando a clarificação observada quando a
task estava em QA e não é reescrito retroativamente. A conclusão canônica da issue e a incorporação
da entrega não comprovam, por si sós, staging, rollout ou produção.

## Limite da revalidação de 2026-08-28

Esta seção registra apenas fatos duráveis revalidados. Ela não altera Linear, GitHub, código ou
artifacts de produto e não promove estado TLC, logs, instruções de branch, briefing de QA,
identidade do connector, rascunhos, credenciais, dados de clientes ou saídas de produção.

## Revalidação após a conclusão da INV-4041

O Linear e o GitHub foram revalidados em 2026-08-28 depois da entrega da INV-4041. A task está
`Done`, com Human Final Effort de um ponto, e sua MILE INV-4057 também está `Done`. As PRs
[portal-web#243](https://github.com/Inventeer/portal-web/pull/243) e
[portal-api#302](https://github.com/Inventeer/portal-api/pull/302) foram incorporadas a `develop`.
Juntas, elas reconciliaram o contexto operacional diretamente consumido nos dois repositórios sem
introduzir mudança de runtime, produto ou contrato.

O [snapshot da INV-4041](./tasks/INV-4041.md) preserva a clarificação que consolidou a entrega em
dois PRs independentes e suas exclusões. A correção de cobertura do Checkbox entregue na PR
[portal-web#242](https://github.com/Inventeer/portal-web/pull/242) permaneceu separada e não integra o
escopo nem o esforço da INV-4041.

O recorte atual do Ciclo 11 contém onze tasks e soma 19 pontos. INV-3970, INV-3967 e INV-4041 estão
concluídas e representam três pontos; restam oito tasks e 16 pontos. Entre as sucessoras, a INV-3973
é a próxima candidata de execução: seu blocker formal INV-3970 está concluído, e sua entrega das três
Gold keys desbloqueia a INV-3968. A recomendação exige nova preparação individual antes do início e
não altera prioridade ou estado no Linear.

## Limite da revalidação pós-INV-4041

Esta atualização registra somente a disposição durável da entrega. Ela não altera Linear, GitHub,
repositórios de produto ou artifacts canônicos; não promove logs, handoff, estado TLC, instruções de
branch, credenciais, dados de clientes ou saídas de produção; e não cria snapshot da INV-3973 antes
de sua preparação e eventual clarificação durável.
