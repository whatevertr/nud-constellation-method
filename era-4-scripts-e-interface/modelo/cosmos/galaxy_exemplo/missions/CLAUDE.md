# missions: onde o trabalho é feito

## Abrir uma mission
1. Criar a pasta com **traço** no nome (ela pode virar repositório): `missions\nome-da-mission\`.
2. Criar o `CLAUDE.md` dela começando com o cabeçalho:
   ```
   ---
   mission: nome-da-mission
   dono: quem cuida (o --por do thinker)
   familia: o grupo
   estado: vivo | analise | manutencao | pausado
   motivo: uma frase do porquê ela existe
   criado: AAAA-MM-DD
   ---
   ```
3. Fazer o primeiro registro no `log.jsonl` **pelo registrador** (nunca à mão).

## O que vai onde
- `lab\storage\`: os materiais (insumos, scripts, referências) **e o que já foi aprovado**.
- `lab\output\`: o resultado que **ainda não foi revisado**.
- `lab\tasks\`: os pedidos pra um manager/worker.
- `repo-[nome]\`: só quando o trabalho vira repositório publicado.

## O fluxo
Sai em `output` → a pessoa (ou o thinker) revisa → o aprovado vai pra `storage` ou pro `repo-[nome]`.

## As ações que mantêm o histórico vivo
- **Pendência nova** vira `tarefa` com `--tag` (o tipo de trabalho, de `tools\tipos.json`); fora de mission, `--pendencia` no módulo.
- **O ciclo:** `aberta` → `fazendo` → `feita` ou `cancelada`. Mudou, registra na hora (`--id tN --status ...`).
- **O que só a pessoa faz** leva `--quem` com o nome dela.
- **Ao fechar o dia:** um `resumo` em cada mission tocada.
