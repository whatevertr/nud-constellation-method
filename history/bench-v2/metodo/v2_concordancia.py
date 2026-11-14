# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import csv, json, sys
from collections import Counter
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent.parent / "dados"


def jl(n):
    return {x["codigo"]: (x["veredito"], x["classe"]) for x in (json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines())}


hai, gem = jl("v2_completo_haiku.jsonl"), jl("v2_completo_gemini.jsonl")
ver = {}
for f in P.glob("veredito_v2_*.csv"):
    for r in csv.DictReader(f.open(encoding="utf-8", newline="")):
        ver[(f.stem.replace("veredito_v2_", ""), r["codigo"].strip())] = (r["veredito"].strip(), r["classe"].strip())
son = {}
for r in csv.DictReader((P / "v2_mapa_conferencia.csv").open(encoding="utf-8", newline="")):
    son[f"{r['laudo']}#{r['n']}"] = ver[(r["lote"], r["codigo"])]
real = lambda v: v in ("verdadeiro", "parcial")
grave = lambda x: real(x[0]) and x[1] in ("critico", "prioridade")
print("cobertura: haiku", len(hai), "| argon", len(gem))
for a, b, na, nb in ((hai, gem, "haiku", "argon"), (son, hai, "sonnet", "haiku"), (son, gem, "sonnet", "argon")):
    k = [c for c in a if c in b]
    n = len(k)
    print(f"{na} x {nb}: {n} pares | real igual {100 * sum(real(a[c][0]) == real(b[c][0]) for c in k) / n:.1f}% | grave igual {100 * sum(grave(a[c]) == grave(b[c]) for c in k) / n:.1f}% | classe igual {100 * sum(a[c][1] == b[c][1] for c in k) / n:.1f}% | falsas {sum(a[c][0] == 'falso' for c in k)} x {sum(b[c][0] == 'falso' for c in k)} | falsa nos dois {sum(a[c][0] == 'falso' and b[c][0] == 'falso' for c in k)}")
