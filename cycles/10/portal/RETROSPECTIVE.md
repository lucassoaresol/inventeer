# Retrospectiva de Entrega do Portal no Ciclo 10 — Lucas Oliveira

- **Ciclo:** 10
- **Recorte por responsável:** Lucas Oliveira
- **Fechado em:** 2026-08-26
- **Snapshot do Linear:** 2026-08-26
- **Evidência de entrega:** 9 tasks em `Done`; 18 pontos de esforço final; 15 PRs vinculadas merged

## Veredito do fechamento

O recorte de Lucas Oliveira no Ciclo 10 está fechado. O Linear registra todas as nove tasks como
`Done`, e o GitHub registra as quinze PRs vinculadas como merged. O ciclo entregou duas capacidades
coerentes do Portal: o primeiro ciclo de vida operacional de Ticket e o painel v1 de Metrics de
entrega.

Este fechamento é documentação histórica. O Linear permanece canônico para hierarquia, ciclo,
estado, responsável, relações e estimativas atuais. Os artifacts de produto permanecem canônicos
para a intenção do produto. O GitHub e os repositórios de produto permanecem canônicos para as
mudanças entregues.

Leituras complementares:

- [planejamento e capacidade: baseline versus fechamento](./PLANEJAMENTO-E-CAPACIDADE.md);
- [pendências e decisões de escopo no fechamento](./PENDENCIAS-DO-FECHAMENTO.md).

## O que foi entregue

### Intake, acompanhamento, ciclo de vida e notificações de Ticket

| Task | Resultado entregue | Evidência merged |
| --- | --- | --- |
| `INV-3828` | Domínio dedicado de Ticket; intake, confirmação, anexo, lista/detail e contrato inicial de permissões com isolamento entre tenants | [portal-api#293](https://github.com/Inventeer/portal-api/pull/293); [inventeer-ops#239](https://github.com/Inventeer/inventeer-ops/pull/239) |
| `INV-3830` | Tickets Home com seis contadores de apresentação, filtros processados no servidor, tratamento visual de estado e fronteira estável para abrir o detail | [portal-web#236](https://github.com/Inventeer/portal-web/pull/236) |
| `INV-3941` | Máquina de estados de Ticket, timeline visível ao solicitante, comandos por ator, ações permitidas, cota de reabertura, motivo de recusa e permissões do ciclo de vida | [portal-api#298](https://github.com/Inventeer/portal-api/pull/298); [inventeer-ops#249](https://github.com/Inventeer/inventeer-ops/pull/249) |
| `INV-3831` | Overlay roteável de Ticket Detail com timeline, comandos do solicitante, cota de reabertura, motivo de recusa e comportamento de fechamento/navegação | [portal-web#238](https://github.com/Inventeer/portal-web/pull/238) |
| `INV-3847` | Notificações por ocorrência para o solicitante, conectadas aos eventos do ciclo de vida de Ticket por meio da fundação existente | [portal-api#299](https://github.com/Inventeer/portal-api/pull/299) |

O recorte entregue mantém Ticket separado de Request e do pipeline governado de intake do IDS. Ele
também separa os lados do solicitante e do Labs por meio de permissões na organização solicitante e
na organização prestadora.

### Metrics de entrega v1

| Task | Resultado entregue | Evidência merged |
| --- | --- | --- |
| `INV-3832` | Permissão explícita de Metrics com escopo de organização, navegação que falha de forma fechada e controle de acesso à rota | [portal-api#285](https://github.com/Inventeer/portal-api/pull/285); [portal-web#228](https://github.com/Inventeer/portal-web/pull/228); [inventeer-ops#201](https://github.com/Inventeer/inventeer-ops/pull/201) |
| `INV-3875` | Fundação compartilhada e com isolamento entre tenants na Portal API e Web, com mapeamento de organização, série mensal normalizada e estados parciais/de erro | [portal-api#286](https://github.com/Inventeer/portal-api/pull/286); [portal-web#229](https://github.com/Inventeer/portal-web/pull/229) |
| `INV-3833` | Aba `Technical` com as tendências suportadas de DORA, confiabilidade e qualidade | [portal-web#230](https://github.com/Inventeer/portal-web/pull/230) |
| `INV-3834` | Aba `Delivery Flow` com `Delivered per week`, `Work in progress` aproximado e `Bug Ratio (All)`, omitindo métricas sem suporte | [portal-api#290](https://github.com/Inventeer/portal-api/pull/290); [portal-web#231](https://github.com/Inventeer/portal-web/pull/231) |

O recorte de Metrics entregou a menor superfície verdadeira suportada pelos contratos de origem.
Dados ausentes ou sem suporte permanecem indisponíveis, em vez de serem convertidos em zero ou em
valores placeholder.

## Leitura da documentação do produto

### O que foi bem estruturado

- O mapa da iniciativa separa Tickets de Metrics e dá a cada frente um resultado explícito.
- Os bloqueios formais correspondem à forma da entrega: a `INV-3875` precede as duas abas de
  Metrics, enquanto a `INV-3941` precede o overlay de Ticket e as notificações do ciclo de vida.
- O ownership entre repositórios está consistente. Portal API possui contratos tenant-safe e
  autoridade; Portal Web consome esses contratos e possui a interação; `inventeer-ops` registra
  mudanças de permissão.
- Mudanças de permissão foram entregues com PRs de documentação no mesmo limite da mudança de
  produto. O catálogo de permissões agora registra Metrics, intake de Ticket, triagem do Labs e
  interação do solicitante.
- As duas capacidades falham de forma fechada nas fronteiras de confiança. O contexto da organização
  e a permissão são resolvidos no servidor; o navegador não seleciona tenant privilegiado nem dimensões
  de Metrics.
- O trabalho de Ticket preserva a regra documentada do Portal: superfícies voltadas ao cliente não
  expõem mecanismos internos do Linear, Labs ou IDS.

### Lacunas e padrões não seguidos de forma consistente

- Antes deste fechamento, o mapa da iniciativa v1 não era atualizado desde sua criação em
  2026-08-11. Ele descrevia todos os itens como `Backlog` e mantinha o responsável original de
  Metrics depois que o Linear atribuiu e concluiu o trabalho do Ciclo 10 com Lucas Oliveira. Este
  fechamento corrigiu os dois campos.
- A primeira promoção de clarificações capturou oito tasks antes do snapshot final de Linear/GitHub.
  Ela omitiu a `INV-3941` e preservou vários estados anteriores ao merge mesmo depois que todas as PRs
  vinculadas haviam sido merged.
- Antes deste fechamento, o README do Portal descrevia o produto principalmente como a porta de
  entrada do IDS. Este fechamento adicionou Tickets e Metrics ao ponto de entrada.
  `PORTAL_Base_Overview` permanece centrado no escopo anterior de Request/IDS e ainda exige uma
  decisão de produto sobre seu versionamento.
- `PORTAL_Permission_Catalog` contém o modelo de permissões entregue, mas permanece `Draft`. O
  fechamento do ciclo não pode convertê-lo em `Approved`; a aprovação do produto é uma ação de
  governança separada.
- `PORTAL_Execution_Plan` está corretamente marcado como histórico, mas não pode ser usado como
  roadmap atual de Tickets ou Metrics. Linear e os mapas mais recentes da iniciativa devem continuar
  como fonte operacional.

### Padrões emergentes que merecem preservação

1. **Extrair fundações compartilhadas como tasks explícitas.** A `INV-3875` e a `INV-3941` mostram o
   mesmo padrão útil: quando várias tasks voltadas ao usuário dependem de um contrato entre
   repositórios, a
   fundação vira uma task de primeira classe e um bloqueio formal. Ela não fica escondida no escopo
   do primeiro consumidor.
2. **Entregar documentação governada com o contrato.** Mudanças de permissão ou autoridade incluem a
   atualização correspondente em `inventeer-ops` no mesmo resultado da task.
3. **Publicar contratos antes dos consumidores.** Estados, permissões, DTOs e ações permitidas que
   pertencem à API são entregues antes da superfície Web que os consome.
4. **Preferir entrega parcial verdadeira.** Metrics sem suporte são omitidas ou marcadas como
   indisponíveis, com escopo explícito de trabalho posterior, em vez de serem simuladas no cliente.

Os dois primeiros padrões se repetiram dentro de um ciclo e são candidatos a um padrão durável de
entrega do Portal. Eles ficam registrados aqui como prática emergente, ainda não como decisão
transversal do workspace.

## Trabalho transferido para o Ciclo 11

- A `INV-3915` leva o intake conversacional de New Ticket para o Ciclo 11.
- A `INV-3942` leva a mediação dos pedidos de contexto de Ticket por Inventeer Intelligence para o
  Ciclo 11.
- Metrics v2 continua nas tasks do Ciclo 11 vinculadas em
  `INV_Portal_V2_Delivery_Metrics_Initiative_Map`.
- Uma task documental sob ownership de produto deve reconciliar `PORTAL_Base_Overview` com Tickets e
  Metrics e decidir se seu escopo v1.2 versionado será ampliado ou preservado como baseline histórico
  do intake IDS.
- Ainda é necessária aprovação de produto antes de mudar `PORTAL_Permission_Catalog` de `Draft`.

## Limite do fechamento

Este fechamento cobre somente as tasks atribuídas a Lucas Oliveira que o Linear atualmente coloca no
Ciclo 10. Ele não fecha a `INV-3811` nem a `INV-3812`, que permanecem em `In Progress` porque o
trabalho do Ciclo 11 não terminou. Ele não afirma deploy, smoke em produção nem rollout para clientes
além das evidências merged indicadas acima.
