# Inventeer Engineering Workspace

Workspace pessoal de engenharia para trabalhar com projetos da Inventeer usando Codex e Claude Code.

Este repositório mantém skills reutilizáveis e pontos de entrada dos projetos. O código dos
produtos fica em repositórios Git independentes sob `repos/`, que é ignorado por este repositório.

As decisões que definem este workspace e seus trade-offs ficam em [`.specs/STATE.md`](.specs/STATE.md).
Esse arquivo registra memória do workspace; specs de produto permanecem nos respectivos repos.

## Estrutura

```text
.
├── .agents/skills/        Skills versionadas; fonte única para os dois engines
├── .claude/skills/        Symlinks para .agents/skills/, porque o Claude não lê .agents/
├── AGENTS.md              Instruções do workspace; CLAUDE.md apenas as importa
├── .specs/STATE.md        Decisões e handoff deste workspace
├── projects/              Pontos de entrada versionados dos projetos
├── scripts/               Automações locais do workspace
├── session-context/       Documentos efêmeros para a sessão (ignorado pelo Git)
└── repos/                 Clones locais independentes (ignorado pelo Git)
```

## Contexto efêmero de sessão

Use `session-context/` para disponibilizar documentos auxiliares que o Codex precise ler durante
uma task, mas que não devam fazer parte do histórico do workspace nem dos repositórios de produto.
O diretório inteiro é ignorado pelo Git; ele pode conter arquivos e subdiretórios organizados por
issue, por exemplo `session-context/INV-1234/`.

Esse local é apenas uma entrada temporária de contexto. Apague seu conteúdo quando ele deixar de
ser necessário e não coloque nele credenciais, dados de clientes ou saídas de produção. Decisões,
specs e evidências que precisem persistir continuam pertencendo às respectivas fontes canônicas.

### Estado transitório do Claude/OMC

Sessões Claude iniciadas na raiz deste workspace centralizam o estado do OMC em
`session-context/runtime/omc/`. A configuração local e específica da máquina fica no campo
`env.OMC_STATE_DIR` de `.claude/settings.local.json`, com caminho absoluto, para que mudanças de
`cwd` não criem `.omc/` em `repos/` nem nos worktrees de produto. O OMC acrescenta seu identificador
de projeto e o escopo da sessão abaixo desse diretório-base.

Esse estado é efêmero, ignorado pelo Git, não canônico e não deve conter credenciais, dados de
clientes, saídas de produção ou transcripts. Remova-o somente depois de encerrar as sessões que
possam depender dele. A regra é transversal ao runtime local do Claude e não altera o contrato
Portal + Codex + TLC da AD-031.

### Artifacts TLC transitórios do Portal

Enquanto o Codex não executar o workflow APEX completo, tasks do Portal entregues por Codex + TLC
guardam somente os artifacts file-backed internos da TLC em
`session-context/portal/<INV-ID>/tlc/`. Eles apoiam execução, retomada local e review, mas não são
canônicos, oficiais nem duráveis e nunca devem ser promovidos como `.specs/` de `portal`,
`portal-api` ou `portal-web`.

Agrupe bundles e checksums em `session-context/portal/<INV-ID>/review/`. Código, testes, ADRs e
documentação oficial permanecem nos repos de produto; Linear e a PR preservam o resumo oficial da
entrega. Após merge e encerramento da issue, o diretório local fica elegível para limpeza. A rota é
um piloto transitório exclusivo do Portal no Codex; Claude/APEX e outros produtos permanecem
inalterados, e o lifecycle oficial do APEX a substituirá quando houver suporte end-to-end no Codex.

## Skills

| Skill | Origem | Versão | Uso |
|---|---|---:|---|
| `tlc-spec-driven` | Tech Lead's Club | 3.2.0 | Especificar, projetar, implementar e verificar mudanças |
| `assistants-task-context` | Local | — | Preparar tasks do produto Assistants para desenvolvimento |
| `portal-task-context` | Local | — | Preparar tasks do Portal e determinar ownership entre produto, API e web |
| `triage-project-cycle` | Local | — | Comparar várias issues, dependências, conflitos e ordem de execução |
| `advance-delivery-front` | Local | — | Coordenar a próxima task e a maturidade da evidência enquanto PRs aguardam |
| `discover-project-context` | Local | — | Descobrir projetos e fluxos sem exigir uma issue Linear |
| `create-review-bundle` | Local | — | Gerar ZIP de review com proveniência, diffs e lineage opcional |
| `apex-*` (28) | Gerado | — | Inspecionar workflows APEX no Codex; superfície experimental, não executor |

As skills necessárias estão versionadas em `.agents/skills/`; não dependem de uma instalação
global. A `tlc-spec-driven` é um fork local vendorizado e deve ser atualizada separadamente das
skills locais. Sua origem, base upstream e personalizações conhecidas ficam em
`.agents/vendor.json`. As políticas específicas de produto continuam nas skills de contexto; as
melhorias genéricas do workflow podem permanecer no fork local da TLC.

Para verificar se há diferença em relação à branch oficial, sem alterar arquivos:

```bash
./scripts/update-vendored-skill.sh --check main
```

O check mostra separadamente as personalizações locais (`base → local`) e as mudanças oficiais
(`base → incoming`). Depois de revisar os dois lados, execute o merge:

```bash
./scripts/update-vendored-skill.sh --merge <ref>
```

O modo `--merge` exige worktree limpo, aplica o novo upstream e reaplica as personalizações como um
patch de três vias. Se houver conflito, ele mantém os marcadores para resolução humana e não avança a
base do manifesto. Depois de resolver e validar, finalize com:

```bash
./scripts/update-vendored-skill.sh --accept <ref>
```

O script não cria commits nem interage com forks ou pull requests. Tanto a personalização quanto
cada merge de upstream devem ser revisados e commitados isoladamente neste workspace.

### Roteamento por intenção

Use uma rota de contexto antes da TLC:

| Intenção | Skill inicial | Handoff |
|---|---|---|
| Comparar ciclo, backlog ou várias issues | `triage-project-cycle` | Skill de task do produto após selecionar uma issue |
| Continuar o ciclo enquanto uma PR aguarda review ou merge | `advance-delivery-front` | Contrato read-only com uma próxima ação; skill de task do produto para a issue selecionada |
| Entender projeto ou fluxo sem issue | `discover-project-context` | Criar/clarificar issue antes de implementar |
| Preparar uma issue Assistants | `assistants-task-context` | Codex: TLC; Claude: APEX se houver `ENV.md`, senão TLC |
| Preparar uma issue Portal | `portal-task-context` | Codex: TLC; Claude: APEX se houver `ENV.md`, senão TLC |
| Empacotar trabalho para review | `create-review-bundle` | Review externo; não implica aprovação |

`advance-delivery-front` mantém a topologia da PR pronta e da próxima task ativa/draft, classifica
dependências, separa maturidade de implementação e validação e planeja a reconciliação pós-merge.
Seu MVP não cria branches, altera PRs ou atualiza o Linear; ele entrega um contrato verificável e
exatamente uma próxima ação antes do handoff para a skill de task do produto e, quando necessário,
para `tlc-spec-driven`.

No handoff Portal para TLC no Codex, substitua a raiz file-backed padrão da TLC pelo diretório local
`session-context/portal/<INV-ID>/tlc/`; essa substituição não altera a skill TLC genérica nem cria
uma spec oficial de produto.

Para gerar um bundle diretamente:

```bash
.agents/skills/create-review-bundle/scripts/create-review-bundle.sh \
  --repo repos/portal-api \
  --base origin/develop \
  --output-dir session-context \
  --label INV-0000 \
  --review-stage initial
```

O ZIP inclui manifesto, lineage, status, commits, checksum e um diff por arquivo. Gerações
corretivas podem usar `--parent-bundle <bundle-anterior.zip>` para registrar o checksum do parent e o
delta de paths. A base padrão é `HEAD`, adequada para revisar apenas mudanças não commitadas.
Caminhos prováveis de credenciais, chaves ou dumps são recusados.

## Engines

O workspace é operado por Codex e por Claude Code sobre a mesma fonte de skills (AD-024). Cada
engine enxergava metade do conjunto, e a diferença é coberta por arquivo:

| | Codex | Claude Code |
|---|---|---|
| Instruções | `AGENTS.md` nativo | `CLAUDE.md`, que importa `AGENTS.md` |
| Skills | `.agents/skills/` nativo | symlinks em `.claude/skills/` |
| MCPs versionados | `apex`, `linear`, `context7` em `.codex/config.toml` | `apex`, `context7` em `.mcp.json` |
| Workflows APEX | wrappers experimentais `apex-*` | comandos nativos do MCP |

Uma skill global de mesmo nome em `~/.claude/skills/` suprime a deste workspace sem aviso, e as
`description` podem ser idênticas. Se uma skill parecer desatualizada no Claude Code, verifique
essa colisão antes de editar arquivos.

## MCPs do workspace

`Context7` é compartilhado pelos dois engines para documentação atual e version-specific das
bibliotecas usadas pelos projetos. Ele usa um servidor stdio por `npx` sem credencial versionada. Na
cadeia de conhecimento da TLC, código e documentação local continuam tendo precedência; o MCP é
consulta externa posterior, não fonte canônica de produto.

`shadcn` pertence ao `portal-web` e também está disponível nos dois engines iniciados por esta raiz.
O servidor shadcn opera com cwd em `repos/portal-web`, onde o `components.json` define registries,
aliases e destinos de instalação. Por isso, o clone desse repo é pré-requisito para iniciar o
servidor. Ferramentas de escrita do shadcn exigem aprovação e só podem ser usadas depois de ler as
instruções locais e verificar o worktree do produto; a configuração na raiz não transfere ownership.

Os candidatos de infraestrutura permanecem fora desta raiz por limites de necessidade e autoridade:

- Cloudflare Docs não tem uso durável durante a migração do Portal para AWS.
- Um MCP AWS só deve ser escolhido quando a migração estiver representada na fonte canônica e houver
  um contrato explícito de autenticação e autoridade; Context7 cobre consultas de biblioteca sem
  antecipar acesso à conta ou mutações de infraestrutura.

Alterações de configuração exigem reiniciar o engine. No Claude Code, aprove o `.mcp.json` do projeto
e confirme em `/mcp`; no Codex, confirme o servidor ativo após reiniciar a sessão pela raiz confiável.

## Preflight de recursos

Antes de suíte completa, build, containers, navegador, mutation testing ou agentes em paralelo,
execute `./scripts/check-machine-resources.sh`. O snapshot informa CPUs, carga, memória disponível,
swap e disco do workspace. Use-o para limitar concorrência ou definir shards completos; limitação da
máquina muda o agendamento, nunca a cobertura exigida pelo gate.

## Workflows do APEX

O Claude Code recebe os workflows do APEX nativamente, como comandos do servidor MCP, e é hoje a
única engine deste workspace que usa APEX como executor de entrega. O Codex consome tools e
resources, mas as sessões reais mostraram que isso não fornece por si só invocação, contexto de
sessão, artifacts e gates completos. Portanto, entregas no Codex usam TLC, inclusive em repos com
`ENV.md` (AD-026).

A rota nativa também falha fechada quando o resource do workflow e a superfície de tools divergem.
O piloto read-only de 2026-08-02 leu `eng-ready` no Claude, mas não conseguiu executá-lo: o workflow
exige `preflight`, a tool não foi publicada e o bloco `=== APEX WORKSPACE ===` não chegou à sessão.
Uma chamada negada, com erro ou sem resultado não é execução APEX. Consulte o
[piloto sanitizado](.specs/features/apex-safety-session-audit/apex-native-pilot.md) e AD-034.

A superfície Codex também expõe operações mutáveis de Git, GitHub, Linear e coordenação multi-repo.
Essas ferramentas exigem aprovação pelo modo `writes`; leituras diagnósticas permanecem disponíveis,
e a presença das operações não amplia ownership nem transforma o MCP em executor suportado.

Os wrappers em `.agents/skills/apex-<id>/` preservam uma superfície experimental para inspeção e
diagnóstico no Codex. Eles não são expostos ao Claude e não devem ser tratados como execução APEX
suportada.

Os wrappers não copiam o corpo dos workflows: cada um aponta para
`apex://framework/workflows/<id>`, mantendo o APEX como fonte canônica. São conteúdo derivado — não
edite.

Para regenerar, o agente obtém o catálogo pela tool `apex_framework_index` e o entrega ao script:

```bash
./scripts/sync-apex-commands.sh --print-contract
./scripts/sync-apex-commands.sh --check --catalog <catalogo.json>
./scripts/sync-apex-commands.sh --apply --catalog <catalogo.json>
```

O `--check` relata criações, atualizações e remoções sem escrever, e sai 1 quando há divergência.
São aceitos os workflows com `description` não vazia e não depreciados — hoje 28 dos 30, excluindo
`README` e `warm-up` (ADR 0032). O contrato de aquisição proíbe ler `apex://framework/runtime`
diretamente, arquivos de credencial do host ou o gateway por HTTP, porque nenhuma dessas rotas é
reproduzível nos dois engines.

Valide o script com `./scripts/test-sync-apex-commands.sh`.

## Aprendizados de sessão

Retrospectivas de skills usam os históricos locais das duas engines associados a esta raiz:
`~/.codex/sessions/` e o projeto correspondente em `~/.claude/projects/`. Sessions retomadas,
sidechains e cópias não contam automaticamente como evidências independentes, e a sessão que faz a
retrospectiva é excluída do recorte.

Os transcripts são evidência efêmera e não são copiados para o repositório. O resultado destilado
segue três destinos: decisões transversais em `.specs/STATE.md`; falhas de execução confirmadas por
validação no mecanismo de lessons da TLC; e achados específicos de produto no repositório ou fonte
canônica do produto. Consulte AD-027.

Use o inventário sanitizado antes da análise qualitativa:

```bash
./scripts/audit-session-history.py \
  --cwd "$PWD" \
  --since 2026-07-29 \
  --exclude-session <ID-DA-SESSAO-CORRENTE>
```

O relatório contém somente contagens agregadas: sessões principais, continuations, subagents ou
sidechains, trabalhos lógicos, tentativas APEX e seus outcomes estruturados.
`apex_tool_successes` contém somente tools com resultado bem-sucedido; falhas, negações e tentativas
sem resultado ficam separadas em `apex_tool_failures`, `apex_tool_denials` e
`apex_tool_unresolved`. Esses campos não afirmam que um workflow APEX terminou. O relatório não
emite prompts, respostas, resultados de tools, caminhos dos histories nem corpos de transcript. O
vínculo de continuation no Codex é uma heurística conservadora: UUID referenciado junto de `caiu` e
`continue`; no Claude, o primeiro `cwd` não vazio define a origem da sessão e apenas sidechains
estruturadas são deduplicadas automaticamente.

## Repositórios locais

Clone os projetos dentro de `repos/`, preservando o nome do repositório remoto:

```bash
git clone <assistants-url> repos/assistants
git clone <ids-url> repos/ids
git clone <inv-cortex-url> repos/inv-cortex
git clone <portal-url> repos/portal
git clone <portal-api-url> repos/portal-api
git clone <portal-web-url> repos/portal-web
```

Clone `inventeer-hub` somente quando o acesso estiver provisionado, pois suas políticas de acesso
ainda estão em definição.

Cada diretório em `repos/` mantém seu próprio histórico Git. Consulte o
[registro de projetos](projects/README.md) para localizar fontes canônicas, relações entre repos e
instruções antes de trabalhar em um produto.

Para atualizar todos os clones no Linux:

```bash
./scripts/update-repos.sh
```

O script usa `develop` quando essa branch existe localmente; caso contrário, usa a branch padrão
publicada pelo `origin`. Worktrees limpos são trocados para essa branch e atualizados somente por
avanço rápido. Repositórios com mudanças locais são reportados como pulados, sem troca de branch.
Opcionalmente, informe outro diretório como primeiro argumento.

O repositório `inventeer-hub` é ignorado explicitamente enquanto suas políticas de acesso estão em
definição; o script não tenta consultar nem atualizar seu remote.

As skills `assistants-task-context` e `portal-task-context` executam esse script automaticamente
antes de carregar o contexto de uma issue. Falhas em repos necessários interrompem a preparação;
repos necessários pulados geram um aviso explícito de possível defasagem.

## Limites

- Linear permanece canônico para estado operacional das issues.
- O IDS permanece canônico para contratos DAP, EPP e DEP.
- Cada repositório de produto permanece canônico para código e specs locais.
- Este workspace não deve armazenar credenciais, dados de clientes ou saídas de produção.
