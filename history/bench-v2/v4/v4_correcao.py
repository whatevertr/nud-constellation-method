# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import csv, json, math, random, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
P = AQUI.parent / "dados"
SEMENTE, N_PERM, N_BOOT = 20261112, 5000, 2000
CAP = ["claude-opus-5-5", "gpt-6.1-sol", "gemini-4-argon"]
PEQ = ["claude-haiku-5-5", "gpt-5.4-mini", "gemini-3.5-flash-lite"]
MODS = CAP + PEQ
BR = {"a": "cru", "b": "só piso", "c": "tríade"}
REPO = {"r1": "método", "r2": "repo A", "r3": "repo B"}
PESO = {"critico": 2, "prioridade": 2, "ajuste": 1, "melhoria": 1, "elogio": -0.5, "informacao": 0.5}
TACA = "🍷"

jl = lambda n: [json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines() if l.strip()]
mapa = {l.split(",")[0]: l.split(",", 1)[1].strip().split("|") for l in (P / "v2_mapa_secreto.csv").read_text(encoding="utf-8").splitlines()[1:]}
gab = {x["codigo"]: x for x in jl("v2_gabarito_consenso.jsonl")}
ver = {c: x["veredito"] for c, x in gab.items()}
rot = {x["codigo"]: x["rotulo"] for x in jl("v3_rotulo.jsonl")}
for n in ("v3_rotulo_revisao.jsonl", "v3_rotulo_releitura.jsonl"):
    rot.update({x["codigo"]: x["rotulo"] for x in jl(n)})
alc = {x["codigo"]: x["alcancava"] for x in jl("v3_alcance.jsonl")}
pes = {x["codigo"]: x["peso_real"] for x in jl("v3_peso_real.jsonl")}
ALE = {f"{a['laudo']}#{a['n']}": a for a in jl("v2_alegacoes.jsonl")}
texto = {l["id"]: l["texto"] for l in jl("v2_laudos.jsonl")}
texto.update({l["id"]: l["texto"] for l in jl("v2_refeitos.jsonl")})
TXT = {V: texto["|".join(x)] for V, x in mapa.items()}
por_laudo = defaultdict(list)
for c in ALE:
    por_laudo[c.split("#")[0]].append(c)
SEM_ALEGACAO = sorted(V for V in mapa if V not in por_laudo)
AUTOR = {c for c, a in ALE.items() if "[autor]" in a["alegacao"].lower()}

tok = lambda s: set(w for w in re.findall(r"[\wÀ-ÿ./_-]{4,}", s.lower()))


def trechos(t):
    out, ant = [], ""
    for l in t.splitlines():
        if not l.strip():
            continue
        out.append((l, ant))
        if re.match(r"\s*(#{1,6} |\*\*|[-*] \*\*|\|)", l) or TACA in l:
            ant = l
    return out


ressalva, casamento = {}, []
for V, cods in por_laudo.items():
    tr = [(l, ant, tok(l)) for l, ant in trechos(TXT[V])]
    for c in cods:
        a = ALE[c]
        ta = tok(a["alegacao"])
        melhor, nota = None, 0.0
        for l, ant, tl in tr:
            s = len(ta & tl) / len(ta) if ta else 0
            if s > nota:
                melhor, nota = (l, ant), s
        achou = nota >= 0.4 and melhor is not None
        taca_trecho = bool(achou and TACA in melhor[0])
        casamento.append(nota)
        ressalva[c] = {"codigo": c, "hedge": bool(a["hedge"]), "taca_no_trecho": taca_trecho, "casou": round(nota, 2),
                       "ressalva": bool(a["hedge"] or taca_trecho or TACA in a["alegacao"] or rot.get(c) == "inferencia_declarada")}
with (AQUI / "v4_ressalva.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for c in sorted(ressalva):
        f.write(json.dumps(ressalva[c], ensure_ascii=False) + "\n")


def caixa(c):
    if c in AUTOR or c not in ver:
        return None
    v, r = ver[c], rot.get(c)
    if r == "inferencia_declarada":
        return "inferencia_falsa" if alc.get(c) == "sim" else "taca_certa"
    if v == "falso":
        return "contradita"
    if v == "nao_verificavel":
        return "anulada_ressalva" if ressalva[c]["ressalva"] else "anulada_seca"
    return "real" if c in pes else None


PONTO = {"contradita": -1, "anulada_seca": -1, "anulada_ressalva": 0.5, "inferencia_falsa": -0.5, "taca_certa": 0.5}


def pontos(c):
    k = caixa(c)
    if k is None:
        return None
    if k == "real":
        return PESO[pes[c]] * (1 if ver[c] == "verdadeiro" else 0.5)
    return PONTO[k]


def medidas(V):
    cods = [c for c in por_laudo[V] if c not in AUTOR]
    conf = [c for c in cods if c in ver]
    ps = [p for p in map(pontos, cods) if p is not None]
    real = lambda c: ver[c] in ("verdadeiro", "parcial")
    pc = lambda n, d: 100 * n / d if d else 0.0
    return {
        "alegacoes": len(cods),
        "taxa_grave_real": pc(sum(real(c) and gab[c]["classe"] in ("critico", "prioridade") for c in conf), len(conf)),
        "taxa_falsa": pc(sum(ver[c] == "falso" for c in conf), len(conf)),
        "pct_anulada_seca": pc(sum(caixa(c) == "anulada_seca" for c in conf), len(conf)),
        "pts_alegacao": sum(ps) / len(ps) if ps else 0.0,
        "pts_laudo": sum(ps),
        "pct_elogio": pc(sum(rot[c] == "elogio" for c in cods), len(cods)),
        "pct_constatacao": pc(sum(rot[c] == "constatacao" for c in cods), len(cods)),
        "tacas_no_texto": TXT[V].count(TACA),
        "pct_com_ressalva": pc(sum(ressalva[c]["ressalva"] for c in cods), len(cods)),
    }


MET = ["alegacoes", "taxa_grave_real", "taxa_falsa", "pct_anulada_seca", "pts_alegacao", "pts_laudo", "pct_elogio", "pct_constatacao", "tacas_no_texto", "pct_com_ressalva"]
NOME = {"alegacoes": "afirmações por laudo", "taxa_grave_real": "taxa de graves reais, % (primária 1)", "taxa_falsa": "taxa de falsas, % (primária 2)",
        "pct_anulada_seca": "anuladas secas, %", "pts_alegacao": "pontos por afirmação", "pts_laudo": "pontos por laudo", "pct_elogio": "elogios, %",
        "pct_constatacao": "constatações, %", "tacas_no_texto": "taças (🍷) por laudo", "pct_com_ressalva": "afirmações com ressalva, %"}
M = {V: medidas(V) for V in por_laudo}
cel = lambda ms, b, g=None: [V for V, x in mapa.items() if V in M and x[0] in ms and x[1] == b and (g is None or x[2] == g)]

rng = random.Random(SEMENTE)


def contraste(ms, b1, b2, k):
    est = [([M[V][k] for V in cel([m], b1, g)], [M[V][k] for V in cel([m], b2, g)]) for m in ms for g in REPO]
    dif = lambda E: statistics.mean(statistics.mean(y) - statistics.mean(x) for x, y in E)
    obs = dif(est)
    boots = sorted(dif([([rng.choice(x) for _ in x], [rng.choice(y) for _ in y]) for x, y in est]) for _ in range(N_BOOT))
    n = 0
    for _ in range(N_PERM):
        E = []
        for x, y in est:
            z = x + y
            rng.shuffle(z)
            E.append((z[:len(x)], z[len(x):]))
        n += abs(dif(E)) >= abs(obs) - 1e-12
    return obs, boots[int(.025 * N_BOOT)], boots[int(.975 * N_BOOT) - 1], (n + 1) / (N_PERM + 1)


GRUPOS = [(m, [m]) for m in MODS] + [("maiores (3)", CAP), ("compactos (3)", PEQ)]
celulas, contrastes = [], []
for nome, ms in GRUPOS:
    for b in "abc":
        Vs = cel(ms, b)
        celulas.append({"grupo": nome, "braco": BR[b], "laudos": len(Vs), **{k: round(statistics.mean(M[V][k] for V in Vs), 3) for k in MET}})
    for b1, b2 in (("a", "b"), ("a", "c"), ("b", "c")):
        for k in MET:
            o, lo, hi, p = contraste(ms, b1, b2, k)
            porrepo = {g: statistics.mean(statistics.mean(M[V][k] for V in cel([m], b2, g)) - statistics.mean(M[V][k] for V in cel([m], b1, g)) for m in ms) for g in REPO}
            contrastes.append({"grupo": nome, "contraste": f"{BR[b2]} − {BR[b1]}", "metrica": k, "diferenca": round(o, 3), "ic_lo": round(lo, 3), "ic_hi": round(hi, 3), "p_perm": round(p, 4),
                               **{f"dif_{REPO[g]}": round(porrepo[g], 3) for g in REPO}})
for nome, linhas in (("v4_celulas.csv", celulas), ("v4_contrastes.csv", contrastes)):
    with (AQUI / nome).open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)

cx = Counter(caixa(c) for c in ALE)
md = ["# Bench v2 · correção da análise (v4)", f"*Gerado por `v4_correcao.py` a partir de `dados/` (nada lá foi alterado). Semente {SEMENTE}; {N_PERM} permutações; {N_BOOT} reamostragens.*", "",
      "## O que entrou na conta",
      f"- Laudos com afirmações: {len(por_laudo)} de {len(mapa)}. Sem afirmações (enviado sem o dossiê): {', '.join(SEM_ALEGACAO)}.",
      f"- Afirmações: {len(ALE)}; fora por citarem o placeholder `[autor]`: {len(AUTOR)}; de opinião (sem veredito): {sum(1 for c in ALE if c not in ver and c not in AUTOR)}.",
      f"- Caixas: " + "; ".join(f"{k} {cx[k]}" for k in ("real", "contradita", "anulada_seca", "anulada_ressalva", "taca_certa", "inferencia_falsa")) + ".",
      f"- Ligação afirmação → trecho do laudo: {100 * sum(n >= .4 for n in casamento) / len(casamento):.0f}% com sobreposição ≥ 0,4 (mediana {statistics.median(casamento):.2f}). "
      f"Ressalva = `hedge` do extrator, ou 🍷 no trecho, ou rótulo de inferência declarada.",
      f"- Origem da ressalva: só `hedge` {sum(1 for r in ressalva.values() if r['hedge'] and not r['taca_no_trecho'])}; só 🍷 no trecho {sum(1 for r in ressalva.values() if r['taca_no_trecho'] and not r['hedge'])}; os dois {sum(1 for r in ressalva.values() if r['taca_no_trecho'] and r['hedge'])}.", ""]
fmt = lambda k, v: f"{v:.2f}" if k in ("pts_alegacao", "taxa_falsa", "pct_anulada_seca") else f"{v:.1f}"
md += ["## Médias por célula (média dos laudos)", "| | " + " | ".join(NOME[k] for k in MET) + " | laudos |", "|---" * (len(MET) + 2) + "|"]
for r in celulas:
    md.append(f"| {r['grupo']} · {r['braco']} | " + " | ".join(fmt(k, r[k]) for k in MET) + f" | {r['laudos']} |")
for ct in ("tríade − cru", "só piso − cru", "tríade − só piso"):
    md += ["", f"## Diferença dentro do repositório: {ct}", "Média das diferenças nos três repositórios. Entre colchetes: IC 95% (bootstrap estratificado); p por permutação. `*` p < 0,05; `**` p < 0,001.", "",
           "| | " + " | ".join(NOME[k] for k in MET) + " |", "|---" * (len(MET) + 1) + "|"]
    for nome, _ in GRUPOS:
        linha = []
        for k in MET:
            r = next(x for x in contrastes if x["grupo"] == nome and x["contraste"] == ct and x["metrica"] == k)
            linha.append(f"{r['diferenca']:+.2f} [{r['ic_lo']:+.2f}; {r['ic_hi']:+.2f}]" + ("**" if r["p_perm"] < .001 else "*" if r["p_perm"] < .05 else ""))
        md.append(f"| {nome} | " + " | ".join(linha) + " |")
md += ["", "## Tríade − cru, por repositório (grupos)", "| grupo | métrica | método | repo A | repo B |", "|---|---|---|---|---|"]
for nome in ("maiores (3)", "compactos (3)"):
    for k in MET:
        r = next(x for x in contrastes if x["grupo"] == nome and x["contraste"] == "tríade − cru" and x["metrica"] == k)
        md.append(f"| {nome} | {NOME[k]} | {r['dif_método']:+.2f} | {r['dif_repo A']:+.2f} | {r['dif_repo B']:+.2f} |")
md += ["", "## As três caixas da antiga \"afirmação falsa\", por modelo e braço (contagem)", "| | contradita | anulada seca | anulada com ressalva | conferíveis |", "|---|---|---|---|---|"]
for m in MODS:
    for b in "abc":
        cs = [c for V in cel([m], b) for c in por_laudo[V] if c in ver and c not in AUTOR]
        k = Counter(caixa(c) for c in cs)
        md.append(f"| {m} · {BR[b]} | {k['contradita']} | {k['anulada_seca']} | {k['anulada_ressalva']} | {len(cs)} |")
(AQUI / "v4_resultados.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print("ok |", len(por_laudo), "laudos |", len(ALE) - len(AUTOR), "afirmacoes na conta | caixas:", dict(cx))
