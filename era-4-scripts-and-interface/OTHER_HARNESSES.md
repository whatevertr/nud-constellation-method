# Levar a Era 4 para outro harness

*O modelo da Era 4 foi feito e testado no Claude Code. Este arquivo conta o que cada peça faz, pra que a instância de outro harness (Codex, Hermes, OpenCode) ache o equivalente no próprio sistema. É um começo: o que está marcado com 🍷 ainda não foi testado.*

> **Nota para a instância que estiver lendo este arquivo.** Não copie os hooks como estão: eles leem o formato que o Claude Code manda e respondem no formato que ele espera. Leia a **intenção** de cada peça, ache o evento equivalente no seu harness e escreva um adaptador fino que chama a mesma lógica. Peça autorização antes de criar ou alterar qualquer configuração.

## O que viaja sem mudar

Estas peças são scripts Python que leem e escrevem arquivos. Funcionam em qualquer harness que rode um comando no terminal:

- **o registrador** (`registrar.py`): a porta única do log. O agente chama por linha de comando; ele valida a linha e escreve no `log.jsonl`;
- **o leitor** (`leitor.py`): lê os logs e monta o texto da chegada e os dados do painel;
- **o buscador e o fatiador** (`buscador.py`, `fatiador.py`): a busca no passado, por sentido e por palavra;
- **o painel** (`app/`): só lê os logs; não depende do harness.

A porta (`CLAUDE.md` em cada pasta) também viaja: o Codex e o OpenCode leem `AGENTS.md`, e o Hermes lê os dois. Onde o harness só lê `AGENTS.md`, o conteúdo é o mesmo.

## O que depende do harness: os hooks

| Peça | A intenção | Quando dispara no Claude Code | O que entra | O que sai |
|---|---|---|---|---|
| **a chegada** (`hook_chegada.py`) | ao abrir a conversa, a instância já sabe onde parou: o último resumo, as tarefas, as decisões e as missions | `SessionStart` (abrir, voltar, limpar, compactar) | a pasta de trabalho (`cwd`) | o texto da chegada, que vira contexto no começo da conversa |
| **a alma** (`hook_alma.py`) | a instância chega sabendo quem é com a pessoa: o último diário | `SessionStart` | a pasta de trabalho | o texto do diário, como contexto; nunca em subagente |
| **a mission** (`hook_mission.py`) | na primeira vez que a instância toca num arquivo de uma mission, recebe o resumo dela | `PostToolUse` nas ferramentas de ler e escrever arquivo | o caminho do arquivo tocado | o resumo da mission, como contexto extra (uma vez por sessão) |
| **a guarda** (`guarda.py`) | cada agente fica fora da casa de quem está acima dele | `PreToolUse` nas ferramentas de arquivo e terminal | o nome do agente, a ferramenta e o caminho | permitir, ou negar com o motivo |

## Os equivalentes que conhecemos

| Peça | Hermes | Codex | OpenCode |
|---|---|---|---|
| **a chegada e a alma** | o hook que roda antes de cada chamada ao modelo pode injetar contexto. 🍷 Não há evento de "abriu a sessão": injete uma vez só, anotando a sessão num arquivo temporário (como faz o `hook_mission.py`) | `SessionStart`, experimental desde março de 2026 🍷 | um plugin que escuta o evento de sessão criada 🍷 |
| **a mission** | o hook depois da ferramenta 🍷 | `PostToolUse`, mas só para comandos de terminal 🍷 | um plugin depois da execução da ferramenta 🍷 |
| **a guarda** | o hook antes da ferramenta, que pode bloquear | `PreToolUse`, mas só para comandos de terminal: a escrita de arquivo passa por fora 🍷 | um plugin antes da execução da ferramenta, que pode bloquear 🍷 |
| **onde mora** | scripts na pasta de hooks do perfil | arquivo próprio de hooks, ativado por chave de funcionalidade | plugins em TypeScript na pasta do projeto ou na global |

Fontes: o Hermes foi lido no código-fonte (31/08/2026); o Codex e o OpenCode, em guias e na documentação pública (19/10/2026). Os nomes de evento mudam entre versões: confira na documentação do harness antes de aplicar.

## Como fazer o adaptador

1. Leia o que o seu harness manda pro script (em geral, um JSON na entrada) e ache o equivalente de: a pasta de trabalho, o nome do agente, a ferramenta e o caminho.
2. Chame a mesma lógica: o leitor, pra chegada; o diário mais recente, pra alma; o log da mission, pra mission; a regra da hierarquia, pra guarda.
3. Responda no formato que o seu harness espera: texto pra injetar contexto, ou a decisão de bloquear.
4. Teste com o `teste_guarda.py` (a guarda) e abrindo uma conversa nova (a chegada e a alma).

Se o seu harness não tem hook nenhum, o método ainda funciona como na Era 2: a instância lê o estado e o diário ao abrir, e escreve os dois ao fechar.
