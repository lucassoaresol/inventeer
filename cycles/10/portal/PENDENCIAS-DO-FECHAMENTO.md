# Pendências e Decisões de Escopo do Portal no Fechamento do Ciclo 10

- **Responsável pelo recorte:** Lucas Oliveira
- **Snapshot:** 2026-08-26
- **Origem:** achados incidentais durante as tasks do Ciclo 10
- **Natureza:** registro histórico; não é backlog nem estado operacional

## Como usar este registro

Os itens abaixo foram reclassificados contra a realidade do fechamento. Um achado aberto só se torna
trabalho comprometido quando possui issue no Linear, que permanece canônico para owner, ciclo,
prioridade e execução. Este documento evita perder o aprendizado sem transformar lembretes de sessão
em backlog paralelo.

Este snapshot não será atualizado com o andamento posterior. A revalidação e a disposição inicial
dos itens herdados estão na
[entrada de pendências do Portal no Ciclo 11](../../11/portal/PENDENCIAS-DE-ENTRADA.md).

## Situação dos achados no fechamento

| ID local | Achado | Situação em 2026-08-26 | Encaminhamento correto |
| --- | --- | --- | --- |
| `FU-01` | Flake de timing em `organization-home.test.tsx` sob carga | Aberto; não fazia parte do diff da `INV-3830` e não havia issue vinculada no snapshot | Criar task focal se continuar reproduzível; estabilizar a espera do estado, sem apenas aumentar timeout |
| `FU-02` | `portal.client.ticket.manage` ausente do catálogo manual do Portal Web | Aberto; a API e o contrato gerado publicam o código, mas a união e o catálogo locais preservam apenas `ticket.view` | Tratar como dívida de sincronização de contrato; não anexar a Metrics nem confundir com `ticket_interaction.manage` |
| `FU-03` | `portal-web/CLAUDE.md` descreve arquitetura e gates obsoletos | Aberto e de alto impacto para agentes; ainda negava o lint, apontava arquivo inexistente e fixava autor incorreto | Task documental própria ou enablement explícito do repo antes de novo trabalho amplo no Web |
| `FU-04` | `Pagination` mantém textos e nomes acessíveis em inglês | Aberto; afeta as superfícies que reutilizam o componente em idiomas diferentes de inglês | Corrigir i18n do componente compartilhado em PR focal, incluindo texto visível e `aria-label` |
| `FU-05` | Grants de requester e triagem ausentes para staging/UAT real de Tickets | Pré-requisito operacional não concluído; o UAT da `INV-3831` foi feito com MSW | Provisionar grants nomeados antes de staging/UAT e então executar a integração real; não tratar como escopo de frontend |
| `FU-06` | Tickets Home difere do frame T-03 em `Reason`, `Your task` e apresentação de `Reopened` | Fechado como decisão de escopo da v1, com lacuna de produto possível | Abrir nova issue somente se produto quiser recuperar o frame completo; não reclassificar a `INV-3830` como entrega incompleta |

## Detalhamento das conclusões

### `FU-01` — flake de Organization Home

O timeout apareceu de forma intermitente em três sessões sob pressão de recursos e não reproduziu na
execução final com o host folgado. Isso não prova regressão da `INV-3830`, que não alterou a tela.
Também não autoriza ignorar a falha: se ela continuar reproduzível, deve ganhar uma task focal para
que gates completos não passem a depender de reexecuções por hábito.

### `FU-02` — divergência no catálogo de permissões

No fechamento, `src/generated/portal-api.d.ts` publicava `portal.client.ticket.view` e
`portal.client.ticket.manage`, enquanto `src/types/api-contracts.ts` mantinha apenas `ticket.view` no
catálogo manual. A `INV-3831` não resolveu nem precisava usar `ticket.manage`: os comandos do
solicitante são autorizados por `portal.client.ticket_interaction.manage`, e `ticket.manage`
permanece o grant do intake. Portanto, o item continuou aberto como sincronização de contrato, sem
bloquear o overlay entregue.

### `FU-03` — instruções obsoletas do Portal Web

O arquivo ainda afirmava que não existia script de lint, embora `npm run lint` estivesse publicado;
apontava `src/bootstrap/session.ts`, que não existia; descrevia TanStack Query como uso isolado da
sessão, apesar de seu uso disseminado; e fixava José Corte como autor humano em um repo operado por
Lucas Oliveira. A regra de não adicionar atribuição de IA permanecia válida. O fechamento não
corrigiu o arquivo porque isso exigia uma mudança documental própria no repo de produto.

### `FU-04` — paginação sem i18n

O componente compartilhado ainda continha `Previous`, `Next`, `Previous page`, `Next page` e
`Pagination` diretamente no JSX. A pendência inclui acessibilidade: traduzir apenas o texto visível
deixaria os nomes anunciados por leitores de tela em inglês.

### `FU-05` — promoção operacional de Tickets

A fundação publicou grants separados por lado da relação:

- organização solicitante: `portal.client.ticket.view` e
  `portal.client.ticket_interaction.manage`;
- organização prestadora: `portal.client.ticket_triage.view` e
  `portal.client.ticket_triage.manage`.

Sem o primeiro par, o requester não consegue exercer leitura e comandos reais; sem o segundo, o
lado Labs não consegue percorrer os estados necessários ao UAT. A validação da `INV-3831` registrou
essa condição como provisioning pendente. Por isso, o ciclo fechou a implementação merged, não o
rollout ou o smoke de staging.

### `FU-06` — frame T-03 versus contrato entregue

A divergência precisa ser lida por parte:

- `Reason` não fazia parte dos seis campos de linha aprovados e não existia no contrato de listagem;
- `Your task` tinha fonte em `task_ref`, mas também ficou fora dos seis campos aprovados;
- `Reopened` foi entregue como status canônico e aparece no chip da coluna de status, não como um
  segundo chip ao lado do assunto conforme o frame.

Assim, a `INV-3830` cumpriu o contrato vigente e declarou `Reason` e `Your task` fora de escopo. Uma
retomada fiel ao frame exigiria decisão de produto e, para `Reason`, evolução do read model da API.

## Outras candidatas técnicas observadas no planejamento

Estas candidatas também permaneciam sem compromisso no Linear no fechamento:

| Candidata | Leitura no fechamento |
| --- | --- |
| Sincronização automática de permissões API/Web | Aberta; `FU-02` é uma ocorrência concreta do problema mais amplo |
| Fidelidade da integração de rotas | Parcialmente mitigada: Tickets acrescentou uma asserção sobre a árvore real, mas parte do teste continuava usando uma árvore representativa |
| Predicado de acesso a Metrics duplicado entre menu e guard | Aberta, de baixo risco; não justificar issue isolada até haver nova repetição ou divergência |
| Suíte E2E descrita pelo ADR-015 sem infraestrutura executável no `package.json` | Aberta; specs existiam, mas Playwright/pixelmatch/axe não formavam um gate executável do repo |
| Consulta direta à organização prestadora dentro de `TicketConfirmationService` | Aberta, de baixo risco funcional; possível correção de fronteira quando o módulo Tickets voltar a ser alterado |

Nenhuma dessas linhas autoriza mudança de código por conta própria. Antes de execução, revalidar o
estado do repo, procurar issue equivalente no Linear e definir owner, aceite e prioridade.
