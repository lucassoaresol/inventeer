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

## Handoff

- **Feature**: Sincronização segura dos repositórios locais
- **Phase / Task**: Implementação, validação e commit — concluídos
- **Completed**: script Linux para atualizar clones por fast-forward, seleção genérica de `develop`, troca segura de branch em worktrees limpos, preservação de alterações locais, exclusão temporária de `inventeer-hub`, documentação no README e integração como primeira etapa das skills de Portal e Assistants
- **In-progress**: none
- **Next step**: executar uma skill de contexto em uma task real e confirmar o preflight de atualização
- **Blockers**: none
- **Uncommitted files**: none
- **Branch**: main
