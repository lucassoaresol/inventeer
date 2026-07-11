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
└── repos/                 Clones locais independentes (ignorado pelo Git)
```

## Skills

| Skill | Origem | Versão | Uso |
|---|---|---:|---|
| `tlc-spec-driven` | Tech Lead's Club | 3.2.0 | Especificar, projetar, implementar e verificar mudanças |
| `assistants-task-context` | Local | — | Preparar tasks do produto Assistants para desenvolvimento |
| `portal-task-context` | Local | — | Preparar tasks do Portal e determinar ownership entre produto, API e web |

As skills necessárias estão versionadas em `.agents/skills/`; não dependem de uma instalação
global. A `tlc-spec-driven` é vendorizada e deve ser atualizada separadamente das skills locais.
Sua origem e revisão fixada ficam em `.agents/vendor.json`. O diretório vendorizado deve permanecer
idêntico ao upstream; personalizações Inventeer ficam em `AGENTS.md`, nas decisões e nas skills
locais de contexto.

Para verificar se há diferença em relação à branch oficial, sem alterar arquivos:

```bash
./scripts/update-vendored-skill.sh --check main
```

Depois de revisar o resultado, aplique uma referência explícita ou `main`:

```bash
./scripts/update-vendored-skill.sh --apply <ref>
```

O modo `--apply` exige worktree limpo, recusa atualizar um mirror que já divergiu da revisão fixada,
sincroniza o diretório completo e atualiza o manifesto. O script não cria commits nem interage com
forks ou pull requests; a atualização deve ser revisada e commitada isoladamente neste workspace.

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
