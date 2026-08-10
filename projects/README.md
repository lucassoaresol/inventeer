# Project Registry

Índice dos projetos atualmente disponíveis no workspace. Os arquivos desta pasta são ponteiros
versionados; os repositórios reais permanecem independentes e ignorados sob `repos/`.

| Tipo | Projeto/referência | Contexto canônico | Repositório(s) de implementação | Raiz Linear | Ponto de entrada |
|---|---|---|---|---|---|
| Foundation | Inventeer Hub Playbook | `repos/inventeer-hub` | — | — | [inventeer-hub.md](inventeer-hub.md) |
| Operações | Inventeer Ops | `repos/inventeer-ops` | — | `INV-255` | [inventeer-ops.md](inventeer-ops.md) |
| Tooling | Inv Cortex CLI | `repos/inv-cortex` | `repos/inv-cortex` | — | [inv-cortex.md](inv-cortex.md) |
| Produto | Assistants | `repos/assistants` | `repos/assistants` | `INV-2228` | [assistants.md](assistants.md) |
| Sistema | IDS | `repos/inventeer-ops/artifacts/products/ids` | — | `INV-88` | [ids.md](ids.md) |
| Produto | Portal | `repos/inventeer-ops/artifacts/products/portal` | `repos/portal-api`, `repos/portal-web` | `INV-254` | [portal.md](portal.md) |

Antes de agir em qualquer repo, leia suas instruções locais (`AGENTS.md`, `CLAUDE.md` e README,
conforme existirem) e confira o worktree Git correspondente.

IDS e Portal continuam sendo projetos lógicos mesmo sem repos documentais próprios. Caminhos sob
`repos/inventeer-ops/artifacts/` são subárvores de um repo Git compartilhado, não aliases de repos.

## Roteamento de trabalho

| Situação | Entrada | Próximo handoff |
|---|---|---|
| Uma issue Assistants selecionada | `assistants-task-context` | TLC ou clarificação da issue |
| Uma issue Portal selecionada | `portal-task-context` | TLC ou clarificação da issue |
| Várias issues, ciclo ou backlog | `triage-project-cycle` | Selecionar uma issue e usar sua skill de produto |
| Projeto, processo ou integração sem issue | `discover-project-context` | Registrar o trabalho canônico antes de implementar |
| Mudança pronta para review | `create-review-bundle` | Compartilhar o ZIP efêmero e preservar o repo-fonte |

As rotas de triagem e discovery leem este registry apenas para localizar fontes canônicas. Elas não
transformam os arquivos de `projects/` em especificação, decisão de produto ou estado operacional.
