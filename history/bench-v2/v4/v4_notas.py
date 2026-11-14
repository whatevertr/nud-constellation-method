# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import csv, json, re, statistics, sys
from collections import defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
P = AQUI.parent / "dados"
CAP = ["claude-opus-5-5", "gpt-6.1-sol", "gemini-4-argon"]
PEQ = ["claude-haiku-5-5", "gpt-5.4-mini", "gemini-3.5-flash-lite"]
BR = {"a": "cru", "b": "só piso", "c": "tríade"}
REPO = {"r1": "método", "r2": "repo A", "r3": "repo B"}
NOTA_FINAL = {"V013": 4.0,
              "V017": 4.5,
              "V129": 7.5,
              "V220": 4.0,
              "V224": 9.0}
SEM_DOSSIE = {"V249"}

jl = lambda n: [json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines() if l.strip()]
mapa = {l.split(",")[0]: l.split(",", 1)[1].strip().split("|") for l in (P / "v2_mapa_secreto.csv").read_text(encoding="utf-8").splitlines()[1:]}
texto = {l["id"]: l["texto"] for l in jl("v2_laudos.jsonl")}
texto.update({l["id"]: l["texto"] for l in jl("v2_refeitos.jsonl")})
ver = {x["codigo"]: x["veredito"] for x in jl("v2_gabarito_consenso.jsonl")}
rot = {x["codigo"]: x["rotulo"] for x in jl("v3_rotulo.jsonl")}
for n in ("v3_rotulo_revisao.jsonl", "v3_rotulo_releitura.jsonl"):
    rot.update({x["codigo"]: x["rotulo"] for x in jl(n)})
por = defaultdict(list)
for a in jl("v2_alegacoes.jsonl"):
    if "[autor]" not in a["alegacao"].lower():
        por[a["laudo"]].append(f"{a['laudo']}#{a['n']}")

PAT = re.compile(r"(?<![\d/])(\d{1,2}(?:[.,]\d{1,2})?)\s*/\s*10\b(?!\s*/)")
CHAVE = re.compile(r"nota|parecer|avalia|veredito|score|geral|final|conclus|classific|\*\*\s*$|#\s*$|: ?\**$")


def nota(V):
    if V in NOTA_FINAL:
        return NOTA_FINAL[V], "conferida a mão"
    t = texto["|".join(mapa[V])]
    for m in PAT.finditer(t):
        v = float(m.group(1).replace(",", "."))
        if v <= 10 and not re.fullmatch(r"0\d", m.group(1)) and CHAVE.search(t[max(0, m.start() - 45):m.start()].replace("\n", " ").lower()):
            return v, "busca"
    return None, "sem nota"


N = {V: nota(V) for V in mapa if V not in SEM_DOSSIE}
with (AQUI / "v4_notas.csv").open("w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["laudo", "modelo", "condicao", "repositorio", "nota", "origem"])
    for V in sorted(N):
        w.writerow([V, mapa[V][0], BR[mapa[V][1]], REPO[mapa[V][2]], N[V][0], N[V][1]])


def linha(ms, g, b):
    Vs = [V for V, x in mapa.items() if V in N and x[0] in ms and x[1] == b and x[2] == g]
    cs = [c for V in Vs for c in por[V]]
    cf = [c for c in cs if c in ver]
    return (statistics.mean(N[V][0] for V in Vs if N[V][0] is not None), 100 * sum(rot[c] == "elogio" for c in cs) / len(cs),
            sum(ver[c] == "falso" for c in cf), len(cf), len(Vs))


md = ["# Bench v2 · recorte por repositório (v4)", "*Gerado por `v4_notas.py`. Nota = a nota de 0 a 10 dada pelo laudo. Cada célula: cru / só piso / tríade.*", "",
      f"Laudos com nota: {sum(1 for v in N.values() if v[0] is not None)} de {len(N)}; conferidas a mão: {len(NOTA_FINAL)}.", ""]
for nome, ms in (("Todos os modelos", CAP + PEQ), ("Maiores", CAP), ("Compactos", PEQ)):
    md += [f"## {nome}", "| repositório | nota média | elogios, % das afirmações | contraditas (contagem) | conferíveis | laudos |", "|---|---|---|---|---|---|"]
    for g in REPO:
        r = [linha(ms, g, b) for b in "abc"]
        md.append(f"| {REPO[g]} | " + " / ".join(f"{x[0]:.2f}" for x in r) + " | " + " / ".join(f"{x[1]:.1f}" for x in r) + " | " + " / ".join(str(x[2]) for x in r)
                  + " | " + " / ".join(str(x[3]) for x in r) + " | " + " / ".join(str(x[4]) for x in r) + " |")
    md.append("")
(AQUI / "v4_recorte_repositorio.md").write_text("\n".join(md), encoding="utf-8")
print("\n".join(md))
