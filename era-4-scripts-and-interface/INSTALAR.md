# INSTALAR.md: a Era 4 do Constellation Method
*Escrito pra IA que vai instalar o método pra uma pessoa. Se você é a pessoa, pode ler também: não tem segredo. Pensado pro Claude Code (app desktop ou terminal). Testado do zero no Windows em 16/10/2026.*

## Antes de instalar: converse
Leia a tese do repositório e converse com a pessoa: como ela trabalha, o que ela faz com IA, onde ela trava. Diga com honestidade se vale a pena.

**O método pede atenção, não manutenção.** Na Era 4, quem registra é o agente (pelo registrador) e quem entrega o contexto são os hooks. O que fica com a pessoa é conferir o que a IA entrega e fechar o dia com um resumo. Pra quem trabalha com IA todo dia e quer mais qualidade e continuidade, esta é a era mais leve. Pra uso pontual, ou pra quem não vai conferir nada, ele ainda pesa mais do que ajuda. Se for testar, comece pequeno.

## O que vem neste pacote
```
cosmos\                         a raiz: regras que valem pra todo agente
└─ galaxy_example\              um universo de trabalho, com um Tars só
   ├─ station\module_thinker\   a casa do thinker: CLAUDE.md (a ficha e o jeito de trabalhar),
   │                            diary\ (o diário), galley\ (a busca no passado),
   │                            .claude\settings.json (os hooks)
   ├─ missions\                 o trabalho; uma mission de exemplo, com lab\storage|output|tasks
   ├─ matrix\                   as skills (de contexto e de ofício)
   ├─ tools\                    registrar, leitor, os 3 hooks, fatiador e buscador (o galley)
   ├─ _to_delete\               a lixeira (só a pessoa esvazia)
   └─ _archived\                o que acabou, guardado
```
**As duas memórias:**
- **a memória de trabalho** é o **log** (`log.jsonl`, escrito só pelo `registrar.py`): o que foi feito, decidido e o que falta;
- **a memória de convívio** é o **diário** (`diary\`): o registro, em primeira pessoa, de como foi trabalhar junto naquele dia.

**Os hooks que entregam as duas, sozinhos:**
- **o de chegada:** quando a sessão abre, entrega o último resumo, as tarefas e as missions;
- **o da alma:** entrega o último diário. "Alma" é o nome que o método dá a isto: o que o agente recebe ao acordar sobre quem ele é e como vocês trabalham juntos. É texto, escrito e lido; não é promessa de consciência;
- **o de mission:** ao tocar numa mission, entrega o resumo dela.

**O galley:** a busca no passado (nos diários e nos registros antigos). Funciona **sem nada instalado**, por palavra: acha quando a pergunta usa as mesmas palavras do texto ("combinado" não acha "combinamos"). Esse limite diminui com o [Ollama](https://ollama.com) e o modelo `qwen3-embedding:0.6b`: aí a busca é também por sentido. O modelo não vem no pacote; a pessoa instala, se quiser. Se o Ollama não responder, o galley cai sozinho na busca por palavra. Fatiar o passado só vale quando ele já não dá pra ler inteiro (uma dezena de arquivos, mais ou menos).

## Passo a passo
1. **Onde mora.** O lugar recomendado é `C:\Users\<nome da pessoa>\cosmos` (no Mac ou Linux, `~/cosmos`): fica na pasta da pessoa, fora de pastas sincronizadas (OneDrive e afins sincronizam no meio do trabalho e confundem os agentes), sem espaço nem acento no caminho. Copie a pasta `model\cosmos\` pra lá.
2. **O Python.** As ferramentas usam só a biblioteca padrão do Python 3.10 ou mais novo. Ache o caminho completo do executável da máquina (no Windows, `where python` ou `py -0p`; cuidado com o atalho da Microsoft Store, que abre a loja em vez do Python). Use sempre o caminho completo.
3. **Os marcadores.** Troque em todos os `.md` e `.json`:
   - `{PYTHON}` → o caminho do Python (no `settings.json`, com barras `/`);
   - `{COSMOS}` → o caminho da pasta `cosmos` (no `settings.json`, com barras `/`);
   - `{AAAA-MM-DD}` → a data de hoje;
   - `{nome da pessoa}`, `{como ela prefere trabalhar}` e os outros `{…}` → com a pessoa, conversando.
4. **Os nomes.** Se a pessoa quiser, renomeie `galaxy_example` e `module_thinker` (e atualize os caminhos do `settings.json` e do `CLAUDE.md` da casa). O `thinker:` do cabeçalho é o nome que o log usa: escolha agora, porque ele não muda depois.
5. **A ficha.** Preencha com a pessoa o cabeçalho do `module_thinker\CLAUDE.md`. O diário de exemplo pode ser apagado (ou substituído) no primeiro dia: o primeiro diário de verdade, o thinker escreve ao fechar.
6. **O primeiro registro.** Rode, da pasta da casa:
   ```
   "{PYTHON}" "{COSMOS}\galaxy_example\tools\registrar.py" "{COSMOS}\galaxy_example\station\module_thinker" --por thinker --tipo nota --tag organizacao --txt "Primeira linha: instalação feita."
   ```
   Tem que voltar `REGISTRADO`.

## Como saber que deu certo
1. Abra uma sessão nova do Claude Code **com a pasta da casa** (`module_thinker`) como pasta de trabalho.
2. Na primeira resposta, o thinker tem que falar do bloco **`=== CHEGADA (hook, Era 4) ===`** e do **`=== ALMA ===`**. Se vieram, a memória continuada está ligada.
3. Peça pra ele registrar uma tarefa na `my-first-mission` e depois buscar no galley. Se os dois funcionarem, está instalado.

**Se a chegada não veio:** confira o caminho do Python no `settings.json` (caminho completo, barras `/`), e se a sessão foi aberta na pasta da casa (os hooks moram no `.claude\settings.json` dela).

**No Codex (ou outro agente):** cada pasta tem um `AGENTS.md` que aponta pro `CLAUDE.md` do lado, então as regras chegam. Os hooks (chegada, alma, mission) foram testados só no Claude Code; em outro agente, peça pra ele rodar, ao abrir, `"{PYTHON}" "{COSMOS}\galaxy_example\tools\leitor.py" chegada "{COSMOS}\galaxy_example\station\module_thinker"`.

## O que este pacote não traz
- **O perfil de agente** (`.claude\agents\<nome>.md`, a alma que vai junto em toda sessão), **de propósito**: o perfil nasce da Tríade, escrito com a pessoa, a partir de como ela trabalha. Um perfil pronto seria de outra pessoa.
- **A guarda** (um hook que barra cada agente fora da área dele): cada pessoa tem as suas áreas; uma versão genérica vem depois.
- **O app painel** (a vista das missions, tarefas e indicadores): numa próxima entrega.

## Uma última coisa
Se, depois de conversar, você achar que o método não serve pra essa pessoa, diga. Esse também é o método funcionando.
