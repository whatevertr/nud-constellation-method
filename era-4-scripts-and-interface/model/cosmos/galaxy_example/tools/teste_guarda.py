"""
teste_guarda.py · o pipe-test da guarda: manda pedidos de mentira pra guarda.py e confere a decisão de cada um.
Rode depois de qualquer mudança na guarda ou no guarda.json. Tem que dar tudo OK antes de ligar um agente novo.
Agente novo: acrescente os casos dele em CASOS (o que ele pode e o que ele não pode).
"""
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
GALAXY = os.path.dirname(AQUI)
CASA = lambda nome: os.path.join(GALAXY, "station", nome, "CLAUDE.md")
MISSION = os.path.join(GALAXY, "missions", "my-first-mission", "CLAUDE.md")

# (descrição, agente, ferramenta, entrada, deve_barrar)
CASOS = [
    ("sessão principal lê a casa do thinker",         "",        "Read", {"file_path": CASA("module_thinker")}, False),
    ("thinker lê a própria casa",                      "thinker", "Read", {"file_path": CASA("module_thinker")}, False),
    ("thinker faz commit",                             "thinker", "Bash", {"command": "git commit -m x"}, False),
    ("thinker apaga de verdade",                       "thinker", "Bash", {"command": "rm notas.md"}, True),
    ("manager lê a mission",                           "manager", "Read", {"file_path": MISSION}, False),
    ("manager lê a própria casa",                      "manager", "Read", {"file_path": CASA("module_manager")}, False),
    ("manager lê a casa do thinker",                   "manager", "Read", {"file_path": CASA("module_thinker")}, True),
    ("manager escreve na casa do thinker",             "manager", "Edit", {"file_path": CASA("module_thinker")}, True),
    ("manager faz push",                               "manager", "Bash", {"command": "git push"}, True),
    ("manager vê o git status",                        "manager", "Bash", {"command": "git status"}, False),
    ("worker lê a casa do manager",                    "worker",  "Read", {"file_path": CASA("module_manager")}, True),
    ("worker lê a casa do thinker pelo terminal",      "worker",  "Bash", {"command": "cat ../station/module_thinker/CLAUDE.md"}, True),
    ("worker trabalha na mission",                     "worker",  "Write", {"file_path": MISSION}, False),
    ("worker move pro _to_delete",                     "worker",  "Bash", {"command": "mv rascunho.md ../../_to_delete/"}, False),
    ("worker apaga (Remove-Item)",                     "worker",  "Bash", {"command": "Remove-Item rascunho.md"}, True),
    ("worker busca na galaxy inteira",                 "worker",  "Grep", {"pattern": "senha", "path": GALAXY}, True),
    ("worker busca só na mission",                     "worker",  "Grep", {"pattern": "post", "path": os.path.dirname(MISSION)}, False),
    ("agente desconhecido lê a casa do worker",        "qualquer", "Read", {"file_path": CASA("module_worker")}, True),
    ("agente desconhecido lê a mission",               "qualquer", "Read", {"file_path": MISSION}, False),
    ("frase com 'formar' não é apagar",                "worker",  "Bash", {"command": "echo 'formar o time'"}, False),
]


def decide(agente, ferramenta, entrada):
    pedido = {"tool_name": ferramenta, "tool_input": entrada, "cwd": os.path.dirname(MISSION)}
    if agente:
        pedido["agent_type"] = agente
    r = subprocess.run([sys.executable, os.path.join(AQUI, "guarda.py")], input=json.dumps(pedido),
                       capture_output=True, text=True, encoding="utf-8")
    return '"deny"' in r.stdout


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    ok = 0
    for desc, agente, ferramenta, entrada, deve in CASOS:
        barrou = decide(agente, ferramenta, entrada)
        certo = barrou == deve
        ok += certo
        print(f"{'OK    ' if certo else 'FALHOU'} | {desc} | {'barrou' if barrou else 'passou'}")
    print(f"\n{ok}/{len(CASOS)}")
    sys.exit(0 if ok == len(CASOS) else 1)
