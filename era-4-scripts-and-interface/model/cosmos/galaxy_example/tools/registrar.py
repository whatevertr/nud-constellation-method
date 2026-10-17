"""
registrar.py · a ÚNICA porta de escrita do log (Era 4).
v0.4.0 · 10/10/2026 (--quem: quem FAZ a tarefa, separado de quem escreve; --canal: onde a peça vai ao ar) · tars (Claude), o thinker do NUD · guardião.
v0.3.0 · 04/10/2026 (aviso de tipo: toda tarefa nova leva um --tag da lista tipos.json).

Ninguém escreve no log à mão: agente e app chamam este script, que confere o formato e
ACRESCENTA uma linha no `log.jsonl` da pasta (módulo ou mission). Nunca edita linha antiga.

Uso (exemplos):
  python registrar.py <pasta> --por thinker --tipo nota    --tag organizacao --txt "..."
  python registrar.py <pasta> --por thinker --tipo tarefa  --tag construcao --txt "..." --prazo 2026-10-10
  python registrar.py <pasta> --por thinker --tipo tarefa  --id t3 --status feita
  python registrar.py <pasta> --por thinker --tipo decisao --tag organizacao --txt "..." --porque "..."
  python registrar.py <pasta> --por thinker --tipo resumo  --tag organizacao --txt "onde paramos | decisões e porquê | o que vem | como ela está"
  python registrar.py <pasta> --por thinker       --tipo tarefa  --tag publicacao --txt "..." --quem pessoa --canal youtube:short --prazo 2026-10-20
  python registrar.py <pasta> --por thinker       --tipo nota    --tag alcance --canal youtube --txt "inscritos=4; views_28d=193"
Campos opcionais: --ref <arquivo com o detalhe>
--quem: quem FAZ a tarefa (pessoa, thinker...). Sem ele, é quem escreveu (--por). É o filtro "é minha" do app.
--canal: plataforma:formato (youtube:longo, instagram:reel, itch:pagina) ou só a plataforma. Tarefa com --canal + --prazo entra no calendário.
Tarefa nova: o --tag é o TIPO de trabalho, um dos que estão em tipos.json (ao lado deste script).
Sem tipo ou fora da lista, a linha entra, mas sai um AVISO pra corrigir com a pessoa.
"""
import argparse
import datetime as dt
import json
import os
import re
import sys

TIPOS = ("tarefa", "nota", "decisao", "resumo")
STATUS = ("aberta", "fazendo", "feita", "cancelada")
LIMITE = {"tarefa": 200, "nota": 300, "decisao": 300, "resumo": 1200}
# a raiz do cosmos = a pasta acima da galaxy destas tools (tools -> galaxy -> cosmos)
RAIZ = os.path.normcase(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
TIPOS_ARQ = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tipos.json")


def tipos_validos():
    try:
        with open(TIPOS_ARQ, encoding="utf-8") as f:
            return list(json.load(f)["tipos"])
    except (OSError, ValueError, KeyError):
        return None


def falhar(msg):
    print("RECUSADO: " + msg, file=sys.stderr)
    sys.exit(2)


def ler(arquivo):
    linhas = []
    if os.path.exists(arquivo):
        with open(arquivo, encoding="utf-8") as f:
            for n, l in enumerate(f, 1):
                l = l.strip()
                if l:
                    try:
                        linhas.append(json.loads(l))
                    except json.JSONDecodeError:
                        falhar(f"o log tem uma linha quebrada (linha {n}). Ninguém edita o log à mão: avise a pessoa.")
    return linhas


def main():
    ap = argparse.ArgumentParser(description="Acrescenta uma linha validada no log.jsonl de uma pasta.")
    ap.add_argument("pasta")
    ap.add_argument("--por", required=True, help="quem escreve (ex.: thinker, sentinela). 'pessoa' só pelo app.")
    ap.add_argument("--tipo", required=True, choices=TIPOS)
    ap.add_argument("--txt", default="")
    ap.add_argument("--tag", default="")
    ap.add_argument("--id", default="")
    ap.add_argument("--status", default="", choices=("",) + STATUS)
    ap.add_argument("--prazo", default="")
    ap.add_argument("--porque", default="")
    ap.add_argument("--ref", default="")
    ap.add_argument("--quem", default="", help="quem FAZ a tarefa (padrão: o --por). 'pessoa' pode: é a pendência que só a pessoa faz.")
    ap.add_argument("--canal", default="", help="plataforma:formato (ex.: youtube:short) ou só a plataforma")
    ap.add_argument("--pelo-app", action="store_true", help="só o app usa: libera --por pessoa")
    ap.add_argument("--pendencia", action="store_true", help="grava no pendencias.jsonl do MÓDULO (a lista viva do que falta, fora de mission), não no log")
    a = ap.parse_args()

    pasta = os.path.abspath(a.pasta)
    if not os.path.normcase(pasta).startswith(RAIZ + os.sep):
        falhar(f"a pasta precisa estar dentro de {RAIZ}.")
    if not os.path.isdir(pasta):
        falhar("a pasta não existe.")
    if not os.path.exists(os.path.join(pasta, "CLAUDE.md")):
        falhar("a pasta não tem CLAUDE.md: só módulo ou mission têm log.")
    por = a.por.strip().lower()
    if not re.fullmatch(r"[a-z0-9_]{2,40}", por):
        falhar("--por: só letras minúsculas, números e _ (ex.: thinker).")
    if por == "pessoa" and not a.pelo_app:
        falhar("só a pessoa assina como 'pessoa', e só pelo app.")
    if a.tag and not re.fullmatch(r"[a-z0-9-]{2,30}", a.tag):
        falhar("--tag: minúsculas, números e traço (ex.: organizacao, publicacao).")
    quem = a.quem.strip().lower()
    if quem and not re.fullmatch(r"[a-z0-9_]{2,40}", quem):
        falhar("--quem: só letras minúsculas, números e _ (ex.: pessoa, thinker).")
    if quem and a.tipo != "tarefa":
        falhar("--quem só vale pra tarefa (é quem faz).")
    canal = a.canal.strip().lower()
    if canal and not re.fullmatch(r"[a-z0-9-]{2,30}(:[a-z0-9-]{2,30})?", canal):
        falhar("--canal: plataforma:formato em minúsculas (ex.: youtube:short, instagram:reel) ou só a plataforma.")
    if canal and a.tipo not in ("tarefa", "nota"):
        falhar("--canal só vale pra tarefa (a peça) ou nota (o alcance).")
    if a.prazo:
        try:
            dt.date.fromisoformat(a.prazo)
        except ValueError:
            falhar("--prazo no formato AAAA-MM-DD.")
    txt = " ".join(a.txt.split())
    if len(txt) > LIMITE[a.tipo]:
        falhar(f"--txt passou do limite de {LIMITE[a.tipo]} caracteres pra '{a.tipo}' ({len(txt)}). O detalhe vai num arquivo e entra no --ref.")

    if a.pendencia and a.tipo != "tarefa":
        falhar("--pendencia só aceita --tipo tarefa.")
    arquivo = os.path.join(pasta, "pendencias.jsonl" if a.pendencia else "log.jsonl")
    antigas = ler(arquivo)
    linha = {"data": dt.datetime.now().strftime("%Y-%m-%dT%H:%M"), "por": por, "tipo": a.tipo}

    if a.tipo == "tarefa":
        ids = {l.get("id") for l in antigas if l.get("tipo") == "tarefa"}
        if a.id:
            if a.id not in ids:
                falhar(f"a tarefa {a.id} não existe neste log.")
            if not a.status:
                falhar("pra mudar uma tarefa existente, diga o --status (aberta, feita, cancelada).")
            linha.update(id=a.id, status=a.status)
            if txt:
                linha["txt"] = txt
        else:
            if not txt:
                falhar("tarefa nova precisa de --txt.")
            n = 1 + max([int(i[1:]) for i in ids if i and i[1:].isdigit()] or [0])
            linha.update(id=f"t{n}", status=a.status or "aberta", txt=txt)
            linha["quem"] = quem or por  # tarefa nova sempre nasce com dono
        if a.id and quem:
            linha["quem"] = quem  # passar a tarefa pra outra pessoa
        if a.prazo:
            linha["prazo"] = a.prazo
    else:
        if not txt:
            falhar(f"'{a.tipo}' precisa de --txt.")
        linha["txt"] = txt
        if a.tipo == "decisao":
            if not a.porque:
                falhar("decisão sem --porque não entra: o porquê é o que evita reabrir a discussão.")
            linha["porque"] = " ".join(a.porque.split())[:300]
        if a.tipo == "resumo":
            resumos = [l for l in antigas if l.get("tipo") == "resumo"]
            linha["id"] = f"r{len(resumos) + 1}"
            if resumos:
                linha["anterior"] = resumos[-1].get("id")
    avisos = []
    if a.tipo == "tarefa" and not a.id:
        validos = tipos_validos()
        if validos is None:
            avisos.append(f"não achei a lista de tipos em {TIPOS_ARQ}: o kanban não vai saber filtrar.")
        elif not a.tag:
            avisos.append(f"tarefa sem tipo. Use --tag com um destes: {', '.join(validos)}. Sem tipo, ela aparece como 'sem tipo' no kanban.")
        elif a.tag not in validos:
            avisos.append(f"o tipo '{a.tag}' não está na lista ({', '.join(validos)}). Se é um tipo novo, combine com a pessoa antes de pôr no tipos.json.")
    if a.tag:
        linha["tag"] = a.tag
    if canal:
        linha["canal"] = canal
    if a.ref:
        linha["ref"] = a.ref
    if a.pelo_app:
        linha["via"] = "app"

    with open(arquivo, "a", encoding="utf-8", newline="\n") as f:
        f.write(json.dumps(linha, ensure_ascii=False) + "\n")
    print("REGISTRADO: " + json.dumps(linha, ensure_ascii=False))
    for av in avisos:
        print("AVISO: " + av)


if __name__ == "__main__":
    main()
