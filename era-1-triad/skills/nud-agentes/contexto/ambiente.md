# O ambiente: os dois tamanhos e as pastas

Este arquivo existe para a instância conseguir montar o ambiente com a pessoa sem precisar do resto do repositório.

## Tamanho 1: projeto no app

Os três documentos (porta, manual, função) ficam no espaço do projeto dentro do app do provedor. A instância não lê sozinha: a pessoa pede, no início de cada trabalho, "leia a porta, o manual e a função antes de começar". Vale manter um arquivo de memória do projeto (o que foi decidido, onde parou), atualizado pela instância quando a pessoa pedir.

**Exemplo no Claude Cowork (setembro de 2026).** Os nomes dos campos mudam com o tempo; a lógica se mantém.

| Documento                          | Onde entra                                                                                  | Observação                                                                                                                                                                                                                |
| ---------------------------------- | ------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Manual** (`how_to_work_with_me`) | *Configurações → Geral → Instruções para o Claude*                                          | Vale para todas as conversas e para o Cowork. É onde a maioria das pessoas põe. Alternativa: nas *Instruções* do projeto, se a pessoa quiser separar por projeto.                                                         |
| **Porta** (`start_here`)           | *Instruções* do projeto (o campo de regras, no canto superior direito da página do projeto) | O objetivo do projeto também pode ir para a memória do projeto: a pasta `claude`, que a instância cria quando a pessoa pede. Essa pasta não é acessível pela pessoa e só aparece na interface depois que tem algo dentro. |
| **Função** (o perfil do agente)    | *Configurações → Cowork* (instruções que valem para todas as sessões do Cowork)             | Alternativa: nas *Instruções* do projeto, quando cada projeto tem um papel diferente. Se o projeto tem pasta conectada com uma porta própria (`CLAUDE.md`, `AGENTS.md` ou config), a porta manda.                         |

Em outros apps, procure o equivalente: um lugar de **instruções permanentes** (manual), um lugar de **arquivos ou instruções do projeto** (porta) e um lugar onde a **persona** da instância se define (função). Se só existir um campo, os três documentos entram nele, nessa ordem: função, manual, porta.

## Tamanho 2: em escala, com agentes configurados

Os mesmos documentos viram configuração da plataforma: a função vira o arquivo do agente, o manual vira o arquivo de contexto herdado pelas pastas, a porta vira o arquivo de contexto do projeto, e os guardrails viram política da plataforma (lista de negação, hook, sandbox). Onde cada camada mora em cada plataforma está em `onde_configurar.md`.

A estrutura de pastas mínima. Uma vez criada, ela não se move nem se apaga, só se acrescenta: as configurações apontam para esses caminhos.

```
Documents/
└── vault_[name]/
    ├── _to_delete/                 ← pré-lixeira: nada é apagado de vez
    ├── projects/
    │   └── project_[name]/
    │       └── start_here.md       ← a porta do projeto
    ├── neighborhood/               ← uma casa por agente
    │   ├── home_thinker/
    │   │   └── memory/             ← estados
    │   ├── home_manager/
    │   └── home_worker/
    └── work_tables/
        └── work_table_[project]/   ← handoff entre agentes
            ├── _task/
            ├── _output/
            └── _states/
```

O que cada peça faz:

- **vault**: a raiz. Uma por área da vida ou por contexto que não deve se misturar (trabalho e pessoal, por exemplo, ficam em vaults diferentes).
- **casa** (`home_[agent]`): onde cada agente é vinculado. Em algumas plataformas a pasta se liga ao identificador do agente: abrir a pasta já abre a instância no papel certo. A `memory/` dentro dela guarda os estados (onde o trabalho parou, o que precisa ser lembrado).
- **projeto** (`project_[name]`): a porta do projeto mora aqui. O trabalho do projeto também.
- **work_table**: onde um agente entrega e outro pega. `_task/` entra a tarefa, `_output/` sai a entrega, `_states/` guarda onde parou.
- **pré-lixeira** (`_to_delete`): nada é apagado de vez. O que sai do caminho vai para cá; a pessoa decide depois.

Como montar com a pessoa: pergunte onde ela quer a raiz; mostre a árvore; crie só depois do "sim". Se ela já tem pastas, encaixe o método nelas em vez de refazer.

## Como abrir cada plataforma no lugar certo

- **Claude Code**: abrir na pasta da casa do agente (`home_[agent]`) ou na pasta do projeto. O arquivo de contexto da pasta mãe é herdado pelas subpastas; o da pasta do projeto carrega sozinho.
- **Codex**: abrir a pasta como projeto (na raiz da sala de trabalho, não numa subpasta, senão a instância fica escopada e não vê a porta). O projeto precisa estar marcado como confiável para a configuração da pasta ser lida.
- **Hermes**: cada agente é um perfil com pasta própria; o perfil é a casa. Tarefas agendadas leem a porta do diretório configurado no job.

Depois de configurar, teste: peça algo que a regra deveria barrar e confirme que barrou. Em algumas plataformas, mudar o texto do papel só faz efeito numa sessão nova; em outras, é preciso reiniciar o processo.
