> Adaptado de `METODO.md` do repositório (mesmo conteúdo, em tom de instrução), para a skill funcionar sozinha. Quando o arquivo do repositório mudar, este muda junto.

# Método: o piso, os guardrails e em que isso se apoia

Este arquivo guarda a explicação do método, para a instância entender o porquê de cada regra antes de ajudar a pessoa. O [README](https://github.com/whatevertr/nud-constellation-method/blob/main/README.pt-BR.md) diz o que é e como usar; aqui está o porquê de cada regra que os agentes carregam.

## Dois modos de usar (mesma arquitetura, investimentos diferentes)

1. **Como projeto.** Os três documentos num espaço de trabalho da interface do provedor de IA. É o jeito manual, custo baixo de manutenção, bom para projetos de curto a médio prazo.
2. **Como agente configurado.** Os mesmos documentos virando configuração de agente na plataforma. Mesmo efeito, só que escalável, para duração a longo prazo, passa a depender da organização de navegação do contexto no espaço do projeto.

A tabela em `onde_configurar.md` (nesta pasta) mostra onde cada camada mora em cada plataforma, com exemplos nas três que a autora do método testou: Claude Code, Codex e Hermes.

## Duas camadas que se reforçam

- **Guardrails determinísticos**: paredes que não dependem do modelo (o que ele não pode executar, onde não pode escrever), mecânico.
- **Piso epistêmico**: regras em prosa que direcionam o comportamento e diminuem o range das respostas por se comportarem como critérios de acerto, que reforçam o foco no objetivo.

## As duas regras que carregam a honestidade

O piso completo (taça e colunas) fica no papel analítico (thinker). O manager e o worker carregam a versão enxuta: a moeda e o "falhou se". Cada papel carrega o piso do tamanho da função dele.

- **A taça 🍷**: a instância marca em uma linha o que percebe mas não conseguiu verificar. O não conferido fica nomeado, não escondido.
- **O jogo da moeda**: antes de conferir, a instância aposta no resultado; depois pontua se acertou. É uma redundância de conferência sobre o que ela previu; os parâmetros da previsão são ajustados a cada erro.

  > **Exemplo.** A instância aposta antes de terminar: *"ela declara a probabilidade calculada, e ou registra o acerto, ou recalcula"*. É um jeito de pedir conferência sobre a própria conclusão, tentando circundar a bajulação em vez de proibi-la. A autora não afirma que isso resolve: é uma observação de uso, não uma prova. Apresente do mesmo jeito.

## Em que degrau este método está

**método** (formalizado e aplicável) → **reproduzível** (terceiros repetem) → **eficaz** (avaliação mede o resultado) → **generalizável** (resultado observado por outros)

A Tríade se declara no **primeiro degrau**: método formalizado, em uso diário, com reprodutibilidade e eficácia ainda em teste. Nomear a escada é o convite: quem quiser ajudar sabe qual degrau está vago.

## Em que o método se apoia

A autora não inventou disciplina nova: está **traduzindo** prática velha de engenharia para um meio novo. Ferramentas e metodologias de análise, mapeamento e gerenciamento de processos também precisam de aplicação de contexto:

- **Poka-Yoke**: evitar o erro pela estrutura, não pela energia do sistema.
- **PDCA**: melhorar checando o resultado analítica e auditivamente, antes da próxima ação.

Sobre a ideia de que "a estrutura em volta do modelo move o resultado", há medição registrando o mesmo modelo variando dezenas de pontos de uma estrutura para outra ([Harness-Bench, 2026](https://arxiv.org/abs/2605.27922), preprint). E a bajulação é produto do treino por preferência humana ([Sharma et al., 2023](https://arxiv.org/abs/2310.13548)), cresce com escala e RLHF ([Perez et al., 2022](https://arxiv.org/abs/2212.09251)), e um perfil do usuário na memória a amplifica (até +45% no caso medido, com casos sem mudança significativa; [Jain et al., CHI 2026](https://doi.org/10.1145/3772318.3791915)). Talvez a bajulação não tenha que ser eliminada e sim direcionada para diminuir as chances de erro.

## Leituras

- Anthropic, *Effective context engineering for AI agents* (2025).
- Liu et al., *Lost in the Middle* (2023), [arXiv:2307.03172](https://arxiv.org/abs/2307.03172).
- Yao et al., *Harness-Bench* (2026, preprint), [arXiv:2605.27922](https://arxiv.org/abs/2605.27922).
- Sharma et al., *Towards Understanding Sycophancy in Language Models* (2023), [arXiv:2310.13548](https://arxiv.org/abs/2310.13548).
- Perez et al., *Discovering Language Model Behaviors with Model-Written Evaluations* (2022), [arXiv:2212.09251](https://arxiv.org/abs/2212.09251).
- Jain et al., *Interaction Context Often Increases Sycophancy in LLMs* (2025), [arXiv:2509.12517](https://arxiv.org/abs/2509.12517).
