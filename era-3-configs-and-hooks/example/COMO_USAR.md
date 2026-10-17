# Como usar a Era 3
*O mesmo esqueleto da Era 2: o que era arquivo pra pedir pra ler vira configuração que carrega sozinha. Testado no Claude Code; no Codex, as regras chegam pelo `AGENTS.md` de cada pasta.*

**O que muda em relação à Era 2:**
- o manual vira o `CLAUDE.md` da raiz (vale pra todas as pastas de baixo), e a porta vira o `CLAUDE.md` da mission;
- a casa do thinker tem um `CLAUDE.md` (quem ele é, o que faz ao acordar e ao fechar) e um `.claude/settings.json`;
- o `settings.json` diz quem mora ali (`agent`), o que nunca se executa (`deny`), o que se pergunta antes (`ask`) e liga os dois hooks;
- **os hooks:** `ultimo_estado.py` entrega o último estado e o último diário sozinho, ao abrir; `nao_apagar.py` barra o comando de apagar antes de ele acontecer.

**Pra instalar:**
1. Copie a pasta `cosmos/` pra pasta da pessoa (fora de pastas sincronizadas, sem espaço nem acento no caminho).
2. No `settings.json`, troque `{PYTHON}` pelo caminho completo do Python 3.10 ou mais novo e `{COSMOS}` pelo caminho da pasta `cosmos` (os dois com barras `/`).
3. O perfil do agente: copie `agents/thinker.md` pra pasta de agentes do usuário (`~/.claude/agents/`) e cole o corpo do modelo `era-1-triad/skills/nud-agentes/modelos/thinker.md` embaixo do cabeçalho.
4. Abra uma sessão nova com a pasta `module_thinker` como pasta de trabalho: na primeira resposta, o thinker tem que falar do bloco `=== ÚLTIMO ESTADO ===`.

Onde cada camada mora em cada plataforma: [`WHERE_TO_CONFIGURE.md`](../WHERE_TO_CONFIGURE.md).
