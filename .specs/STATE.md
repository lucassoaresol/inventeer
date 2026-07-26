# Workspace State

Este arquivo registra somente decisões e handoff do workspace pessoal. Specs, designs e validações
de produtos devem permanecer nos respectivos repositórios sob `repos/`.

## Decisions

### AD-001
- **Decision**: Manter este repositório como ponto de entrada pessoal para engenharia na Inventeer, sem torná-lo fonte canônica dos produtos.
- **Reason**: Centralizar skills e navegação permite um setup reproduzível sem competir com código, Linear ou governança corporativa.
- **Trade-off**: O workspace depende de ponteiros para fontes externas e não funciona como documentação completa dos produtos.
- **Alternatives considered**: Manter skills globalmente em cada máquina; versionar o contexto diretamente em cada produto desde o início.
- **Scope**: Todo o workspace.
- **Date**: 2026-07-10
- **Status**: active

### AD-002
- **Decision**: Clonar repositórios de trabalho em `repos/<nome>` e ignorar integralmente `/repos/` no Git deste workspace.
- **Reason**: Cada produto preserva histórico, branch, regras e lifecycle Git independentes enquanto permanece acessível a partir de um único diretório do Codex.
- **Trade-off**: Clones não são provisionados pelo Git deste workspace e precisam ser recriados em cada máquina.
- **Alternatives considered**: `.repos/` oculto; `repo/` no singular; submodules; clones fora deste workspace.
- **Scope**: Descoberta e operação de todos os repositórios de produto.
- **Date**: 2026-07-10
- **Status**: active

### AD-003
- **Decision**: Versionar skills do Codex diretamente em `.agents/skills/`.
- **Reason**: Esse layout já foi comprovado no repositório EDREN e permite descoberta local sem instalador, cópia global ou adapter.
- **Trade-off**: O workspace assume Codex como engine e não busca portabilidade automática para outros agentes.
- **Alternatives considered**: `skills/` na raiz com instalador; `$CODEX_HOME/skills`; `.codex/skills`; adapters por engine.
- **Scope**: Autoria, descoberta e distribuição das skills deste workspace.
- **Date**: 2026-07-10
- **Status**: active

### AD-004
- **Decision**: Vendorizar `tlc-spec-driven` 3.2.0 em `.agents/skills/` e atualizá-la separadamente das skills locais.
- **Reason**: O setup deve funcionar em futuras máquinas sem depender de skills instaladas globalmente.
- **Trade-off**: O repositório passa a acompanhar atualizações e preservar atribuição da dependência vendorizada.
- **Alternatives considered**: Depender da instalação global; copiar a versão 3.1.0 do EDREN; reimplementar o workflow localmente.
- **Scope**: Especificação, design, execução, validação e memória realizados por TLC.
- **Date**: 2026-07-10
- **Status**: active

### AD-005
- **Decision**: Separar preparação de contexto do Assistants (`assistants-task-context`) do workflow de entrega (`tlc-spec-driven`).
- **Reason**: Hierarquia Linear, DoDs e convenções do Assistants são conhecimento específico; Specify, Design, Tasks e Execute são capacidades genéricas já cobertas pela TLC.
- **Trade-off**: Alguns trabalhos acionam duas skills em sequência e exigem um handoff explícito de contexto.
- **Alternatives considered**: Fazer fork da TLC; duplicar seu workflow na skill do Assistants; usar apenas a TLC sem contexto de projeto.
- **Scope**: Tasks pertencentes ao produto Assistants, raiz `INV-2228`.
- **Date**: 2026-07-10
- **Status**: active

### AD-006
- **Decision**: Manter pontos de entrada versionados em `projects/` como ponteiros leves para fontes canônicas.
- **Reason**: O Codex precisa localizar rapidamente repositório, documentos e skills aplicáveis sem copiar conteúdo governado.
- **Trade-off**: Os ponteiros precisam ser atualizados quando caminhos ou fontes canônicas mudarem.
- **Alternatives considered**: Copiar documentação dos produtos; embutir todos os caminhos dentro das skills; depender apenas de descoberta informal.
- **Scope**: Onboarding e navegação entre projetos Inventeer.
- **Date**: 2026-07-10
- **Status**: active

### AD-007
- **Decision**: Manter specs, designs, tasks e validações de produto dentro do repositório do produto; `.specs/STATE.md` deste repo registra somente memória do workspace.
- **Reason**: A capacidade pertence ao workspace, mas o estado produzido pertence ao produto que será implementado e revisado.
- **Trade-off**: O histórico completo de uma entrega exige entrar no repositório aninhado correspondente.
- **Alternatives considered**: Centralizar todas as specs neste workspace; não persistir decisões do workspace; criar um `DECISIONS.md` fora da convenção TLC.
- **Scope**: Persistência de decisões, specs e evidências.
- **Date**: 2026-07-10
- **Status**: active

### AD-008
- **Decision**: Registrar projetos separadamente de seus repos e permitir que um ponto de entrada represente uma topologia multi-repo.
- **Reason**: Assistants e IDS usam um repo principal, enquanto Portal distribui produto, backend e frontend entre `portal`, `portal-api` e `portal-web`.
- **Trade-off**: O registry precisa manter relações e limites de ownership além de uma simples lista de clones.
- **Alternatives considered**: Um manifesto por repo sem visão de produto; tratar cada repo de Portal como projeto independente; depender apenas dos nomes das pastas.
- **Scope**: `projects/` e navegação cross-repo do workspace.
- **Date**: 2026-07-10
- **Status**: active

### AD-009
- **Decision**: Registrar `inventeer-hub` como foundation read-only do workspace, separado dos produtos e do IDS.
- **Reason**: O Hub é o Playbook tenant-neutral e fonte dos standards `HUB_*` consumidos por todos os spokes como referência, não um produto comum de implementação.
- **Trade-off**: Consultas podem atravessar mais um repo e mudanças no Playbook exigem protocolos próprios em vez de serem tratadas como ajustes locais.
- **Alternatives considered**: Não clonar o Hub; tratá-lo como produto no registry; copiar standards necessários para este workspace.
- **Scope**: Consulta de naming, hierarquia, workspace, Linear, contexto, plugins e onboarding.
- **Date**: 2026-07-10
- **Status**: active

### AD-010
- **Decision**: Criar `portal-task-context` como skill irmã de `assistants-task-context`, com raiz Linear `INV-254` e entendimento explícito da topologia `portal` + `portal-api` + `portal-web`.
- **Reason**: Tasks do Portal precisam combinar intenção e artifacts do produto com ownership técnico distribuído entre backend e frontend antes de especificar ou implementar.
- **Trade-off**: As duas skills de produto repetem parte do workflow de preparação até que uso real justifique extrair uma base comum.
- **Alternatives considered**: Generalizar imediatamente uma única skill para todos os produtos; usar a skill de Assistants com parâmetros; depender apenas da TLC e dos AGENTS.md dos repos.
- **Scope**: Issues descendentes de `INV-254` e trabalho nos três repos do Portal.
- **Date**: 2026-07-10
- **Status**: active

### AD-011
- **Decision**: Tornar `repos/ids` uma dependência contextual condicional da skill `portal-task-context` para comportamentos governados pelo pipeline IDS.
- **Reason**: Portal apresenta e implementa etapas do intake e dos Gates, mas os contratos e standards de DAP/EPP/DEP, aprovação, rigor e handoff permanecem canônicos no IDS.
- **Trade-off**: Tasks com semântica de pipeline exigem leitura cross-repo adicional; tasks puramente locais devem registrar IDS como não aplicável para evitar carga desnecessária.
- **Alternatives considered**: Carregar IDS em toda task de Portal; confiar apenas nos artifacts de Portal; copiar standards IDS para Portal; consultar IDS informalmente sem regra na skill.
- **Scope**: Preparação, especificação, implementação e validação de issues descendentes de `INV-254` com dimensão IDS.
- **Date**: 2026-07-10
- **Status**: active

### AD-012
- **Decision**: Tornar `repos/ids` uma dependência contextual condicional da skill `assistants-task-context` para trabalho governado por DAP, EPP, DEP ou Gates.
- **Reason**: Assistants refina contratos do IDS, mas escopo, DoDs, constraints de engenharia e evidências de entrega permanecem canônicos no workspace do produto dentro de `repos/ids`.
- **Trade-off**: Tasks governadas exigem leitura cross-repo; mudanças internas de runtime devem declarar IDS como não aplicável para evitar contexto desnecessário.
- **Alternatives considered**: Carregar IDS em toda task; confiar somente nos artifacts do repo Assistants; copiar contratos para perto do código; consultar IDS informalmente sem regra na skill.
- **Scope**: Issues descendentes de `INV-2228` com impacto em contratos, Gates, rigor ou evidências de entrega.
- **Date**: 2026-07-10
- **Status**: active

### AD-013
- **Decision**: Centralizar a atualização segura dos clones locais em `scripts/update-repos.sh` e executá-la como primeira etapa das skills `portal-task-context` e `assistants-task-context`.
- **Reason**: Preparar tasks com código atualizado reduz conclusões baseadas em clones defasados e evita duplicar regras de sincronização entre skills.
- **Trade-off**: O início do fluxo passa a depender de acesso aos remotes; worktrees com mudanças locais permanecem intocados e geram aviso de possível defasagem. Repositórios com branch local `develop` usam essa branch; os demais usam a branch padrão do `origin`.
- **Alternatives considered**: Atualização manual antes de cada task; executar `git pull` diretamente em cada skill; atualizar apenas o repo inicialmente identificado como alvo.
- **Scope**: Preparação de contexto de Portal e Assistants e manutenção dos clones sob `repos/`.
- **Date**: 2026-07-10
- **Status**: active

### AD-014
- **Decision**: Preparar issues de Assistants e Portal com revisão inicial em português no chat, artefatos canônicos finais em inglês somente após aprovação explícita, orientação funcional e operacional antes de decisões e estado `Draft` até aprovação, salvo instrução diferente do usuário; criar arquivo intermediário de revisão apenas quando solicitado.
- **Reason**: O uso real mostrou que decisões técnicas tomadas antes de estabelecer o modelo mental, a operação e o contrato editorial geram retrabalho e dificultam distinguir entendimento, aprovação e prontidão para implementação.
- **Trade-off**: A preparação ganha uma etapa editorial e pedagógica adicional, que deve permanecer adaptativa para não burocratizar tasks simples ou usuários que já dominam o contexto.
- **Alternatives considered**: Alterar a `tlc-spec-driven` vendorizada; produzir diretamente em inglês; deixar idioma, profundidade e status apenas implícitos no chat.
- **Scope**: Skills locais de contexto de produto e seus handoffs para a TLC; não altera a `tlc-spec-driven` vendorizada.
- **Date**: 2026-07-10
- **Status**: active

### AD-015
- **Decision**: Manter `.agents/skills/tlc-spec-driven` como mirror byte a byte do pacote oficial `tech-leads-club/agent-skills`, registrar a revisão upstream fixada em `.agents/vendor.json` e realizar checks ou atualizações somente pelo script local `scripts/update-vendored-skill.sh`.
- **Reason**: Separar o conteúdo oficial das políticas Inventeer permite detectar alterações acidentais, incorporar melhorias upstream com diff reproduzível e manter toda personalização exclusiva deste workspace fora do pacote vendorizado.
- **Trade-off**: A atualização passa a depender de rede, `git`, `curl`, `tar`, `rsync` e `jq`; políticas locais não podem ser implementadas editando diretamente a TLC.
- **Alternatives considered**: Manter um fork; aplicar patches locais dentro da skill; copiar atualizações manualmente; depender apenas da instalação global.
- **Scope**: Vendor e atualização da `tlc-spec-driven` neste workspace; não cria commits, forks ou PRs no repositório oficial.
- **Date**: 2026-07-10
- **Status**: superseded by AD-016

### AD-016
- **Decision**: Manter `tlc-spec-driven` como fork local baseado em uma revisão upstream fixada, permitir personalizações exclusivas deste workspace dentro da skill e incorporar atualizações oficiais por merge de três vias entre base, local e incoming.
- **Reason**: Alguns aprendizados são melhorias deliberadas do próprio workflow TLC neste workspace; preservá-los junto à skill torna o comportamento consistente, enquanto a base fixada permite distinguir claramente mudanças oficiais e locais durante upgrades.
- **Trade-off**: O diretório deixa de ser um mirror puro e futuras atualizações exigem revisão humana de diffs e possíveis conflitos; a Inventeer assume a manutenção dessas personalizações sem propor mudanças ao repositório oficial.
- **Alternatives considered**: Mirror upstream sem personalizações; skill complementar; patches externos reaplicados manualmente; fork remoto com PRs upstream.
- **Scope**: `tlc-spec-driven` e seu processo de atualização somente neste workspace; nenhuma interação de escrita com o repositório oficial.
- **Date**: 2026-07-10
- **Status**: active

### AD-017
- **Decision**: Reservar `session-context/`, integralmente ignorado pelo Git, para documentos auxiliares fornecidos durante uma sessão e necessários apenas ao trabalho corrente.
- **Reason**: Tasks podem depender de contexto ad hoc que precisa estar acessível ao Codex sem virar histórico do workspace, spec de produto ou fonte canônica concorrente.
- **Trade-off**: O conteúdo não é reproduzido em outra máquina nem preservado pelo Git; materiais que se tornem evidência ou decisão durável precisam ser promovidos deliberadamente à fonte canônica adequada.
- **Alternatives considered**: Usar `/tmp`; guardar arquivos dentro do repo de produto; versionar um diretório de contexto; reutilizar `.skill-results/`.
- **Scope**: Entrada efêmera de documentos para sessões neste workspace.
- **Date**: 2026-07-13
- **Status**: active

### AD-018
- **Decision**: Separar triagem de múltiplas issues (`triage-project-cycle`) e discovery sem issue
  (`discover-project-context`) das skills de contexto de task única de Assistants e Portal.
- **Reason**: Sessões reais incluíram planejamento de ciclos, comparação de várias tasks e desenho de
  fluxos ainda sem Linear; forçar esses casos no contrato de uma issue única ampliava contexto,
  misturava objetivos e enfraquecia o handoff para execução.
- **Trade-off**: O workspace ganha duas rotas adicionais e precisa transferir explicitamente a issue
  selecionada ou o trabalho canonizado para a skill de produto adequada.
- **Alternatives considered**: Ampliar as skills de produto com múltiplos modos; criar uma única skill
  genérica de contexto; usar diretamente a TLC; continuar tratando os casos informalmente.
- **Scope**: Preparação comparativa e discovery read-only dos projetos registrados neste workspace.
- **Date**: 2026-07-15
- **Status**: active

### AD-019
- **Decision**: Automatizar bundles efêmeros de review com a skill local `create-review-bundle`,
  usando um script read-only para o repo-fonte que gera manifesto, status, commits, diff por arquivo
  e checksum SHA-256, com rejeição de caminhos provavelmente sensíveis.
- **Reason**: Reviews recentes repetiram manualmente a criação de ZIPs, captura de diffs, proveniência
  e checksums; uma automação determinística reduz retrabalho e torna o conteúdo verificável.
- **Trade-off**: O fluxo depende de Bash, Git, `zip`, `unzip` e `sha256sum`; a rejeição por caminho não
  substitui a inspeção humana do diff para detectar conteúdo sensível em arquivos comuns.
- **Alternatives considered**: Adicionar imediatamente o comando ao `inv-cortex`; manter scripts ad
  hoc por sessão; versionar bundles; gerar um único diff sem manifesto por arquivo.
- **Scope**: Evidências temporárias de review produzidas neste workspace; não substitui validação,
  aprovação ou artifacts canônicos dos produtos.
- **Date**: 2026-07-15
- **Status**: active

### AD-020
- **Decision**: Configurar o servidor MCP `apex` somente no escopo deste workspace por meio de
  `.codex/config.toml`, removendo sua entrada da configuração global do Codex.
- **Reason**: O APEX pertence ao fluxo de engenharia dos projetos Inventeer neste workspace e não
  deve aparecer nem consumir contexto em sessões Codex iniciadas em diretórios não relacionados.
- **Trade-off**: O projeto precisa estar marcado como confiável e novas sessões devem usar este
  workspace como raiz para carregar o servidor; os repositórios Git independentes sob `repos/` não
  herdam essa camada quando abertos diretamente. Mudanças de configuração exigem reiniciar o Codex.
- **Alternatives considered**: Manter o MCP global; usar um profile global selecionado manualmente;
  habilitar e desabilitar o servidor por sessão.
- **Scope**: Configuração Codex e disponibilidade do APEX MCP neste workspace.
- **Date**: 2026-07-20
- **Status**: active

### AD-021
- **Decision**: Configurar o servidor MCP `linear` somente no escopo deste workspace por meio de
  `.codex/config.toml`, removendo sua entrada da configuração global do Codex e preservando o modo
  de aprovação de ferramentas como `prompt`.
- **Reason**: O Linear é a fonte canônica de execução dos projetos Inventeer deste workspace e não
  precisa ficar disponível em sessões Codex iniciadas para trabalhos não relacionados.
- **Trade-off**: Assim como o APEX, o Linear só é carregado quando este workspace é a raiz confiável
  da sessão; os repositórios Git independentes sob `repos/` não herdam essa configuração quando
  abertos diretamente.
- **Alternatives considered**: Manter o MCP global; usar um profile global selecionado manualmente;
  habilitar e desabilitar o servidor por sessão.
- **Scope**: Configuração Codex e disponibilidade do Linear MCP neste workspace.
- **Date**: 2026-07-20
- **Status**: active

### AD-022
- **Decision**: Coordenar frentes contínuas de entrega com no máximo uma PR pronta para review e uma
  próxima task em implementação ou PR draft por repositório; priorizar tasks independentes e
  permitir no máximo um nível de PR dependente com boundary SHA registrado, mantendo-a draft até a
  reconciliação com a branch de integração.
- **Reason**: Review e aprovação são esperas externas; o ciclo deve continuar sem misturar escopos,
  esconder dependências ou criar stacks difíceis de recuperar após squash merge.
- **Trade-off**: O fluxo adiciona classificação, metadados e uma etapa de reconciliação; algumas
  tasks conflitantes ainda precisarão aguardar quando não houver trabalho independente seguro.
- **Alternatives considered**: Parar até cada merge; abrir várias PRs prontas sem ordem; manter stacks
  ilimitados; embutir toda a coordenação na TLC; tratar cada transição informalmente.
- **Scope**: Seleção, preparação, review e reconciliação de tasks consecutivas nos repositórios
  registrados neste workspace.
- **Date**: 2026-07-22
- **Status**: active

### AD-023
- **Decision**: Tratar implementação e validação como eixos distintos de maturidade da entrega,
  vincular todo PASS ao SHA/surface/contrato/gates efetivamente verificados, invalidá-lo após qualquer
  mudança relevante e encadear gerações efêmeras de review bundle por checksum e delta de paths.
- **Reason**: Sessões reais produziram várias gerações de evidência para a mesma issue e mostraram
  que implementação validada, commitada, publicada e promovível não são estados equivalentes.
- **Trade-off**: O fluxo passa a carregar mais metadados, exige revalidação após correções e adiciona
  parsing/checksum de parent bundles; em troca, impede promoção com evidência obsoleta e torna o churn
  de review auditável sem criar uma nova fonte canônica.
- **Alternatives considered**: Tratar todo PASS como pronto para review; inferir lineage apenas pelo
  nome dos ZIPs; incorporar validação à `advance-delivery-front`; manter atomicidade por contagem de
  arquivos; registrar findings externos como lessons sem confirmação independente.
- **Scope**: `advance-delivery-front`, `create-review-bundle`, fork local `tlc-spec-driven` e seus
  handoffs neste workspace; não altera produtos, Linear ou GitHub.
- **Date**: 2026-07-23
- **Status**: active

### AD-024
- **Decision**: Operar este workspace com Codex e Claude Code sobre uma única fonte de skills em
  `.agents/skills/`, expondo-a ao Claude por symlinks em `.claude/skills/` e instruções por
  `CLAUDE.md` importando `AGENTS.md`; declarar o MCP `apex` também em `.mcp.json`; e derivar
  wrappers `apex-<id>` a partir da tool `apex_framework_index`, apenas para o Codex.
- **Reason**: Cada engine enxerga metade do conjunto. O Claude não descobre `.agents/skills/` nem lê
  `AGENTS.md`; o Codex consome tools e resources do APEX mas não materializa seus prompts como
  comandos. As duas lacunas se resolvem por arquivo, sem duplicar conteúdo nem eleger um engine.
- **Trade-off**: O repositório passa a carregar uma camada de exposição que precisa acompanhar cada
  skill nova, e os wrappers são conteúdo derivado que exige re-sync quando o catálogo APEX mudar. Os
  symlinks dependem de `core.symlinks` habilitado no clone. Em troca, não há cópia divergente e
  nenhum engine vira cidadão de segunda classe.
- **Alternatives considered**: Copiar as skills para `.claude/skills/`; manter a TLC instalada
  globalmente; materializar o corpo dos workflows APEX nos wrappers; obter o catálogo por
  `resources/read` de `apex://framework/runtime`; expor os wrappers também ao Claude.
- **Scope**: Descoberta de skills, instruções e MCP deste workspace nos dois engines; geração dos
  wrappers APEX. Não altera produtos, Linear, GitHub nem o conteúdo das skills.
- **Date**: 2026-07-26
- **Status**: active

### AD-025
- **Decision**: Tratar o APEX como executor de entrega nos repositórios de produto e manter
  `tlc-spec-driven` como fallback restrito a este workspace e aos repos sem `ENV.md`. As skills
  locais de contexto continuam responsáveis pela preparação, em qualquer um dos dois casos.
- **Reason**: O APEX cobre o pipeline de entrega de ponta a ponta e vai além da TLC em deploy,
  release, segurança e gates determinísticos; manter os dois como executores criaria pipelines
  concorrentes de spec, task e gate. Mas o APEX exige repo de produto, ticket e stack profile, e não
  cobre o desenvolvimento das próprias skills deste workspace — que é o que a TLC vem executando.
- **Trade-off**: Duas rotas de execução coexistem enquanto a adoção do APEX não se completa, e a
  escolha entre elas depende de verificar `ENV.md` no repo alvo. A TLC também não tem equivalente
  APEX para sua camada de lessons e para a rastreabilidade de requisitos, que ficam sem sucessora
  caso ela seja aposentada.
- **Alternatives considered**: Aposentar a TLC imediatamente; manter os dois executores sem
  precedência; copiar a TLC para cada repo de produto; adiar o APEX até cobrir os casos da TLC.
- **Scope**: Escolha do executor de entrega neste workspace e nos repositórios registrados sob
  `repos/`. Hoje apenas `portal-api` e `portal-web` têm `ENV.md` e `AGENTS.md` do APEX.
- **Date**: 2026-07-26
- **Status**: active

## Handoff

- **Feature**: Dual-engine workspace (Codex + Claude Code)
- **Phase / Task**: Execute complete — three commits delivered
- **Completed**: exposure layer at `d14b489` (7 skill symlinks, `CLAUDE.md`, `.mcp.json`,
  `.claude/settings.json`); `scripts/sync-apex-commands.sh` and 28 APEX wrappers at `35a9910`;
  AD-024, AD-025, docs and `scripts/test-sync-apex-commands.sh` with 14/14 tests and 6/6 killed
  mutants in this commit
- **In-progress**: none
- **Next step**: run `init-apex` on `assistants`, `ids`, `inv-cortex` and `portal` to complete the
  APEX adoption assumed by AD-025; re-sync the wrappers when the APEX catalog changes
- **Blockers**: none
- **Uncommitted files**: none after the closure commit
- **Branch**: main
- **Open questions**: `config.command` of `apex://framework/runtime` is visible to Claude Code but
  not to Codex, suggesting the gateway negotiates per client; not investigated, and not required by
  the acquisition contract, which uses `apex_framework_index`. The global copy at
  `~/.claude/skills-backup-tlc-spec-driven-3.1.0` is outside Git and still awaits disposal.
