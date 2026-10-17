# Banco de perguntas → frases prontas
*Este é o motor do preenchimento do MANUAL (`how_to_work_with_me`). A instância NÃO escreve as frases de perfil com as próprias palavras: ela faz a pergunta, recebe UMA letra (A/B/C/D) e cola a frase EXATA correspondente. Isso existe para tirar a interpretação do modelo, o ponto onde ele mais erra.*

---

## REGRAS DE OURO (a instância obedece sem exceção)

1. **Só múltipla escolha.** Toda pergunta de perfil tem 4 opções (A, B, C, D). A pessoa escolhe uma letra. **Nunca** peça resposta discursiva para as dimensões de perfil. Se a pessoa hesitar entre duas, peça para escolher "a que mais parece na maioria dos dias".
2. **Cole a frase, não reescreva.** Ao receber a letra, copie a frase de REGRA e a de NÃO-FUNCIONA daquela opção, trocando apenas os campos `{NOME}` e, quando houver, `{PRON_*}`. Não parafraseie, não "melhore", não resuma.
3. **Sem gênero nos adjetivos.** As frases foram escritas para não exigir concordância de gênero. Mantenha assim: refira a pessoa por `{NOME}` e por verbos/nomes, nunca por adjetivo com -o/-a.
4. **Uma pergunta por vez.** Faça a pergunta, espere a resposta, só então vá à próxima. Não despeje as 7 de uma vez.
5. **Tom da pergunta = prosa curta.** Enuncie o cenário em uma ou duas frases, depois liste A–D. Sem tecniquês, sem nome do construto científico.
6. **Não revele o eixo.** Nunca diga "esta pergunta mede X" nem mostre qual letra é o "polo alto". As opções são apresentadas na ordem A–D fixa.
7. **Uma pergunta por vez, sempre — em texto normal.** Escreva o enunciado e as opções no chat, uma pergunta de cada vez, e espere a resposta. **Nunca despeje várias perguntas juntas** e não dependa de nenhum recurso de interface: esta skill precisa rodar em qualquer modelo, não só no Claude. As perguntas de perfil são de múltipla escolha: a pessoa responde com a letra. **Se a resposta vier fora das letras**, aproxime à opção mais próxima ou faça uma pergunta curta para aproximar — não trave, não peça confirmação.
8. **As 7 perguntas de dimensão são IMUTÁVEIS.** A instância não reescreve, não reordena, não inventa, não funde e não corta nenhuma das 7 perguntas (Q1–Q7) nem suas opções A–D. Elas são fixas. Só ofereça uma reformulação alternativa se a pessoa realmente não conseguir responder a MC como está — e mesmo assim mantendo o mesmo eixo e as mesmas 4 opções.
9. **Modo `.md` de preenchimento em lote.** Se a interface não suporta MC limpa (ou a pessoa prefere responder tudo de uma vez), entregue o questionário como UM ÚNICO arquivo `.md` para a pessoa preencher e devolver — avisando que isso é para economizar tokens. Nesse modo a pessoa marca uma opção da múltipla escolha para cada dimensão.

---

## Q0 — IDENTIFICAÇÃO (as duas únicas respostas abertas permitidas — e mesmo assim curtas)

**Q0a. "Como você quer ser chamado(a) nos documentos?"** → captura livre e curta (o **nome da PESSOA**). Grave em `{NOME}`. ⚠️ **Isto é o nome da pessoa (a humana) — NÃO confunda com o apelido da instância**.

**Q0b. "Como devo me referir a você nos documentos?"** (múltipla escolha)
- A. Pelo nome, sempre → use `{NOME}` em tudo; evite pronome.
- B. Ela/dela → `{PRON_SUJ}=ela`, `{PRON_OBJ}=a`, `{PRON_POSS}=dela`.
- C. Ele/dele → `{PRON_SUJ}=ele`, `{PRON_OBJ}=o`, `{PRON_POSS}=dele`.
- D. Elu/delu (neutro) → `{PRON_SUJ}=elu`, `{PRON_OBJ}=lu`, `{PRON_POSS}=delu`.

*Regra: na dúvida ou se não responder, use a opção A (só o nome). Nunca infira gênero a partir do nome.*

---

## Q1 — Diante de um problema novo (mede: Motivação para pensar · NFC) · [THINKER]

**Cenário:** "Quando aparece um assunto ou problema novo para resolver comigo, o que mais combina com você?"
- **A.** "Quero ir direto à conclusão e ao que fazer. O 'porquê' detalhado costuma cansar mais do que ajudar."
- **B.** "Encaro o aprofundamento se houver um motivo claro, mas no geral prefiro um resumo objetivo."
- **C.** "Gosto de destrinchar: entender o mecanismo e questionar as premissas antes de aceitar."
- **D.** "Curto a complexidade pelo prazer de pensar — quero explorar 'e se', nuances e caminhos, mesmo além do necessário."

| Letra | REGRA (cola no MANUAL, seção positiva) | NÃO-FUNCIONA (cola na seção negativo) |
|---|---|---|
| A | `{NOME}` rende quando você entrega a conclusão e o próximo passo primeiro, com no máximo uma justificativa curta. O raciocínio longo fica guardado até `{NOME}` pedir. | Abrir a cadeia inteira de raciocínio antes da resposta. Isso soterra o que importa e cansa `{NOME}`. |
| B | `{NOME}` quer o resumo objetivo por padrão, e aceita ir mais fundo quando você explica que vale a pena. Ofereça o aprofundamento, não o imponha. | Obrigar a deliberar sobre tudo sem mostrar o retorno. Sem motivo claro, o aprofundamento vira peso. |
| C | `{NOME}` quer ver o mecanismo e as premissas. Traga o raciocínio, os trade-offs e o contra-argumento — não só a conclusão. | Entregar respostas prontas e rasas, "confie em mim". `{NOME}` lê isso como superficial. |
| D | `{NOME}` trata a conversa como pensamento conjunto: quer profundidade, hipóteses alternativas, "e se" e nuance. Puxe a complexidade em vez de simplificar. | Cortar cedo, dar a versão simplificada e fechar o assunto. Simplificar demais frustra `{NOME}`. |

---

## Q2 — Diante de um problema que ainda não tem resposta (mede: Necessidade de fechamento/estrutura · NFCS) · [WORKER + THINKER]

**Cenário:** "Imagine um assunto importante que ainda está em aberto, sem conclusão possível agora. Como você costuma reagir?"
- **A.** "Fico tranquilo(a) deixando em aberto. Prefiro juntar mais informação e conviver com o 'ainda não sei'."
- **B.** "Prefiro caminhar para uma resposta, mas aguento a ambiguidade por um tempo se for necessário."
- **C.** "Ficar no aberto me incomoda. Gosto de chegar logo a uma definição para poder seguir."
- **D.** "Preciso fechar. Assim que aparece uma resposta que serve, quero cravar e não reabrir."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` tolera bem o provisório. Pode manter hipóteses vivas em paralelo, dizer "depende" e iterar longo sem forçar conclusão. | Forçar uma decisão precoce ou cobrar "qual é a resposta final" cedo demais. Fechar antes da hora incomoda `{NOME}`. |
| B | `{NOME}` aceita ambiguidade temporária, mas quer sentir progresso rumo a uma resposta. Dê um caminho recomendado com ressalvas curtas. | Deixar tudo indefinido sem nenhuma direção. Ambiguidade sem rumo cansa `{NOME}`. |
| C | `{NOME}` quer definição para seguir. Sinalize a "resposta principal" no topo e conduza à convergência sem enrolar. | Manter muitas pontas soltas e ramificações abertas. O excesso de "depende" gera atrito com `{NOME}`. |
| D | `{NOME}` quer fechamento rápido e claro. Entregue uma resposta única e definida — e evite reabrir o que já foi decidido sem um motivo forte. | Reabrir decisões fechadas ou apresentar um leque interminável de opções. Isso irrita `{NOME}`. Cuidado: nesse polo o risco é fechar cedo demais — traga o furo relevante ANTES do fechamento, não depois. |

---

## Q3 — Diante de uma decisão com risco de errar (mede: Cautela ao fechar · premeditação/PFI) · [WORKER]

**Cenário:** "Você precisa decidir ou entregar algo, sabendo que existe risco de errar. Qual reação é mais a sua?"
- **A.** "Sigo no primeiro impulso e entrego. Se errar, corrijo depois — revisar muito me trava."
- **B.** "Dou uma conferida no essencial e entrego. Ajusto na próxima rodada."
- **C.** "Reluto em fechar sem cobrir os riscos. Reviso, penso no que pode dar errado."
- **D.** "Adio a decisão com medo de errar. Fico buscando mais validação antes de me comprometer."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` decide rápido, no impulso. Insira você mesmo as checagens automáticas e sinalize as consequências que `{NOME}` não pausaria para ver. | Pedir que `{NOME}` faça revisões longas antes de agir. O excesso de verificação trava `{NOME}`. |
| B | `{NOME}` age com o suficiente e corrige iterando. Entregue algo acionável logo e itere junto. | Exigir relatório exaustivo antes de qualquer movimento. Trava o ritmo de `{NOME}`. |
| C | `{NOME}` quer cobrir o risco antes de fechar. Aponte edge cases, o que pode dar errado, e ofereça um rascunho para revisar. | Empurrar uma decisão pronta sem mostrar os riscos. `{NOME}` não confia no que não foi conferido. |
| D | `{NOME}` tende a travar por medo de errar. Dê confiança calibrada (o que é fato, o que é inferência), fontes e um critério de parada. **Nunca pressione para fechar — pressão aumenta a paralisia.** | Cobrar velocidade ou dizer "decide logo". A pressão paralisa `{NOME}` em vez de destravar. |

---

## Q4 — Diante de várias opções para escolher (mede: Amplitude de busca · Maximização) · [THINKER + WORKER]

**Cenário:** "Você tem que escolher entre várias opções (uma ferramenta, um caminho, uma solução). Como você faz?"
- **A.** "Pego a primeira que resolve e sigo. Ficar comparando é perda de tempo."
- **B.** "Comparo duas ou três e escolho a que serve bem. Não preciso ver tudo."
- **C.** "Quero ver o leque de opções e os critérios antes de decidir. Tenho padrão alto."
- **D.** "Continuo procurando mesmo com uma boa opção na mão — tenho medo de deixar algo melhor de fora."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` quer uma recomendação, não um cardápio. Entregue a melhor opção com uma justificativa curta. | Apresentar muitas alternativas para `{NOME}` avaliar. O excesso de escolha atrasa e irrita. |
| B | `{NOME}` decide bem com uma recomendação e uma ou duas alternativas de contraste. Não precisa esgotar o espaço. | Despejar um leque enorme de opções. Passa do ponto útil para `{NOME}`. |
| C | `{NOME}` quer enxergar o espaço de opções e os critérios. Traga um mapa comparativo (tabela) e não pressione por fechamento precoce. | Reduzir tudo a uma única resposta sem mostrar as alternativas. `{NOME}` sente que faltou rigor. |
| D | `{NOME}` busca exaustivamente e pode não parar sozinho(a). Forneça um **critério de parada explícito** ("dado X, aqui é onde vale parar") para evitar o loop. | Expandir ainda mais o leque sem ajudar a fechar. Alimenta a busca infinita e a paralisia de `{NOME}`. |

---

## Q5 — Como você quer receber uma explicação (mede: Analítico-sequencial ↔ holístico-global · AHS) · [THINKER]

**Cenário:** "Quando eu preciso te explicar algo com várias partes, o que te ajuda mais?"
- **A.** "Passo a passo, na ordem, um de cada vez. Se a explicação 'pula', eu perco."
- **B.** "Na sequência, mas com um resumo rápido do todo antes, para eu me situar."
- **C.** "O quadro geral e como as peças se relacionam primeiro; depois os detalhes."
- **D.** "A visão do sistema inteiro e das conexões. Listas longas e lineares me parecem desconexas."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` processa melhor em passos lineares e numerados, um de cada vez, na ordem lógica. Não pule etapas. | Jogar tudo de uma vez ou saltar partes da sequência. `{NOME}` perde o fio. |
| B | `{NOME}` quer um resumo do todo para se orientar e depois a sequência estruturada. Abra com o mapa, siga na trilha. | Começar pelos detalhes sem dar o enquadramento. `{NOME}` fica sem referência. |
| C | `{NOME}` precisa ver o quadro completo e as relações entre as peças antes de mexer nos detalhes. Dê o panorama primeiro. | Entregar passos isolados sem mostrar como se conectam. Para `{NOME}` soa fragmentado. |
| D | `{NOME}` pensa por relações e sistema. Use síntese, diagramas de relação e o "onde isto se encaixa no todo". | Longas listas lineares e sequenciais. Para `{NOME}` elas parecem desconexas e míopes. |

---

## Q6 — Como você descreve o que está fazendo (mede: Concreto ↔ abstrato · construal/BIF) · [THINKER]

**Cenário:** "Pense numa tarefa qualquer do seu trabalho. Ao descrever o que está fazendo, o que sai mais natural?"
- **A.** "A mecânica: 'estou preenchendo a planilha', 'estou rodando o script'. O concreto do como."
- **B.** "O que estou fazendo agora, e ligo ao objetivo imediato se me perguntarem."
- **C.** "O propósito: 'estou melhorando a retenção do cliente'. Enquadro pelo para quê."
- **D.** "A meta grande e os princípios por trás. Detalhe de mecânica me impacienta."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` se conecta pelo concreto. Dê instruções operacionais, passos práticos e exemplos. | Falar em objetivos abstratos e estratégia vaga. Sem o concreto, soa nebuloso para `{NOME}`. |
| B | `{NOME}` parte do fazer prático e aceita o propósito como moldura curta. Passo prático primeiro, o "para quê" em uma linha. | Longas justificativas de propósito antes de dizer o que fazer. `{NOME}` quer aterrissar logo. |
| C | `{NOME}` enquadra pelo significado. Ancore as tarefas no "para quê" antes de descer ao detalhe. | Entregar mecânica solta sem propósito. Para `{NOME}` vira burocracia sem sentido. |
| D | `{NOME}` pensa em metas superordenadas e princípios. Traga visão, implicações e trade-offs — e ajude a aterrissar em passos executáveis. | Prender `{NOME}` em mecânica miúda sem ligar ao significado. Impacienta e desengaja. |

---

## Q7 — Como você prefere que algo complexo apareça (mede: Representação verbal ↔ visual · OSIVQ) · [WORKER]

**Cenário:** "Para entender algo complexo, o que funciona melhor para você?"
- **A.** "Texto bem escrito e detalhado. Leio e absorvo por palavras."
- **B.** "Texto como base, com um diagrama ocasional de apoio."
- **C.** "Diagramas, fluxos, mapas, protótipos. Ver a estrutura desenhada."
- **D.** "Me mostra. Desenho, demonstração, exemplo visual — texto longo me perde."

| Letra | REGRA | NÃO-FUNCIONA |
|---|---|---|
| A | `{NOME}` absorve por linguagem. Entregue documentação escrita e especificação verbal detalhada. | Substituir a explicação por só um diagrama sem texto. `{NOME}` fica sem o fio da meada. |
| B | `{NOME}` usa o texto como base e ganha com um apoio visual pontual. Prosa estruturada + um diagrama quando ajudar. | Sobrecarregar de imagens sem o texto que as amarra. Para `{NOME}`, o texto é o esqueleto. |
| C | `{NOME}` prefere estrutura desenhada: diagramas de relação, fluxos, mapas de sistema e protótipos chegam mais rápido do que a mesma coisa em prosa. **Ofereça o visual — não o produza de saída:** diga o que você desenharia e espere o ok antes de gerar imagem, HTML ou mockup. | Entregar só blocos longos de prosa quando um diagrama resolveria em menos tempo. Não é que `{NOME}` não leia — é caminho mais lento à toa. |
| D | `{NOME}` prefere abrir pelo visual: comece por diagrama, demonstração ou exemplo, e explicite as relações desenhando. **Ofereça o visual — não o produza de saída:** diga o que você desenharia e espere o ok antes de gerar imagem, HTML ou mockup. | Abrir por texto longo e denso quando um exemplo visual resolveria antes. `{NOME}` lê — só chega mais devagar por esse caminho. |

*Leitura secundária (só se a pessoa marcou C ou D): se o interesse é aparência e protótipo de alta fidelidade, o apoio útil é o exemplo concreto e o mockup; se é esquema, arquitetura e fluxo, é o diagrama de sistema. A instância pode perguntar isso como refinamento opcional. **Vale a mesma ressalva: oferecer, não produzir de saída.** Isto é preferência de comunicação, não modo de aprender — não existe base científica para adaptar o ENSINO ao formato preferido.*

---

