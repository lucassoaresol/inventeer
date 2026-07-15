# Workspace Context Routing and Review Bundles

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** Portuguese

## Objective

Separar triagem de múltiplas issues e discovery sem issue dos fluxos de task única, e substituir a
criação manual de bundles de review por uma automação local, verificável e read-only para o
repositório analisado.

## Acceptance Criteria

1. **WCR-01 — Cycle triage:** quando o usuário fornecer várias issues, um ciclo ou um recorte de
   backlog, o workspace deve oferecer uma skill que compare readiness, dependências formais,
   colisões de código e ordem de execução sem preparar cada issue integralmente.
2. **WCR-02 — Discovery sem issue:** quando o usuário pedir entendimento de um projeto ou fluxo sem
   issue Linear, o workspace deve oferecer uma skill que use o registry para localizar fontes
   canônicas, separe fatos de hipóteses e não invente hierarquia Linear.
3. **WCR-03 — Handoff:** quando uma issue for selecionada ou criada, as novas rotas devem transferir
   o trabalho para a skill de contexto do produto, preservando seu contrato de task única.
4. **RB-01 — Conteúdo:** quando houver mudanças em relação à base escolhida, a automação deve gerar
   ZIP com manifesto, status, commits, índice, um diff por arquivo e checksum SHA-256.
5. **RB-02 — Superfície:** arquivos rastreados, removidos e não rastreados devem aparecer
   individualmente no bundle.
6. **RB-03 — Não mutação:** a geração do bundle não deve alterar o status do repo-fonte.
7. **RB-04 — Segurança:** bases inválidas, conjuntos vazios e caminhos prováveis de credenciais,
   chaves ou dumps devem ser recusados.
8. **DOC-01 — Descoberta:** README, registry, AGENTS e decisões do workspace devem documentar as
   novas rotas, limites e handoffs.

## Out of Scope

- Alterar `inv-cortex` ou qualquer repositório sob `repos/`.
- Modificar Linear durante triagem ou discovery.
- Incluir resultados de testes que não tenham sido fornecidos e verificados separadamente.
- Transformar bundles efêmeros em artifacts canônicos ou aprovações.
