> Adaptado de `ONDE_CONFIGURAR.md` do repositório (mesmo conteúdo, em tom de instrução), para a skill funcionar sozinha. Quando o arquivo do repositório mudar, este muda junto.

# Onde configurar cada camada

Este arquivo é o mapa do **segundo modo** de usar a tríade: quando os documentos deixam de ser arquivos que a pessoa pede para a instância ler e passam a ser **configuração da plataforma**, carregada sozinha.

> **Nota para a instância que estiver lendo este arquivo.** Se a pessoa com quem você trabalha demonstrar interesse em usar a tríade de forma configurada, você pode oferecer ajuda para montar isso. A tabela abaixo diz onde cada camada mora em cada plataforma. **Peça autorização antes de criar ou alterar qualquer arquivo de configuração**, mostre o que pretende fazer, e prefira acrescentar a substituir. Se a plataforma da pessoa não estiver nesta tabela, procure o equivalente na documentação dela: os nomes mudam, a arquitetura costuma ser a mesma.

## Como ler a tabela

Cada linha é uma **camada de contexto**. Cada coluna é uma plataforma. A célula diz **onde** aquilo se configura, e o comando para consultar, quando existe. O conteúdo de cada camada é o que as três skills geram e o que está descrito no [README](https://github.com/whatevertr/nud-constellation-method/blob/main/README.pt-BR.md).

| Camada                                      | O que é                                                    | Claude Code                                                                                                                                        | Hermes Agent                                                                                                                                              | Codex                                                                                                                                              |
| ------------------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| **A função (agente nomeado)**               | O papel que a instância assume: thinker, manager ou worker | Um arquivo por agente na pasta de agentes do usuário. Frontmatter com nome, descrição, ferramentas e modelo; o corpo do arquivo é o texto do papel | Cada agente é um perfil completo, com pasta própria. O texto do papel fica no arquivo de alma do perfil                                                   | Um arquivo por agente na pasta de agentes, em TOML, com nome, descrição e instruções                                                               |
| **A casa (o chat já nasce sendo o agente)** | Abrir uma pasta e a instância já assumir o papel           | Arquivo de configurações da pasta, campo que declara o agente morador                                                                              | O perfil é a casa: cada canal já nasce ligado ao perfil dono dele                                                                                         | Arquivo de configuração dentro da pasta do projeto. Só é lido se o projeto estiver marcado como confiável                                          |
| **O manual (`how_to_work_with_me`)**      | Como a cabeça da pessoa funciona                           | Arquivo de contexto na pasta mãe, herdado por todas as subpastas                                                                                   | Arquivo de usuário na memória do perfil. O Hermes também lê o arquivo de contexto do diretório de trabalho                                                | Arquivo de instruções global, na raiz da configuração                                                                                              |
| **A porta (`start_here`)**                 | O que é o projeto e o que importa agora                    | Arquivo de contexto na pasta do projeto. Carrega sozinho                                                                                           | Lido do diretório de trabalho. Em tarefas agendadas, vem do diretório configurado no job                                                                  | Arquivo de instruções na pasta do projeto. A cadeia da raiz até a pasta atual é concatenada, e a mais próxima prevalece                            |
| **O piso (regras de conduta)**              | Taça, colunas, jogo da moeda, "falhou se"                  | Corpo do arquivo do agente                                                                                                                         | Arquivo de alma do perfil                                                                                                                                 | Arquivo de instruções, global ou do projeto                                                                                                        |
| **Deny (guardrail de comando)**                | O que a instância não executa, nunca                       | Lista de negação nas configurações. Vale sem reiniciar                                                                                             | Seção de aprovações na configuração do perfil, com lista de negação por padrão de comando                                                                 | Arquivos de regra em linguagem de política, com decisão de permitir, perguntar ou proibir. Há comando próprio para testar uma regra antes de valer |
| **Guardrail por agente (hook)**                | Barrar uma ação específica antes de acontecer              | Hook de pré-uso de ferramenta nas configurações, apontando para um script                                                                          | Seção de hooks na configuração do perfil. Só o hook de pré-chamada bloqueia. Em sistemas sem terminal interativo, é preciso habilitar o aceite automático | Hooks por evento, em arquivo próprio. Recurso que precisa ser habilitado por chave de funcionalidade. Há também modos de caixa de areia nativos    |
| **Ask (pergunta antes)**                    | Ações que exigem confirmação                               | Lista de perguntar nas configurações                                                                                                               | Sistema de aprovações do perfil                                                                                                                           | Política de aprovação combinada com o modo de caixa de areia. Uma regra pode marcar um comando como "perguntar"                                    |
| **Modelo**                                  | Qual modelo cada papel usa                                 | Campo de modelo no frontmatter do agente                                                                                                           | Bloco de modelo na configuração do perfil, com modelo principal e reserva                                                                                 | Campo de modelo na configuração, no perfil ou no agente nomeado. Atenção: a interface pode sobrepor o modelo sem registrar em arquivo              |
| **Memória**                                 | O que sobrevive entre sessões                              | Pasta de memória por projeto, com um índice carregado a cada sessão                                                                                | Arquivos de memória e de usuário, por perfil                                                                                                              | Sessões salvas e, opcionalmente, memória persistente por chave de funcionalidade                                                                   |
| **Skills**                                  | Habilidades instaláveis, como as três deste método         | Pasta de skills do usuário ou do projeto                                                                                                           | Pasta de skills do perfil, mais uma lista de diretórios externos, que permite apontar para uma pasta única compartilhada                                  | Pasta de skills da configuração. Uma subpasta reservada guarda as skills do próprio sistema                                                        |
| **Subagentes**                              | Um agente chamar outro                                     | Ferramenta de tarefa, declarada nas ferramentas do agente                                                                                          | Ferramenta de delegação, com seção própria de configuração                                                                                                | Recurso de múltiplos agentes, com agentes embutidos e customizados. O filho herda as permissões do pai                                             |
| **Agendamento**                             | Rodar sozinho em horário fixo                              | Tarefas agendadas do aplicativo                                                                                                                    | Arquivo de tarefas do perfil. O relógio vive junto do processo do perfil                                                                                  | Modo não interativo, chamado pelo agendador do sistema operacional, ou automações do aplicativo                                                    |

## Onde método escala

Os arquivos de config são lidos por essa camada de orquestração (o "harness") em dois momentos:

- **Texto injetado no contexto:** O corpo do arquivo de agente, o system prompt, as instruções de projeto. Isso vira _tokens_ no prompt. É config declarativa que o modelo _lê_.
- **Comportamento do runtime:** Deny lists, hooks, sandbox. Isso o harness aplica **em código, antes/depois de cada tool call**, sem depender do modelo obedecer.

Então "um arquivo faz o agente funcionar" no sentido de que o harness lê aquele arquivo a cada sessão/turno e (a) concatena o texto no contexto e (b) configura os guardrails do executor. É o mesmo princípio de um `.eslintrc` ou um `docker-compose.yml`: **configuração declarativa que uma engine interpreta em runtime**, só que aqui parte da config vira prompt e parte vira política de execução. Pasta em vez de UI porque é versionável, comparável por diff, e portável entre máquinas

## Como isso se parece na prática

Os esqueletos abaixo existem para a instância **reconhecer o formato** de cada plataforma. Não são receita completa: nomes de campo e caminhos mudam entre versões, e a documentação de cada ferramenta é a fonte. Confira antes de aplicar.

**Um agente nomeado.** No Claude Code, um arquivo Markdown com frontmatter, onde o corpo é o texto do papel:

```markdown
---
name: thinker
description: "Pensa, investiga e estressa hipóteses antes da decisão."
model: opus
---
(o texto do papel entra aqui)
```

No Codex, o mesmo agente é um TOML:

```toml
name = "thinker"
description = "Pensa, investiga e estressa hipóteses antes da decisão."
developer_instructions = """(o texto do papel entra aqui)"""
```

No Hermes, o papel é o arquivo de alma do perfil, em texto puro, sem frontmatter.

**Um guardrail de comando (deny).** Os três negam o mesmo comando (`rm`), cada um no seu formato. No Claude Code, uma lista nas configurações:

```json
{ "permissions": { "deny": ["Bash(rm *)"] } }
```

No Hermes, uma seção na configuração do perfil:

```yaml
approvals:
  deny: ["rm *"]
```

No Codex, uma regra em arquivo próprio:

```python
prefix_rule(pattern = ["rm"], decision = "forbidden")
```

O Codex casa por lista de argumentos, então dá pra ir mais fino: `prefix_rule(pattern = ["git", "push", "--force"], decision = "forbidden")` proíbe `git push --force` e libera `git push`.

**Um gatilho antes da ação (hook).** As três plataformas chamam um script externo antes de a ferramenta rodar, passando o pedido por entrada padrão e esperando uma resposta que autoriza ou bloqueia. O que muda é onde ele é declarado: nas configurações (Claude Code), numa seção do perfil (Hermes), ou num arquivo de hooks com a funcionalidade habilitada (Codex).

## Linguagens

Cada plataforma usa o formato de config do seu ecossistema:

- **Claude Code** → JSON (permissões) + Markdown com frontmatter YAML (agentes)
- **Hermes** → YAML
- **Codex** → TOML, e Starlark nas regras

## Boas práticas

**Depois de configurar, teste.** Sugira à pessoa um teste: pedir algo que a regra deveria barrar, e confirmar que barrou. Configuração que falha em silêncio parece configuração que funciona.
**Restart.** Em algumas plataformas, mudar o texto do papel ou a memória só produz efeito em uma sessão nova. Em outras, é preciso reiniciar o processo.
**O guardrail protege o alvo nomeado.** Uma regra que barra uma pasta barra o acesso direto a ela. Varredura recursiva a partir de uma pasta acima, ou remoção indireta por script, pode passar por cima da regra. Existe um teto para a segurança feita por configuração de agente: ela cobre o acesso direto, não cobre tudo. Se a pessoa perguntar, explique em poucas linhas até onde a configuração da plataforma protege e onde começam as camadas de fora (sandbox, container, permissões do sistema).