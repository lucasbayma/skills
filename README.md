# Candango Skills

[![skills.sh](https://skills.sh/b/lucasbayma/skills)](https://skills.sh/lucasbayma/skills)

Candango é um conjunto de skills para levar uma feature do setup do repo até UAT, com planejamento, especificação, issues verticais, execução autônoma, TDD, validação externa e wrap-up.

## Usage

Instale pelo `skills.sh`:

```bash
npx skills@latest add lucasbayma/skills
```

Selecione o conjunto recomendado:

- `candango-setup`
- `candango-caveman`
- `candango-discover`
- `candango-design`
- `candango-tdd`
- `candango-plan`
- `candango-spec`
- `candango-issues`
- `candango-uat`
- `candango-executor`
- `candango-uat-runner`
- `candango-wrap-up`

Em cada repo alvo, rode o setup uma vez:

```text
Use $candango-setup to configure this repo for autonomous feature delivery.
```

Depois use o fluxo completo quando quiser entregar uma feature de ponta a ponta:

```text
Use $candango-discover to clarify this feature:

<feature request>

Then use $candango-plan, $candango-spec, $candango-issues, $candango-uat,
$candango-executor, $candango-uat-runner, and $candango-wrap-up.
All communication and reports must use $candango-caveman.
```

Para uma feature pequena e já clara:

```text
Use $candango-plan to plan this small feature:

<feature request>

Then use $candango-spec, $candango-issues, $candango-uat, and
$candango-executor.
```

Se houver tela, fluxo, dashboard, app, formulário ou qualquer superfície visual, rode `candango-design` antes de fechar plano, spec e issues:

```text
Use $candango-design to create/edit screens for this feature.
Target surface: local HTML prototype.
```

## Loop completo

### Ciclo de desenvolvimento

![Ciclo completo de desenvolvimento Candango](./docs/calango-development-cycle.svg)

### Ciclo do executor

![Loop do executor com TDD e validação externa](./docs/executor-cycle.svg)

O ponto importante: o executor que implementa não valida o próprio trabalho. Ele escreve código com TDD; outro subagent, sem o contexto da conversa do executor e sem permissão para editar, revisa o diff contra spec, issue e UAT. Se falhar, a main agent transforma o parecer em nova rodada de TDD. Só depois entram UAT manual e validação final do repo.

## Skills

### [`candango-setup`](./skills/candango/candango-setup/SKILL.md)

Configura o repo para o fluxo Candango. Descobre ou pergunta qual tracker usar, onde ficam docs de feature, qual comando valida o trabalho, onde salvar dashboard, como tratar artefatos de design e quais regras os agentes devem seguir.

Ele cria documentação local para que as outras skills não dependam de memória da conversa. Rode uma vez por repo, e rode de novo só quando mudar tracker, convenção de docs ou processo de validação.

### [`candango-caveman`](./skills/candango/candango-caveman/SKILL.md)

Define o estilo de comunicação do fluxo: curto, direto, sem enchimento, mas mantendo substância técnica. O objetivo é reduzir ruído em planos, specs, issues, relatórios de executor, pareceres de validator, histórico de dashboard, UAT e PR.

Use quando quiser que todo o ciclo produza respostas e relatórios de alto sinal.

### [`candango-discover`](./skills/candango/candango-discover/SKILL.md)

Clareia uma feature antes de planejar. Ele lê docs, ADRs, contexto de domínio, configs do repo e código relevante antes de perguntar. Quando pergunta, faz uma pergunta por vez, com uma recomendação.

Serve para resolver termos ambíguos, regras de negócio, atores, permissões, paths felizes, erros, contratos, UX, rollout, UAT, slicing, validação final e prontidão para execução autônoma. O resultado é contexto de feature suficiente para plano, spec, issues e UAT.

### [`candango-design`](./skills/candango/candango-design/SKILL.md)

Entra quando a feature tem interface: tela web, app, dashboard, admin, onboarding, checkout, settings, formulário, tabela, fluxo ou mudança visual. Ele produz ou revisa artefatos de design antes de fechar plano e spec.

O caminho recomendado é protótipo HTML local primeiro, depois portar para a base real. Os artefatos gerados viram referência para plano, spec, issues e UAT visual.

### [`candango-plan`](./skills/candango/candango-plan/SKILL.md)

Transforma pedido, contexto e decisões em um plano implementável. Ele registra problema, usuários, resultado esperado, não-objetivos, restrições, riscos, decisões e slices verticais.

A skill diferencia feature pequena, média e grande. Para cada slice, define resultado, dependências, sinais de aceitação, risco e se pode rodar AFK ou precisa de HITL.

### [`candango-spec`](./skills/candango/candango-spec/SKILL.md)

Transforma o plano aprovado em especificação técnica. Ela descreve arquitetura, contratos, dados, permissões, erros, observabilidade, estratégia de testes, validação e rollout.

A spec deve permitir que outro agente implemente sem contexto escondido, que o validator revise sem inventar requisito, e que as issues sejam criadas sem virar lista horizontal de camadas.

### [`candango-issues`](./skills/candango/candango-issues/SKILL.md)

Quebra plano e spec em issues verticais e executáveis. Cada issue precisa ser pequena o bastante para validar sozinha, mas completa o bastante para entregar comportamento observável.

Ela modela dependências, `blocked_by`, `unblocks`, parent, critérios de aceitação, tipo AFK/HITL, expectativas de validação e links para UAT/design quando existirem. Antes de escrever ou publicar issues, mostra a proposta e espera aprovação.

### [`candango-uat`](./skills/candango/candango-uat/SKILL.md)

Gera cenários de aceite a partir das regras de negócio, plano, spec, issues e artefatos de design. O foco é comportamento externo, não detalhe interno.

Os UATs usam Given/When/Then, têm prioridade, indicam se são automáticos, manuais ou ambos, e apontam quais acceptance criteria provam. Durante execução, o validator usa esses UATs como oráculo de negócio.

### [`candango-tdd`](./skills/candango/candango-tdd/SKILL.md)

É a skill usada pelo executor para implementar uma issue por vez. O ciclo é RED, GREEN, REFACTOR: um teste de comportamento falha, a menor implementação passa, a limpeza acontece só enquanto tudo está verde.

Os testes devem passar por interfaces públicas, resistir a refactors e verificar comportamento real. A saída do executor sempre inclui issue, comportamento implementado, testes, arquivos alterados, comandos e riscos.

### [`candango-executor`](./skills/candango/candango-executor/SKILL.md)

Orquestra a execução autônoma. A main agent escolhe issues desbloqueadas, atualiza dashboard, dispara um executor com `candango-tdd`, dispara um validator independente, decide se volta para correção, UAT ou done, e roda a validação final.

O executor pode editar código. O validator não edita; ele recebe diff, spec, issue e UAT, mas não recebe a conversa do executor. Isso força validação externa em vez de autoaprovação.

### [`candango-uat-runner`](./skills/candango/candango-uat-runner/SKILL.md)

Roda UAT manual ou semiautomático depois da implementação. Ele guia um cenário por vez, executa checks automáticos quando possível, dá passos manuais claros para o usuário e registra passou, falhou ou bloqueou.

Quando um UAT falha, ele captura repro, esperado, atual, evidências e contexto relacionado, depois manda esse pacote para o `candango-executor` reiniciar o loop de correção com TDD e validator.

### [`candango-wrap-up`](./skills/candango/candango-wrap-up/SKILL.md)

Finaliza a feature. Limpa arquivos temporários de dashboard, verifica testes e validação final, checa status de UAT, classifica o PR como feat, bugfix ou chore, prepara commit e cria PR.

O PR deve deixar claro o que mudou, por quê, quais UATs passaram ou ficaram pendentes, quais comandos validaram o trabalho e se houve limpeza de arquivos temporários.

## Referências e créditos

Candango combina ideias próprias com skills e padrões que usei como base:

- [`mattpocock/skills`](https://github.com/mattpocock/skills): referência principal para skills pequenas e compostáveis, TDD disciplinado, perguntas fortes antes de implementar, docs locais de domínio e issues verticais.
- [`grill-with-docs`](https://github.com/mattpocock/skills/tree/main/skills/engineering/grill-with-docs), de Matt Pocock: base para o fluxo de stress-test de requisitos contra docs, ADRs e linguagem de domínio.
- [`tdd`](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd), de Matt Pocock: base para o ciclo RED/GREEN/REFACTOR orientado por comportamento.
- [`huashu-design`](https://github.com/alchaincyf/huashu-design), de alchaincyf: base para a skill de design HTML, protótipos, telas, demos visuais e artefatos de interface.
- `caveman`: adaptada de uma skill local de comunicação ultra-comprimida, inspirada no estilo de relatórios curtos usado no ecossistema de skills.

As demais skills do Candango conectam essas peças em um ciclo completo: setup do repo, clarificação, design opcional, plano, spec, issues, UAT, execução autônoma, validação independente, UAT guiado e wrap-up.
