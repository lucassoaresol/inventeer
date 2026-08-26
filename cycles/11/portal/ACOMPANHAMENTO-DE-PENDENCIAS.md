# Acompanhamento de Pendências do Portal no Ciclo 11

- **Responsável pelo recorte:** Lucas Oliveira
- **Ciclo:** 11
- **Aberto em:** 2026-08-26
- **Última revalidação:** 2026-08-26
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
