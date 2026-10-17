r"""
buscador.py · busca no galley por SENTIDO (e mostra a fonte de cada pedaço achado).
v0.5.0 · 12/10/2026 (peso por tipo: seção de decisão/regra/lição desempata) · tars (Claude), o thinker do NUD · guardião.
v0.4.0 · 12/10/2026 (a busca por palavra vira BM25: palavra rara pesa mais).
v0.3.0 · 12/10/2026 (busca HÍBRIDA: sentido + palavra juntos, por fusão de ranking).
v0.2.0 · 12/10/2026 (glossário na raiz do galley; plano B por palavra quando o Ollama não responde).
v0.1.0 · 03/10/2026.

Uso:
  python buscador.py <galley\states ou galley\diaries> "a pergunta" [--n 5] [--palavra]
A pergunta vira números (o mesmo modelo do fatiador), e o buscador devolve os pedaços
com o sentido mais parecido, do mais pro menos parecido, com o parentesco (0 a 1) e a fonte.
A busca normal olha o galley\states\; o galley\diaries\ só quando a autora pedir.
Plano B: se o Ollama não responder (ou com --palavra), busca por PALAVRA nos mesmos pedaços.
"""
import json
import math
import os
import re
import sys
import unicodedata
import urllib.error
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODELO = "qwen3-embedding:0.6b"
OLLAMA = "http://127.0.0.1:11434/api/embed"
# o Qwen3-Embedding pede uma instrução na PERGUNTA (nos pedaços, não)
INSTRUCAO = "Instruct: Dada uma pergunta sobre o trabalho passado, ache os trechos de registro que respondem\nQuery: "


def embed(textos):
    req = urllib.request.Request(OLLAMA, data=json.dumps({"model": MODELO, "input": textos}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=300))["embeddings"]


def expandir(pergunta, galley):
    """Pergunta em palavra simples, registro em jargão: o glossário DO THINKER (no galley dele) faz a ponte.
    Cada Tars cuida do seu: o jargão de cada universo é diferente."""
    gl = None
    for p in (os.path.join(galley, "glossario.json"), os.path.join(os.path.dirname(galley), "glossario.json")):
        try:   # o glossário mora na raiz do galley (um por thinker); dentro da subpasta também vale
            gl = {k: v for k, v in json.load(open(p, encoding="utf-8")).items() if not k.startswith("_")}
            break
        except Exception:
            continue
    if not gl:
        return pergunta
    extra = [v for k, v in gl.items() if k.lower() in pergunta.lower()]
    return pergunta + (" (" + "; ".join(extra) + ")" if extra else "")


def cos(a, b):
    return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))


def norm(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


# palavras vazias: aparecem em quase todo texto e não dizem do que se fala (pesam ruído no BM25)
VAZIAS = set(norm("""como foi pra para mim que com uma uns umas dos das nos nas num numa por pelo pela mas mais muito
muita sobre onde qual quais tem ter tinha ser era foram está estava estão aqui ali então também sim isso isto esse
essa este esta aquele aquela ele ela eles elas você vocês voce vcs meu minha seu sua nosso nossa quando quem porque
pois até sem sempre ainda depois antes agora hoje ontem coisa coisas vez vezes fazer feito fez lembra lembro""").split())


# seção que guarda o que é durável (decisão, regra, causa, lição) ganha um empurrão pequeno: desempata, não esconde o resto
SECAO_FORTE = re.compile(r"decis|decidid|regra|licao|aprend|causa|conserto|piso|verdades")
AUTORIDADE = 1.12


def palavras(s):
    return [t for t in re.findall(r"\w{3,}", norm(s)) if t not in VAZIAS]


def por_palavra(pedacos, pergunta, n, k1=1.5, b=0.75):
    """Por PALAVRA, com BM25 (12/10): a palavra RARA na coleção pesa mais que a comum ("bifurcou" > "como"),
    a repetição satura, e pedaço comprido não ganha só por ser comprido. Bônus pros pares de palavras da
    pergunta que aparecem em sequência no pedaço (frase quase literal, o caso do 'prompt frio')."""
    termos = palavras(pergunta)
    docs = {i: palavras(p.get("secao", "") + " " + p["texto"]) for i, p in pedacos.items()}
    N = len(docs) or 1
    media = sum(len(d) for d in docs.values()) / N
    df = {t: sum(1 for d in docs.values() if t in set(d)) for t in set(termos)}
    idf = {t: math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5)) for t in df}
    pares = {f"{a} {c}" for a, c in zip(termos, termos[1:])}
    nota = []
    for i, d in docs.items():
        if not d:
            continue
        freq = {}
        for t in d:
            freq[t] = freq.get(t, 0) + 1
        s = sum(idf[t] * freq[t] * (k1 + 1) / (freq[t] + k1 * (1 - b + b * len(d) / media)) for t in idf if t in freq)
        if s <= 0:
            continue
        juntos = " ".join(d)
        s += sum(2.0 for par in pares if par in juntos)
        nota.append((round(s, 2), i))
    nota.sort(reverse=True)
    return [(s, pedacos[i]) for s, i in nota[:n]]


def por_sentido(pedacos, galley, pergunta, n):
    q = embed([INSTRUCAO + expandir(pergunta, galley)])[0]
    with open(os.path.join(galley, "vetores.jsonl"), encoding="utf-8") as f:
        vetores = {v["id"]: v["vetor"] for v in map(json.loads, filter(str.strip, f))}
    nota = sorted(((cos(q, v), i) for i, v in vetores.items() if i in pedacos), reverse=True)
    return [(round(s, 3), pedacos[i]) for s, i in nota[:n]]


def buscar(galley, pergunta, n=3, palavra=False):
    """HÍBRIDA (12/10): roda o SENTIDO e a PALAVRA e junta pela posição de cada um (fusão por ranking).
    O sentido acha quando a pergunta usa outras palavras; a palavra acha a frase quase literal,
    que o modelo pequeno às vezes perde (o teste do 'prompt frio', 12/10)."""
    with open(os.path.join(galley, "pedacos.jsonl"), encoding="utf-8") as f:
        pedacos = {p["id"]: p for p in map(json.loads, filter(str.strip, f))}
    pal = por_palavra(pedacos, expandir(pergunta, galley), 30)
    if palavra:
        return pal[:n]
    try:
        sen = por_sentido(pedacos, galley, pergunta, 30)
    except (urllib.error.URLError, OSError, TimeoutError):
        print("(plano B: o Ollama não respondeu, então a busca é só por PALAVRA)")
        return pal[:n]
    fusao = {}
    for lista in (sen, pal):
        for pos, (_, p) in enumerate(lista, 1):
            fusao[p["id"]] = fusao.get(p["id"], 0) + 1 / (60 + pos)
    for i in fusao:   # peso por tipo (12/10, ideia do ai-memory do Akita): num empate, ganha o que é decisão/regra/lição
        fusao[i] *= AUTORIDADE if SECAO_FORTE.search(norm(pedacos[i].get("secao", ""))) else 1.0
    melhores = sorted(fusao.items(), key=lambda kv: kv[1], reverse=True)[:n]
    return [(round(s * 1000, 1), pedacos[i]) for i, s in melhores]


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 5
    for s, p in buscar(os.path.abspath(sys.argv[1]), sys.argv[2], n, "--palavra" in sys.argv):
        print(f"\n[{s}] {p['fonte']} · era {p.get('era', '?')} · {p.get('dono', p.get('por', '?'))} · seção: {p['secao']} · {p['data']}")
        print(p["texto"][:600] + ("…" if len(p["texto"]) > 600 else ""))
