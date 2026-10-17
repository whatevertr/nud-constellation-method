# Era 3: configs e hooks
*Usa as Eras 1 e 2 e acrescenta a configuração da plataforma.*

**O que melhorou em relação à Era 2:** os documentos deixaram de ser arquivos que a pessoa pede pra instância ler e viraram **configuração**:
- o agente nomeado (a função vira um perfil);
- a casa (abrir uma pasta e a instância já nascer sendo o agente);
- as listas do que ela não executa e do que pergunta antes;
- os hooks, que barram uma ação antes de ela acontecer.

O contexto passou a chegar sozinho, e os guardrails passaram a valer sem depender do modelo lembrar deles.

## Duas camadas que se reforçam

- **Guardrails determinísticos**: paredes que não dependem do modelo (o que ele não pode executar, onde não pode escrever), mecânico. Chegam nesta era.
- **Piso epistêmico**: o da Era 1 (as regras em prosa que os agentes carregam; ver [`METHOD.md`](../era-1-triad/METHOD.md)). Continua valendo: um não substitui o outro.

## O que tem aqui

- [`WHERE_TO_CONFIGURE.md`](WHERE_TO_CONFIGURE.md): onde cada camada mora em cada plataforma testada (Claude Code, Hermes, Codex);
- [`example/COMO_USAR.md`](example/COMO_USAR.md): o que muda em relação à Era 2 e como instalar;
- [`example/`](example/): a mesma pasta da Era 2 virando configuração: os `CLAUDE.md` (o manual, a galaxy, a casa e a porta), o `settings.json` da casa e dois hooks (`ultimo_estado.py`, que entrega o último estado ao abrir, e `nao_apagar.py`, que barra o apagar), mais o perfil do agente.
