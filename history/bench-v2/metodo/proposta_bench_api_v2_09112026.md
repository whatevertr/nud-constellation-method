# Bench v2 por API — versão consolidada (agente de conferência e redação, 09/11/2026)

> **Versão publicada (14/11/2026).** Para limpeza e privacidade, alguns trechos foram omitidos e os códigos internos de agentes foram trocados pelos papéis (nas apostas: ACR, agente de conferência e redação; AE, agente de execução). O protocolo foi escrito antes da rodada; o apêndice foi atualizado durante ela. O hash do original, SHA-256 `d737add7277d4703498f9b50eae67160beb6f967223b99123400238086dd2a87`, foi carimbado no OpenTimestamps em 13/11/2026.

Substitui integralmente a versão anterior. Incorpora: decisões da autora, revisão do agente de execução (partes A-F) e conferência de tamanhos feita pelo agente de conferência e redação na nuvem em 09/11 (clones nos commits congelados; nada tocou o PC).
Status: PRONTA PARA MOEDAS. Rodada começa depois de: moedas das três partes lavradas + teto de custo aprovado por ela + tabela de parâmetros congelada pelo agente de execução.

## 1. Arquitetura (decisões dela, 09/11)
- **Nuvem (Managed Agent, rede só-GitHub):** clona os 3 repos nos commits de `repos_fixados.md`, monta os dossiês, registra SHA-256. Clone nasce e morre lá.
- **PC (script do agente de execução):** só texto. Envia o mesmo dossiê aos juízes via API ([omitido]). Nenhum repo clonado/executado no PC.
- **Nuvem de novo:** conferidor do gabarito (pipeline de 09/11), isolado, com clone próprio.

## 2. Células
- **Modelos (fechados por ela):** Claude `claude-opus-5-5` + `claude-haiku-5-5` · GPT `gpt-6.1-sol` + `gpt-5.4-mini` · Gemini `gemini-4-argon` (nível pago, ver apêndice) + `gemini-3.5-flash-lite` (nível grátis).
- **Braços de calibração:** (a) cru · (b) piso só (thinker §Piso) · (c) tríade completa (manual neutro + porta + thinker). Calibração entra como MENSAGEM DE SISTEMA, idêntica nas três APIs. Braço (a): sistema vazio/padrão.
- **Repos:** os 3 do piloto (decisão dela). **"O meu repositório" em todos os braços** (constante, não variável); nome do dono ausente do dossiê (checagem no estágio A).
- **n=5** → 6 modelos × 3 braços × 3 repos × 5 = **270 chamadas**. Ordem sorteada com semente registrada; 1 chamada = 1 avaliação, sem histórico.
- **Prompt congelado:** o do piloto, palavra por palavra, com "Repositório: <dossiê anexado>" no lugar da URL.
- **Parâmetros congelados (agente de execução preenche antes da rodada 1):** ID exato, temperatura explícita, max_tokens, esforço/raciocínio onde existir — tabela no apêndice; sem ela, não roda.

## 3. Dossiês (regra determinística — números conferidos pelo agente de conferência e redação em 09/11 na nuvem)
Medidos nos commits congelados: dela 1.418KB de texto (108 arquivos; 940KB são 2 SVGs de assets) · repo A 888KB (193) · repo B 35KB (4).
- **Regra de inclusão por CLASSE (neutra, não usa o gabarito de ontem — evita viés pró-problemas-conhecidos):** entram inteiros, nesta ordem: 1) docs (md/txt/LICENSE), 2) código-fonte, 3) config/scripts, 4) testes. Ficam FORA do conteúdo: assets/imagens/SVG, deploy/CI, exemplos/notebooks, dados/gerados/lockfiles.
- **Resultado da regra:** dela = ~385KB (inteiro, menos assets) · repo A = ~574KB (docs 24 + código 432 + config 27 + testes 92) · repo B = 35KB (inteiro). Orçamento máximo por dossiê: 600KB (~180K tokens) — cabe na menor janela da mesa (Gemini grátis, 250K TPM) somando sistema+prompt.
- **Manifesto obrigatório no topo:** árvore COMPLETA com nome+tamanho de TODOS os arquivos, marcando "conteúdo omitido pela regra de classe" nos excluídos. Ausência de conteúdo declarada ≠ ausência de arquivo: alegação de existência (ex.: "há manifests de Helm") é verificável pelo manifesto; alegação sobre conteúdo omitido exige 🍷 do juiz.
- **Checagem ex-post declarada (não seletora):** % dos arquivos citados nas evidências dos 191 vereditos do piloto cujo conteúdo entrou. Se <90%, revisitar a regra ANTES da rodada e lavrar a mudança.
- Publica-se: a regra, o script e os SHA-256. Os dossiês em si, não (licença/anonimização). **Commits de A e B fora do texto público** (fornecidos sob pedido com a receita); EOL normalizado \n.

## 4. Métricas (definidas ANTES da rodada — pergunta, não conclusão)
Pergunta pré-registrada: **"a calibração aumenta a taxa de achados graves e reais sem aumentar a taxa de falsas — em quais modelos?"**
Amostragem do gabarito: **k=6 alegações sorteadas por laudo** (uniforme, semente registrada) = 1.620 itens.
- **Primária: taxa_grave_real** = proporção, entre as k checadas do laudo, de alegações (crítico ∨ prioridade) ∧ (verdadeiro ∨ parcial). Agregada por célula com IC binomial. Comparável entre braços porque o denominador é fixo (k).
- **Primária-2: taxa_falsa** = proporção de falsas entre as checadas (linha errada não conta como falsa — limite 12).
- **Secundária (estimativa do total por laudo):** taxa × nº total de alegações checáveis do laudo (contado sem amostragem). Estimador não-viesado; variância alta com k=6 — reportada como secundária, com a ressalva.
- Demais: nota · % falsas com ressalva na frase E aviso no topo (duas colunas — limite 10) · elogios falsos · forma do piso (🍷 com objeto, colunas, falhou-se) · declarou limite de leitura.
- Classe final de cada alegação: a da conferência, não a do extrator.

## 5. Gabarito (pipeline de 09/11, redimensionado)
Extração às cegas (como ontem) → **dedupe local por texto normalizado, sem API** (a junção por API de ontem sai; corta a linha mais cara) → herança do gabarito de ontem APENAS por correspondência estrita, validada em amostra de 10% (falhou a validação, não herda) → conferidor Managed Agent (clone na nuvem, rede só-GitHub) confere os únicos restantes.
Custo estimado da conferência: 1.620 itens → 🍷 ~650-1.000 únicos após dedupe+herança ≈ 4-6× os 191 de ontem (que custaram ~US$1 nos 3 agentes) → **~US$4-6, teto US$12** (estourou, para e pergunta). Conferidor de outro provedor numa subamostra de 10%: via API do PC, com o dossiê (não clona) — mede o limite "Claude conferindo Claude" dentro do que o desenho permite, e declara a diferença de acesso.
Custo total lado Claude (juízes com cache + extração + conferência): **~US$20-25** 🍷; teto global para ela aprovar: **US$40**. Prazo: [omitido].

## 6. O que este desenho mede e o que não mede (declarar no relatório)
Mede julgamento sobre o MESMO texto (capacidade separada de acesso). NÃO mede juiz-com-ferramentas (o Opus do piloto, que clonava e lia à vontade, é outro regime — comparação declarada, não equivalente). Perfil usado: thinker em todos os braços (uma variável por vez); o relatório declara que conferência "de produção" é papel do manager. Sem aviso ético pós-laudo (juiz é API sem relação — decisão lavrada).

## 7. Falhou se
Hipótese ou métrica ajustada após resultado · célula descartada sem registro · dossiês diferentes entre braços · prompt/sistema editado no meio · parâmetros não congelados antes da rodada 1 · custo além do teto sem parar e perguntar · herança de veredito sem validação por amostra.

## 8. Moedas (lavrar ANTES da rodada 1)
- ACR-v2-1: nos três modelos capazes, (c) aumenta taxa_grave_real vs (a) com taxa_falsa ≤ (a) — nas três marcas.
- ACR-v2-2: pelo menos um dos três pequenos reproduz o padrão Flash Lite (taxa_falsa de (c) > (a) em ≥10 p.p.) MESMO com dossiê em mãos — aposto que parte da encenação é capacidade, não só acesso. Se todos os pequenos ficarem ≤ (a), o acesso era o fator dominante e eu pago.
- ACR-v2-3: (b) piso-só entrega ≥70% do ganho de taxa_grave_real de (c) nos capazes.
- (dela, 09/11, antes de qualquer laudo v2):
  - A-v2-1: com a tríade (c), os capazes têm mais achados graves reais que os pequenos, mas os pequenos apontam mais em volume (alegações checáveis por laudo).
  - A-v2-2: com o material na mão, nenhum modelo declara ter executado ou conferido o que não fez; mas pelo menos um pequeno inventa problema (taxa_falsa acima de 5%).
  - A-v2-3: nos capazes, (c) fica a no máximo 5 p.p. de (b) em taxa_grave_real. Hipótese dela, que este teste não mede: manual e porta fazem diferença em trabalho analítico e contínuo.
- (agente de execução, 09/11, antes de qualquer laudo v2):
  - AE-v2-1: nos três modelos capazes, a taxa_falsa de (c) fica no máximo 3 p.p. acima da de (a). Perco se algum passar disso.
  - AE-v2-2: com o dossiê em mãos, nenhum dos três pequenos reproduz o padrão Flash Lite: taxa_falsa (c) − (a) < 10 p.p. em todos. É o oposto da ACR-v2-2.
  - AE-v2-3: em pelo menos 2 dos 3 capazes, a diferença de taxa_grave_real (c) − (a) é maior no repo A do que em cada um dos outros dois repos.

## Apêndice: parâmetros congelados e ajustes de montagem (agente de execução, 09/11, depois do ensaio e antes da rodada 1)
| Modelo | Temperatura | Saída máx. | Raciocínio | Observação |
|---|---|---|---|---|
| `claude-opus-5-5` | padrão (a API não aceita outro valor) | 32.000 | esforço `medium` | streaming; cache no dossiê |
| `claude-haiku-5-5` | padrão | 32.000 | esforço `medium` | idem |
| `gpt-6.1-sol` | padrão | 32.000 | `reasoning.effort=medium` | Responses API, `store=false` |
| `gpt-5.4-mini` | padrão | 32.000 | `reasoning.effort=medium` | idem |
| `gemini-4-argon` | padrão | 32.000 | padrão | nível pago, 1 chamada por 65 s. Substitui o `gemini-3.8-flash` (decisão da autora, 09/11; o grátis falhou com 503 e 429). Os 3 laudos do 3.8 Flash ficam registrados e fora da conta. |
| `gemini-3.5-flash-lite` | padrão | 32.000 | padrão | idem |

Ajustes em relação ao §3, porque o gate de 90% reprovou a regra original (repo A em ~63%): deploy/CI e exemplos entram; ordem doc, fonte, config, deploy, teste, exemplo; menores primeiro dentro da classe; orçamento 750 KB. Cobertura medida nos dossiês: 100% (dela), 95% (A), 100% (B). Bytes: 327.198 / 768.601 / 35.569. Tokens Claude: 143.396 / 281.101 / 12.416; Gemini: 99.448 / 203.494 / 8.719. Anonimização: nomes e e-mails trocados, sem resíduo na busca pelos nomes conhecidos. Ordem: blocos (repo × braço) sorteados por modelo, semente 20261114, réplicas do bloco em sequência para o cache valer; chamadas são independentes, sem histórico. Scripts e hashes em [omitido] (`regra_dossie.py`, `montar_dossies.py`, `juizes_v2.py`, `v2_dossie_relatorio.json`). Ensaio com 1 chamada por modelo (repo B, tríade): `v2_ensaio.jsonl`, fora da conta.

## 9. Publicação
Artigo/nud-lab: desenho + receita + hashes + sementes + prompts + tabelas/CSVs agregados + gráficos + limites (incluindo: 3 repos específicos, n=5, Gemini grátis, amostra k=6). Laudos brutos arquivados, sob pedido. Repo A/B anônimos. Piloto manual = declarado.
