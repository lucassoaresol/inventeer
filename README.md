# Inventeer Engineering Workspace

Workspace pessoal de engenharia para trabalhar com projetos da Inventeer usando Codex.

Este repositório mantém skills reutilizáveis e pontos de entrada dos projetos. O código dos
produtos fica em repositórios Git independentes sob `repos/`, que é ignorado por este repositório.

As decisões que definem este workspace e seus trade-offs ficam em [`.specs/STATE.md`](.specs/STATE.md).
Esse arquivo registra memória do workspace; specs de produto permanecem nos respectivos repos.

## Estrutura

```text
.
├── .agents/skills/        Skills versionadas e descobertas pelo Codex
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
| Preparar uma issue Assistants | `assistants-task-context` | `tlc-spec-driven`, quando necessário |
| Preparar uma issue Portal | `portal-task-context` | `tlc-spec-driven`, quando necessário |
| Empacotar trabalho para review | `create-review-bundle` | Review externo; não implica aprovação |

`advance-delivery-front` mantém a topologia da PR pronta e da próxima task ativa/draft, classifica
dependências, separa maturidade de implementação e validação e planeja a reconciliação pós-merge.
Seu MVP não cria branches, altera PRs ou atualiza o Linear; ele entrega um contrato verificável e
exatamente uma próxima ação antes do handoff para a skill de task do produto e, quando necessário,
para `tlc-spec-driven`.

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
