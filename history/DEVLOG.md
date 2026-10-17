# Devlog — registro de mudança e correção

O que muda aqui, quando e por quê. Inclui o que a conferência derrubou, inclusive contra mim. Registro curto, sem narrativa.

---

## 16/10/2026 — o repositório se organiza por eras, e chega a Era 4

**Mudou:** o repositório passou a ter uma pasta por era (`era-1-triad`, `era-2-states-and-diaries`, `era-3-configs-and-hooks`, `era-4-scripts-and-interface`), cada uma só com o que aquela era acrescenta; quem usa uma era usa as anteriores. A história (cronologia, este devlog e o `FOUNDATIONS.md`) foi para `history/`. Entrou a Era 4: o modelo de pastas `cosmos`, com o registrador, os hooks de chegada, de alma e de mission, e o galley (busca híbrida no passado), testado do zero no Windows. Entrou na raiz a skill `nud-install-constellation-method`, que conversa com a pessoa e instala a Era 4; a `nud-agentes` voltou a só entregar os três perfis. O `METODO.md` se desmontou por era: o piso ficou na Era 1 (`METHOD.md`), os guardrails determinísticos foram para a Era 3, e o degrau, o apoio e as leituras foram para `history/FOUNDATIONS.md`. O README foi reescrito: instalar em destaque, o que é, a hipótese e o que cada era melhorou. Nomes de pasta e de arquivo em inglês; o conteúdo segue bilíngue.

**Por quê:** a cada escala nova o repositório era reestruturado. Com uma pasta por era, a próxima era é só mais uma pasta. E o método é um só, o da era mais recente: as anteriores são os degraus que levaram até ele, não opções de produto.

**O degrau mudou:** o método passa do primeiro para o segundo degrau (reproduzível): pelo menos três pessoas além da autora usaram e reproduziram o método. Duas relataram melhora no resultado; são relatos, não medição, então o terceiro degrau segue vago.

**O que a conferência derrubou:**
- O guia de instalação prometia que o galley funcionava "sem nada instalado". O teste de instalação passou 12/12, mas na máquina de teste o Ollama estava ligado: o caminho sem Ollama nunca rodou, e o teste não tinha como pegar o problema. Relendo o código, a chamada ao Ollama no `fatiador.py` não tinha plano B (o `buscador.py` tinha): sem o Ollama, o fatiador pararia com erro. Isso foi visto no código, não numa execução. Corrigido: sem o Ollama, o fatiador guarda os pedaços e avisa. O conserto foi testado simulando o Ollama desligado: o fatiador guardou os pedaços e a busca por palavra achou o trecho.
- O `FOUNDATIONS` dizia que o mesmo modelo varia "dezenas de pontos" de uma estrutura para outra. A versão atual do Harness-Bench (v2, 15/10/2026) mostra até 16 pontos percentuais, mediana perto de 8, com uma rodada por combinação. Corrigido para o que a fonte sustenta.

*EN: the repository is now organized by era, one folder each, holding only what that era adds; each era uses the ones before it. History (chronology, this devlog, FOUNDATIONS) moved to `history/`. Era 4 arrives: the `cosmos` folder model with the registrar, the arrival/soul/mission hooks and the galley (hybrid search over the past), tested from scratch on Windows. A root skill, `nud-install-constellation-method`, talks with the person and installs Era 4; `nud-agentes` goes back to delivering the three profiles. `METODO.md` was split by era. The README was rewritten with install up front. Folder and file names are now in English. Why: the repo was being restructured at every new scale; now a new era is just a new folder, and the method is one, the latest era's. The rung moves to the second (reproducible): at least three people besides the author used and reproduced it; two reported better results, which are reports, not measurement. What the check knocked down: the guide promised the galley worked with nothing installed, and the install test passed 12/12, but the test machine had Ollama running, so the no-Ollama path never ran. Rereading the code, `fatiador.py` had no fallback for Ollama (the search script did): without it, the slicer would stop with an error. This was seen in the code, not in a run. Fixed: without Ollama it keeps the pieces and warns; the fix was tested with Ollama simulated off. Also: FOUNDATIONS said the same model varies "tens of points" across harnesses; the current Harness-Bench (v2, Oct 15 2026) shows up to 16 percentage points, median near 8, one run per combination. Corrected to what the source supports.*

## 13/09/2026 — as imagens entram

**Mudou:** entrou a imagem da **estrutura de contexto** (os três agentes e o acesso de cada um às pastas) no topo da seção "Onde usar" dos dois READMEs, e a imagem das **três skills** (skill / você faz / você recebe) no topo de `skills/README.md`. Todas em `<picture>` com versão dia (padrão) e noite (modo escuro), SVG. Arquivos em `assets/` e `skills/assets/`. A árvore de pastas em texto continua abaixo da imagem, para copiar os nomes.

*EN: the context-structure image (the three agents and each one's folder access) goes at the top of "Where to use" in both READMEs, and the three-skills image at the top of skills/README.md. Both as `<picture>` with day/night SVG. The text folder tree stays below the image, for copying names.*

## 12/09/2026 — README vira "como usar", a explicação vai para METODO.md, e a nud-agentes vira o guia de montagem

**Mudou:** o README (PT) foi reordenado: uma frase, "O que é" (a história no lugar de "O problema"), contexto mínimo, agentes, **como usar** (as três skills, em ordem, com um exemplo datado no Claude Cowork), onde usar (a estrutura de pastas) e links. Saíram do README e foram para `METODO.md`: dois modos, as duas camadas, as duas regras da honestidade, o degrau, em que me apoio e as leituras. Cortados de vez: "+ contexto = + tokens" e "onde funciona e onde não". A skill `nud-agentes` deixou de só entregar os três perfis: agora carrega o contexto do método (`contexto/ambiente.md`, mais cópias fiéis de `METODO.md` e `ONDE_CONFIGURAR.md`) e um passo a passo de montagem que conversa antes de fazer, pede os documentos das outras duas skills, entrega os perfis e monta junto, no tamanho que a pessoa escolher. Nos seis perfis (`agents/` e `modelos/`): o "[a preencher]" de conectores virou uma frase que já funciona vazia, e as pastas de trabalho passaram a usar os nomes do desenho (`_task/`, `_output/`, `_states/`).

**Por quê:** leitores (inclusive um teste em casa) não entendiam o que fazer: o README explicava o que é, não o que fazer; a skill dos agentes cuspia três arquivos e a instância ficava confusa. Documentação tem tipos que não se misturam: o README passa a ser o "como usar", a explicação mora num arquivo próprio, e a skill precisa funcionar sozinha, para quem baixou só ela.

**Também:** `skills/README.md` novo (apresenta as três, ordem, instalação) e um `.zip` por skill dentro de `skills/`, gerado por `skills/build_zips.py` (rodar depois de qualquer mudança numa skill). As cópias dentro da `nud-agentes` foram adaptadas para tom de instrução (não são mais cópias byte a byte; a nota no topo diz "adaptado de").

**Pendente:** a imagem do harness volta ao README e uma imagem entra em `skills/README.md`; os READMEs de cada skill podem ser aposentados agora que existe o da pasta; as cópias dentro da skill precisam mudar junto com os arquivos-fonte.

*EN: the PT README was reordered into a "how to use" (one sentence, the story, minimum context, agents, the three skills in order with a dated Claude Cowork example, folder structure, links); the explanation moved to `METODO.md`; two sections were cut. The `nud-agentes` skill now carries the method's context and a step-by-step that talks before doing, asks for the other two documents, delivers the profiles and builds the setup with the person, at the size they choose. Profiles: the "[to fill]" placeholder became a sentence that works empty; work folders now match the diagram names. Why: readers could not tell what to do. Pending: the harness image, and keeping the in-skill copies in sync with their sources.*

## 03/09/2026 — exemplos de deny comparaveis, e "guardrail" no lugar de "parede"

**Mudou:** em ONDE_CONFIGURAR.md, os tres exemplos de deny passam a negar o mesmo comando (`rm`), com uma linha extra mostrando a granularidade por argumento do Codex. "parede" vira "guardrail" em todo o arquivo.

**Por que:** os exemplos usavam comandos diferentes (`rm`/`del` contra `git push --force`), o que fazia parecer que negavam coisas diferentes; e "parede" e metafora, "guardrail" e o termo reconhecido, ja usado no README. Apontado por um leitor.

*EN: the three deny examples now block the same command (`rm`), with an extra line showing Codex's argument-level granularity; "wall" becomes "guardrail" throughout. The examples had used different commands, which made them look like they blocked different things; flagged by a reader.*

## 02/09/2026 — três skills no lugar de uma, e a escala em pastas

**Mudou:** a skill única virou três, uma por peça da tríade. Entrou a tabela de onde configurar cada camada por plataforma, e uma prévia do modelo mínimo de fluxo de contexto em pastas. Os três perfis de agente ganharam guardrails e limite alinhado ao uso real. Saíram as ilustrações e o PDF de exemplo.

**Por quê:** cada peça precisa ser usável sozinha. A skill única obrigava a carregar as três para usar uma.

**O que a conferência derrubou:** a primeira montagem copiou os arquivos de regras inteiros para dentro de cada skill e acrescentou uma seção mandando a instância ignorar as partes que não eram dali. Instruir a ignorar não é separar. Refeita desmembrando os arquivos, cada skill com o trecho que é seu. A fidelidade das frases foi verificada por comparação byte a byte, não por leitura.

*EN: one skill became three, one per layer, so each can be used on its own. Added a table of where each layer is configured per platform, and a first sketch of the folder model. The three agent profiles gained guardrails and a realistic turn limit; illustrations and the sample PDF were removed. What the review rejected: the first build copied the rule files whole into each skill and told the instance to ignore what did not belong there. Instructing to ignore is not separating. Rebuilt by actually splitting the files; sentence fidelity verified by byte-level comparison, not by reading.*

## 21/08/2026 — uma frase minha, maior que a evidência

**Mudou:** o README dizia que o harness "move o resultado tanto quanto o próprio modelo". Corrigido para o que a fonte sustenta.

**Por quê:** Harness-Bench mede o gap **entre harnesses** no mesmo modelo, não harness contra modelo. Conferência cega (três juízes independentes) rebaixou a afirmação para insuficiente.

*EN: my own blind review demoted a claim; the README now says what the source actually measures (a gap between harnesses, not harness vs. model).*

## 21/08/2026 — um absoluto virou decisão de engenharia

**Mudou:** o MANIFESTO dizia "nenhuma defesa interna ao modelo é confiável". A versão nova preserva a decisão de projeto sem alegar impossibilidade.

**Por quê:** era uma alegação que eu não provei, e há resultados de mitigação por inferência na literatura. O porquê arquitetural fica explícito: personalização pode amplificar concordância, então Manual e Função não moram no mesmo documento.

*EN: replaced an absolute ("no internal defense is reliable") with the engineering decision it always was; personalization and checking now explicitly live in separate documents.*

## 21/08/2026 — citação atualizada e ressalva acrescentada

**Mudou:** Jain et al. saiu de preprint para publicação revisada (CHI 2026). O número virou "até +45% no caso medido" (topo da faixa, Gemini 2.5 Pro; +33% Claude Sonnet 4; +16% GPT 4.1 Mini). Acrescentada a ressalva de que o efeito não é universal: dos cinco modelos testados, o Llama 4 Scout não muda significativamente com perfil de memória e o GPT 5.1 não muda com nenhum dos dois contextos.

**Por quê:** citar o número de topo sem a faixa e sem as exceções é overclaim.

**O que a conferência derrubou:** uma conferência anterior marcou "+33% Sonnet 4" e "+16% GPT 4.1 Mini" como inexistentes no paper. Reabrir a fonte mostrou que existem (Abstract p. 2, §4.1 p. 8). A conferência corrigiu a própria conferência.

*EN: Jain et al. citation upgraded to the peer-reviewed CHI 2026 version; the figure is now "up to +45% in the measured case" (top of range, Gemini 2.5 Pro; +33% Claude Sonnet 4; +16% GPT 4.1 Mini), with the caveat that the effect is not universal. An earlier check had marked two of those figures as absent from the paper; reopening the source showed they exist. The review corrected its own review.*
