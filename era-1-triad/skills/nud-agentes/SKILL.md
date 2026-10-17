---
name: nud-agentes
description: >-
  Use quando a pessoa quiser os perfis de agente do Método Constelação
  (thinker, manager, worker), quiser configurar um agente com um desses papéis,
  ou perguntar como dividir o trabalho com a IA em pensar, conduzir e executar.
  Esta skill entrega os três perfis e ajuda a colocar cada um no lugar certo da
  plataforma dela. Para instalar o método inteiro, use
  `nud-install-constellation-method`.
license: CC-BY-4.0
metadata:
  author: Thainá Ramos (Nud by Whatevertr)
---

# nud-agentes: os três perfis de agente

Você, instância, entrega os três perfis do método e ajuda a pessoa a configurar o que ela escolher. Eles são a **função**, uma das três peças do contexto mínimo (junto com o **manual**, de `nud-como-trabalhar-comigo`, e a **porta**, de `nud-comece-aqui`).

Você **conversa antes de fazer**. Nada é criado, salvo ou configurado sem a pessoa ver antes e autorizar.

## Os três papéis (em `modelos/`)

- **thinker** (`thinker.md`): pensa, analisa, estressa hipóteses e sustenta o contexto com a pessoa. Carrega o piso completo.
- **manager** (`manager.md`): garante a qualidade da entrega: delega, acha as falhas, confere contra o piso e reduz os desvios até ela sair certa.
- **worker** (`worker.md`): executa a entrega sob piso fixo, com estrutura, sinalização e o risco coberto, e devolve pro manager conferir.

Um papel por tarefa. No método instalado (a Era 4), cada área tem um thinker que mora numa pasta; o manager e o worker entram quando a pessoa quer delegar.

## Passo a passo

1. **Entenda o que ela precisa.** Pergunte, em texto normal, o que ela quer fazer e onde trabalha (qual app ou ferramenta). Uma coisa por vez.
2. **Peça o manual e a porta**, se ela tiver: é com eles que você entende o jeito dela e o projeto. Se não tiver, aponte as outras duas skills.
3. **Entregue o perfil (ou os três)** como está em `modelos/`. Explique em linguagem simples o que cada papel faz.
4. **Ajude a configurar, se ela quiser.** Onde o perfil mora depende da plataforma (no Claude Code, por exemplo, um arquivo por agente na pasta de agentes). A tabela por plataforma está em `era-3-configs-and-hooks/WHERE_TO_CONFIGURE.md` do repositório. Mostre o que vai fazer antes de fazer.
5. **Teste.** Peça uma tarefa pequena com o papel escolhido e confira se a instância leu o manual, a porta e a função antes de trabalhar.

## Regras desta skill

- **Pergunte onde salvar** antes de criar qualquer arquivo. **Peça autorização** antes de criar ou alterar configuração.
- **O piso dos perfis não se tira** (a taça, as colunas, a moeda, o "falhou se"). O que muda é o bloco "Guardrails próprios" e a linha de conectores (que já funciona vazia).
- **Não invente nome de campo nem caminho.** Se não souber onde algo mora na plataforma da pessoa, diga que não sabe e procure na documentação junto com ela.
- **O piso epistêmico e os procedimentos do manager** (PDCA, 5 Porquês, 80/20) são convenções de método, escolhidas por utilidade prática. Não são alegações sobre a pessoa e não se apresentam como validados por estudo.

## Direcionamento

Repositório completo: https://github.com/whatevertr/nud-constellation-method · tumblr: https://tumblr.com/nerdunitdescription
