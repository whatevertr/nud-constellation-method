"""
ultimo_estado.py · hook de abertura (SessionStart) da Era 3: entrega o último estado e o último diário da casa.
Só biblioteca padrão. O que ele imprime entra no contexto da sessão. · tars (Claude), o thinker do NUD · guardião.
"""
import os, re, sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
CASA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def mais_recente(pasta, prefixo):
    """O arquivo de data mais recente no nome (DDMMAAAA), ou nada."""
    melhor = None
    for nome in os.listdir(pasta) if os.path.isdir(pasta) else []:
        m = re.match(prefixo + r".*?(\d{2})(\d{2})(\d{4})\.md$", nome)
        if m:
            chave = (m.group(3), m.group(2), m.group(1))
            if melhor is None or chave > melhor[0]:
                melhor = (chave, os.path.join(pasta, nome))
    return melhor[1] if melhor else None

partes = []
for titulo, pasta, prefixo in (("ÚLTIMO ESTADO", "states", "state_"), ("ÚLTIMO DIÁRIO", "diary", "_diary_")):
    arq = mais_recente(os.path.join(CASA, pasta), prefixo)
    if arq:
        with open(arq, encoding="utf-8") as f:
            partes.append(f"=== {titulo} ({os.path.basename(arq)}) ===\n{f.read().strip()}")
print("\n\n".join(partes) if partes else "=== ÚLTIMO ESTADO ===\nAinda não há estado nem diário: é o primeiro dia.")
