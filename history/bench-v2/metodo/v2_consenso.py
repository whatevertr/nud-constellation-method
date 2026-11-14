# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import csv, json, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent.parent / "dados"
GRAV = ["critico", "prioridade", "ajuste", "melhoria", "descricao", "elogio"]
VCONS = ["falso", "nao_verificavel", "parcial", "verdadeiro"]


def jl(n):
    return {x["codigo"]: (x["veredito"], x["classe"]) for x in (json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines())}


hai, gem = jl("v2_completo_haiku.jsonl"), jl("v2_completo_gemini.jsonl")
_j = [json.loads(l) for l in (P / "v2_juiz_fable.jsonl").read_text(encoding="utf-8").splitlines()]
juiz = {x["codigo"]: (x["veredito"], x["classe"]) for x in _j if not x["lote"].startswith("e_")}
juiz_classe = {x["codigo"]: (x["veredito"], x["classe"]) for x in _j if x["lote"].startswith("e_")}
juiz_discorda_veredito = 0
ver = {}
for f in P.glob("veredito_v2_*.csv"):
    for r in csv.DictReader(f.open(encoding="utf-8", newline="")):
        ver[(f.stem.replace("veredito_v2_", ""), r["codigo"].strip())] = (r["veredito"].strip(), r["classe"].strip())
son = {f"{r['laudo']}#{r['n']}": ver[(r["lote"], r["codigo"])] for r in csv.DictReader((P / "v2_mapa_conferencia.csv").open(encoding="utf-8", newline=""))}


def maioria(vals, ordem):
    c = Counter(vals).most_common()
    topo = [v for v, n in c if n == c[0][1]]
    if len(topo) == 1:
        return topo[0], False
    return sorted(topo, key=ordem.index)[-1 if ordem is GRAV else 0], True


saida, fonte, empates_crit = [], Counter(), Counter()
for c in sorted(set(hai) | set(gem)):
    vs = [x for x in (hai.get(c), gem.get(c), son.get(c)) if x]
    if c in juiz:
        v, k = juiz[c]
        reg = {"codigo": c, "veredito": v, "classe": k, "fonte": "juiz_fable"}
    else:
        v, _ = maioria([x[0] for x in vs], VCONS)
        k, emp = maioria([x[1] for x in vs], GRAV)
        reg = {"codigo": c, "veredito": v, "classe": k, "fonte": "acordo" if len({x[1] for x in vs}) == 1 else ("classe_em_disputa" if emp else "maioria_classe")}
        if emp:
            empates_crit["envolve critico" if "critico" in {x[1] for x in vs} else "sem critico"] += 1
            reg["classes_dos_conferidores"] = sorted({x[1] for x in vs})
            if c in juiz_classe:
                reg["classe"] = juiz_classe[c][1]
                reg["fonte"] = "juiz_fable_classe"
                if (juiz_classe[c][0] in ("verdadeiro", "parcial")) != (v in ("verdadeiro", "parcial")):
                    juiz_discorda_veredito += 1
    reg["conferidores"] = len(vs)
    fonte[reg["fonte"]] += 1
    saida.append(reg)
with (P / "v2_gabarito_consenso.jsonl").open("w", encoding="utf-8", newline="\n") as f:
    for r in saida:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print("alegacoes no gabarito:", len(saida))
print("de onde veio:", dict(fonte))
print("empates de classe:", dict(empates_crit), "| nos empates, o juiz discordou de real/nao real em:", juiz_discorda_veredito)
print("vereditos:", dict(Counter(r["veredito"] for r in saida)))
print("classes (reais):", dict(Counter(r["classe"] for r in saida if r["veredito"] in ("verdadeiro", "parcial"))))
