# Engine-Aware Skill Learning

**Status:** Approved
**Review language:** Portuguese
**Canonical language:** Portuguese

## Objective

Usar os históricos locais de Codex e Claude Code como evidência retrospectiva para melhorar as
skills e o fluxo do workspace, sem transformar transcripts em fonte canônica, e corrigir o
roteamento de execução para refletir a capacidade efetivamente observada de cada engine.

## Acceptance Criteria

1. **ESL-01 — Evidência multi-engine:** retrospectivas de skills devem consultar as sessões Codex e
   Claude Code associadas à raiz deste workspace, distinguir sessões principais de continuations ou
   cópias e excluir a própria retrospectiva do conjunto de evidência.
2. **ESL-02 — Capacidade versus execução:** a documentação deve distinguir acesso do Codex a tools e
   resources APEX de uma execução suportada do workflow, que também exige invocação, contexto de
   sessão, artifacts e gates requeridos pelo workflow.
3. **ESL-03 — Roteamento atual:** no Codex, entregas devem usar `tlc-spec-driven`; no Claude Code,
   repos com `ENV.md` devem usar APEX e os demais devem usar TLC. As skills locais de contexto
   continuam preparando a task antes do executor.
4. **ESL-04 — Wrappers honestos:** wrappers `apex-*` expostos ao Codex devem se declarar
   experimentais e diagnósticos, sem alegar que executam um workflow APEX suportado.
5. **ESL-05 — Destino dos aprendizados:** decisões transversais devem ir para `.specs/STATE.md`;
   falhas de execução confirmadas por validação devem entrar em `.specs/lessons.json` somente pelo
   script da TLC; achados de produto devem permanecer no produto; transcripts brutos não devem ser
   copiados nem versionados.
6. **ESL-06 — Consistência:** `AGENTS.md`, `README.md`, decisões e conteúdo gerado dos wrappers não
   devem fornecer orientações conflitantes sobre executor ou rastreio de aprendizados.

## Evidence Basis

- 90 rollouts Codex encontrados em `~/.codex/sessions/2026/07` com metadata apontando para esta
  raiz, incluindo quatro retrospectivas anteriores de skills e fluxo.
- 13 registros Claude encontrados no projeto correspondente em `~/.claude/projects/`, incluindo a
  criação da camada dual-engine e a entrega/revisão da INV-3286.
- Codex `019fa649-046f-7500-a0d1-050760e68e5e` e
  `019fa683-cb7c-7b33-b5d3-26077367ff48`: resources APEX acessíveis, mas `preflight`,
  `write_session_artifact`, `run_gate`, `SESSION_ID` e/ou acesso do runner ao repo indisponíveis.
- Claude `e6a4a1c9-9d9c-4ba7-8aa0-1c92d1c473d7`: workflow e artifacts APEX usados na INV-3286,
  com fallback explícito quando `run_gate` e alguns primitives não estavam expostos.

## Out of Scope

- Alterar o servidor, catálogo ou contratos canônicos do APEX.
- Modificar Linear, GitHub ou qualquer repositório sob `repos/`.
- Copiar conteúdo integral de transcripts ou armazenar credenciais e outputs sensíveis.
- Declarar paridade futura do Codex antes de uma nova validação end-to-end.
