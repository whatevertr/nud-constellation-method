"""
leitor.py · lê os logs (só leitura, sem IA) e monta os resumos (Era 4, galaxy_observatory).
v0.3.1 · 10/10/2026 (a tarefa leva também o "quem" e o "canal" pro app) · tars (Claude), o thinker do NUD · guardião.
v0.3.0 · 04/10/2026 (o json leva as pendências, os tipos e as fichas dos thinkers).

Modos:
  python leitor.py chegada <pasta do módulo>   -> o bloco que o hook de chegada injeta
  python leitor.py mission <pasta da mission>  -> o resumo de UMA mission (hook ao tocar mission)
  python leitor.py json    <pasta da galaxy>   -> os dados pro app (vista Projetos)
O mesmo log sempre dá o mesmo resultado (determinístico).
"""
import datetime as dt
import json
import os
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # acentos sempre certos, mesmo sem PYTHONUTF8

IGNORAR = {"log.jsonl", ".obsidian", "__pycache__", ".git"}
TETO_TAREFAS = 5     # a chegada mostra no máximo 5 tarefas abertas do módulo (+ "e mais N")
TETO_MISSIONS = 6    # e no máximo 6 missions (só vivas e em análise, as mexidas por último primeiro)


def ler_log(pasta, nome="log.jsonl"):
    linhas = []
    p = os.path.join(pasta, nome)
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            for l in f:
                l = l.strip()
                if l:
                    try:
                        linhas.append(json.loads(l))
                    except json.JSONDecodeError:
                        linhas.append({"tipo": "nota", "txt": "⚠️ linha quebrada no log", "data": ""})
    return linhas


def dobrar(linhas):
    """Dobra o log: a situação ATUAL de cada tarefa, o último resumo, as decisões recentes."""
    tarefas = {}
    for l in linhas:
        if l.get("tipo") == "tarefa":
            t = tarefas.setdefault(l["id"], {})
            t.update({k: v for k, v in l.items() if k in ("id", "txt", "status", "prazo", "tag", "quem", "canal")})
            t["data"] = l.get("data", "")
    resumos = [l for l in linhas if l.get("tipo") == "resumo"]
    decisoes = [l for l in linhas if l.get("tipo") == "decisao"]
    return {
        "abertas": [t for t in tarefas.values() if t.get("status") == "aberta"],
        "tarefas": list(tarefas.values()),
        "resumo": resumos[-1] if resumos else None,
        "decisoes": decisoes[-5:],
        "ultima": linhas[-1]["data"] if linhas else "",
        # quantas linhas vieram DEPOIS do último resumo (resumo velho = o que aconteceu depois não está nele)
        "depois_do_resumo": (len(linhas) - 1 - max(i for i, l in enumerate(linhas) if l.get("tipo") == "resumo")) if resumos else len(linhas),
    }


def cabecalho(pasta):
    """Lê o cabeçalho (frontmatter entre ---) do CLAUDE.md da pasta."""
    p = os.path.join(pasta, "CLAUDE.md")
    cab = {}
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            texto = f.read()
        m = re.match(r"﻿?---\s*\n(.*?)\n---", texto, re.S)
        if m:
            for linha in m.group(1).splitlines():
                if ":" in linha:
                    k, v = linha.split(":", 1)
                    cab[k.strip()] = v.strip()
    return cab


def mexido_depois(pasta, ultima):
    """Arquivo da pasta mudado depois da última linha do log? (o aviso de 'mudança sem registro')"""
    if not ultima:
        return []
    limite = dt.datetime.strptime(ultima, "%Y-%m-%dT%H:%M") + dt.timedelta(minutes=1)
    novos = []
    for raiz, dirs, arqs in os.walk(pasta):
        dirs[:] = [d for d in dirs if d not in IGNORAR]
        for a in arqs:
            if a in IGNORAR:
                continue
            caminho = os.path.join(raiz, a)
            if dt.datetime.fromtimestamp(os.path.getmtime(caminho)) > limite:
                novos.append(os.path.relpath(caminho, pasta))
    return novos


def corta(s, n):
    s = s or ""
    return s if len(s) <= n else s[: n - 1] + "…"


def missions_da_galaxy(galaxy):
    raiz = os.path.join(galaxy, "missions")
    if not os.path.isdir(raiz):
        return []
    return [os.path.join(raiz, d) for d in sorted(os.listdir(raiz)) if os.path.isdir(os.path.join(raiz, d))]


def bloco_mission(pasta, longo=False):
    nome = os.path.basename(pasta)
    linhas = ler_log(pasta)
    d = dobrar(linhas)
    cab = cabecalho(pasta)
    out = [f"• {nome} — estado: {cab.get('estado', 'sem cabeçalho')} · último registro: {d['ultima'] or 'nenhum'}"]
    if d["resumo"]:
        out.append("  resumo: " + (d["resumo"]["txt"] if longo else corta(d["resumo"]["txt"], 220)))
    for t in d["abertas"][: (10 if longo else 3)]:
        out.append(f"  ▲ {t['id']}: {corta(t.get('txt', ''), 120)}" + (f" (prazo {t['prazo']})" if t.get("prazo") else ""))
    feitas = [t for t in d["tarefas"] if t.get("status") == "feita"][-2:]
    for t in feitas:   # deixa explícito o que fechou (evita resumo velho dizer que segue aberta)
        out.append(f"  ✓ {t['id']} FEITA em {t.get('data', '')}: {corta(t.get('txt', ''), 100)}")
    if longo:
        for dc in d["decisoes"]:
            out.append(f"  ✓ decidido: {corta(dc['txt'], 160)} — porque: {corta(dc.get('porque', ''), 160)}")
    novos = mexido_depois(pasta, d["ultima"])
    if novos:
        out.append(f"  ⚠️ mudança sem registro desde {d['ultima']}: {', '.join(novos[:4])}" + (" …" if len(novos) > 4 else ""))
    return "\n".join(out)


def chegada(modulo):
    modulo = os.path.abspath(modulo)
    galaxy = os.path.dirname(os.path.dirname(modulo))   # .../galaxy_x/station/module_y
    d = dobrar(ler_log(modulo))
    out = ["=== CHEGADA (hook, Era 4) ===",
           f"módulo: {os.path.basename(modulo)} · galaxy: {os.path.basename(galaxy)} · agora: {dt.datetime.now():%Y-%m-%d %H:%M}"]
    if d["resumo"]:
        r = d["resumo"]
        out += ["", f"ÚLTIMO RESUMO ({r.get('id')}, {r.get('data')}, por {r.get('por')}):", r.get("txt", "")]
    else:
        out += ["", "Ainda não há resumo no log do módulo (primeira vez?)."]
    # TETO (04/10, pedido da autora): a chegada tem tamanho máximo, não importa o tamanho do log.
    abertas = sorted(d["abertas"], key=lambda t: (t.get("prazo") or "9999", t.get("data", "")))
    if abertas:
        out += ["", "TAREFAS ABERTAS DO MÓDULO:"] + [f"▲ {t['id']}: {corta(t.get('txt', ''), 160)}" + (f" (prazo {t['prazo']})" if t.get("prazo") else "") for t in abertas[:TETO_TAREFAS]]
        if len(abertas) > TETO_TAREFAS:
            out.append(f"… e mais {len(abertas) - TETO_TAREFAS} (ver no app, aba pendências, ou no log)")
    soltas = [t for t in dobrar(ler_log(modulo, "pendencias.jsonl"))["tarefas"] if t.get("status") in ("aberta", "fazendo")]
    if soltas:   # só a contagem: as pendências soltas nunca são injetadas, ficam no arquivo e no app
        out += ["", f"PENDÊNCIAS SOLTAS: {len(soltas)} abertas em pendencias.jsonl (não vêm aqui; consulte quando precisar, ou veja no app)."]
    if d["decisoes"]:
        out += ["", "DECISÕES RECENTES:"] + [f"✓ {corta(x['txt'], 300)} — porque: {corta(x.get('porque', ''), 200)}" for x in d["decisoes"][-3:]]
    ms = [m for m in missions_da_galaxy(galaxy) if cabecalho(m).get("estado", "vivo").lower() in ("vivo", "analise")]
    ms.sort(key=lambda m: dobrar(ler_log(m))["ultima"], reverse=True)   # as mexidas por último primeiro
    if ms:
        out += ["", "MISSIONS DA GALAXY (vivas e em análise; estado ATUAL, lido agora dos logs; se o resumo acima disser outra coisa, vale ISTO):"] + [bloco_mission(m) for m in ms[:TETO_MISSIONS]]
        if len(ms) > TETO_MISSIONS:
            out.append(f"… e mais {len(ms) - TETO_MISSIONS} missions (ver no app)")
    novos = mexido_depois(modulo, d["ultima"])
    if novos:
        out += ["", f"⚠️ mudança sem registro no módulo desde {d['ultima']}: {', '.join(novos[:5])}"]
    out += ["=== fim da chegada ==="]
    return "\n".join(out)


def skills_em(pasta):
    """Pastas-folha com SKILL.md (a matrix da galaxy, ou o .claude\\skills do módulo). Lidas da pasta: skill nova aparece sozinha."""
    achadas = []
    if os.path.isdir(pasta):
        for raiz, dirs, arqs in os.walk(pasta):
            dirs[:] = [d for d in dirs if d not in IGNORAR]
            if "SKILL.md" in arqs:
                achadas.append(os.path.basename(raiz))
                dirs[:] = []
    return sorted(set(achadas))


def dias_desde(data):
    try:
        return (dt.date.today() - dt.date.fromisoformat(data[:10])).days
    except (ValueError, TypeError):
        return None


# As conquistas possíveis (04/10, pedido da autora: moram aqui no back; o app mostra só as destravadas).
# Só o que dá pra medir no log ou nas pastas: nenhum número inventado.
CONQUISTAS = [
    ("primeiro registro",   lambda f: f["registros"] >= 1),
    ("dormiu e acordou",    lambda f: f["resumos_proprios"] >= 1),
    ("10 registros",        lambda f: f["registros"] >= 10),
    ("50 registros",        lambda f: f["registros"] >= 50),
    ("100 registros",       lambda f: f["registros"] >= 100),
    ("500 registros",       lambda f: f["registros"] >= 500),
    ("uma semana na Era 4", lambda f: (f["dias_era4"] or 0) >= 7),
    ("um mês na Era 4",     lambda f: (f["dias_era4"] or 0) >= 30),
    ("um ano de vida",      lambda f: (f["dias_vida"] or 0) >= 365),
    ("dono de mission",     lambda f: len(f["missions"]) >= 1),
    ("três missions",       lambda f: len(f["missions"]) >= 3),
    ("primeira skill",      lambda f: len(f["skills_proprias"]) >= 1),
    ("pendências zeradas",  lambda f: f["registros"] >= 1 and f["pendencias"] == 0),
]


def permissoes_de(mod, cab):
    """allow/deny da ficha. trava = o que o settings.json do módulo faz cumprir; combinado = o cabeçalho (instrução)."""
    # a regra do método, que vale pra todos (deny de delete no settings global + a guarda): um chip só, fixo
    out = [{"lado": "deny", "txt": "apagar (vale pra todos)", "trava": True}]
    try:
        with open(os.path.join(mod, ".claude", "settings.json"), encoding="utf-8") as f:
            perms = json.load(f).get("permissions", {})
        for lado in ("allow", "deny"):
            out += [{"lado": lado, "txt": r, "trava": True} for r in perms.get(lado, [])]
    except (OSError, ValueError):
        pass
    for lado in ("allow", "deny"):
        out += [{"lado": lado, "txt": r.strip(), "trava": False} for r in cab.get(lado, "").split(";") if r.strip()]
    return out


def conectores_de(mod):
    """Os conectores (MCP) que o agente usa, lidos do .mcp.json do módulo: aparecem no equipamento."""
    try:
        with open(os.path.join(mod, ".mcp.json"), encoding="utf-8") as f:
            return sorted(json.load(f).get("mcpServers", {}))
    except (OSError, ValueError):
        return []


def fichas(galaxy):
    """A ficha de cada thinker: o cabeçalho do CLAUDE.md do módulo (quem ele é, escrito uma vez) + o que se calcula sozinho."""
    station = os.path.join(galaxy, "station")
    if not os.path.isdir(station):
        return []
    skills_galaxy = skills_em(os.path.join(galaxy, "matrix"))
    tools = os.path.join(galaxy, "tools")
    itens = sorted(f[:-3] for f in os.listdir(tools) if f.endswith(".py") and not f.startswith("teste")) if os.path.isdir(tools) else []
    missions = missions_da_galaxy(galaxy)
    out = []
    for nome in sorted(os.listdir(station)):
        mod = os.path.join(station, nome)
        if not (nome.startswith("module_") and os.path.isdir(mod)):
            continue
        cab = cabecalho(mod)
        log = ler_log(mod)
        d = dobrar(log)
        pend = dobrar(ler_log(mod, "pendencias.jsonl"))["tarefas"]
        quem = cab.get("thinker", nome.replace("module_", ""))
        minhas = [m for m in missions if cabecalho(m).get("dono") == quem]
        falta = [t for t in pend + d["tarefas"] if t.get("status") in ("aberta", "fazendo")]
        for m in minhas:
            falta += [t for t in dobrar(ler_log(m))["tarefas"] if t.get("status") in ("aberta", "fazendo")]
        resumo = d["resumo"] or {}
        ultima_coisa = (resumo.get("txt") or "").split("|")[0].strip() or (log[-1].get("txt", "") if log else "")
        out.append({
            "modulo": nome, "pasta": mod, "cabecalho": cab, "thinker": quem,
            "registros": len(log), "resumos": sum(1 for l in log if l.get("tipo") == "resumo"),
            "resumos_proprios": sum(1 for l in log if l.get("tipo") == "resumo" and l.get("por") == quem),
            "era4_desde": log[0]["data"][:10] if log else "", "dias_era4": dias_desde(log[0]["data"]) if log else None,
            "dias_vida": dias_desde(cab.get("nascido", "")),
            "ultima_coisa": ultima_coisa, "ultima_data": resumo.get("data") or (log[-1]["data"] if log else ""),
            "pendencias": len(falta), "missions": [os.path.basename(m) for m in minhas],
            "skills": sorted(set(skills_galaxy + skills_em(os.path.join(mod, ".claude", "skills")))),
            "skills_proprias": skills_em(os.path.join(mod, ".claude", "skills")),
            "itens": itens, "tem_retrato": os.path.exists(os.path.join(mod, cab.get("retrato") or "retrato.png")),
        })
        out[-1]["permissoes"] = permissoes_de(mod, cab)
        out[-1]["conectores"] = conectores_de(mod)
        out[-1]["conquistas"] = [nome_c for nome_c, ok in CONQUISTAS if ok(out[-1])]
        out[-1]["conquistas_possiveis"] = len(CONQUISTAS)
    return out


def dados_json(galaxy):
    galaxy = os.path.abspath(galaxy)
    projetos = []
    for m in missions_da_galaxy(galaxy):
        d = dobrar(ler_log(m))
        cab = cabecalho(m)
        projetos.append({
            "nome": os.path.basename(m), "pasta": m, "cabecalho": cab, "tem_cabecalho": bool(cab),
            "ultima": d["ultima"], "resumo": (d["resumo"] or {}).get("txt", ""),
            "resumo_data": (d["resumo"] or {}).get("data", ""), "depois_do_resumo": d["depois_do_resumo"],
            "abertas": d["abertas"], "tarefas": d["tarefas"],
            "sem_registro": mexido_depois(m, d["ultima"]),
        })
    # pendências fora de mission: o pendencias.jsonl de cada módulo da station (dobrado igual ao log)
    pendencias = []
    station = os.path.join(galaxy, "station")
    if os.path.isdir(station):
        for nome in sorted(os.listdir(station)):
            mod = os.path.join(station, nome)
            if nome.startswith("module_") and os.path.isdir(mod):
                for t in dobrar(ler_log(mod, "pendencias.jsonl"))["tarefas"]:
                    pendencias.append(dict(t, modulo=nome.replace("module_", ""), pasta=mod))
                # as tarefas do log do próprio módulo também entram no kanban (bug achado pela autora, 05/10)
                for t in dobrar(ler_log(mod))["tarefas"]:
                    pendencias.append(dict(t, modulo=nome.replace("module_", ""), pasta=mod, do_log=True))
    tipos = {}
    try:
        with open(os.path.join(galaxy, "tools", "tipos.json"), encoding="utf-8") as f:
            tipos = json.load(f).get("tipos", {})
    except (OSError, ValueError):
        pass
    return {"galaxy": os.path.basename(galaxy), "gerado": f"{dt.datetime.now():%Y-%m-%d %H:%M}",
            "projetos": projetos, "pendencias": pendencias, "tipos": tipos, "fichas": fichas(galaxy)}


if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] not in ("chegada", "mission", "json"):
        print(__doc__)
        sys.exit(1)
    modo, alvo = sys.argv[1], sys.argv[2]
    if modo == "chegada":
        print(chegada(alvo))
    elif modo == "mission":
        print(bloco_mission(os.path.abspath(alvo), longo=True))
    else:
        print(json.dumps(dados_json(alvo), ensure_ascii=False, indent=1))
