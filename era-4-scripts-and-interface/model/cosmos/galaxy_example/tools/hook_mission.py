"""
hook_mission.py · hook PostToolUse (Era 4). Na PRIMEIRA vez, nesta sessão, que o agente lê ou mexe
num arquivo de uma mission (missions/<nome>/...), injeta o resumo do log daquela mission.
Imita o CLAUDE.md de subpasta, que o Claude Code carrega quando o agente toca um arquivo de lá.
Só lê o log; anota em %TEMP% quais missions já entraram nesta sessão.
v0.1.0 · 02/10/2026 · tars (Claude), o thinker do NUD · guardião.
"""
import json
import os
import re
import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")   # acentos sempre certos, mesmo sem PYTHONUTF8
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import leitor  # noqa: E402

try:
    entrada = json.load(sys.stdin)
except Exception:
    sys.exit(0)
ti = entrada.get("tool_input") or {}
alvo = str(ti.get("file_path") or ti.get("path") or "")
m = re.search(r"^(.*?[\\/]missions[\\/][^\\/]+)", alvo.replace("/", "\\"), re.I)
if not m:
    sys.exit(0)
mission = os.path.abspath(m.group(1))
if not os.path.exists(os.path.join(mission, "log.jsonl")):
    sys.exit(0)

sessao = re.sub(r"[^A-Za-z0-9_-]", "", entrada.get("session_id", "sem_sessao"))[:60]
marca = os.path.join(tempfile.gettempdir(), "cosmos_hooks", f"missions_{sessao}.json")
os.makedirs(os.path.dirname(marca), exist_ok=True)
ja = []
if os.path.exists(marca):
    try:
        ja = json.load(open(marca, encoding="utf-8"))
    except Exception:
        ja = []
if mission.lower() in ja:
    sys.exit(0)
ja.append(mission.lower())
json.dump(ja, open(marca, "w", encoding="utf-8"))

try:
    texto = "=== MISSION (hook, Era 4): primeira vez nesta sessão ===\n" + leitor.bloco_mission(mission, longo=True) + "\n=== fim ==="
except Exception as erro:
    texto = f"⚠️ HOOK DE MISSION FALHOU ({erro}). Avise a pessoa."
print(json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": texto}}, ensure_ascii=False))
sys.exit(0)
