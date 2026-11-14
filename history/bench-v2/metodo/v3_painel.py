# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import html, json, math, re, statistics, sys
from collections import Counter, defaultdict
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
P = Path(__file__).resolve().parent.parent / "dados"
CAP = {"claude-opus-5-5", "gpt-6.1-sol", "gemini-4-argon"}
PROV = {"claude": ["claude-opus-5-5", "claude-haiku-5-5"], "gpt": ["gpt-6.1-sol", "gpt-5.4-mini"], "gemini": ["gemini-4-argon", "gemini-3.5-flash-lite"]}
BR = {"a": "cru", "b": "só piso", "c": "tríade"}

CORES = {"critico": ("#3d2b8f", "#8f7ff0", "#fff"), "prioridade": ("#9085e9", "#c8c0f7", "#111"), "ajuste": ("#1c5cab", "#3987e5", "#fff"),
         "melhoria": ("#86b6ef", "#9ec5f4", "#111"), "elogio": ("#eda100", "#eab308", "#111"), "constatacao": ("#a59d92", "#8d877e", "#111"),
         "informacao": ("#a59d92", "#8d877e", "#111"), "inferencia_declarada": ("#e87ba4", "#d55181", "#111"),
         "afirmacao_falsa": ("#26242b", "#f0efec", "#fff"), "inferencia_falsa": ("#e87ba4", "#d55181", "#111"), "anulada": ("#ddd6cc", "#403c37", "#111"),
         "acertou": ("#1baf7a", "#199e70", "#111"), "exagerou": ("#eb6834", "#d95926", "#111"), "subestimou": ("#2a78d6", "#3987e5", "#fff")}
NOME = {"critico": "crítico", "prioridade": "prioridade", "ajuste": "ajuste", "melhoria": "melhoria", "elogio": "elogio", "constatacao": "constatação",
        "informacao": "informação", "inferencia_declarada": "inferência declarada", "afirmacao_falsa": "afirmação falsa", "inferencia_falsa": "inferência falsa",
        "anulada": "anulada (fora do alcance)", "acertou": "acertou o grau", "exagerou": "exagerou o grau", "subestimou": "subestimou o grau"}
CAT_ROT = ["critico", "prioridade", "ajuste", "melhoria", "elogio", "constatacao", "inferencia_declarada"]
CAT_5 = ["critico", "prioridade", "ajuste", "melhoria", "elogio", "informacao", "afirmacao_falsa", "inferencia_falsa", "anulada"]
CAT_9 = ["acertou", "exagerou", "subestimou", "afirmacao_falsa", "inferencia_falsa"]
PESO = {"critico": 2, "prioridade": 2, "ajuste": 1, "melhoria": 1, "elogio": -0.5, "informacao": 0.5}
GRAU_ROT = {"critico": 4, "prioridade": 3, "ajuste": 2, "melhoria": 2, "elogio": 1, "constatacao": 1}
GRAU_PES = {"critico": 4, "prioridade": 3, "ajuste": 2, "melhoria": 2, "elogio": 1, "informacao": 1}


def jl(n):
    return [json.loads(l) for l in (P / n).read_text(encoding="utf-8").splitlines()]


mapa = {l.split(",")[0]: l.split(",", 1)[1].strip().split("|") for l in (P / "v2_mapa_secreto.csv").read_text(encoding="utf-8").splitlines()[1:]}
ver = {x["codigo"]: x["veredito"] for x in jl("v2_gabarito_consenso.jsonl")}
rot = {x["codigo"]: x["rotulo"] for x in jl("v3_rotulo.jsonl")}
rot.update({x["codigo"]: x["rotulo"] for x in jl("v3_rotulo_revisao.jsonl")})
rot.update({x["codigo"]: x["rotulo"] for x in jl("v3_rotulo_releitura.jsonl")})
alc = {x["codigo"]: x["alcancava"] for x in jl("v3_alcance.jsonl")}
pes = {x["codigo"]: x["peso_real"] for x in jl("v3_peso_real.jsonl")}
I = []
for a in jl("v2_alegacoes.jsonl"):
    c = f"{a['laudo']}#{a['n']}"
    m, b = mapa[a["laudo"]][:2]
    I.append((m, b, a["laudo"], c))
laudos = defaultdict(set)
for m, b, ld, c in I:
    laudos[(m, b)].add(ld)


def especie(c):
    v, r = ver.get(c), rot.get(c)
    if v is None or r is None:
        return None
    inf = r == "inferencia_declarada"
    if inf:
        return "inferencia_falsa" if alc.get(c) == "sim" else None
    if v in ("falso", "nao_verificavel"):
        return "afirmacao_falsa"
    return None


def pontos_da(c):
    v, r = ver.get(c), rot.get(c)
    if v is None or r is None:
        return None
    inf = r == "inferencia_declarada"
    if inf:
        return -0.5 if alc.get(c) == "sim" else 0.5
    if v == "nao_verificavel":
        return -1
    if v == "falso":
        return -1
    if c not in pes:
        return None
    return PESO[pes[c]] * (1 if v == "verdadeiro" else 0.5)


def cat5(c):
    e = especie(c)
    if e:
        return e
    v = ver.get(c)
    if v == "nao_verificavel":
        return "anulada"
    return pes.get(c)


def cat9(c):
    v, r = ver.get(c), rot.get(c)
    if v is None or r is None or v == "nao_verificavel":
        return None
    e = especie(c)
    if e:
        return e
    if r == "inferencia_declarada":
        return None
    if c not in pes:
        return None
    gr, gp = GRAU_ROT[r], GRAU_PES[pes[c]]
    return "acertou" if gr == gp else ("exagerou" if gr > gp else "subestimou")


DADOS = []
W, ESQ, DIR = 1000, 230, 110
LARG = W - ESQ - DIR


def eixo(y, h):
    return "".join(f'<line x1="{ESQ + LARG * p / 100:.1f}" y1="{y}" x2="{ESQ + LARG * p / 100:.1f}" y2="{y + h}" class="grade"/>'
                   f'<text x="{ESQ + LARG * p / 100:.1f}" y="{y - 6}" class="eixo" text-anchor="{"end" if p == 100 else "middle"}">{p}%</text>' for p in (0, 25, 50, 75, 100))


def barras100(linhas, cats, cab="total", extra=None):
    DADOS.append(("barras", linhas, cats, extra))
    H, GAP, y0 = 30, 10, 26
    altura = y0 + sum((22 if r == "—" else H + GAP) for r, _ in linhas) + 10
    out = [f'<svg viewBox="0 0 {W} {altura}" class="g" role="img">', eixo(y0 - 4, altura - y0)]
    y = y0
    for rot_, cont in linhas:
        if rot_ == "—":
            out.append(f'<text x="8" y="{y + 15}" class="grupo">{html.escape(cont)}</text>')
            y += 22
            continue
        tot = sum(cont.get(k, 0) for k in cats)
        out.append(f'<text x="{ESQ - 10}" y="{y + 20}" text-anchor="end" class="rot">{html.escape(rot_)}</text>')
        x = ESQ
        for k in cats:
            n = cont.get(k, 0)
            if not n:
                continue
            w, pct = LARG * n / tot, 100 * n / tot
            dica = f"{rot_} · {NOME[k]}: {pct:.1f}% · {n} de {tot}"
            out.append(f'<rect x="{x:.2f}" y="{y}" width="{max(w - 2, .5):.2f}" height="{H}" rx="2" class="s s-{k}" data-dica="{html.escape(dica)}"/>')
            if w > 34:
                out.append(f'<text x="{x + w / 2 - 1:.1f}" y="{y + 20}" text-anchor="middle" class="num t-{k}">{pct:.0f}%</text>')
            x += w
        lado = f"{tot}" + (f" (+{extra[rot_]})" if extra and extra.get(rot_) else "")
        out.append(f'<text x="{ESQ + LARG + 8}" y="{y + 20}" class="tot">{lado}</text>')
        y += H + GAP
    out.append(f'<text x="{ESQ + LARG + 8}" y="16" class="eixo">{cab}</text></svg>')
    return "".join(out)


def tabela(linhas, cats, extras=None):
    extras = extras or []
    cab = "".join(f"<th>{NOME[k]}</th>" for k in cats) + "<th>total</th>" + "".join(f"<th>{n}</th>" for n, _ in extras)
    corpo = []
    for r, cont in linhas:
        if r == "—":
            corpo.append(f'<tr class="tg"><td colspan="{len(cats) + 2 + len(extras)}">{html.escape(cont)}</td></tr>')
            continue
        tot = sum(cont.get(k, 0) for k in cats)
        cel = "".join(f"<td>{cont.get(k, 0)}<small> ({100 * cont.get(k, 0) / tot:.1f}%)</small></td>" if tot else "<td>0</td>" for k in cats)
        corpo.append(f"<tr><td>{html.escape(r)}</td>{cel}<td>{tot}</td>" + "".join(f"<td>{d.get(r, 0)}</td>" for _, d in extras) + "</tr>")
    return f'<details><summary>ver a tabela</summary><table><tr><th></th>{cab}</tr>{"".join(corpo)}</table></details>'


def ic95(v):
    if len(v) < 2:
        return (statistics.mean(v) if v else 0), 0
    t = {14: 2.145, 13: 2.160, 12: 2.179}.get(len(v) - 1, 1.96)
    return statistics.mean(v), t * statistics.stdev(v) / math.sqrt(len(v))


def pontos(linhas, titulo_eixo, fmt="{:.2f}", contagem=None, piso=None):
    DADOS.append(("pontos", linhas, fmt, titulo_eixo, contagem))
    H, y0 = 26, 26
    meds = [ic95(v) for r, v in linhas if r != "—"]
    lo = min([m - e for m, e in meds] + [0]) if piso is None else piso
    hi = max(m + e for m, e in meds)
    hi += (hi - lo) * .05
    esc = lambda v: ESQ + LARG * (v - lo) / (hi - lo)
    altura = y0 + sum((22 if r == "—" else H) for r, _ in linhas) + 10
    out = [f'<svg viewBox="0 0 {W} {altura}" class="g" role="img">']
    bruto = (hi - lo) / 5
    base = 10 ** math.floor(math.log10(bruto))
    passo = next(k * base for k in (1, 2, 5, 10) if k * base >= bruto)
    t = math.ceil(lo / passo) * passo
    while t <= hi:
        out.append(f'<line x1="{esc(t):.1f}" y1="{y0 - 4}" x2="{esc(t):.1f}" y2="{altura - 6}" class="grade{" zero" if abs(t) < 1e-9 else ""}"/><text x="{esc(t):.1f}" y="{y0 - 10}" class="eixo" text-anchor="middle">{fmt.format(t)}</text>')
        t += passo
    y = y0
    for r, v in linhas:
        if r == "—":
            out.append(f'<text x="8" y="{y + 15}" class="grupo">{html.escape(v)}</text>')
            y += 22
            continue
        m, e = ic95(v)
        a, z = (max(m - e, piso) if piso is not None else m - e), m + e
        lado = fmt.format(m) + (f" ({contagem[r]})" if contagem else "")
        dica = f"{r}: média {fmt.format(m)} · IC 95% {fmt.format(a)} a {fmt.format(z)} · {len(v)} laudos" + (f" · {contagem[r]} no total" if contagem else "")
        out.append(f'<text x="{ESQ - 10}" y="{y + 17}" text-anchor="end" class="rot">{html.escape(r)}</text>'
                   f'<line x1="{esc(a):.1f}" y1="{y + 13}" x2="{esc(z):.1f}" y2="{y + 13}" class="ic"/>'
                   f'<circle cx="{esc(m):.1f}" cy="{y + 13}" r="5" class="ponto" data-dica="{html.escape(dica)}"/>'
                   f'<rect x="{esc(m) - 12:.1f}" y="{y + 1}" width="24" height="24" fill="transparent" data-dica="{html.escape(dica)}"/>'
                   f'<text x="{ESQ + LARG + 8}" y="{y + 17}" class="tot">{lado}</text>')
        y += H
    out.append(f'<text x="{ESQ + LARG + 8}" y="16" class="eixo">{titulo_eixo}</text></svg>')
    return "".join(out)


def leg(cats):
    return "".join(f'<span class="leg"><i class="s-{k}"></i>{NOME[k]}</span>' for k in cats)


def grupos_cap(f_cel):
    L = []
    for nome, f in (("capazes", lambda m: m in CAP), ("pequenos", lambda m: m not in CAP)):
        L.append(("—", nome))
        for b in "abc":
            L.append((f"{nome} · {BR[b]}", f_cel(lambda m, f=f: f(m), b)))
    return L


def grupos_prov(f_cel, somado=False):
    L = []
    for pv, ms in PROV.items():
        L.append(("—", pv))
        if somado:
            for b in "abc":
                L.append((f"{pv} · {BR[b]}", f_cel(lambda m, ms=ms: m in ms, b)))
        else:
            for mm in ms:
                for b in "abc":
                    L.append((f"{mm} · {BR[b]}", f_cel(lambda m, mm=mm: m == mm, b)))
    return L


cont_rot = lambda fm, b: Counter(rot[c] for m, bb, ld, c in I if fm(m) and bb == b and c in rot)
secoes = []
LER13 = "Tudo o que os laudos alegaram, pelo <b>RÓTULO</b>: o que cada frase afirma, lido da frase isolada. É o que o usuário recebe, sem conferir. Não há categoria \"falsa\" aqui. " + leg(CAT_ROT)
secoes.append(("1. O que os laudos afirmam, por capacidade", LER13, barras100(grupos_cap(cont_rot), CAT_ROT, "alegações"), tabela(grupos_cap(cont_rot), CAT_ROT)))
secoes.append(("2. O que os laudos afirmam, por provedor", "Os dois modelos de cada provedor somados. " + LER13, barras100(grupos_prov(cont_rot, True), CAT_ROT, "alegações"), tabela(grupos_prov(cont_rot, True), CAT_ROT)))
secoes.append(("3. O que os laudos afirmam, por modelo", "Cada modelo nos três braços, agrupado por provedor. " + LER13, barras100(grupos_prov(cont_rot), CAT_ROT, "alegações"), tabela(grupos_prov(cont_rot), CAT_ROT)))

for esp, titulo, desc in (("afirmacao_falsa", "4a. Afirmação falsa (−1 na pontuação)", "O laudo afirmou algo que o gabarito diz que é falso, ou afirmou seco o que não dava pra ver no material (anulada sem marcador de não-conferência)."),
                          ("inferencia_falsa", "4b. Inferência falsa (−0,5 na pontuação)", "O laudo declarou não poder conferir algo que o material alcançava (rótulo \"inferência declarada\" e, na pergunta própria feita ao Fable com o dossiê aberto, o material alcançava), independente de o conteúdo estar certo. A taça usada certo (o material não alcançava) não entra aqui: ela soma na pontuação.")):
    L, cont = [], {}
    for pv, ms in PROV.items():
        L.append(("—", pv))
        for mm in ms:
            for b in "abc":
                vals, n = [], 0
                for ld in laudos[(mm, b)]:
                    cs = [c for m, bb, l2, c in I if l2 == ld and c in ver]
                    k = sum(1 for c in cs if especie(c) == esp)
                    n += k
                    vals.append(100 * k / len(cs) if cs else 0)
                L.append((f"{mm} · {BR[b]}", vals))
                cont[f"{mm} · {BR[b]}"] = n
    secoes.append((titulo, desc + " Percentual das alegações conferíveis de cada laudo. Ponto = média dos 15 laudos; traço = intervalo de 95% (se os traços de dois braços se cruzam, a diferença cabe no ruído). Na direita: a média em % e, entre parênteses, a contagem total.",
                   pontos(L, "% (contagem)", "{:.1f}", cont, piso=0), ""))

cont5 = lambda fm, b: Counter(cat5(c) for m, bb, ld, c in I if fm(m) and bb == b and rot.get(c) == "critico" and c in ver and cat5(c))
L5 = grupos_cap(cont5) + grupos_prov(cont5)
LER5 = ("Só as alegações que o laudo <b>afirmou como crítico</b> (RÓTULO). A cor é <b>o que o fato era</b>: o PESO REAL quando o gabarito diz verdadeiro ou parcial; "
        "afirmação falsa quando o gabarito diz falso; anulada quando estava fora do alcance do material. <b>Violeta escuro = era crítico mesmo.</b> " + leg(CAT_5))
secoes.append(("5. O que o laudo chamou de crítico: o que era de fato", LER5, barras100(L5, CAT_5, "chamou de crítico"), tabela(L5, CAT_5)))

p_al, p_ld = [], []
for pv, ms in PROV.items():
    p_al.append(("—", pv))
    p_ld.append(("—", pv))
    for mm in ms:
        for b in "abc":
            va, vl = [], []
            for ld in laudos[(mm, b)]:
                ps = [p for p in (pontos_da(c) for m, bb, l2, c in I if l2 == ld) if p is not None]
                vl.append(sum(ps))
                va.append(sum(ps) / len(ps) if ps else 0)
            p_al.append((f"{mm} · {BR[b]}", va))
            p_ld.append((f"{mm} · {BR[b]}", vl))
REGRA = ("Pesos do PESO REAL: crítico +2 · prioridade +2 · ajuste +1 · melhoria +1 · elogio −0,5 · informação +0,5. "
         "Pontos da alegação: verdadeira = peso × 1; parcial = peso × 0,5; falsa = −1 (afirmação falsa); anulada com inferência declarada = +0,5 (avisou que não dava pra conferir); "
         "anulada sem o aviso = −1 (afirmação falsa); inferência declarada: se o material alcançava o que ela diz não ter conferido = −0,5 (inferência falsa), se não alcançava = +0,5 (taça certa).")
secoes.append(("7. Pontuação, por alegação", REGRA + " Por alegação = a média por frase, sem premiar quem fala mais. Ponto = média dos 15 laudos; traço = intervalo de 95%.", pontos(p_al, "pts/alegação"), ""))
secoes.append(("8. Pontuação, total por laudo", "A mesma regra somada no laudo inteiro. Aqui quem fala mais ganha mais: leia junto com o gráfico 7.", pontos(p_ld, "pts/laudo", "{:.0f}"), ""))

def cont9(fm, b):
    return Counter(cat9(c) for m, bb, ld, c in I if fm(m) and bb == b and cat9(c))
L9 = grupos_cap(cont9) + grupos_prov(cont9)
graves, anul, tacas, lado9 = {}, {}, {}, {}
def soma(fm, b, teste):
    return sum(1 for m, bb, ld, c in I if fm(m) and bb == b and teste(c))
celulas = [(f"{nome} · {BR[b]}", f, b) for nome, f in (("capazes", lambda m: m in CAP), ("pequenos", lambda m: m not in CAP)) for b in "abc"]
celulas += [(f"{mm} · {BR[b]}", (lambda m, mm=mm: m == mm), b) for pv, ms in PROV.items() for mm in ms for b in "abc"]
for rot_, f, b in celulas:
    graves[rot_] = soma(f, b, lambda c: cat9(c) == "subestimou" and pes.get(c) in ("critico", "prioridade"))
    anul[rot_] = soma(f, b, lambda c: ver.get(c) == "nao_verificavel")
    tacas[rot_] = soma(f, b, lambda c: ver.get(c) in ("verdadeiro", "parcial", "falso") and rot.get(c) == "inferencia_declarada" and alc.get(c) == "nao")
    lado9[rot_] = anul[rot_] + tacas[rot_]
LER9 = ("O grau que o laudo <b>afirmou</b> (RÓTULO) contra o tamanho que o fato <b>tem</b> (PESO REAL), nas alegações conferíveis. "
        "Graus: crítico > prioridade > ajuste ou melhoria > elogio, constatação ou informação. "
        "<b>Verde = acertou o grau</b>; laranja = exagerou; azul = subestimou; preto = afirmação falsa; rosa = inferência falsa. "
        "Ficam fora da conta as anuladas (fora do alcance do material) e as taças certas (o laudo avisou que não dava pra conferir, e não dava): a soma das duas aparece entre parênteses na direita. "
        "Na tabela, a coluna <b>\"das quais graves\"</b> conta, dentro de \"subestimou\", as alegações cujo PESO REAL é crítico ou prioridade: o achado certo, despriorizado. " + leg(CAT_9))
EXTRAS9 = [("subestimou: das quais graves", graves), ("anuladas (fora)", anul), ("taças certas (fora)", tacas)]
secoes.append(("9. O grau que o laudo afirmou contra o tamanho do fato", LER9, barras100(L9, CAT_9, "total (fora)", lado9), tabela(L9, CAT_9, EXTRAS9)))

falta_peso = sum(1 for c, v in ver.items() if v in ("verdadeiro", "parcial") and c not in pes)
sem_ver = sum(1 for m, b, ld, c in I if c not in ver)
css = "".join(f".s-{k}{{fill:{c[0]};background:{c[0]}}}.t-{k}{{fill:{c[2]}}}" for k, c in CORES.items())
css_esc = "".join(f".s-{k}{{fill:{c[1]};background:{c[1]}}}.t-{k}{{fill:{'#f0efec' if k in ('anulada', 'constatacao', 'informacao') else '#111'}}}" for k, c in CORES.items())
corpo = "".join(f'<section><h2>{t}</h2><p>{d}</p>{s}{tb}</section>' for t, d, s, tb in secoes)
doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Bench v2 painel v3</title>
<style>:root{{--fundo:#f4efe8;--tinta:#22202a;--tinta2:#5b5862;--grade:#d9d2c8;--ic:#5b5862}}
{css}
@media (prefers-color-scheme:dark){{:root{{--fundo:#22202a;--tinta:#ece6f5;--tinta2:#b9b3c6;--grade:#3a3742;--ic:#b9b3c6}}{css_esc}}}
body{{background:var(--fundo);color:var(--tinta);font-family:ui-monospace,Consolas,monospace;margin:16px auto;max-width:1040px;padding:0 16px}}
h1{{font-size:18px}}h2{{font-size:15px;margin:34px 0 4px}}p{{font-size:13px;color:var(--tinta2);max-width:880px}}
.g{{width:100%;height:auto;display:block}}.rot,.tot{{font-size:12px;fill:var(--tinta)}}.grupo{{font-size:12px;font-weight:700;fill:var(--tinta);text-transform:uppercase;letter-spacing:.06em}}
.eixo{{font-size:11px;fill:var(--tinta2)}}.num{{font-size:11px;font-weight:700}}.grade{{stroke:var(--grade);stroke-width:1}}.grade.zero{{stroke:var(--tinta2)}}.ic{{stroke:var(--ic);stroke-width:2;stroke-linecap:round}}.ponto{{fill:var(--tinta)}}
.leg{{display:inline-flex;align-items:center;margin:0 14px 6px 0;font-size:12px}}.leg i{{width:12px;height:12px;display:inline-block;margin-right:5px;border-radius:2px;border:1px solid var(--grade)}}
details{{margin:6px 0 0;font-size:12px}}summary{{cursor:pointer;color:var(--tinta2)}}table{{border-collapse:collapse;margin-top:6px;font-size:11px}}td,th{{border-bottom:1px solid var(--grade);padding:3px 6px;text-align:right}}td:first-child{{text-align:left}}tr.tg td{{font-weight:700;text-align:left}}small{{color:var(--tinta2)}}
#dica{{position:fixed;pointer-events:none;background:var(--tinta);color:var(--fundo);font-size:12px;padding:5px 8px;border-radius:4px;display:none;max-width:360px;z-index:9}}rect.s:hover{{opacity:.8}}</style></head>
<body><h1>// bench v2 · painel (camada de análise refeita)</h1>
<p><b>Três colunas, três perguntas.</b> <b>GABARITO</b> = o veredito (verdadeiro, parcial, falso ou anulada: fora do alcance do material), já conferido. <b>RÓTULO</b> = o que cada frase afirma e com que peso, lido da frase isolada (Fable 5.2, cego pra modelo, braço e repositório). <b>PESO REAL</b> = supondo a frase verdadeira, que tamanho o fato tem, com o dossiê do repositório aberto (Fable 5.2, cego pra modelo e braço; só nas verdadeiras e parciais). As duas colunas novas vieram de sessões separadas: uma nunca viu a pergunta nem as respostas da outra.</p>
<details><summary>como o gabarito e as colunas foram montados (ressalva)</summary><p>O gabarito veio de três conferidores (Sonnet 5.5 com o repositório clonado numa amostra; Haiku 5.5 e Gemini 4 Argon lendo o mesmo dossiê que os laudos leram), com o Fable 5.2 como juiz às cegas onde discordaram; vale o que dava pra ver no dossiê. O RÓTULO e o PESO REAL seguem o manual de categorização aprovado pela autora (nota do agente de conferência e redação, 12/11/2026), com a regra da voz passiva ("não foi verificado"): só é inferência declarada quando é o avaliador que não pôde conferir; na dúvida, é. Pra cada inferência declarada, uma pergunta própria ao Fable 5.2, com o dossiê aberto e cego pra modelo e braço, decide se a taça procedia: "o material alcançava o que a frase diz não ter conferido?" (a alcançabilidade nunca se infere do veredito). Três frases suspeitas de rótulo trocado foram relidas com os testes da voz passiva e do condicional técnico. No PESO REAL o repositório é visível pelo dossiê (limite declarado). Ficaram de fora: {sem_ver} alegações de opinião, que não têm veredito; {falta_peso} alegação verdadeira ou parcial sem resposta do PESO REAL. A classe antiga do gabarito, o campo "hedge" e o grau extraído antes não são mais usados.</p></details>
<p><b>Como ler:</b> 1 a 3 = só o RÓTULO (o que os laudos afirmam). 4 = as falsas, nas duas espécies. 5 e 9 = o RÓTULO contra o PESO REAL (o que o laudo afirmou contra o tamanho do fato). 7 e 8 = a pontuação. Passe o mouse em qualquer barra ou ponto pra ver o número.</p>
{corpo}<div id="dica"></div>
<script>const d=document.getElementById('dica');document.addEventListener('mousemove',e=>{{const t=e.target.closest('[data-dica]');if(!t){{d.style.display='none';return}}d.textContent=t.dataset.dica;d.style.display='block';d.style.left=Math.min(e.clientX+14,innerWidth-370)+'px';d.style.top=(e.clientY+14)+'px'}});</script></body></html>"""
(P / "v3_painel.html").write_text(doc, encoding="utf-8")

sem_tag = lambda s: re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", s)).strip()
md = ["# Bench v2 · o painel em texto (camada de análise refeita)", "*Gerado por `v3_painel.py` junto com `v3_painel.html`, dos mesmos números.*", "",
      sem_tag(doc.split("<h1>")[1].split("<details>")[0]), "", "**Ressalva:** " + sem_tag(doc.split("(ressalva)</summary><p>")[1].split("</p>")[0]), ""]
for (titulo, desc, _, _), dado in zip(secoes, DADOS):
    md += [f"## {titulo}", sem_tag(desc), ""]
    if dado[0] == "barras":
        _, linhas, cats, _ = dado
        ex = EXTRAS9 if titulo.startswith("9.") else []
        md += ["| | " + " | ".join(NOME[k] for k in cats) + " | total |" + "".join(f" {n} |" for n, _ in ex), "|---" * (len(cats) + 2 + len(ex)) + "|"]
        for r, cont in linhas:
            if r == "—":
                md.append(f"| **{cont}** |" + " |" * (len(cats) + 1 + len(ex)))
                continue
            tot = sum(cont.get(k, 0) for k in cats)
            md.append(f"| {r} | " + " | ".join(f"{100 * cont.get(k, 0) / tot:.1f}% ({cont.get(k, 0)})" if tot else "0" for k in cats) + f" | {tot} |" + "".join(f" {d.get(r, 0)} |" for _, d in ex))
    else:
        _, linhas, fmt, eixo_t, contagem = dado
        md += [f"| | média ({eixo_t}) | IC 95% | laudos |" + (" contagem |" if contagem else ""), "|---|---|---|---|" + ("---|" if contagem else "")]
        for r, v in linhas:
            if r == "—":
                md.append(f"| **{v}** | | | |" + (" |" if contagem else ""))
                continue
            m, e = ic95(v)
            a_ = max(m - e, 0) if eixo_t.startswith("%") else m - e
            md.append(f"| {r} | {fmt.format(m)} | {fmt.format(a_)} a {fmt.format(m + e)} | {len(v)} |" + (f" {contagem[r]} |" if contagem else ""))
    md.append("")
(P / "v3_painel_texto.md").write_text("\n".join(md), encoding="utf-8")
print("ok v3_painel.html e v3_painel_texto.md |", len(I), "alegacoes |", sem_ver, "sem veredito |", falta_peso, "sem peso real")
