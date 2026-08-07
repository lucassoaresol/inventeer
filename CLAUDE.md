# Instruções para Claude Code

@AGENTS.md

## Engine

Este workspace é operado por Codex e por Claude Code. As instruções acima são compartilhadas: este
arquivo existe apenas porque o Claude Code lê `CLAUDE.md` enquanto o Codex lê `AGENTS.md`. Não
duplique conteúdo aqui; edite `AGENTS.md`.

## Descoberta de skills

- `.agents/skills/` é a fonte única das skills e é descoberto nativamente pelo Codex.
- `.claude/skills/` contém symlinks relativos para os mesmos diretórios, porque o Claude Code não
  lê `.agents/skills/`.
- Ao adicionar uma skill, crie o diretório em `.agents/skills/` e o symlink correspondente.
- Uma skill global de mesmo nome em `~/.claude/skills/` suprime a versão deste workspace. Se uma
  skill parecer desatualizada no Claude Code, verifique essa colisão antes de editar os arquivos.

## MCP

O servidor `apex` é declarado por workspace em `.mcp.json`, equivalente ao que
`.codex/config.toml` faz para o Codex (AD-020). O Linear não é declarado aqui: no Claude Code ele
já chega pelo connector da claude.ai, e declará-lo de novo duplicaria o conjunto de ferramentas.
O GitHub também é declarado em `.mcp.json` como servidor HTTP read-only; o header de autenticação
expande `GITHUB_PAT_TOKEN` em runtime e nunca deve receber um token literal versionado.
