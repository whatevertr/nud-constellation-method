---
name: nud-comece-aqui
description: >-
  Use quando o usuário pedir para criar/montar um `start_here`, o
  "documento de porta" de um projeto, definir objetivo prático/fundamentação
  teórica/objetivo abstrato de um trabalho para a IA, ou pedir "ensina a IA
  onde começar no meu projeto", "monta a porta do meu projeto", "quero que a
  IA entenda o que estamos construindo antes de trabalhar". Acione também
  quando o usuário mencionar a "Tríade de Contexto" e quiser especificamente
  a peça de contexto do TRABALHO/PROJETO (não o perfil da pessoa, não os
  papéis worker/thinker/manager, para isso use `nud-como-trabalhar-comigo`
  e `nud-agentes`).
license: CC-BY-4.0
metadata:
  author: Thainá Ramos (Nud by Whatevertr)
---

# nud-comece-aqui

Esta skill conduz a conversa sobre o PROJETO e entrega o arquivo `start_here.md` preenchido, que serve como PORTA de contexto que ensina uma instância de IA onde ela está entrando: o tema, o objetivo, e o porquê o projeto é importante.

## Passo a passo

1. **Leia** `regras/regras_de_preenchimento.md` e `regras/perguntas_do_projeto.md` antes de começar.
2. **Faça as 3 perguntas do projeto**, uma por vez, em texto normal, sem mostrar os títulos internos. O texto exato de cada pergunta e a regra de "uma de cada vez, sem mostrar título" estão em `regras/perguntas_do_projeto.md`. Siga esse arquivo à risca, não reescreva as perguntas aqui.
3. **Preencha** `modelos/start_here.md` com as respostas. Cabeçalho e rodapé seguem exatamente o que está descrito em `regras/regras_de_preenchimento.md`.
4. **Pergunte à pessoa onde salvar o arquivo**, ou oriente a salvar na área dedicada do projeto.
5. **Entregue o arquivo** e diga como usar para o objetivo da pessoa: aponte de volta para o `Objetivo prático` e o `Objetivo abstrato` que ela mesma respondeu, e explique em uma frase como esse arquivo orienta o trabalho a partir dali.

## Onde o documento vive e como ele é lido

O `start_here.md` vai no espaço dedicado a arquivos do projeto (ou numa pasta no computador local, dedicada ao projeto).

**Em espaços dedicados a arquivos do projeto dentro do app do provedor da IA:** ele não funciona sozinho, é preciso pedir à instância que o leia no início do trabalho. Vale guardar e atualizar um arquivo de memória do projeto, é o que permite retomar o trabalho sem reler tudo do zero.

**Em espaços dedicados no seu computador, pasta de projetos/repositórios:** funciona se traduzida conforme a configuração descrita em https://github.com/whatevertr/nud-constellation-method.

## Complemento

`how_to_work_with_me` (skill `nud-como-trabalhar-comigo`) e os arquivos de papel (skill `nud-agentes`) complementam este documento. NUD recomenda usar os três documentos.

---
Para entender melhor ou se aprofundar, repositório: https://github.com/whatevertr/nud-constellation-method & tumblr: https://tumblr.com/nerdunitdescription
