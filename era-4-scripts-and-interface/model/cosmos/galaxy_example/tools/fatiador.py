r"""
fatiador.py · corta textos antigos (states, diários) em pedaços, etiqueta e gera os números de sentido.
v0.2.1 · 16/10/2026 (sem Ollama, guarda os pedaços e avisa, em vez de quebrar).
v0.2.0 · 12/10/2026 (tipo, era e dono vêm de fora, não do nome; data DDMMAAAA ou AAAA-MM-DD; aceita pasta) · tars (Claude), o thinker do NUD · guardião.
v0.1.0 · 03/10/2026.

Os ORIGINAIS ficam intactos: o fatiador só LÊ. Os pedaços (cópia do texto, cortada e organizada)
e os números vão pro galley do módulo, uma subpasta por fonte (galley\states\, galley\diaries\):
  <galley>\\pedacos.jsonl  -> um pedaço por linha: id, fonte, caminho, secao, data, tipo, era, dono, texto
  <galley>\\vetores.jsonl  -> id + os números (embedding) de cada pedaço

Uso:
  python fatiador.py <pasta galley> --tipo state|diario --era 3 --dono thinker <arquivo.md ou pasta> [...]
Uma pasta entra inteira (os .md de dentro, sem subpastas).
Corte: por seção (títulos #, ##, ###); seção grande é dividida por parágrafo, até ~800 caracteres.
Fatiar de novo o mesmo arquivo SUBSTITUI os pedaços dele (não duplica).
"""
import json
import os
import re
import sys
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

MODELO = "qwen3-embedding:0.6b"
OLLAMA = "http://127.0.0.1:11434/api/embed"
LIMITE = 800


def embed(textos):
    req = urllib.request.Request(OLLAMA, data=json.dumps({"model": MODELO, "input": textos}).encode("utf-8"),
                                 headers={"Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=600))["embeddings"]


def secoes(texto):
    """Divide o markdown em (titulo, corpo) pelos títulos #, ##, ###."""
    atual, corpo, out = "(início)", [], []
    for linha in texto.splitlines():
        m = re.match(r"^#{1,3}\s+(.*)", linha)
        if m:
            if "".join(corpo).strip():
                out.append((atual, "\n".join(corpo).strip()))
            atual, corpo = m.group(1).strip(), []
        else:
            corpo.append(linha)
    if "".join(corpo).strip():
        out.append((atual, "\n".join(corpo).strip()))
    return out


def picar(corpo):
    """Junta parágrafos até ~LIMITE caracteres; parágrafo gigante é cortado por frase."""
    partes = []
    unidades = []
    for bloco in re.split(r"\n\s*\n", corpo):
        # cada item de lista (- , * , 1. ) é uma unidade própria: não misturar assuntos num pedaço
        unidades += [u for u in re.split(r"\n(?=\s*(?:[-*]|\d+\.)\s)", bloco) if u.strip()]
    for par in unidades:
        par = par.strip()
        if not par:
            continue
        if len(par) <= LIMITE:
            partes.append(par)
        else:
            atual = ""
            for frase in re.split(r"(?<=[.!?;])\s+|\n", par):
                if atual and len(atual) + len(frase) + 1 > LIMITE:
                    partes.append(atual.strip())
                    atual = ""
                atual += frase + " "
            if atual.strip():
                partes.append(atual.strip())
    pedacos, atual = [], ""
    for p in partes:
        # só junta unidades PEQUENAS (assunto curto); unidade com corpo próprio vira pedaço sozinha
        if atual and (len(atual) + len(p) + 2 > LIMITE or len(atual) >= 250):
            pedacos.append(atual)
            atual = ""
        atual = (atual + "\n\n" + p) if atual else p
    if atual:
        pedacos.append(atual)
    return pedacos


def data_do_nome(nome):
    """A data mora no nome: AAAA-MM-DD (alguns states de agosto) ou DDMMAAAA (o resto)."""
    m = re.search(r"(20\d{2})-(\d{2})-(\d{2})", nome)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
    m = re.search(r"(\d{2})(\d{2})(20\d{2})", nome)
    return f"{m.group(3)}-{m.group(2)}-{m.group(1)}" if m else ""


def argumentos(argv):
    """Separa as opções (--tipo, --era, --dono) dos arquivos; pasta vira a lista dos .md dela."""
    opc, arquivos, i = {"tipo": "", "era": "", "dono": ""}, [], 0
    while i < len(argv):
        a = argv[i]
        if a.startswith("--") and a[2:] in opc and i + 1 < len(argv):
            opc[a[2:]] = argv[i + 1]
            i += 2
            continue
        if os.path.isdir(a):
            arquivos += sorted(os.path.join(a, n) for n in os.listdir(a) if n.lower().endswith(".md"))
        else:
            arquivos.append(a)
        i += 1
    return opc, arquivos


def ler_jsonl(p):
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as f:
        return [json.loads(l) for l in f if l.strip()]


def gravar_jsonl(p, linhas):
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        for l in linhas:
            f.write(json.dumps(l, ensure_ascii=False) + "\n")
    os.replace(tmp, p)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    galley = os.path.abspath(sys.argv[1])
    opc, arquivos = argumentos(sys.argv[2:])
    if not (opc["tipo"] and opc["era"] and opc["dono"]):
        print("RECUSADO: diga --tipo (state ou diario), --era e --dono. O fatiador não adivinha pelo nome do arquivo.")
        sys.exit(2)
    os.makedirs(galley, exist_ok=True)
    p_ped, p_vet = os.path.join(galley, "pedacos.jsonl"), os.path.join(galley, "vetores.jsonl")
    pedacos, vetores = ler_jsonl(p_ped), {v["id"]: v for v in ler_jsonl(p_vet)}
    for caminho in arquivos:
        caminho = os.path.abspath(caminho)
        nome = os.path.basename(caminho)
        with open(caminho, encoding="utf-8") as f:
            texto = f.read()
        base = os.path.splitext(nome)[0].strip("_")
        velhos = {p["id"] for p in pedacos if p.get("caminho") == caminho}   # refatiar substitui (pelo caminho)
        pedacos = [p for p in pedacos if p["id"] not in velhos]
        vetores = {k: v for k, v in vetores.items() if k not in velhos}
        if any(p["id"].startswith(base + "#") for p in pedacos):
            print(f"RECUSADO: já existe no galley outro arquivo chamado {nome} (os ids colidiriam). Nada foi gravado.")
            sys.exit(2)
        novos = []
        for titulo, corpo in secoes(texto):
            for i, t in enumerate([t for t in picar(corpo) if re.search(r"\w", t)], 1):   # pula pedaço sem texto (ex.: só "---")
                novos.append({"id": f"{base}#{len(novos) + 1:02d}", "fonte": nome, "caminho": caminho,
                              "secao": titulo, "parte": i, "data": data_do_nome(nome), "tipo": opc["tipo"],
                              "era": opc["era"], "dono": opc["dono"], "texto": t})
        try:
            nums = embed([f"{p['secao']}\n{p['texto']}" for p in novos]) if novos else []
        except OSError:   # sem Ollama: guarda os pedaços mesmo assim (a busca por palavra já funciona)
            nums = []
            print(f"{nome}: o Ollama não respondeu; pedaços guardados sem os números de sentido. "
                  "Pra ganhar a busca por sentido, ligue o Ollama e fatie este arquivo de novo.")
        for p, v in zip(novos, nums):
            vetores[p["id"]] = {"id": p["id"], "modelo": MODELO, "vetor": [round(x, 5) for x in v]}
        pedacos += novos
        print(f"{nome}: {len(novos)} pedaços")
    gravar_jsonl(p_ped, pedacos)
    gravar_jsonl(p_vet, list(vetores.values()))
    print(f"galley: {len(pedacos)} pedaços no total -> {galley}")


if __name__ == "__main__":
    main()
