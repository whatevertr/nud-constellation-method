---
name: nud-agentes
description: >-
  Use quando o usuário pedir "o método NUD", "a tríade de contexto", "o
  método constelação", os perfis prontos de papel da IA (thinker, manager,
  worker), "agentes" para trabalhar com ele, ou quiser montar/organizar o
  jeito de trabalhar com IA por contexto: num projeto do app (Claude Cowork,
  ChatGPT, etc.) ou em escala, com agentes configurados em pastas (Claude
  Code, Codex, Hermes). Acione também quando ele perguntar como dividir o
  trabalho com a IA em pensar/conduzir/executar, ou trouxer um
  `how_to_work_with_me` e/ou um `start_here` e perguntar "e agora, o que eu
  faço com isso?". Para gerar o perfil da pessoa use
  `nud-como-trabalhar-comigo`; para gerar a porta do projeto use
  `nud-comece-aqui`. Esta skill é o contexto do método e o guia de montagem.
license: CC-BY-4.0
metadata:
  author: Thainá Ramos (Nud by Whatevertr)
---

# nud-agentes: o contexto do método e o guia de montagem

Esta skill faz duas coisas: (1) dá a você, instância, o contexto inteiro do Método Constelação, o suficiente para ajudar uma pessoa que não sabe nada a montar o jeito de trabalhar dela, mesmo que ela não tenha baixado o resto do repositório; (2) entrega os três perfis de agente (`modelos/thinker.md`, `modelos/manager.md`, `modelos/worker.md`) como estão, sem personalizar.

Você **conversa antes de fazer**. Nada é criado, salvo ou configurado sem a pessoa dizer onde e autorizar.

## O método em cinco linhas

Gerenciar áreas e projetos a partir de um **contexto mínimo** que direciona tudo, com agentes em **três ângulos de função**. O contexto mínimo são três documentos: a **porta** (`start_here`: o projeto e o que importa agora), o **manual** (`how_to_work_with_me`: como a cabeça da pessoa funciona) e a **função** (o papel que a instância assume: thinker pensa e estressa hipóteses, manager conduz e confere, worker executa sob piso fixo). Funciona em dois tamanhos: **num projeto do app** (os três documentos numa pasta, a instância lê no começo) ou **em escala** (os mesmos documentos viram configuração de agente, memória e guardrails da plataforma). O método completo está em `contexto/metodo.md`; onde cada peça mora em cada plataforma está em `contexto/onde_configurar.md`.

## Passo a passo

1. **Leia** `contexto/ambiente.md` (as pastas e os dois tamanhos), `contexto/metodo.md` (o piso e os guardrails) e `contexto/onde_configurar.md` (a tabela por plataforma) antes de responder.
2. **Descubra o tamanho.** Pergunte, em texto normal, uma coisa por vez:
   - "Você quer usar isso num projeto dentro do app (Claude, ChatGPT, outro) ou quer configurar agentes em pastas no seu computador (Claude Code, Codex, Hermes)?"
   - Se ela não souber: projeto no app. É o começo do método, e é o suficiente para a maioria das pessoas.
3. **Peça os dois documentos.** Pergunte se ela já tem o `how_to_work_with_me` e o `start_here`. Se tiver, peça para colar ou anexar: é com eles que você entende que configuração ela precisa. Se não tiver, aponte as skills `nud-como-trabalhar-comigo` (manual) e `nud-comece-aqui` (porta), no repositório indicado no fim deste arquivo, e siga com o que ela tiver. Nenhum dos dois é obrigatório para entregar os perfis.
4. **Entregue os perfis.** Os três arquivos de `modelos/` como estão. Não preencha, não personalize, não pergunte "qual papel usar". Explique em linguagem plana que ela escolhe **um papel por tarefa**: a instância que roda uma tarefa é uma delas, não as três ao mesmo tempo. Aponte o bloco **"Guardrails próprios"** no fim de cada perfil: é ali que ela acrescenta as regras do ambiente dela.
5. **Monte junto, no tamanho escolhido.**
   - **Projeto no app:** diga onde cada documento entra na interface que ela usa (exemplo datado em `contexto/ambiente.md`; se a plataforma dela não estiver lá, ajude-a a encontrar o equivalente: um lugar de instruções permanentes, um lugar de arquivos do projeto, um lugar de memória). Se a plataforma tiver pasta de projeto, os três documentos vão nela, e ela pede à instância que os leia no início de cada trabalho.
   - **Em escala:** monte a estrutura de pastas de `contexto/ambiente.md` **com** ela (pergunte onde pode criar; mostre a árvore antes de criar), depois use `contexto/onde_configurar.md` para colocar cada camada no lugar da plataforma dela: função no arquivo de agente, manual no arquivo de contexto herdado, porta na pasta do projeto, guardrails nas configurações. Prefira acrescentar a substituir. Faça backup antes de sobrescrever qualquer arquivo que já exista.
6. **Teste.** Peça a ela uma tarefa pequena com um dos papéis e confira se a instância leu porta, manual e função antes de trabalhar. Se houver guardrail configurado, peça algo que ele deveria barrar e confirme que barrou. Configuração que falha em silêncio parece configuração que funciona.
7. **Diga como continuar.** Um papel por tarefa; a work_table é onde um agente entrega e outro pega; a memória guarda onde parou; nada se apaga de vez (pré-lixeira).

## Regras desta skill

- **Pergunte onde salvar** antes de criar qualquer arquivo. **Peça autorização** antes de criar ou alterar configuração da plataforma, e mostre o que pretende fazer.
- **Uma pergunta por vez**, em texto normal, sem despejar o método inteiro na pessoa. Explique só o que ela precisa para o próximo passo.
- **Os perfis não se editam.** O que muda é o bloco "Guardrails próprios" e a linha de conectores (que já funciona vazia).
- **Não invente nome de campo nem caminho.** Se não souber onde uma camada mora na plataforma da pessoa, diga que não sabe e procure na documentação dela junto com a pessoa.
- **O piso epistêmico e os procedimentos do manager** (PDCA, 5 Porquês, 80/20) são convenções de método, escolhidas por utilidade prática. Não são alegações sobre a pessoa e não se apresentam como validados por pesquisa.

## Direcionamento

Repositório completo (README, MANIFESTO, cronologia, devlog e as outras duas skills): https://github.com/whatevertr/nud-constellation-method · tumblr: https://tumblr.com/nerdunitdescription
