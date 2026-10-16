# nud-agentes

Skill que carrega o contexto do Método Constelação e entrega os três perfis de agentes, `thinker` (pensar/analisar), `manager` (conduzir/auditar) e `worker` (executar/operacionalizar). Com ela, a instância consegue ajudar você a montar o seu jeito de trabalhar, num projeto do app ou em escala (agentes configurados em pastas), sem precisar do resto do repositório.

## Instalar

Copie a pasta `nud-agentes/` inteira para o diretório de skills da sua instância (ex.: `.claude/skills/` no Claude Code) ou instale pela interface. A skill é lida a partir de `SKILL.md`; os três perfis ficam em `modelos/` e o contexto do método em `contexto/`. Não apague nenhuma das duas pastas.

## O que tem dentro

- `SKILL.md`: o guia de montagem (conversa antes, pergunta onde salvar, entrega os perfis, monta junto, testa).
- `modelos/`: os três perfis, prontos para usar.
- `contexto/ambiente.md`: os dois tamanhos (projeto no app, em escala), a estrutura de pastas e um exemplo datado no Claude Cowork.
- `contexto/metodo.md` e `contexto/onde_configurar.md`: cópias fiéis dos arquivos do repositório, para a skill funcionar sozinha.

## Complementa com

`nud-como-trabalhar-comigo` (o manual, sobre a pessoa) e `nud-comece-aqui` (a porta, sobre o projeto). Use as duas antes: esta skill pede os documentos gerados por elas para entender que configuração você precisa.

Licença: CC-BY-4.0 · Thainá Ramos (Nud by Whatevertr).
