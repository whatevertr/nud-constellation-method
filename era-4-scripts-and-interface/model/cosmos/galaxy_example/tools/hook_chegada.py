"""
hook_chegada.py · hook SessionStart (Era 4). Roda quando a sessão abre, volta, é limpa ou compactada.
Se a sessão está num módulo (station/module_x com log.jsonl), imprime o bloco de CHEGADA:
o Claude Code coloca esse texto no começo da conversa. Só lê; nunca escreve.
v0.1.0 · 02/10/2026 · tars (Claude), o thinker do NUD · guardião.
"""
import json
import os
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # acentos sempre certos, mesmo sem PYTHONUTF8

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leitor  # noqa: E402

try:
    entrada = json.load(sys.stdin)
except Exception:
    entrada = {}
cwd = os.path.abspath(entrada.get("cwd") or os.getcwd())
origem = entrada.get("source", "?")

if os.path.basename(os.path.dirname(cwd)).lower() == "station" and os.path.exists(os.path.join(cwd, "CLAUDE.md")):
    try:
        print(leitor.chegada(cwd))
        print(f"(origem da chegada: {origem})")
    except Exception as erro:   # o hook nunca derruba a sessão: avisa e segue
        print(f"⚠️ HOOK DE CHEGADA FALHOU ({erro}). Avise a pessoa: o resumo do log não foi injetado.")
sys.exit(0)
