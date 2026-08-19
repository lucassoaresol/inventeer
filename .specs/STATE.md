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
- **Status**: superseded by AD-042

### AD-011
- **Decision**: Tornar `repos/ids` uma dependência contextual condicional da skill `portal-task-context` para comportamentos governados pelo pipeline IDS.
- **Reason**: Portal apresenta e implementa etapas do intake e dos Gates, mas os contratos e standards de DAP/EPP/DEP, aprovação, rigor e handoff permanecem canônicos no IDS.
- **Trade-off**: Tasks com semântica de pipeline exigem leitura cross-repo adicional; tasks puramente locais devem registrar IDS como não aplicável para evitar carga desnecessária.
- **Alternatives considered**: Carregar IDS em toda task de Portal; confiar apenas nos artifacts de Portal; copiar standards IDS para Portal; consultar IDS informalmente sem regra na skill.
- **Scope**: Preparação, especificação, implementação e validação de issues descendentes de `INV-254` com dimensão IDS.
- **Date**: 2026-07-10
- **Status**: superseded by AD-042

### AD-012
- **Decision**: Tornar `repos/ids` uma dependência contextual condicional da skill `assistants-task-context` para trabalho governado por DAP, EPP, DEP ou Gates.
- **Reason**: Assistants refina contratos do IDS, mas escopo, DoDs, constraints de engenharia e evidências de entrega permanecem canônicos no workspace do produto dentro de `repos/ids`.
- **Trade-off**: Tasks governadas exigem leitura cross-repo; mudanças internas de runtime devem declarar IDS como não aplicável para evitar contexto desnecessário.
- **Alternatives considered**: Carregar IDS em toda task; confiar somente nos artifacts do repo Assistants; copiar contratos para perto do código; consultar IDS informalmente sem regra na skill.
- **Scope**: Issues descendentes de `INV-2228` com impacto em contratos, Gates, rigor ou evidências de entrega.
- **Date**: 2026-07-10
- **Status**: superseded by AD-042

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
- **Status**: superseded by AD-026

### AD-026
- **Decision**: Escolher o executor de entrega por engine e por repositório: no Claude Code, usar
  APEX quando o repo tiver `ENV.md` e TLC nos demais; no Codex, usar TLC para especificação,
  implementação e validação em todos os repos até uma nova validação end-to-end do APEX. Tools,
  resources e wrappers `apex-*` no Codex são superfície experimental e diagnóstica, não execução
  suportada do workflow. As skills locais de contexto continuam preparando a task nos dois engines.
- **Reason**: Sessões Codex reais (`019fa649-046f-7500-a0d1-050760e68e5e` e
  `019fa683-cb7c-7b33-b5d3-26077367ff48`) conseguiram ler workflows e chamar tools APEX, mas não
  receberam `preflight`, `write_session_artifact`, `run_gate`, `SESSION_ID` ou acesso do runner ao
  repo, impedindo o pipeline completo. A sessão Claude
  `e6a4a1c9-9d9c-4ba7-8aa0-1c92d1c473d7` operou workflow, artifacts e entrega APEX da INV-3286,
  declarando seus fallbacks quando algumas tools não estavam expostas.
- **Trade-off**: A rota diverge entre engines e mantém os wrappers Codex sem função de entrega; em
  troca, o workspace deixa de confundir conectividade MCP com execução do framework e evita gates
  improvisados apresentados como APEX. A paridade poderá ser reavaliada quando uma sessão Codex
  criar contexto e artifacts, executar os gates requeridos e concluir um workflow end-to-end.
- **Alternatives considered**: Manter AD-025 baseado apenas em `ENV.md`; retirar o APEX também do
  Claude; considerar leitura de resource equivalente a invocação; remover imediatamente os
  wrappers experimentais.
- **Scope**: Seleção do executor neste workspace e nos repositórios sob `repos/`; não altera o APEX,
  produtos, Linear ou GitHub.
- **Date**: 2026-07-28
- **Status**: superseded by AD-045

### AD-027
- **Decision**: Usar os históricos locais de Codex e Claude Code associados à raiz do workspace
  como evidência retrospectiva para evolução das skills, sem versionar transcripts; distinguir
  sessões principais, continuations e cópias, excluir a retrospectiva corrente e destilar cada
  achado na fonte adequada: decisão transversal em `STATE.md`, lesson de execução somente após
  validação pelo script da TLC e achado de produto na fonte canônica do produto.
- **Reason**: As retrospectivas anteriores consultaram apenas o histórico Codex, enquanto a adoção
  dual-engine e a INV-3286 mostraram comportamentos relevantes somente no Claude. Contar arquivos
  ou resumes como experiências independentes inflaria recorrência, e copiar transcripts criaria
  uma fonte de contexto sensível, ruidosa e não portátil.
- **Trade-off**: A análise exige deduplicação e julgamento de proveniência, e seus ponteiros de
  sessão podem não existir em outra máquina; em troca, a memória versionada permanece pequena,
  sanitizada e coerente com as fontes canônicas e com o hard gate de lessons da TLC.
- **Alternatives considered**: Analisar somente a engine ativa; importar JSONL para o repo; registrar
  toda observação como lesson; tratar continuations e sidechains como recorrências distintas.
- **Scope**: Retrospectivas e manutenção de skills e workflows deste workspace; não autoriza ler,
  copiar ou persistir credenciais, dados de clientes ou outputs de produção.
- **Date**: 2026-07-28
- **Status**: active

### AD-028
- **Decision**: Exigir um snapshot read-only de CPUs, carga, memória disponível, swap e filesystem
  antes de cargas potencialmente pesadas e fazer a TLC adaptar concorrência ou sharding sem reduzir
  a cobertura do gate.
- **Reason**: Sessões independentes nas duas engines registraram quedas durante suítes, paralelismo e
  uso de agentes; o host atual tem 2 CPUs, memória disponível limitada e nenhum swap. A TLC já
  permitia shards equivalentes, mas não exigia medir a capacidade corrente antes da execução.
- **Trade-off**: Toda etapa pesada ganha um preflight curto e pode executar com menos concorrência;
  em troca, a estratégia deixa de depender de capacidade presumida e preserva a sessão e a cobertura.
- **Alternatives considered**: Fixar sempre um worker; registrar apenas a limitação do `portal-api`;
  confiar na observação manual depois que a carga começar; reduzir o gate em máquinas menores.
- **Scope**: Trabalho complexo neste workspace e fork local da TLC; não define capacidade de CI nem
  altera comandos canônicos dos repositórios de produto.
- **Date**: 2026-07-28
- **Status**: active

### AD-029
- **Decision**: Versionar o MCP `context7` no escopo desta raiz para Codex e Claude Code, sem
  credenciais, preservando código e documentação local como fontes anteriores na cadeia de
  conhecimento; não configurar aqui MCPs de shadcn, Cloudflare ou AWS.
- **Reason**: A TLC já referencia Context7 e os repos usam stacks externas diversas, mas o servidor
  não estava disponível de forma reproduzível. Shadcn depende do cwd de `portal-web`; Cloudflare
  perde utilidade com a migração do Portal para AWS; e a superfície AWS atual exige uma decisão
  canônica de migração, autenticação e autoridade ainda ausente dos ponteiros versionados.
- **Trade-off**: O primeiro start de Context7 depende de Node/npm e rede e suas respostas continuam
  sendo contexto externo não canônico. Em troca, os dois engines ganham a mesma consulta atual de
  bibliotecas sem ampliar acesso a contas ou infraestrutura.
- **Alternatives considered**: Manter apenas busca web; adicionar Context7 globalmente; configurar
  shadcn com wrapper de cwd na raiz; adotar Cloudflare Docs pelo runtime legado; antecipar AWS MCP.
- **Scope**: Configuração MCP e documentação desta raiz; qualquer MCP de produto exige mudança
  separada no repositório owner.
- **Date**: 2026-07-28
- **Status**: superseded by AD-030

### AD-030
- **Decision**: Versionar os MCPs `context7` e `shadcn` nesta raiz para Codex e Claude Code, sem
  credenciais; executar shadcn com cwd explícito em `repos/portal-web`, manter suas escritas sujeitas
  a aprovação e não configurar Cloudflare ou AWS neste momento.
- **Reason**: O EDREN comprovou que os dois formatos de configuração suportam cwd específico por
  engine, e `portal-web` possui um `components.json` canônico e declara shadcn/ui como direção de UI.
  Isso torna a dependência de cwd um requisito verificável de roteamento, não um bloqueio técnico.
- **Trade-off**: O servidor shadcn só inicia em ambientes que clonaram `repos/portal-web`, seu
  primeiro uso depende de Node/npm e rede, e qualquer escrita ainda precisa respeitar as instruções
  e o worktree do repo de produto. Cloudflare perde utilidade com a migração para AWS, enquanto AWS
  continua aguardando contrato canônico de autenticação e autoridade.
- **Alternatives considered**: Manter shadcn somente no repo de produto; usar wrapper na raiz;
  manter a exclusão da AD-029; configurar Cloudflare Docs ou antecipar AWS MCP.
- **Scope**: Disponibilidade dos MCPs nos engines iniciados por esta raiz; não transfere ownership do
  Portal Web nem autoriza mutações em `repos/portal-web`.
- **Date**: 2026-07-28
- **Status**: active

### AD-031
- **Decision**: Durante o piloto de tasks do Portal executadas por Codex + TLC, manter artifacts
  file-backed internos da TLC em `session-context/portal/<INV-ID>/tlc/` e bundles em
  `session-context/portal/<INV-ID>/review/`, sem criar ou promover `.specs/` nos repos do Portal; o
  material local apoia execução, retomada e review, mas não é evidência canônica, oficial ou durável.
- **Reason**: O Portal aceita o lifecycle oficial de artifacts do APEX, mas o Codex ainda usa TLC e
  entregas reais mostraram que remover `.specs/` antes da PR deixa a retomada e a validação sem um
  local de trabalho previsível. `session-context/` já é a superfície efêmera e ignorada pelo Git
  destinada a contexto local.
- **Trade-off**: A rota melhora continuidade na mesma máquina sem contaminar branches de produto,
  mas não oferece portabilidade cross-machine nem persistência oficial; a próxima task Portal deve
  validar a mecânica antes que a prática seja considerada consolidada.
- **Alternatives considered**: Continuar removendo `.specs/` no fim da entrega; aceitar `.specs/`
  nos repos Portal; alterar a TLC genérica; aguardar APEX no Codex sem preservar artifacts locais;
  tratar bundles efêmeros como fonte canônica.
- **Scope**: Somente tasks do Portal executadas por Codex + TLC. Não altera Claude/APEX, outros
  produtos, Linear, repos de produto ou a skill TLC vendorizada. O diretório fica elegível para
  limpeza após merge e encerramento da issue, e a rota será retirada quando o Codex executar APEX
  end-to-end.
- **Date**: 2026-07-31
- **Status**: superseded by AD-045

### AD-032
- **Decision**: Manter as leituras diagnósticas do MCP `apex` disponíveis no Codex e exigir
  aprovação do engine para suas ferramentas de escrita por meio de
  `default_tools_approval_mode = "writes"`; a superfície mutável não amplia ownership nem torna o
  APEX um executor suportado no Codex.
- **Reason**: O catálogo atual passou a expor commit, push, criação de PR, atualização de task e
  orquestração multi-repo, enquanto AD-026 mantém o uso Codex estritamente experimental e
  diagnóstico. A configuração anterior não expressava uma fronteira de consentimento para essas
  mutações.
- **Trade-off**: Operações APEX mutáveis no Codex ganham uma interação de aprovação; em troca,
  consultas read-only continuam rápidas e uma expansão do gateway não concede autoridade
  silenciosamente. Claude/APEX permanece inalterado como rota nativa de entrega elegível.
- **Alternatives considered**: Exigir prompt para toda tool APEX; desabilitar o servidor no Codex;
  confiar apenas nas instruções de chat; promover o APEX a executor por disponibilidade de tools.
- **Scope**: Configuração e uso do MCP APEX no Codex iniciado por esta raiz; não altera Claude,
  produtos, Linear, GitHub ou repositórios aninhados.
- **Date**: 2026-08-02
- **Status**: active

### AD-033
- **Decision**: Iniciar retrospectivas deste workspace com
  `scripts/audit-session-history.py`, que agrega metadados das sessões Codex e Claude, deduplica
  continuations Codex e sidechains Claude, exclui explicitamente a sessão corrente e conta outcomes
  APEX somente a partir de pares estruturados de chamada e resultado, sem emitir conteúdo dos
  transcripts. Sucessos, falhas, negações e tentativas sem resultado permanecem separados.
- **Reason**: O recorte posterior a AD-027 contém muitas continuations após quedas, e buscas textuais
  simples também encontram nomes de tools injetados nas instruções, inflando tanto experiências
  quanto uso APEX. A análise manual é repetitiva e fácil de contaminar.
- **Trade-off**: A ligação de continuation Codex depende da convenção textual com UUID, `caiu` e
  `continue`, e o Claude só deduplica sidechains explicitamente marcadas; em troca, o inventário é
  reproduzível, conservador e não persiste prompts, respostas ou resultados.
- **Alternatives considered**: Continuar com comandos ad hoc; copiar JSONL para o workspace; contar
  cada arquivo como sessão independente; inferir uso APEX por ocorrência textual de nomes de tools.
- **Scope**: Retrospectivas de skills e fluxo deste workspace; não interpreta outcomes de produto,
  não modifica histories e não transforma metadados locais em fonte canônica.
- **Date**: 2026-08-02
- **Status**: active

### AD-034
- **Decision**: Considerar um workflow APEX executável somente quando a sessão recebe o contexto de
  workspace exigido pelo resource canônico, o servidor publica todas as tools requeridas e cada
  gate produz um resultado estruturado. Ausência de contexto/tool, negação, erro ou tentativa sem
  resultado bloqueia a execução e não pode ser substituída silenciosamente por inspeção manual
  apresentada como APEX.
- **Reason**: Um piloto read-only no Claude Code 2.1.220 contra `repos/portal-api` leu com sucesso
  `apex://framework/workflows/eng-ready`, mas não recebeu o bloco `=== APEX WORKSPACE ===` e não
  encontrou a tool `preflight` exigida pelo próprio workflow. Duas chamadas diagnósticas também
  foram negadas pelo modo não interativo. Assim, a rota nativa reproduziu a mesma lacuna contratual
  observada no Codex e não concluiu Step 1.
- **Trade-off**: A presença de `ENV.md`, `AGENTS.md`, do servidor MCP e do resource deixa de bastar
  para declarar readiness, e workflows com version skew param cedo. Em troca, o workspace não
  confunde descoberta, tentativa ou fallback com execução e ganha um critério objetivo de
  revalidação end-to-end.
- **Alternatives considered**: Considerar a leitura do resource como execução; conceder aprovação e
  ignorar a tool ausente; reproduzir `preflight` manualmente com Glob/Read; retirar imediatamente a
  escolha de APEX no Claude para todos os workflows.
- **Scope**: Declarações de execução APEX neste workspace, nos dois engines. Não altera o servidor
  APEX, os repositórios de produto, Linear ou GitHub; AD-026 continua escolhendo o executor, mas a
  execução deve falhar fechada quando o contrato do workflow não estiver disponível.
- **Date**: 2026-08-02
- **Status**: active

### AD-035
- **Decision**: Centralizar o estado local do OMC para sessões Claude iniciadas nesta raiz em
  `session-context/runtime/omc/`, configurando o caminho absoluto por `OMC_STATE_DIR` no arquivo
  ignorado `.claude/settings.local.json`. Tratar o diretório como runtime efêmero, não canônico e
  elegível para limpeza somente depois de encerradas as sessões que possam depender dele.
- **Reason**: Duas sessões Claude reais mudaram de `cwd` durante a execução e hooks do OMC criaram
  `.omc/` em `repos/assistants` e no diretório agregador `repos/`. `session-context/` já é a
  superfície local ignorada pelo Git; um state root absoluto mantém a resolução estável e evita
  contaminar worktrees de produto sem transformar runtime em artifact durável.
- **Trade-off**: A configuração real é específica desta máquina e não acompanha o Git; uma cópia do
  workspace em outro caminho precisa configurar seu próprio valor local. Em troca, os repos de
  produto permanecem limpos e o estado continua disponível para retomada na máquina atual.
- **Alternatives considered**: Usar `~/.claude/omc`; manter `.omc/` por repo e apenas ignorá-lo;
  criar um marker `.omc-workspace`; calcular a variável em `SessionStart`; armazenar em `/tmp`.
- **Scope**: Runtime local do Claude/OMC iniciado nesta raiz. Não altera AD-031, o lifecycle oficial
  do APEX, repos de produto ou fontes canônicas; não autoriza persistir credenciais, dados de
  clientes, saídas de produção ou transcripts em `session-context/`.
- **Date**: 2026-08-02
- **Status**: active

### AD-036
- **Decision**: Para entregas Portal executadas por Codex + TLC, persistir checkpoints locais em
  `session-context/portal/<INV-ID>/tlc/STATE.md` com
  `scripts/update-tlc-checkpoint.py` depois de gate, commit, bundle, criação ou atualização de PR e
  mudança de validation concluídos com sucesso; atualizar somente `## Handoff` e não avançar estado
  quando a transição correspondente falhar.
- **Reason**: O histórico de outra máquina para INV-3145 passou de quatro para oito arquivos de
  sessão, e as quatro continuations adicionais caíram após teste focal, revisão, suíte completa e
  espera de CI. Como a duração variou de cerca de 30 minutos a 7h38, carga da máquina não explica
  sozinha a perda de continuidade; o handoff restrito a pausa consciente deixa uma janela evitável.
- **Trade-off**: O checkpoint reduz a reconstrução ao trabalho posterior à última transição estável,
  mas continua efêmero, single-writer, local à máquina e sem portabilidade cross-machine. Processos
  registrados podem estar stale e devem ter sua liveness revalidada na retomada.
- **Alternatives considered**: Manter handoff apenas em pausas conscientes; tentar escrever somente
  em um hook de queda; versionar checkpoints no Git; usar Linear ou a PR como log operacional fino;
  modificar a TLC vendorizada para todos os produtos.
- **Scope**: Somente Portal + Codex + TLC durante a rota transitória da AD-031. Preserva AD-031,
  AD-032, Claude/APEX, repos de produto, fontes canônicas e a TLC vendorizada; mantém a privacidade
  da AD-027 e o lifecycle de limpeza após merge e encerramento da issue.
- **Date**: 2026-08-02
- **Status**: superseded by AD-045

### AD-037
- **Decision**: Versionar o GitHub MCP remoto oficial nos dois engines desta raiz, autenticado em
  runtime exclusivamente por `GITHUB_PAT_TOKEN`, limitado aos toolsets
  `pull_requests,repos,actions,git` e fechado para escrita por `X-MCP-Readonly: true`; no Codex,
  preservar também `default_tools_approval_mode = "writes"` como defesa adicional. Usar essa
  superfície somente como evidência de PR, commits, reviews, checks e histórico pós-merge, mantendo
  Linear canônico para issues e cada repositório canônico para código e testes.
- **Reason**: A retrospectiva encontrou 21 PRs revisadas e mostrou que o espelho de diffs do Linear
  preserva parte das threads, mas não cobre de modo suficiente buscas de commits, checks, reviews e
  correções posteriores. O `gh` funciona fora do sandbox mediante aprovação explícita, mas não
  fornece por si só uma superfície MCP reproduzível para os dois engines; APEX expõe apenas
  operações GitHub pontuais. Um MCP GitHub read-only preenche a lacuna sem conceder escrita.
- **Trade-off**: Cada máquina precisa fornecer um PAT local de menor privilégio e reiniciar o engine;
  ausência, expiração ou escopo insuficiente da variável bloqueia consultas privadas. A superfície
  adiciona ferramentas e dependência do serviço remoto, mas exclui comentários, approvals, merges
  e outras mutações por desenho.
- **Alternatives considered**: Reautenticar e depender apenas do `gh`; continuar usando o espelho de
  diffs do Linear; ampliar o APEX; usar somente o Code Review do Codex Cloud; instalar o servidor
  local por Docker; habilitar todos os toolsets ou ferramentas de escrita do GitHub MCP.
- **Scope**: Evidência read-only de GitHub em sessões Codex e Claude iniciadas por esta raiz. Não
  transfere ownership, não altera GitHub, Linear ou repos de produto e não autoriza persistir tokens
  em arquivos versionados, transcripts ou chat.
- **Date**: 2026-08-07
- **Status**: active

### AD-038
- **Decision**: Adotar `review-pull-request` como piloto read-only dedicado à revisão e re-revisão de
  PRs existentes, especialmente trabalho de outro dev, sempre ligado ao base SHA, head SHA, issue/DoD,
  checks e validações realmente observados. Exigir findings comportamentais no formato
  evidência-impacto-condição, revalidar o head antes do parecer e classificar outcomes como decididos,
  indeterminados ou sem escape confirmado. No Linear, ler a issue-alvo uma vez por review e expandir
  parents, relations ou ancestry somente com uma razão capaz de alterar o parecer, reutilizando o
  contexto em re-review quando o `updatedAt` não mudar. Aplicar a mesma economia por snapshot em
  triage e continuidade; manter ancestry completa nas skills de task somente quando elas forem
  acionadas para preparação formal, não como entrada padrão de PR review. Avaliar 5–10 reviews reais
  com o novo contrato antes de promovê-lo a regra transversal consolidada.
- **Reason**: A retrospectiva encontrou 21 PRs e uso inconsistente de metadados, checks e diffs. Uma
  baseline GitHub de 10 PRs merged (`portal-api` #268–#272, #274, #277 e #280; `portal-web` #224 e
  #226) encontrou somente 2 PRs com threads persistidas: 7 findings, dos quais 5 tinham severidade
  explícita. Os patches corretivos, testes/checks finais e aprovação posterior sustentam 7/7 como
  `accepted-fixed` e 0/7 como falso positivo decidido; nas outras 8 PRs, aprovação sem threads não
  permite reconstruir findings ausentes. A busca posterior por IDs rastreáveis encontrou 0 escapes
  confirmados até 2026-08-07, mas as janelas de 0–11 dias e a ausência de vínculo não provam zero
  defeitos escapados. No recorte de sessões, 24 das 41 reviews estreitas consultaram Linear e fizeram
  215 leituras de issue — quase 9 por sessão que usou Linear — sem que toda review precisasse de
  ancestry completa; isso justificou separar contrato mínimo da issue de preparação integral da task.
- **Trade-off**: A revisão ganha coleta de identidade, contexto e uma revalidação final, e métricas
  podem permanecer indeterminadas quando o GitHub não preserva a decisão. A expansão progressiva do
  Linear exige julgamento e pode ainda chegar à ancestry completa; em troca, evita leituras repetidas
  ou irrelevantes sem sacrificar DoDs herdados. O workflow também deixa de tratar aprovação, thread
  resolvida, check verde ou ausência de fix posterior como proxies de qualidade. O piloto ainda não
  demonstra ganho causal e precisa de uso prospectivo antes de ampliar a política.
- **Alternatives considered**: Embutir review na TLC; ampliar as skills de contexto de produto;
  considerar `apex-eng-review` executável no Codex; usar `create-review-bundle` em toda PR; medir
  apenas approvals e threads resolvidas; publicar automaticamente findings no GitHub.
- **Scope**: Reviews read-only feitas neste workspace. Não implementa correções, não modifica
  produto, Linear ou GitHub, não substitui validação do executor e não transforma métricas do piloto
  em fonte canônica de produto.
- **Date**: 2026-08-07
- **Status**: active

### AD-039
- **Decision**: Endurecer o piloto `review-pull-request` revalidando base e head SHA antes do
  parecer, tornando verdicts bloqueantes determinísticos para findings P0–P2 não resolvidos e
  persistindo somente metadados de outcome em um ledger JSONL de schema fechado sob
  `session-context/review-pilot/`. O ledger é local, ignorado, efêmero e não canônico; deve ser
  produzido e agregado por `scripts/pr-review-pilot.py`, sem prosa, comentários, diffs, código,
  credenciais, dados de clientes, saída de produção ou transcripts. Consolidar a validação da raiz
  em `scripts/test-workspace.sh` e exigir snapshots Linear com retrieval time e `updatedAt` para
  qualquer reutilização entre workflows, refrescando quando um input ou evento relevante mudar.
- **Reason**: A auditoria posterior à AD-038 encontrou que as métricas prospectivas estavam apenas
  descritas, sem mecanismo reproduzível de coleta; que mudança da base podia tornar o diff stale sem
  alterar o head; que os testes protegiam texto, mas não outcomes; e que a validação completa exigia
  treze comandos manuais. O schema fechado permite medir o piloto sem transformar chat ou conteúdo
  de review em uma nova fonte de dados.
- **Trade-off**: Cada review ganha uma escrita local sanitizada e o gate completo fica mais longo;
  em troca, as 5–10 reviews podem ser agregadas de forma comparável e regressões de contrato passam
  a ter testes comportamentais. O ledger continua single-machine e não prova outcomes ausentes; a
  materialização local de heads remotos permanece adiada até o piloto medir sua necessidade real.
- **Alternatives considered**: Depender do histórico das sessões; versionar resultados do piloto;
  registrar texto completo dos findings; publicar métricas no Linear ou GitHub; materializar todo
  head remoto antecipadamente; manter apenas testes estáticos e comandos de gate separados.
- **Scope**: Workflow e evidência local de review desta raiz. Não modifica GitHub, Linear, repos de
  produto, branches ou worktrees e não promove AD-038 a regra transversal antes do piloto real.
- **Date**: 2026-08-07
- **Status**: active

### AD-040
- **Decision**: Aplicar os validadores determinísticos da TLC de forma prospectiva a artefatos
  criados ou materialmente revisados sob a TLC 3.3.0; executar o gate aplicável antes de confirmar
  spec, aprovar tasks, criar commit ou encerrar validation, e fazer o gate da raiz usar fixtures
  comportamentais isoladas. Não varrer nem revalidar retroativamente o arquivo histórico de specs.
- **Reason**: O upstream 3.3.0 introduziu gates reproduzíveis, mas seus parsers originais não
  reconheciam todos os formatos Markdown já usados neste workspace e não possuíam cobertura
  comportamental suficiente. O hardening local validou caminhos positivos e negativos sem impor a
  documentos antigos um contrato inexistente quando foram produzidos.
- **Trade-off**: Transições novas ganham comandos explícitos e testes adicionais, enquanto o acervo
  histórico permanece heterogêneo e não recebe certificação retroativa. Em troca, novas regressões
  falham de forma determinística sem uma migração ampla e arriscada do passado.
- **Alternatives considered**: Reescrever e validar todo o histórico; importar 3.3.0 sem hardening;
  manter os novos scripts disponíveis mas opcionais; incorporar um sweep global ao gate da raiz.
- **Scope**: Artifacts TLC deste workspace criados ou materialmente revisados sob 3.3.0. Não altera
  fontes canônicas de produto, contratos IDS, o roteamento por engine da AD-026 nem artifacts
  históricos que não sejam revisados.
- **Date**: 2026-08-08
- **Status**: active

### AD-041
- **Decision**: Evoluir `scripts/audit-session-history.py` para um contrato v2 aditivo, preservar
  todos os outcomes APEX existentes, medir concentração de abortos e compactações em sessões
  primárias deduplicadas e fechar cohorts por janela UTC semiaberta `[since, until)`. Persistir
  somente agregados sanitizados em um piloto que termina após dez sessões primárias elegíveis ou a
  próxima feature longa, antes de propor nova automação operacional.
- **Reason**: AD-036 comprovou interrupções e reconstrução de contexto em entregas reais, mas o
  auditor anterior não separava frequência total de concentração nem congelava um baseline contra
  sessões futuras. O EDREN validou esses dois controles sem precisar persistir transcripts.
- **Trade-off**: O relatório ganha campos, versão e limites temporais que exigem manutenção de
  fixtures, enquanto histories locais ainda podem receber backfill dentro da janela fechada. Em
  troca, retrospectivas tornam drift da fonte explícito e decisões de automação passam a depender
  de evidência delimitada sem perder o diagnóstico APEX existente.
- **Alternatives considered**: Copiar integralmente o auditor do EDREN e perder detalhes APEX;
  manter cohorts abertos; propor imediatamente um runner; persistir IDs ou paths para facilitar
  reconciliação manual.
- **Scope**: Retrospectivas e resiliência de sessão deste workspace. Não altera histories locais,
  engines, repositórios de produto, Linear, GitHub, APEX nem a rota Portal + Codex + TLC da AD-036.
- **Date**: 2026-08-08
- **Status**: active

### AD-042
- **Decision**: Tratar `repos/inventeer-ops` como o único repo documental compartilhado do tenant,
  preservar IDS e Portal como projetos lógicos e resolver seus contextos respectivamente em
  `artifacts/products/ids/` e `artifacts/products/portal/`; manter `portal-api` e `portal-web` como
  repos canônicos de implementação e preservar os plugins movidos dentro de suas subárvores.
- **Reason**: INV-3713 arquivou os spokes documentais e consolidou seus conteúdos no repo de
  operações. Paths literais para `repos/ids` e `repos/portal` agora apontam para clones congelados e
  podem bloquear preparação ou carregar contratos obsoletos.
- **Trade-off**: Contexto de produtos diferentes compartilha um worktree e exige paths mais longos,
  leitura do contexto raiz e escopo de escrita explícito. Em troca, Git roots, autoridade documental
  e ownership de implementação permanecem inequívocos sem aliases de compatibilidade.
- **Alternatives considered**: Manter clones arquivados; criar symlinks `repos/ids` e `repos/portal`;
  copiar os artifacts necessários para skills ou repos de código; remover os projetos lógicos do
  registry.
- **Scope**: Registry, setup local, discovery, preparação de tasks Assistants e Portal e consumo
  read-only de IDS neste workspace. Não autoriza alterar `inventeer-ops`, contratos IDS ou repos de
  produto sem escopo próprio.
- **Date**: 2026-08-10
- **Status**: active

### AD-043
- **Decision**: Versionar o MCP remoto oficial do Figma nos dois engines desta raiz, autenticado
  somente por OAuth em runtime e com ferramentas de escrita sujeitas à aprovação do engine no
  Codex. Usá-lo para contexto estruturado, variáveis, assets e screenshots dos arquivos Figma aos
  quais o usuário concedeu acesso, sem persistir tokens no workspace.
- **Reason**: O trabalho de interface precisa consultar frames e variantes exatos do Figma em vez de
  depender apenas de screenshots ou transcrição manual do design, e o workspace já opera integrações
  MCP reproduzíveis nos dois engines.
- **Trade-off**: Cada engine ou máquina pode exigir autenticação e refresh próprios, e a configuração
  adiciona ferramentas externas à sessão. Em troca, o handoff de design fica estruturado e
  verificável sem armazenar credenciais ou copiar o arquivo Figma para o Git.
- **Alternatives considered**: Configurar apenas o Codex; usar links e screenshots sem MCP; manter o
  servidor global; persistir token pessoal em variável ou arquivo versionado.
- **Scope**: Sessões Codex e Claude iniciadas por esta raiz. A integração não transfere ownership,
  não autoriza mudanças em arquivos Figma ou repos de produto e não substitui as fontes canônicas
  de código, testes ou documentação.
- **Date**: 2026-08-11
- **Status**: active

### AD-044
- **Decision**: Encerrar o piloto delimitado da AD-041 e autorizar roteamento de contexto,
  guardrail staged, checkpoint `pre-heavy` e evidência recuperável do gate somente ao workspace
  raiz e à rota Portal + Codex + TLC já delimitada.
- **Reason**: O gatilho da próxima feature longa foi concluído, o cohort final registrou 34 sessões
  Codex e 4 Claude primárias, e 13 continuations confirmaram reconstrução recorrente. As taxas de
  aborto e compactação melhoraram, mas as demais metas não foram medidas prospectivamente e não
  podem ser inferidas pelo auditor sanitizado.
- **Trade-off**: O workspace ganha automações locais pequenas e verificáveis, mas mantém recibos e
  checkpoints efêmeros, opt-in e ligados ao estado exato. O fechamento não autoriza automação nos
  repositórios de produto nem substitui validação terminal fresca.
- **Alternatives considered**: Manter o piloto aberto apesar do gatilho; copiar o workflow completo
  do EDREN; ampliar imediatamente o runner aos repos de produto; rejeitar toda automação por falta
  das métricas prospectivas.
- **Scope**: Navegação, segurança staged, continuidade Portal + Codex + TLC e gate agregado desta
  raiz. Preserva AD-024, AD-026, AD-031, AD-036, fontes canônicas e ownership dos repos em `repos/`.
- **Date**: 2026-08-12
- **Status**: superseded by AD-045

### AD-045
- **Decision**: Usar `tlc-spec-driven` como executor de especificação, implementação e validação
  tanto no Codex quanto no Claude Code. Para tasks do Portal nos dois engines, manter artifacts TLC,
  bundles e checkpoints sob `session-context/portal/<INV-ID>/`, preservando APEX apenas como
  superfície experimental e diagnóstica até uma nova decisão baseada em execução end-to-end que
  satisfaça AD-034.
- **Reason**: O recorte sanitizado de 2026-07-28 a 2026-08-18, contrato v2 e com a retrospectiva
  corrente excluída, contém 30 sessões primárias Codex e 5 Claude. Duas sessões Codex e uma Claude
  tiveram tools APEX bem-sucedidas, mas somente como operações isoladas; o histórico e o piloto
  nativo da AD-034 não demonstram um workflow completo com contexto, todas as tools e gates
  estruturados. A rota TLC do Portal já possui artifacts locais, checkpoints e gates testados.
- **Trade-off**: O workspace abre mão do lifecycle oficial APEX no Claude e passa a manter artifacts
  TLC efêmeros também nesse engine. Em troca, as duas engines seguem o mesmo contrato de construção,
  revisão e continuação. O layout é reproduzível em outra máquina, mas seu conteúdo não sincroniza:
  retomadas cross-machine reconstroem o estado de Linear, Git, PRs e fontes canônicas ou consomem um
  pacote temporário sanitizado transferido explicitamente.
- **Alternatives considered**: Manter o roteamento por engine da AD-026; retirar o APEX somente do
  Claude; sincronizar `session-context/` por Git; remover o MCP APEX e os wrappers; aguardar outra
  execução sem consolidar o fluxo já praticado.
- **Scope**: Executor de entrega nos dois engines e continuidade de tasks do Portal neste workspace.
  Substitui AD-026, AD-031, AD-036 e AD-044, preservando suas automações de raiz e estendendo a rota
  Portal + TLC ao Claude. Não altera produtos, Linear, GitHub, repos em `repos/`, fontes canônicas,
  a TLC vendorizada ou o critério de revalidação APEX da AD-034.
- **Date**: 2026-08-17
- **Status**: active

### AD-046
- **Decision**: Vincular retrospectivas a receipts sanitizados do contrato v3 e Handoffs
  versionados a um SHA comportamental, estado de publicação e allowlist de evidência; separar
  `Contract status` de `Operational status` e manter ações transitórias fora do estado durável.
- **Reason**: O contrato anterior misturava instâncias físicas, continuations e fluxos lógicos,
  contava exclusões solicitadas como aplicadas e não permitia reproduzir a proveniência entre
  máquinas. O Handoff também reteve uma instrução de push depois que os commits já estavam
  publicados, enquanto apontar literalmente para o commit que contém o próprio Handoff criaria uma
  autorreferência impossível.
- **Trade-off**: O auditor v3 quebra consumidores dos nomes ambíguos e o Handoff ganha schema,
  helper e consulta obrigatórios. Em troca, cohorts ficam portáteis e verificáveis, descendants
  documentais de fechamento não invalidam o SHA comportamental e ausência de upstream ou schema
  válido deixa de ser confundida com freshness.
- **Alternatives considered**: Preservar aliases v2; persistir cwd e IDs para reconciliação;
  comparar apenas com `HEAD`; deixar freshness como disciplina textual; registrar push ou PR no
  Handoff; representar contrato e operação com um único PASS.
- **Scope**: Retrospectivas, relatórios de validação materialmente revisados e Handoff versionado
  desta raiz. Não altera histories, repositórios em `repos/`, fontes canônicas de produto, Linear,
  GitHub ou artifacts efêmeros de Portal.
- **Date**: 2026-08-18
- **Status**: active

## Handoff
- **Feature**: Retrospective Evidence Freshness
- **Phase / Task**: Validation complete
- **Completed**: auditor contract v3 and portable receipt, freshness-aware Handoff, dual validation verdicts, 25-suite root gate and 3/3 killed mutants
- **In progress**: none
- **Next durable step**: Start the Value Increment workflow improvement
- **Blockers**: none
- **Uncommitted files**: .specs/LESSONS.md, .specs/lessons.json
- **Branch**: main
- **Contract status**: PASS
- **Operational status**: PASS
- **Recorded at**: 2026-08-19T02:10:30Z
- **Valid at SHA**: 653de07cc9900154543aae73b58e77a4d0de9fb0
- **Publication state**: unpublished
- **Evidence-only paths**: .specs/STATE.md, .specs/features/INDEX.md, .specs/features/retrospective-evidence-freshness/spec.md, .specs/features/retrospective-evidence-freshness/validation.md
- **Invalidated by**: behavioral SHA ancestry break; non-evidence descendant; publication state change
