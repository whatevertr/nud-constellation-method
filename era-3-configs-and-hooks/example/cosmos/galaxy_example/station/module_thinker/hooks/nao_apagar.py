"""
nao_apagar.py · hook de antes da ferramenta (PreToolUse) da Era 3: barra o comando de apagar antes de ele acontecer.
Lê o pedido da ferramenta (JSON na entrada). Se o comando apaga, sai com código 2 e explica: o agente recebe o recado
e move pro _to_delete em vez de apagar. Só biblioteca padrão. · tars (Claude), o thinker do NUD · guardião.
"""
import json, re, sys

APAGA = re.compile(r"(^|[\s;&|(])(rm|rmdir|del|erase|rd|Remove-Item|unlink|shred)(\s|$)", re.IGNORECASE)
try:
    pedido = json.load(sys.stdin)
except ValueError:
    sys.exit(0)
comando = (pedido.get("tool_input") or {}).get("command", "")
if pedido.get("tool_name") == "Bash" and APAGA.search(comando):
    print("Apagar de verdade, não: mova pro _to_delete/ da galaxy. Só a pessoa esvazia.", file=sys.stderr)
    sys.exit(2)
sys.exit(0)
