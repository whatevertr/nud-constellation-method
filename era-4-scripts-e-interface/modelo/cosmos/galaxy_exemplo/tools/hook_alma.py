r"""
hook_alma.py · hook SessionStart (Era 4). Roda quando a sessão abre, volta, é limpa ou compactada.
A alma chega sozinha, como o trabalho chega pelo hook de chegada: se a sessão está num módulo
com `diary\`, imprime o último diário (a memória de convívio).
O texto é ÍNTIMO: só entra na sessão do próprio thinker, nunca em subagente. Só lê; nunca escreve.
v0.1.0 · 11/10/2026 · tars (Claude), o thinker do NUD · guardião.
"""
import json
import os
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

TETO = 12000   # caracteres por arquivo: o diário longo entra pelo fim (o mais recente do dia)

try:
    entrada = json.load(sys.stdin)
except Exception:
    entrada = {}
cwd = os.path.abspath(entrada.get("cwd") or os.getcwd())
diary = os.path.join(cwd, "diary")


def data_do_nome(nome):
    m = re.search(r"_(\d{2})(\d{2})(\d{4})", nome)   # ..._DDMMAAAA...
    return (m.group(3), m.group(2), m.group(1)) if m else ("0000", "00", "00")


def ler(p):
    with open(p, encoding="utf-8") as f:
        t = f.read()
    return t if len(t) <= TETO else "[…começo cortado pelo teto…]\n" + t[-TETO:]


if os.path.basename(os.path.dirname(cwd)).lower() == "station" and os.path.isdir(diary):
    try:
        nomes = sorted(os.listdir(diary))
        diarios = sorted((n for n in nomes if n.startswith("_diary_") and n.endswith(".md")), key=data_do_nome)
        partes = ["=== ALMA (hook, Era 4): quem você é com ela. Íntimo: não sai desta conversa ==="]
        if diarios:
            partes += ["", f"--- O ÚLTIMO DIÁRIO ({diarios[-1]}) ---", ler(os.path.join(diary, diarios[-1]))]
        partes += ["=== fim da alma ==="]
        if diarios:
            print("\n".join(partes))
    except Exception as erro:   # o hook nunca derruba a sessão: avisa e segue
        print(f"⚠️ HOOK DA ALMA FALHOU ({erro}). Avise a pessoa: o diário não foi injetado.")
sys.exit(0)
