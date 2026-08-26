# Registro de Clarificações por Ciclo

Este diretório preserva snapshots curados de clarificação de tasks por ciclo de planejamento. É uma
memória durável do workspace, não um espelho do Linear nem um repositório de especificações de
produto.

## Autoridade

- Linear permanece canônico para hierarquia, ciclo, estado, responsável, relações, estimativas e
  execução atuais.
- A documentação de produto permanece canônica para intenção e contratos governados do produto.
- Os repositórios de produto permanecem canônicos para código, testes e decisões técnicas locais.
- Um registro de ciclo preserva o que foi clarificado para planejamento em uma data específica.
  Revalide seus fatos antes de preparar, implementar, revisar ou retomar uma issue.

## Estrutura

```text
cycles/<ciclo>/README.md
cycles/<ciclo>/<produto>/PENDENCIAS-DE-ENTRADA.md
cycles/<ciclo>/<produto>/ACOMPANHAMENTO-DE-PENDENCIAS.md
cycles/<ciclo>/<produto>/PENDENCIAS-DO-FECHAMENTO.md
cycles/<ciclo>/<produto>/tasks/INV-<id>.md
```

Cada registro de task contém conclusões duráveis, decisões, limites de escopo, dependências materiais
e referências às fontes canônicas. Cronologia de sessão, artifacts TLC, estado de processos locais,
logs, pacotes de revisão, credenciais, dados de clientes e saídas de produção permanecem em
`session-context/`, que é ignorado, ou em seus sistemas canônicos.

Os registros de pendências são opcionais e têm três etapas distintas:

1. **Entrada do ciclo:** revalida o que foi herdado contra Linear e fontes atuais, registra o recorte
   comprometido e separa trabalho canônico, candidata ainda sem issue e decisão encerrada.
2. **Acompanhamento:** acumula revalidações materiais ocorridas depois da entrada, com evidência e
   limites explícitos, sem reescrever o snapshot inicial nem presumir backlog.
3. **Fechamento do ciclo:** registra descobertas do período, a disposição de cada item e o que será
   levado à entrada seguinte.

Uma pendência versionada não cria backlog. Somente a issue no Linear define owner, prioridade, ciclo
e execução. O documento de entrada e o de fechamento permanecem como snapshots; o acompanhamento
pode evoluir durante o ciclo e é destilado no fechamento. O ciclo seguinte cria sua própria etapa em
vez de reescrever a anterior.

## Ciclo de vida

Promova uma clarificação somente depois de separar seu resultado durável do handoff de trabalho. Não
copie um handoff bruto para esta árvore. Se uma issue receber uma clarificação materialmente nova em
outro ciclo, preserve o registro anterior e crie um novo registro no ciclo posterior. O Linear, não
a localização do diretório, informa qual ciclo contém atualmente a issue.

## Ciclos disponíveis

- [Ciclo 10](./10/README.md)
- [Ciclo 11](./11/README.md)
