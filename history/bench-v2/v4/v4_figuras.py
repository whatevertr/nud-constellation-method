# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import csv, html, json, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
P, OUT = AQUI.parent / "dados", AQUI.parent / "relatorio_final" / "figuras"
OUT.mkdir(parents=True, exist_ok=True)
CAP = ["claude-opus-5-5", "gpt-6.1-sol", "gemini-4-argon"]
PEQ = ["claude-haiku-5-5", "gpt-5.4-mini", "gemini-3.5-flash-lite"]
CURTO = {"claude-opus-5-5": "Opus 5.5", "gpt-6.1-sol": "GPT-6.1-sol", "gemini-4-argon": "Gemini 4 Argon", "claude-haiku-5-5": "Haiku 5.5",
         "gpt-5.4-mini": "GPT-5.4-mini", "gemini-3.5-flash-lite": "Flash Lite 3.5", "maiores (3)": "MAIORES (3)", "compactos (3)": "COMPACTOS (3)"}
BR = {"a": "cru", "b": "só piso", "c": "tríade"}
COR = {"critico": "#3d2b8f", "prioridade": "#9085e9", "ajuste": "#1c5cab", "melhoria": "#86b6ef", "elogio": "#eda100", "constatacao": "#a59d92",
       "inferencia_declarada": "#e87ba4", "verdadeiro": "#1baf7a", "parcial": "#9bd8bf", "contradita": "#26242b", "anulada_seca": "#eb6834",
       "anulada_ressalva": "#f3b8cd", "anulada": "#ddd6cc", "cru": "#a59d92", "só piso": "#2a78d6", "tríade": "#3d2b8f"}
CLARO = {"critico", "ajuste", "contradita", "tríade", "só piso"}
NOME = {"critico": "crítico", "prioridade": "prioridade", "ajuste": "ajuste", "melhoria": "melhoria", "elogio": "elogio", "constatacao": "constatação",
        "inferencia_declarada": "inferência declarada", "verdadeiro": "verdadeira", "parcial": "parcial", "contradita": "contradita",
        "anulada_seca": "anulada seca", "anulada_ressalva": "anulada com ressalva", "anulada": "anulada"}
FUNDO, TINTA, TINTA2, GRADE = "#f4efe8", "#22202a", "#5b5862", "#d9d2c8"
FONTE = "ui-monospace,Consolas,Menlo,monospace"
e = html.escape


def svg(w, h, corpo, titulo):
    css = (f"text{{font-family:{FONTE};fill:{TINTA}}}.r{{font-size:12px}}.g{{font-size:12px;font-weight:700;letter-spacing:.05em}}"
           f".x{{font-size:11px;fill:{TINTA2}}}.n{{font-size:11px;font-weight:700}}.t{{font-size:14px;font-weight:700}}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" role="img" aria-label="{e(titulo)}"><style>{css}</style>'
            f'<rect width="{w}" height="{h}" fill="{FUNDO}"/>{corpo}</svg>')


def legenda(cats, x, y, passo=None):
    out, cx = [], x
    for k in cats:
        out.append(f'<rect x="{cx}" y="{y - 10}" width="12" height="12" rx="2" fill="{COR[k]}"/><text x="{cx + 17}" y="{y}" class="r">{e(NOME.get(k, k))}</text>')
        cx += passo or (30 + 7.4 * len(NOME.get(k, k)))
    return "".join(out)


def barras(linhas, cats, arq, titulo, total_txt="total", escala=None, fmt_lado=None):
    W, ESQ, DIR, H, GAP, y0 = 1000, 200, 150, 24, 7, 62
    L = W - ESQ - DIR
    alt = y0 + sum(22 if r == "—" else H + GAP for r, _ in linhas) + 12
    o = [f'<text x="12" y="20" class="t">{e(titulo)}</text>', legenda(cats, 12, 42)]
    ticks = (0, 25, 50, 75, 100) if not escala else [escala[0] * i / 4 for i in range(5)]
    for p in ticks:
        x = ESQ + L * p / (100 if not escala else escala[0])
        o.append(f'<line x1="{x:.1f}" y1="{y0 - 4}" x2="{x:.1f}" y2="{alt - 8}" stroke="{GRADE}"/><text x="{x:.1f}" y="{y0 - 8}" class="x" text-anchor="middle">{p:g}%</text>')
    o.append(f'<text x="{ESQ + L + 26}" y="{y0 - 8}" class="x">{e(total_txt)}</text>')
    y = y0
    for r, cont in linhas:
        if r == "—":
            o.append(f'<text x="12" y="{y + 15}" class="g">{e(cont.upper())}</text>')
            y += 22
            continue
        tot = sum(cont.get(k, 0) for k in cats) if not escala else escala[1][r]
        o.append(f'<text x="{ESQ - 8}" y="{y + 16}" text-anchor="end" class="r">{e(r)}</text>')
        x = ESQ
        for k in cats:
            n = cont.get(k, 0)
            if not n or not tot:
                continue
            pct = 100 * n / tot
            w = L * pct / (100 if not escala else escala[0])
            o.append(f'<rect x="{x:.2f}" y="{y}" width="{max(w - 1.5, .6):.2f}" height="{H}" rx="2" fill="{COR[k]}"><title>{e(r)} · {NOME[k]}: {pct:.1f}% ({n})</title></rect>')
            if w > 34 and not escala:
                o.append(f'<text x="{x + w / 2:.1f}" y="{y + 16}" text-anchor="middle" class="n" style="fill:{"#fff" if k in CLARO else "#111"}">{pct:.0f}%</text>')
            x += w
        o.append(f'<text x="{ESQ + L + 8}" y="{y + 16}" class="r">{e(fmt_lado(r, cont, tot) if fmt_lado else str(tot))}</text>')
        y += H + GAP
    (OUT / arq).write_text(svg(W, alt, "".join(o), titulo), encoding="utf-8")


jl = lambda n: [json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines() if l.strip()]
mapa = {l.split(",")[0]: l.split(",", 1)[1].strip().split("|") for l in (P / "v2_mapa_secreto.csv").read_text(encoding="utf-8").splitlines()[1:]}
ver = {x["codigo"]: x["veredito"] for x in jl("v2_gabarito_consenso.jsonl")}
rot = {x["codigo"]: x["rotulo"] for x in jl("v3_rotulo.jsonl")}
for n in ("v3_rotulo_revisao.jsonl", "v3_rotulo_releitura.jsonl"):
    rot.update({x["codigo"]: x["rotulo"] for x in jl(n)})
ALE = {f"{a['laudo']}#{a['n']}": a for a in jl("v2_alegacoes.jsonl")}
res = {json.loads(l)["codigo"]: json.loads(l)["ressalva"] for l in (AQUI / "v4_ressalva.jsonl").read_text(encoding="utf-8").splitlines()}
NA_CONTA = [c for c, a in ALE.items() if "[autor]" not in a["alegacao"].lower()]
celulas = list(csv.DictReader((AQUI / "v4_celulas.csv").open(encoding="utf-8")))
contr = list(csv.DictReader((AQUI / "v4_contrastes.csv").open(encoding="utf-8")))
mb = lambda c: mapa[c.split("#")[0]][:2]

CAT_ROT = ["critico", "prioridade", "ajuste", "melhoria", "elogio", "constatacao", "inferencia_declarada"]
L3 = []
for nome, ms in (("maiores", CAP), ("compactos", PEQ)):
    L3.append(("—", nome))
    for b in "abc":
        L3.append((f"{nome} · {BR[b]}", Counter(rot[c] for c in NA_CONTA if mb(c)[0] in ms and mb(c)[1] == b)))
barras(L3, CAT_ROT, "fig3_rotulos.svg", "O que os laudos afirmam, por capacidade e condição", "afirmações")
print("FIG3"); [print(" ", r, {k: f"{100 * c[k] / sum(c.values()):.1f}% ({c[k]})" for k in CAT_ROT}, sum(c.values())) for r, c in L3 if r != "—"]


def caixa(c):
    if c not in ver or rot[c] == "inferencia_declarada":
        return None
    return {"falso": "contradita", "nao_verificavel": "anulada_ressalva" if res[c] else "anulada_seca"}.get(ver[c])


CAT_CX = ["contradita", "anulada_seca", "anulada_ressalva"]
L2, den = [], {}
for nome, ms in (("maiores", CAP), ("compactos", PEQ)):
    L2.append(("—", nome))
    for m in ms:
        for b in "abc":
            cs = [c for c in NA_CONTA if c in ver and mb(c) == [m, b]]
            r = f"{CURTO[m]} · {BR[b]}"
            den[r] = len(cs)
            L2.append((r, Counter(k for k in map(caixa, cs) if k)))
barras(L2, CAT_CX, "fig2_falsas.svg", "Afirmações contraditas e anuladas, em % das afirmações conferíveis", "contagem / conferíveis", escala=(7, den),
       fmt_lado=lambda r, c, t: f"{c['contradita']}·{c['anulada_seca']}·{c['anulada_ressalva']} / {t}")

L6 = []
for k in CAT_ROT:
    cs = [c for c in NA_CONTA if c in ver and rot[c] == k]
    cont = Counter({"verdadeiro": "verdadeiro", "parcial": "parcial", "falso": "contradita", "nao_verificavel": "anulada"}[ver[c]] for c in cs)
    L6.append((NOME[k], cont))
CAT_V = ["verdadeiro", "parcial", "anulada", "contradita"]
barras(L6, CAT_V, "fig6_rotulo_veredito.svg", "Cada tipo de afirmação contra o gabarito (todas as condições)", "conferíveis")
print("FIG6"); [print(" ", r, {k: f"{100 * c[k] / sum(c.values()):.1f}% ({c[k]})" for k in CAT_V}, sum(c.values())) for r, c in L6]

W, ESQ, DIR, H, y0 = 1000, 200, 190, 20, 62
Lg = W - ESQ - DIR
mx = 45
o = ['<text x="12" y="20" class="t">Marcas de não-verificação (🍷) por laudo, por modelo e condição</text>', legenda(["cru", "só piso", "tríade"], 12, 42, 110)]
for t in range(0, mx + 1, 10):
    x = ESQ + Lg * t / mx
    o.append(f'<line x1="{x:.1f}" y1="{y0 - 4}" x2="{x:.1f}" y2="{y0 + 2 * 22 + 18 * (H + 3) + 6 * 8 - 6}" stroke="{GRADE}"/><text x="{x:.1f}" y="{y0 - 8}" class="x" text-anchor="middle">{t}</text>')
o.append(f'<text x="{ESQ + Lg + 8}" y="{y0 - 8}" class="x">🍷/laudo · % com ressalva</text>')
y = y0
for nome, ms in (("maiores", CAP), ("compactos", PEQ)):
    o.append(f'<text x="12" y="{y + 15}" class="g">{nome.upper()}</text>')
    y += 22
    for m in ms:
        for b in "abc":
            r = next(x for x in celulas if x["grupo"] == m and x["braco"] == BR[b])
            v, pr = float(r["tacas_no_texto"]), float(r["pct_com_ressalva"])
            o.append(f'<text x="{ESQ - 8}" y="{y + 14}" text-anchor="end" class="r">{e(CURTO[m])} · {BR[b]}</text>'
                     f'<rect x="{ESQ}" y="{y}" width="{max(Lg * v / mx, .8):.1f}" height="{H}" rx="2" fill="{COR[BR[b]]}"/>'
                     f'<text x="{ESQ + Lg + 8}" y="{y + 14}" class="r">{v:.1f} · {pr:.0f}%</text>')
            y += H + 3
        y += 8
(OUT / "fig5_tacas.svg").write_text(svg(W, y + 6, "".join(o), "Taças por laudo"), encoding="utf-8")

METS = [("taxa_grave_real", "graves reais (p.p.)"), ("taxa_falsa", "falsas (p.p.)"), ("alegacoes", "afirmações por laudo"), ("pts_laudo", "pontos por laudo")]
GR = CAP + ["maiores (3)"] + PEQ + ["compactos (3)"]
W, ESQ, PW, GAP, RH, y0 = 1100, 150, 215, 20, 30, 84
o = ['<text x="12" y="20" class="t">Diferença contra a condição "cru", comparada dentro de cada repositório (IC 95%)</text>',
     f'<rect x="12" y="32" width="11" height="11" fill="none" stroke="{COR["só piso"]}" stroke-width="2"/><text x="29" y="42" class="r">só piso − cru</text>'
     f'<circle cx="170" cy="38" r="5.5" fill="{COR["tríade"]}"/><text x="181" y="42" class="r">tríade − cru</text>'
     f'<text x="300" y="42" class="x">traço = intervalo de 95%; se cruza o zero, a diferença cabe no ruído</text>']
alt = y0 + len(GR) * RH + 14
for i, g in enumerate(GR):
    yy = y0 + i * RH
    if g.startswith(("maiores", "compactos")):
        o.append(f'<rect x="0" y="{yy - 2}" width="{W}" height="{RH}" fill="#e9e2d8"/>')
    o.append(f'<text x="{ESQ - 10}" y="{yy + 18}" text-anchor="end" class="{"g" if "(" in g else "r"}">{e(CURTO[g])}</text>')
for j, (k, nome) in enumerate(METS):
    x0 = ESQ + j * (PW + GAP)
    rs = [r for r in contr if r["metrica"] == k and r["contraste"] in ("só piso − cru", "tríade − cru")]
    lim = max(max(abs(float(r["ic_lo"])), abs(float(r["ic_hi"]))) for r in rs) * 1.08
    sx = lambda v: x0 + PW / 2 + (PW / 2) * v / lim
    o.append(f'<text x="{x0 + PW / 2}" y="{y0 - 22}" text-anchor="middle" class="g">{e(nome)}</text>')
    passo = next(p for p in (0.5, 1, 2, 5, 10, 20) if lim / p <= 3.2)
    t = -int(lim / passo) * passo
    while t <= lim:
        o.append(f'<line x1="{sx(t):.1f}" y1="{y0 - 6}" x2="{sx(t):.1f}" y2="{alt - 10}" stroke="{TINTA2 if abs(t) < 1e-9 else GRADE}"/>'
                 f'<text x="{sx(t):.1f}" y="{y0 - 9}" class="x" text-anchor="middle">{t:+g}</text>')
        t += passo
    for i, g in enumerate(GR):
        for ct, dy, cor in (("só piso − cru", 9, COR["só piso"]), ("tríade − cru", 21, COR["tríade"])):
            r = next(x for x in rs if x["grupo"] == g and x["contraste"] == ct)
            d, lo, hi = float(r["diferenca"]), float(r["ic_lo"]), float(r["ic_hi"])
            yy = y0 + i * RH + dy
            o.append(f'<line x1="{sx(lo):.1f}" y1="{yy}" x2="{sx(hi):.1f}" y2="{yy}" stroke="{cor}" stroke-width="2" stroke-linecap="round"/>')
            dica = f"<title>{e(CURTO[g])} · {ct} · {nome}: {d:+.2f} [{lo:+.2f}; {hi:+.2f}] p={r['p_perm']}</title>"
            if ct.startswith("só"):
                o.append(f'<rect x="{sx(d) - 4.5:.1f}" y="{yy - 4.5}" width="9" height="9" fill="{FUNDO}" stroke="{cor}" stroke-width="2">{dica}</rect>')
            else:
                o.append(f'<circle cx="{sx(d):.1f}" cy="{yy}" r="5" fill="{cor}">{dica}</circle>')
(OUT / "fig4_diferencas.svg").write_text(svg(W, alt, "".join(o), "Diferenças contra o cru"), encoding="utf-8")

W, Hh = 1000, 300
cx = lambda x, y, w, h, t1, t2, cor="#fff": (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{cor}" stroke="{TINTA2}"/>'
                                               f'<text x="{x + w / 2}" y="{y + h / 2 - 3}" text-anchor="middle" class="n" style="font-size:12px">{e(t1)}</text>'
                                               f'<text x="{x + w / 2}" y="{y + h / 2 + 14}" text-anchor="middle" class="x">{e(t2)}</text>')
seta = lambda x1, y1, x2, y2: f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{TINTA2}" stroke-width="1.5" marker-end="url(#s)"/>'
o = [f'<defs><marker id="s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="{TINTA2}"/></marker></defs>',
     '<text x="12" y="20" class="t">O desenho do estudo</text>',
     cx(20, 50, 170, 56, "3 repositórios", "congelados em um commit"), seta(190, 78, 222, 78),
     cx(225, 50, 170, 56, "3 dossiês de texto", "iguais para todos"), seta(395, 78, 427, 78),
     cx(430, 50, 250, 56, "6 modelos × 3 condições × 5", "270 avaliações, sem ferramentas"), seta(680, 78, 712, 78),
     cx(715, 50, 265, 56, "extração às cegas", "11.832 afirmações"),
     seta(848, 106, 848, 138),
     cx(715, 140, 265, 56, "gabarito (veredito)", "2 conferidores + amostra com clone + juiz", "#eaf6f0"), seta(715, 168, 683, 168),
     cx(430, 140, 250, 56, "rótulo de cada afirmação", "juiz cego: modelo, condição, repo", "#ece9fb"), seta(430, 168, 398, 168),
     cx(225, 140, 170, 56, "ressalva (🍷)", "lida no texto do laudo", "#fbe9f0"),
     seta(310, 196, 310, 228),
     cx(20, 230, 960, 50, "análise: cada condição comparada com o \"cru\" dentro do mesmo repositório", "2 métricas primárias do protocolo + análise exploratória (postura, volume, ressalva)", "#fff")]
(OUT / "fig1_desenho.svg").write_text(svg(W, Hh, "".join(o), "Desenho do estudo"), encoding="utf-8")
print("ok:", sorted(p.name for p in OUT.glob("*.svg")))
