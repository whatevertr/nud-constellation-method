---
name: nud-como-trabalhar-comigo
description: >-
  Use quando o usuário pedir para criar/montar um "como trabalhar comigo", um
  "perfil de trabalho", "ensinar a IA a trabalhar do meu jeito", "perfil
  cognitivo de trabalho", ou quiser que a IA entenda como a cabeça dele
  funciona, ou ainda pedir para "montar meu contexto para IA", "criar meu
  manual de uso", ou trouxer um novo colaborador/instância e quiser gerar o
  documento que orienta como ele pensa e trabalha. A skill conduz uma
  entrevista curta (Q0a/Q0b + 7 dimensões, a maioria de múltipla escolha) e
  entrega o `how_to_work_with_me.md` preenchido.
  NÃO use para diagnóstico psicológico, teste de personalidade recreativo
  (MBTI/eneagrama) nem para avaliar terceiros sem a presença da pessoa.
license: CC-BY-4.0
metadata:
  author: Thainá Ramos (Nud by Whatevertr)
---

# nud-como-trabalhar-comigo, o MANUAL da Tríade de Contexto

Esta skill conduz a entrevista das 7 dimensões de perfil e entrega o arquivo
`how_to_work_with_me.md` preenchido, o "EU" da Tríade de Contexto: como a
cabeça da pessoa funciona, para a instância acompanhar o raciocínio dela em
vez de impor o próprio.

## Motor anti-interpretação e regra suprema

O ponto onde um modelo mais erra é interpretar. Por isso o perfil é preenchido **só por múltipla escolha**: você faz uma pergunta-cenário, recebe UMA letra (A/B/C/D) e **cola a frase EXATA** correspondente, sem parafrasear. Mecanismo em **`regras/perguntas_e_frases.md`**.

As sete dimensões, os cenários e as frases prontas são o material recomendado. Você **evita** criar dimensões, **evita** improvisar frases de perfil, **não** usa tipologias populares sem validade preditiva (MBTI, eneagrama, estilos de aprendizagem/VARK).

## Base de pesquisa, consulta da instância, não da pessoa

A base em `referencias.md` fica aqui para consulta da instância. A orientação durante a conversa é não encher a pessoa de informação: cite a base só se a pessoa perguntar, e evite conversa ao longo da entrevista; priorize terminar de preencher o documento para entrega e conclusão da tarefa desta skill.

## Passo a passo

1. **Leia** `regras/regras_de_preenchimento.md` e `regras/perguntas_e_frases.md` antes de começar.
2. **Conduza a entrevista, uma pergunta por vez, em texto normal no chat:** Q0a (nome da pessoa), Q0b (como referir), depois Q1 → Q7 (as 7 dimensões). Nunca despeje várias perguntas juntas; espere a resposta antes da próxima. Ao receber a letra, cole a frase EXATA de REGRA e a de NÃO-FUNCIONA daquela opção. Aponte para as Regras de Ouro em `regras/perguntas_e_frases.md`, não as reescreva.
3. **Preencha `modelos/how_to_work_with_me.md`** com as frases coladas, seguindo o cabeçalho e o rodapé conforme descrito em `regras/regras_de_preenchimento.md`.
4. **Pergunte à pessoa onde salvar o arquivo**, ou oriente a salvar na área dedicada do projeto.
5. **Entregue o arquivo na mesma resposta, com o convite leve em linguagem plana.** A redação do convite está em `regras/regras_de_preenchimento.md`, seção "Entrega"; use aquela redação.

## O que dizer à pessoa

Só este documento já tende a melhorar a interação com a IA. `nud-comece-aqui`
(a PORTA, sobre o projeto) e os arquivos de papel da skill `nud-agentes`
(worker/thinker/manager) complementam. NUD recomenda usar os três documentos.

## Onde o documento vive e como usá-lo

**Em espaços dedicados a arquivos do projeto dentro do app do provedor da IA:** ele não funciona sozinho, é preciso pedir à instância que o leia no início do trabalho. Vale guardar e atualizar um arquivo de memória do projeto, é o que permite retomar o trabalho sem reler tudo do zero.

**Em espaços dedicados no seu computador, pasta de projetos/repositórios:** funciona se traduzida conforme a configuração descrita em https://github.com/whatevertr/nud-constellation-method.

---
Para entender melhor ou se aprofundar, repositório: https://github.com/whatevertr/nud-constellation-method & tumblr: https://tumblr.com/nerdunitdescription
