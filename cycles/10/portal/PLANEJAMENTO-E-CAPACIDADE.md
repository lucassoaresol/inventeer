# Retrospectiva de Planejamento e Capacidade do Portal no Ciclo 10

- **Responsável:** Lucas Oliveira
- **Ciclo:** 10, de 2026-08-12 a 2026-08-26
- **Baseline de planejamento:** 2026-08-12
- **Fechamento reconciliado:** 2026-08-26
- **Escopo:** tasks de entrega do Portal atribuídas a Lucas Oliveira

## Propósito e limite

Este documento preserva a parte durável da análise de planejamento e capacidade feita durante o
ciclo. Ele compara a intenção inicial com o que o Linear e as entregas merged registravam no
fechamento. As previsões abaixo são evidência histórica de planejamento, não uma estimativa atual e
nem um novo modelo oficial de capacidade.

Linear permanece canônico para ciclo, responsável, estado e estimativa. A
[retrospectiva de entrega](./RETROSPECTIVE.md) registra o resultado funcional, e os
[snapshots de task](./tasks/README.md) preservam a clarificação de cada entrega.

## Planejado versus realizado

| Medida | Baseline de 2026-08-12 | Fechamento de 2026-08-26 |
| --- | ---: | ---: |
| Tasks de entrega | 7 | 9 |
| Pontos Tech oficiais | 14 | 18 |
| Goal Points pelo fator de referência `1,5` | 21 | 27 |
| Capacidade de referência de Lucas | 19 | 19 |
| Utilização pelo modelo | 110,5% | 142,1% |
| Situação | Meta aspiracional, acima da capacidade formal | 9 tasks em `Done`; 15 PRs vinculadas merged |

O baseline técnico provisório produzido durante o refinamento chegou a 19 pontos para as sete tasks
originais. Ele não foi escrito no Linear nem virou compromisso. O fechamento ficou em 18 pontos,
mas por uma composição diferente: os HPEs das tasks originais foram preservados e duas fundações
foram contratadas como tasks próprias.

| Fundação descoberta durante o planejamento | Forma assumida na execução | Esforço final |
| --- | --- | ---: |
| BFF tenant-safe e contrato mensal compartilhado de Metrics | `INV-3875` | 2 pontos |
| Ciclo de vida, timeline, comandos e permissões de Ticket | `INV-3941` | 2 pontos |

Isso confirma uma premissa acertada do planejamento: fundações entre repositórios não deveriam ser
absorvidas silenciosamente pelo primeiro consumidor. A diferença entre 14 e 18 pontos ficou visível
na composição do ciclo, em vez de ser escondida nas tasks de interface.

## Ordem realmente executada

| Data de conclusão no Linear | Task | Papel na sequência |
| --- | --- | --- |
| 2026-08-14 | `INV-3832` | Abriu a frente Metrics com permissão e acesso fail-closed |
| 2026-08-17 | `INV-3875` | Materializou a fundação compartilhada de dados de Metrics |
| 2026-08-18 | `INV-3833` | Entregou a aba `Technical` sobre a fundação |
| 2026-08-19 | `INV-3834` | Reutilizou a fundação na aba `Delivery Flow` |
| 2026-08-21 | `INV-3828` | Criou o domínio e o intake inicial de Ticket |
| 2026-08-24 | `INV-3830` | Entregou a leitura do Tickets Home |
| 2026-08-25 | `INV-3941` | Publicou o ciclo de vida e os contratos compartilhados de Ticket |
| 2026-08-25 | `INV-3847` | Conectou eventos de Ticket às notificações do solicitante |
| 2026-08-25 | `INV-3831` | Fechou a experiência Web do Ticket Detail |

A frente Metrics seguiu a onda prevista: gate, fundação e consumidores. A frente Tickets preservou
a direção geral de domínio antes das superfícies, mas ganhou a `INV-3941` entre a lista e os
consumidores do ciclo de vida. Notificações concluíram antes do overlay Web porque ambos já podiam
consumir a fundação publicada pela API; não havia bloqueio formal exigindo que a interface fosse
mergeada primeiro.

## O que o planejamento antecipou bem

- A meta inicial já excedia a capacidade formal de 19 Goal Points; portanto, não deveria ser
  comunicada como compromisso confortável.
- Metrics precisava começar pelo gate de permissão e por uma fronteira server-side tenant-safe.
- As abas `Technical` e `Delivery Flow` precisavam compartilhar série mensal, normalização e estados
  parcial, indisponível e de erro.
- Ticket era um domínio novo e não cabia ser tratado como duas telas frontend-only.
- As notificações dependiam de eventos e deep links estáveis do ciclo de vida de Ticket.
- As lacunas comuns deveriam ganhar tasks e HPE próprios, sem dupla contagem.

## O que mudou durante a execução

- A permissão de Metrics, inicialmente tratada como decisão aberta, foi contratada como
  `portal.client.metrics.view` e entregue na `INV-3832`.
- A task de apoio de Metrics deixou de ser hipótese e virou a `INV-3875`.
- A fundação de ciclo de vida de Ticket deixou de ficar implícita entre `INV-3831` e `INV-3847` e
  virou a `INV-3941`.
- O recorte de Delivery Flow preferiu métricas verdadeiras e suportadas; itens sem contrato ficaram
  fora da v1 em vez de receber placeholders.
- A integração real do Ticket Detail não chegou a staging/UAT no ciclo por falta de grants de
  requester. A entrega local foi validada com MSW, sem alegação de rollout.
- `INV-3915`, `INV-3942` e Metrics v2 passaram ao Ciclo 11; nenhuma das nove tasks contabilizadas
  neste fechamento ficou incompleta.

## Leitura do resultado de capacidade

Concluir 27 Goal Points pelo fator de referência, diante de uma capacidade nominal de 19, não torna
o modelo automaticamente inválido nem transforma 142,1% em uma nova expectativa. O ciclo foi
executado com assistência de IA, decomposição explícita de fundações e várias entregas pequenas,
mas a análise histórica não separa com confiabilidade horas humanas, espera por revisão, trabalho
offline e latência de decisões.

O dado útil para ciclos seguintes é o desvio de composição: uma frente aparentemente formada por
sete tasks terminou exigindo nove. O sinal de risco de 19 pontos ficou próximo dos 18 pontos finais,
mas por redistribuição de escopo, não porque a previsão de horas tenha sido comprovada. Planejamento
futuro deve continuar expondo tasks de fundação cedo e usar o histórico somente como calibração,
não como promessa de throughput.

## Decisões preservadas para o próximo planejamento

1. Manter HPE oficial até existir evidência suficiente para reestimar; lacunas novas recebem task e
   HPE próprios.
2. Planejar fundações compartilhadas antes das superfícies consumidoras.
3. Separar capacidade nominal, esforço Tech e Goal Points; nenhum deles, sozinho, representa horas
   líquidas de execução.
4. Tratar dependência externa e provisionamento como trabalho visível, mesmo quando não alteram
   código.
5. Não converter o desempenho de um ciclo assistido por IA em compromisso automático para o ciclo
   seguinte.
