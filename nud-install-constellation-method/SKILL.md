---
name: nud-install-constellation-method
description: >-
  Use quando a pessoa pedir pra instalar "o método", "o Método Constelação",
  "o Constellation Method", "o método NUD" ou "a tríade", ou quiser um agente
  que conheça o jeito dela de trabalhar e continue de um dia pro outro. Esta
  skill conversa com a pessoa, explica o que o método é e o que ele custa, e
  instala a versão atual (a Era 4) no computador dela. Para o manual da pessoa
  use `nud-como-trabalhar-comigo`; para a porta de um projeto, `nud-comece-aqui`;
  para os perfis dos agentes, `nud-agentes`.
license: CC-BY-4.0
metadata:
  author: Thainá Ramos (Nud by Whatevertr)
---

# nud-install-constellation-method: instala o Método Constelação

Você, instância, vai **instalar o método no computador da pessoa**, conversando com ela. Sempre a versão atual, a **Era 4**, que já traz dentro as anteriores. As eras não são opções de produto: são os degraus que levaram até aqui.

Você **conversa antes de fazer**. Nada é criado, salvo ou configurado sem a pessoa ver antes e autorizar.

## O mapa do fluxo de contexto (pra você ancorar o raciocínio)

Na dúvida sobre o objetivo de alguma peça, volte aqui. Cada era usa as anteriores:

1. **Era 1, a Tríade:** as skills que ajudam a definir um chão comum entre a pessoa e o agente: o **manual** (como ela trabalha), a **porta** (o que é o projeto e o que importa agora) e a **função** (o perfil do agente: thinker, manager ou worker). Juntos, são o **contexto mínimo**.
2. **Era 2, estados e diários:** com o contexto mínimo pronto, entra a **memória**, com manutenção manual: o estado (onde paramos) e o diário (como foi trabalhar junto), que a próxima conversa consulta.
3. **Era 3, configs e hooks:** o contexto mínimo vira **configuração de agente personalizado**, e os hooks e o system prompt garantem que o contexto chegue, sem depender de alguém lembrar.
4. **Era 4, scripts e interface:** o fluxo de contexto é **padronizado e automatizado**, com um **painel** que mostra as missions, as pendências e a ficha de cada thinker (um registrador único escreve o log; hooks entregam o último resumo e o último diário ao abrir), e o passado vira **contexto de consulta** buscável: o **galley**, uma busca híbrida (por sentido, com embeddings, e por palavra, com BM25, unidas por fusão de ranking) sobre os registros antigos fatiados em pedaços. É a parte de recuperação de um RAG, usada sob demanda: o agente busca quando precisa.

## O que você está instalando (explique assim, em linguagem simples)

- **O que melhora o trabalho com o agente é uma dinâmica de convívio.** Cada área de trabalho da pessoa vira uma **galaxy**, e cada galaxy tem um **thinker**: um agente que conhece o jeito dela de trabalhar, ajuda a pensar e orquestra junto com ela todos os trabalhos daquela área. Cada trabalho é uma **mission**.
- **Ele continua de um dia pro outro.** O que foi feito e decidido fica num registro (o log); como foi trabalhar junto fica num diário. Os dois chegam sozinhos quando uma conversa nova abre.
- **O custo, sem esconder:** o método pede atenção. A pessoa confere o que a IA entrega e fecha o dia com um resumo, e a estrutura de pastas pede algum cuidado. É o custo de trabalhar desse jeito, e é uma escolha. Se ela não quer esse tipo de relação de trabalho, diga com honestidade que talvez o método não sirva pra ela.
- **Onde roda:** testado no **Claude Code** (app desktop ou terminal), com Python 3.10 ou mais novo. No Codex, as regras chegam pelo `AGENTS.md` de cada pasta, mas os hooks só foram testados no Claude Code.

## Passo a passo

1. **Converse.** Pergunte, uma coisa por vez, como ela trabalha, em que áreas e o que faz hoje com IA. Explique o bloco acima. Pergunte se ela quer seguir.
2. **Baixe o repositório** numa pasta de trabalho temporária: `git clone https://github.com/whatevertr/nud-constellation-method`. Sem git ou sem internet, peça pra pessoa baixar o zip (no GitHub, "Code → Download ZIP") e te dizer onde salvou.
3. **O contexto mínimo (Era 1).** As três skills estão em `era-1-triad/skills/` do repositório:
   - o **manual** (`nud-como-trabalhar-comigo`): alimenta o "Quem você ajuda" da raiz e o jeito do thinker;
   - a **porta** (`nud-comece-aqui`) de cada projeto: vira o `CLAUDE.md` da mission;
   - os **perfis** (`nud-agentes`): o do thinker é o ponto de partida da casa dele; o manager e o worker ficam pra quando ela quiser delegar.
   Se a pessoa já tiver o manual e a porta, peça pra colar ou anexar. Se não tiver, faça com ela, seguindo as skills.
4. **Siga o guia da Era 4:** `era-4-scripts-and-interface/INSTALAR.md` (ou `INSTALL.md`, em inglês). Ele é o passo a passo completo: onde mora, o Python, os marcadores, os nomes, a ficha do thinker, o primeiro registro e como saber que deu certo. **Mostre a árvore de pastas antes de criar.**
5. **As galaxies.** Uma por área que a pessoa escolher (comece com uma), cada uma com o seu thinker.
6. **As missions.** Cada trabalho vira uma mission em `missions\nome-da-mission\`. Se a pessoa trabalha principalmente com repositórios, **o repositório mora dentro da mission** (`missions\nome\repo-nome\`). A `lab\` (materiais, rascunhos, o que ainda não foi revisado) não é obrigatória, mas ajuda a organizar: sugira.
7. **O painel e os exemplos.** Ofereça o painel (`cosmos\app\`, passo 7 do guia): ele precisa do `pywebview`, instalado só com o sim da pessoa. Mostre a mission e a skill de exemplo (dados fictícios, pro painel não abrir vazio) e explique que, quando ela quiser começar de verdade, as duas pastas vão inteiras pro `_to_delete`.
8. **Teste** como manda o guia ("Como saber que deu certo").
9. **Diga como continuar:** abrir a conversa sempre na pasta da casa do thinker; fechar o dia com um resumo (e o diário, se ela quiser); nada se apaga de vez (vai pro `_to_delete`, e só ela esvazia).

## Pra quem quer fazer à mão
Tudo o que esta skill faz está no `INSTALAR.md` da Era 4, no repositório. A pessoa pode ler e instalar sozinha.

## Regras desta skill

- **Pergunte onde salvar** antes de criar qualquer arquivo. **Peça autorização** antes de criar ou alterar configuração, e mostre o que pretende fazer.
- **Uma pergunta por vez**, em texto normal. Explique só o que ela precisa pro próximo passo.
- **O piso dos perfis não se tira** (a taça, as colunas, a moeda, o "falhou se"). O que muda é o que é da pessoa: o nome, o jeito, os guardrails próprios.
- **Não invente nome de campo nem caminho.** Se não souber onde algo mora na plataforma da pessoa, diga que não sabe e procure na documentação junto com ela.

## Direcionamento

Repositório completo (o que é cada era, o MANIFESTO, a história): https://github.com/whatevertr/nud-constellation-method · tumblr: https://tumblr.com/nerdunitdescription
