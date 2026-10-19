# Era 1: a Tríade
*O ponto de partida: o contexto mínimo. Todas as outras eras usam esta.*

**O que ela trouxe:** antes, cada instância começava sem contexto, e a pessoa explicava tudo de novo a cada conversa. A Tríade organizou o mínimo que a instância precisa pra trabalhar contextualizada em convívio em três documentos, e deu a ela um papel claro que direciona o foco do trabalho.

## O contexto mínimo

Três documentos, três camadas:

- **a porta** (`start_here`): onde a instância entra. O tema, o objetivo, o porquê aquilo importa agora = contextualização do objetivo;
- **o manual** (`how_to_work_with_me`): como a sua cabeça funciona. Os seus critérios de colaboração = contextualização da comunicação humano/IA;
- **a função** (o perfil do agente), **thinker**/**manager**/**worker**, ou análise/auditoria/execução = contextualização do que é indispensável para o cumprimento do objetivo.

## Os três agentes

Num trabalho pequeno, a tarefa é pontual: ou é análise, ou é conferência, ou é execução. Escolhe-se um agente e usa-se só ele. Para gerenciar, os três trabalham em camadas no mesmo projeto, e o que chega até a pessoa é só o resultado, pronto para a decisão. O que dá confiança para deixar os agentes gerenciando é o piso que cada um carrega:

- **Execução operacionalizada** (worker): recebe a tarefa com contexto limpo, pra reduzir o viés de quem desenhou o processo.
- **Conferência auditiva** (manager): confere o que voltou contra o que foi combinado.
- **Conferência analítica** (thinker): estressa a hipótese antes de ela virar decisão, e planeja o próximo.

O piso que os três carregam está explicado em [`METHOD.md`](METHOD.md).

## Onde funcionou

Num projeto do app do provedor: os três documentos entram na configuração do projeto, e pronto. É simples e funcional para um trabalho pontual.

**Exemplo no Claude Cowork (setembro de 2026):** o manual vai em *Configurações → Geral → Instruções para o Claude* (vale para todas as conversas) ou nas *Instruções* do projeto; a porta vai nas *Instruções* do projeto; o perfil do agente vai em *Configurações → Cowork* ou nas *Instruções* do projeto. Os nomes dos campos mudam com o tempo; a lógica se mantém: manual = como você trabalha, porta = o que é o projeto, função = o papel da instância.

## O que tem aqui

- [`skills/`](skills/): as três skills que geram o contexto mínimo, uma por documento (`nud-como-trabalhar-comigo`, `nud-comece-aqui`, `nud-agentes`), cada uma como pasta aberta e como `.zip`.
- [`METHOD.md`](METHOD.md): o piso epistêmico e as duas regras que carregam a honestidade.

## Em outro harness

Os três documentos são texto, então funcionam em qualquer lugar que deixe a instância ler instruções: o projeto de qualquer app de provedor, o `AGENTS.md` do Codex e do OpenCode, o arquivo de alma de um perfil do Hermes. O nome do campo muda; a camada é a mesma.
