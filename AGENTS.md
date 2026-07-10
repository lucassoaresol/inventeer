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

## Skills

- As skills requeridas ficam em `.agents/skills/`; não presuma equivalentes globais.
- Leia completamente o `SKILL.md` selecionado antes de agir.
- Use `assistants-task-context` para preparar uma issue do produto Assistants.
- Use `portal-task-context` para preparar uma issue do Portal e determinar os repos em escopo.
- Use `tlc-spec-driven` quando o trabalho exigir especificação, design, implementação ou validação.
- Não duplique o workflow da TLC em skills específicas de projeto.
- Trate `tlc-spec-driven` como conteúdo vendorizado e atualize-a em commit isolado.

## Segurança

- Não armazene credenciais, tokens, dados de clientes ou saídas de produção neste workspace.
- Não copie corpos de contratos DAP, EPP ou DEP.
- Não altere Linear ou repositórios em `repos/` durante descoberta sem solicitação explícita.
