# Entrada de Pendências do Portal no Ciclo 11

- **Responsável pelo recorte:** Lucas Oliveira
- **Ciclo:** 11
- **Snapshot:** 2026-08-26
- **Etapa:** entrada do ciclo
- **Natureza:** histórico de revalidação; não é backlog nem autorização de execução

## Fontes e frescor

Os clones foram atualizados antes desta leitura. O snapshot usa:

- `portal-web` `develop@598d8129a1e414b35a773200b1dd9cf9feed09ed`;
- `portal-api` `develop@1fde03a7eb2230a9e70acf0e54d124f166d11edc`;
- `inventeer-ops` `main@bcae1fb7a7ef54d0a87af9f17d93292496e43a67`;
- PR documental [inventeer-ops#256](https://github.com/Inventeer/inventeer-ops/pull/256), aberta
  em `d4167dfcf961245610f48108d72e7ca1426e5b69` e ainda não incorporada a `main`;
- Linear consultado em 2026-08-26 para issues do Ciclo 11 atribuídas a Lucas Oliveira.

Nenhum teste foi executado nesta revalidação. Estados de teste abaixo vêm da última evidência
registrada e são distinguidos de inspeção atual de arquivo e histórico Git.

## Recorte de entrada do Ciclo 11

| Frente | Tasks no ciclo | Pontos |
| --- | --- | ---: |
| Metrics v2 | `INV-3971`, `INV-3972`, `INV-3969`, `INV-3974`, `INV-3968`, `INV-3973`, `INV-3967`, `INV-3970` | 16 |
| Tickets | `INV-3942`, `INV-3915` | 4 |
| **Total** | **10 tasks** | **20** |

`INV-3975` e `INV-3976` pertencem ao projeto Metrics v2 e estão atribuídas a Lucas, mas não estavam
no Ciclo 11 neste snapshot; por isso não entram na soma. Issues-pai com zero pontos também foram
excluídas. Linear permanece canônico caso a composição mude.

## Pendências herdadas do fechamento do Ciclo 10

| ID | Situação na entrada do Ciclo 11 | Relação com o ciclo | Disposição inicial |
| --- | --- | --- | --- |
| `FU-01` — flake de `organization-home.test.tsx` | Sem commit corretivo desde o fechamento; a última evidência é intermitente sob carga, não uma falha reexecutada agora | Pode contaminar gates completos do Portal Web usados por Metrics v2 e Tickets | Reproduzir de forma focal antes de criar task; se persistir, registrar issue própria |
| `FU-02` — `ticket.manage` ausente do catálogo manual Web | Confirmado: o contrato gerado publica `ticket.view` e `ticket.manage`, mas a união e o catálogo locais mantêm apenas `ticket.view` | `INV-3915` retoma o intake, cuja autorização canônica usa `ticket.manage` | Resolver dentro da task somente se o fence exigir o código; caso contrário, criar dívida explícita de contrato |
| `FU-03` — `portal-web/CLAUDE.md` obsoleto | Confirmado: ainda nega o lint, aponta `src/bootstrap/session.ts` inexistente, reduz TanStack Query à sessão e fixa autor incorreto | Afeta diretamente agentes que iniciarão a ampla frente Metrics v2 | Priorizar correção documental própria antes do primeiro trabalho Web amplo |
| `FU-04` — `Pagination` sem i18n | Confirmado: textos visíveis, `aria-label` e nome do `nav` continuam em inglês no JSX | Não bloqueia as dez tasks; qualquer nova superfície paginada amplia o alcance | Criar issue focal quando priorizado; não absorver por proximidade em Metrics |
| `FU-05` — grants reais de Ticket | Não há evidência canônica de provisioning e smoke após o fechamento; a condição não pode ser resolvida por inspeção de repo | Bloqueia staging/UAT real do ciclo de vida já entregue e deve preceder alegações ponta a ponta nas tasks de Tickets | Vincular a uma ação operacional nomeada antes do primeiro staging/UAT |
| `FU-06` — frame T-03 versus Tickets Home | Continua encerrado como decisão de escopo da v1; `Reason` e `Your task` não foram contratados e `Reopened` aparece na coluna de status | Não é pendência automática do Ciclo 11 | Não carregar como dívida; nova issue somente após decisão de produto |

O [snapshot de fechamento do Ciclo 10](../../10/portal/PENDENCIAS-DO-FECHAMENTO.md) preserva o
contexto completo de origem. Esta tabela registra apenas a revalidação na virada do ciclo.

## Candidatas técnicas herdadas

| Candidata | Estado atual | Tratamento no Ciclo 11 |
| --- | --- | --- |
| Sincronização automática de permissões API/Web | Aberta; `FU-02` é ocorrência concreta | Avaliar como contrato compartilhado, não como correção isolada de Metrics |
| Fidelidade da integração de rotas | Parcialmente mitigada pela asserção da árvore real adicionada em Tickets; parte do harness continua representativa | Observar durante a migração do shell v2; criar trabalho somente se houver lacuna verificável |
| Predicado de acesso a Metrics duplicado no Web | Ainda existe entre menu e guard | `INV-3970` pode revelar um terceiro consumidor; consolidar somente se o fence da task justificar |
| Infraestrutura E2E do ADR-015 | Continua sem scripts e dependências executáveis no `package.json`, apesar das specs existentes | Registrar decisão própria antes de alegar gate E2E para as telas v2 |
| Consulta direta da organização prestadora em `TicketConfirmationService` | Continua fora do repositório do módulo, sem mudança desde `INV-3828` | Baixo risco; corrigir quando uma task de Tickets tocar a mesma fronteira, sem ampliar escopo silenciosamente |

## Novos pontos acrescentados na entrada

### `C11-01` — gate completo do Portal API não estava integralmente verde

A validação terminal da `INV-3834`, em 2026-08-19, registrou falha reproduzível em isolamento no
teste `ai-engine-keepalive.spec.ts`, fora do diff de Metrics. O arquivo e sua integração não receberam
commit posterior no `develop` atual. Esta revalidação não executou o teste, portanto o estado correto
é: **última evidência vermelha, correção não observada**, e não “falha novamente comprovada hoje”.

Não foi encontrada issue Linear equivalente pela busca focal. Antes do primeiro gate completo de
Portal API no Ciclo 11, reexecutar o caso; se falhar, criar issue própria no domínio Chat. Não
incorporar a correção numa task Metrics.

### `C11-02` — promoção operacional de Metrics v1 segue sem issue

`METRICS-24` exige configuração de ambiente, mapping organização → Collector, grant autorizado e
smokes de sucesso, falta de permissão, organização sem mapping, timeout, 502 e resposta stale sem
falsos zeros. Esse trabalho ficou fora do código da `INV-3875` e não foi encontrado como task própria
no Linear. As PRs de Metrics v1 estão merged, mas isso não prova promoção, staging ou rollout.

O Ciclo 11 já inicia Metrics v2. Antes de usar a v1 como baseline operacional, criar ou vincular uma
ação com owner e ambiente explícitos. Ela não deve ficar escondida em `INV-3970` ou `INV-3967`, que
tratam do shell e da migração de cards.

### `C11-03` — `Portal_ERD` não representa mais o schema vivo

O artifact aprovado ainda declara geração em 2026-04-27, quatorze migrations e um inventário baseado
em doze entidades. O `portal-api` atual possui 69 migrations e schemas próprios para Notifications,
mapping de Metrics e o domínio Ticket, incluindo intake, anexos e timeline. O README do Portal ainda
descreve o ERD como derivado do schema vivo, tornando a divergência uma afirmação documental atual,
não apenas uma baseline histórica.

Esse gap merece task documental de produto com decisão entre duas saídas: atualizar o ERD contra o
schema atual ou renomear/reclassificar o artifact como baseline histórica. Não corrigir por partes
durante uma task funcional.

## Observações novas que ainda não justificam backlog

- O bloco de autenticação e autorização `401/403` permanece duplicado entre as duas rotas Metrics da
  API. A v2 pode aumentar a repetição; consolidar quando houver terceiro uso ou alteração conjunta.
- A propagação de `stale` possui cobertura em Collector, domínio, serviço e Web, mas não há uma
  asserção de rota HTTP ponta a ponta com `stale: true`. Tratar como gap de cobertura somente se o
  fence de uma task v2 modificar esse contrato.
- O campo morto `approximate?: true` citado na validação da `INV-3834` não aparece mais no estado
  atual e, portanto, não foi carregado como pendência.

## Etapa esperada no fechamento do Ciclo 11

O fechamento deve criar `cycles/11/portal/PENDENCIAS-DO-FECHAMENTO.md` e, para cada ID acima:

1. registrar se virou issue Linear, foi resolvido, foi descartado por decisão ou permanece candidato;
2. adicionar novos achados duráveis descobertos nas tasks do ciclo;
3. separar entrega merged de provisioning, staging, rollout e validação real;
4. carregar somente os itens ainda materiais para a entrada do Ciclo 12;
5. preservar este documento como snapshot de entrada, sem reescrevê-lo com o estado final.
