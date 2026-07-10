# Inv Cortex CLI Entry Point

## Identidade

- Tipo: developer tooling.
- Repositório local esperado: `repos/inv-cortex`.
- Binário instalado: `inv`.
- Versão observada no bootstrap: `0.2.2`.

## Papel

A CLI `inv` automatiza workflows de desenvolvimento Inventeer, incluindo workspaces Portal baseados
em Git worktrees, runtime isolado, testes, push, stage e criação de PR.

## Pontos de entrada

Leia em `repos/inv-cortex`, conforme a necessidade:

1. `CLAUDE.md` — contrato operacional e layout dos workspaces.
2. `README.md` — visão geral, instalação e manutenção.
3. `libs/cli/README.md` — comandos e lifecycle detalhado.
4. `libs/cli/src/commands/` — implementação dos comandos.
5. `libs/cli/src/lib/` — paths, Git, Docker, portas, env e Linear.

## Estado neste workspace

- A CLI está disponível, mas worktrees foram deixados fora do escopo do bootstrap inicial.
- Não crie uma automação paralela de Git/Docker sem primeiro avaliar extensão da `inv`.
- Comandos destrutivos, especialmente `inv wt destroy`, exigem preflight explícito de worktrees
  limpos e aprovação do usuário.
