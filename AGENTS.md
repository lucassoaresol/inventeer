# Workspace Instructions

Este é o workspace pessoal de engenharia de Lucas Oliveira para projetos da Inventeer.

## Propósito

- Desenvolver e validar skills do Codex.
- Manter pontos de entrada leves para projetos da Inventeer.
- Trabalhar com repositórios Git independentes clonados sob `repos/`.
- Validar skills localmente antes de propor adoção nos projetos.

## Fontes canônicas

- Linear é canônico para hierarquia, estado, owner e execução das issues.
- `repos/inventeer-hub` é referência read-only para standards e Playbook compartilhados.
- O repositório `ids` é canônico para contratos DAP, EPP e DEP.
- Cada repositório de produto é canônico para seu código, testes, artifacts e specs locais.
- Os arquivos em `projects/` são ponteiros; não substituem nem copiam fontes canônicas.
- `.specs/STATE.md` registra decisões e handoff deste workspace, não specs dos produtos.

Antes de alterar a estrutura, convenções ou workflow deste workspace, leia as decisões ativas em
`.specs/STATE.md`. Novas decisões transversais devem ser anexadas com o próximo ID `AD-NNN`; decisões
substituídas permanecem no histórico e apontam para sua sucessora.

## Repositórios aninhados

- Os projetos vivem em `repos/` e são ignorados por este repositório.
- Cada diretório sob `repos/` é um repositório Git independente.
- Antes de modificar um projeto, leia suas instruções locais e verifique seu worktree.
- Execute comandos Git no repositório alvo ou use `git -C repos/<projeto>`.
- Não modifique mais de um projeto sem autorização explícita.
- Não clone repositórios automaticamente sem solicitação.
- Trate `inventeer-hub` como referência read-only, salvo quando o escopo for manutenção do Playbook.

## Engines

- Este workspace é operado por Codex e por Claude Code (AD-024).
- `AGENTS.md` é a fonte das instruções; `CLAUDE.md` apenas o importa. Edite este arquivo.
- `.agents/skills/` é a fonte única das skills. O Codex a descobre nativamente; o Claude a alcança
  por symlinks relativos em `.claude/skills/`. Ao criar uma skill, crie também o symlink.
- Uma skill global de mesmo nome em `~/.claude/skills/` suprime a versão deste workspace sem aviso,
  e as `description` podem ser idênticas. Suspeite dessa colisão antes de concluir que uma skill
  está desatualizada.
- O MCP `apex` é declarado por workspace nos dois engines: `.codex/config.toml` e `.mcp.json`.
- O MCP `github` é declarado nos dois engines em modo remoto read-only e usa somente a variável
  local `GITHUB_PAT_TOKEN`; nunca grave o token em arquivos versionados ou no chat.
- Nas sessões Claude iniciadas nesta raiz, mantenha `OMC_STATE_DIR` configurado localmente em
  `.claude/settings.local.json` para `session-context/runtime/omc`. O caminho deve ser absoluto para
  permanecer estável após mudanças de `cwd`; hooks não devem criar `.omc/` na raiz, em `repos/` ou
  nos worktrees de produto. Esse estado é efêmero, ignorado pelo Git, não canônico e só fica
  elegível para limpeza após as sessões correspondentes encerrarem (AD-035).

## Skills

- As skills requeridas ficam em `.agents/skills/`; não presuma equivalentes globais.
- Leia completamente o `SKILL.md` selecionado antes de agir.
- Use `assistants-task-context` para preparar uma issue do produto Assistants.
- Use `portal-task-context` para preparar uma issue do Portal e determinar os repos em escopo.
- Use `triage-project-cycle` para comparar várias issues, ciclos ou frentes antes de selecionar uma
  task para preparação individual.
- Use `advance-delivery-front` quando uma PR aguardar review ou merge e for necessário selecionar,
  contratar ou reconciliar a próxima task sem interromper o ciclo.
- Use `review-pull-request` para revisar ou re-revisar uma PR existente, especialmente trabalho de
  outro dev, com evidência read-only ancorada aos SHAs de base e head. Findings ficam no chat por
  padrão; a skill não corrige código, comenta, aprova nem faz merge.
- Durante `review-pull-request`, leia primeiro somente a issue Linear alvo e expanda contexto com
  justificativa quando DoD herdado, dependência, IDS, hierarquia ou ownership afetar o parecer; não
  execute automaticamente a preparação completa da skill de produto nem reutilize o espelho de PR
  do Linear quando a evidência equivalente estiver disponível no GitHub.
- Durante o piloto definido por AD-038/AD-039, registre somente o schema sanitizado com
  `scripts/pr-review-pilot.py` em `session-context/review-pilot/`. O ledger é ignorado, efêmero,
  não canônico e não pode conter prosa de review, comentários, diffs, código, credenciais, dados de
  clientes, saída de produção ou transcripts; agregue-o antes de avaliar a promoção do workflow.
- Use `discover-project-context` para entender um projeto ou fluxo quando não houver issue Linear;
  não use discovery para contornar uma issue existente.
- Use `create-review-bundle` para empacotar evidências e diffs por arquivo sem modificar o repo
  revisado.
- Trate as skills `apex-*` como wrappers experimentais de inspeção no Codex. Elas leem
  `apex://framework/workflows/<id>`, mas não criam uma execução APEX suportada nem substituem
  prompts nativos, contexto de sessão, artifacts ou gates ausentes. Não as use como executor de
  entrega; não edite seu conteúdo gerado. No Claude Code, use os workflows nativos do MCP `apex`.
- No Codex, mantenha ferramentas de escrita do MCP `apex` sujeitas a aprovação. A exposição de
  operações Git, GitHub, Linear ou multi-repo não amplia ownership nem autoriza execução APEX.
- Antes de declarar um workflow APEX executável, confirme que o servidor publica todas as tools que
  o resource canônico exige e que a sessão recebeu o bloco `=== APEX WORKSPACE ===`. Falta de tool,
  contexto, aprovação ou resultado bloqueia a execução; não apresente fallback manual como APEX.
- Escolha o executor por engine e repositório (AD-026): no Claude Code, use APEX quando o repo tiver
  `ENV.md` e TLC nos demais; no Codex, use sempre `tlc-spec-driven` para especificação,
  implementação e validação, inclusive em repos com `ENV.md`, até nova decisão baseada em uma
  execução APEX end-to-end. A preparação continua sendo das skills locais de contexto.
- Para tasks do Portal executadas por Codex + TLC, mantenha artifacts file-backed da TLC em
  `session-context/portal/<INV-ID>/tlc/`, nunca em `.specs/` dos repos Portal. Esse material é local,
  efêmero, não canônico e não durável; agrupe bundles em
  `session-context/portal/<INV-ID>/review/` e torne o diretório elegível para limpeza após merge e
  encerramento da issue. A rota é transitória e deve ser retirada quando o Codex executar APEX
  end-to-end; não a aplique ao Claude/APEX nem a outros produtos (AD-031).
- Para checkpoints TLC resilientes nessa rota Portal + Codex + TLC, invoque
  `scripts/update-tlc-checkpoint.py` somente depois que uma transição produzir seu resultado com sucesso:
  gate concluído (`gate`), commit atômico criado (`commit`), bundle criado (`bundle`), PR criada ou
  atualizada (`pr`) ou estado de validation alterado (`validation`); não avance o checkpoint como se uma transição que falhou tivesse concluído.
  Grave em
  `session-context/portal/<INV-ID>/tlc/STATE.md`; em `Uncommitted files`, registre somente paths, sem
  diffs ou conteúdo. Trate processo registrado como contexto e confira sua liveness ao retomar. O
  helper atualiza apenas `## Handoff`; decisões e outras seções permanecem intactas (AD-036).
- Mantenha a divisão: triage compara issues e ondas; `advance-delivery-front` coordena a topologia de
  PRs/tasks; `review-pull-request` revisa a mudança submetida sem mutá-la; a skill de produto prepara
  uma issue; a TLC executa e verifica essa issue.
- Não duplique o workflow da TLC em skills específicas de projeto.
- Trate `tlc-spec-driven` como conteúdo vendorizado e atualize-a em commit isolado.
- Em retrospectivas de skills e fluxo, consulte os históricos locais das duas engines associados a
  esta raiz: `~/.codex/sessions/` e o projeto correspondente em `~/.claude/projects/`. Diferencie
  sessões principais, continuations e cópias; não conte a própria retrospectiva como evidência.
  Use `scripts/audit-session-history.py` como inventário inicial sanitizado, com `cwd` exato,
  recorte temporal fechado com `--since` e `--until` e o ID da sessão corrente em
  `--exclude-session`; registre `contract_version`, limites e quantidade de exclusões antes de
  interpretar resultados somente depois dessa deduplicação.
  Diferencie `apex_tool_successes` de `apex_tool_failures`, `apex_tool_denials` e
  `apex_tool_unresolved`; esses campos descrevem outcomes de tools, e tentativa ou sucesso de uma
  tool isolada não prova execução de workflow.
  Não copie transcripts para o Git. Destile decisão transversal em `.specs/STATE.md`, lesson de
  execução somente após validação pelo script da TLC e achado de produto na fonte do produto
  (AD-027).

## MCPs

- Use Context7 somente depois de código e documentação local, para confirmar APIs e padrões atuais
  de bibliotecas.
- Use o MCP GitHub read-only para evidência de PRs, commits, reviews, checks e histórico pós-merge.
  Linear continua canônico para issues e execução; cada repo continua canônico para código e testes.
- Mantenha o MCP GitHub restrito aos toolsets `pull_requests,repos,actions,git` e com
  `X-MCP-Readonly: true`. Sua disponibilidade não autoriza comentários, approvals, merges ou outras
  mutações no GitHub; qualquer futura ampliação de escrita exige nova decisão transversal.
- Ancore conclusões de review ao base SHA e head SHA observados e revalide ambos antes do parecer.
  Se `GITHUB_PAT_TOKEN` estiver ausente ou inválido, reporte o bloqueio sem expor ou persistir a
  credencial e use apenas fontes read-only já disponíveis, declarando a limitação.
- Use o MCP shadcn somente para trabalho em `repos/portal-web`; ele opera com cwd nesse repo e segue
  seu `components.json`, suas instruções locais e seu worktree.
- Antes de qualquer ferramenta de escrita do shadcn, confirme que `repos/portal-web` está clonado,
  leia as instruções do repo, verifique o worktree e obtenha a aprovação exigida pelo engine.
- A disponibilidade do MCP nesta raiz não transfere ownership nem autoriza mudanças de produto.
- Cloudflare e AWS permanecem fora da configuração até uma nova decisão transversal explícita.

## Recursos da máquina

- Antes de tarefas potencialmente pesadas — suíte completa, build, containers, navegador, mutation
  testing ou agentes em paralelo — execute `./scripts/check-machine-resources.sh` e registre no chat
  a disponibilidade observada e a decisão de concorrência.
- Dimensione workers pela capacidade disponível no momento, não apenas pelo total nominal da
  máquina. Em host restrito, prefira concorrência limitada e shards determinísticos; execute todos
  os shards e agregue o resultado antes de chamar o gate de completo.
- Refaça o snapshot antes de uma etapa pesada posterior quando a sessão for longa ou a carga do host
  tiver mudado. Uma limitação de recurso pode alterar a estratégia, nunca reduzir a cobertura.
- Use `bash scripts/test-workspace.sh` como gate agregado da raiz; testes focais continuam válidos
  durante implementação, mas não substituem o gate completo no fechamento.

## Segurança

- Não armazene credenciais, tokens, dados de clientes ou saídas de produção neste workspace.
- Se o usuário fornecer uma credencial ou um valor com aparência de segredo no chat, não repita o valor;
  trate natureza incerta como potencial segredo e use `[REDACTED]` quando precisar referenciá-lo.
- Não coloque o valor recebido em comandos exibidos, logs, commits, checkpoints ou artifacts versionados;
  prefira `.env` ignorado ou entrada interativa para fornecimento local.
- Se houver possibilidade de exposição, oriente a rotação de forma condicional, sem afirmar que a credencial continua ativa.
- Não copie corpos de contratos DAP, EPP ou DEP.
- Não altere Linear ou repositórios em `repos/` durante descoberta sem solicitação explícita.
- Durante `advance-delivery-front`, não altere Linear, GitHub, branches, worktrees ou arquivos de
  produto; o MVP produz somente evidência, contrato e uma próxima ação.
