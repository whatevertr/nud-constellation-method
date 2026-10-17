"""
painel.py · o app da Era 4: o painel do cosmos.
v0.7.0 · 17/10/2026 (versão pública: acha a raiz sozinho; cada galaxy é lida pelo leitor dela) · tars (Claude), o thinker do NUD · guardião.

Abre o painel.html numa janela e entrega os dados lidos dos logs de todas as galaxies. Só lê.
Mora em <cosmos>\\app\\ : a raiz é a pasta de cima, e toda pasta galaxy_* dela entra no painel.

Precisa do pywebview (a única coisa fora da biblioteca padrão):
  "<o seu python>" -m pip install pywebview
Abrir:
  "<o seu python>" "<cosmos>\\app\\painel.py"          (no Windows, pythonw.exe abre sem a janela preta)
Testar sem janela (imprime os dados):
  "<o seu python>" "<cosmos>\\app\\painel.py" --json
"""
import base64
import importlib.util
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)   # <cosmos>\app\ -> <cosmos>


def galaxies():
    return [os.path.join(RAIZ, n) for n in sorted(os.listdir(RAIZ))
            if n.startswith("galaxy_") and os.path.isdir(os.path.join(RAIZ, n))]


_leitores = {}
def leitor_de(galaxy):
    """Cada galaxy é lida pelo leitor dela (tools\\leitor.py)."""
    caminho = os.path.join(galaxy, "tools", "leitor.py")
    if caminho not in _leitores:
        spec = importlib.util.spec_from_file_location("leitor_" + os.path.basename(galaxy), caminho)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        _leitores[caminho] = mod
    return _leitores[caminho]


def ler_tudo():
    out = []
    for g in galaxies():
        try:
            out.append(leitor_de(g).dados_json(g))
        except Exception as erro:   # uma galaxy com problema não derruba o painel
            out.append({"galaxy": os.path.basename(g), "erro": str(erro), "projetos": [], "fichas": [], "pendencias": []})
    return {"raiz": RAIZ, "galaxies": out}


def dentro_da_raiz(alvo):
    return os.path.normcase(alvo).startswith(os.path.normcase(RAIZ) + os.sep)


class Api:
    def abrir_pasta(self, pasta):
        """Abre a pasta no gerenciador de arquivos. Só o que está dentro da raiz cosmos."""
        alvo = os.path.abspath(pasta or "")
        if dentro_da_raiz(alvo) and os.path.isdir(alvo):
            if sys.platform.startswith("win"):
                os.startfile(alvo)
            else:
                import subprocess
                subprocess.Popen(["open" if sys.platform == "darwin" else "xdg-open", alvo])
            return True
        return False

    def retrato(self, arquivo):
        """Devolve a imagem do retrato como data URL. Só imagem, só de dentro da raiz cosmos."""
        alvo = os.path.abspath(arquivo or "")
        tipos = {".png": "image/png", ".gif": "image/gif", ".webp": "image/webp", ".jpg": "image/jpeg", ".svg": "image/svg+xml"}
        ext = os.path.splitext(alvo)[1].lower()
        if ext in tipos and dentro_da_raiz(alvo) and os.path.isfile(alvo):
            with open(alvo, "rb") as f:
                return f"data:{tipos[ext]};base64," + base64.b64encode(f.read()).decode()
        return ""

    def dados(self):
        try:
            return ler_tudo()
        except Exception as erro:
            return {"erro": str(erro), "galaxies": []}


if __name__ == "__main__":
    if "--json" in sys.argv:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        print(json.dumps(ler_tudo(), ensure_ascii=False, indent=1))
        sys.exit(0)
    import webview
    webview.create_window("cosmos · painel", os.path.join(AQUI, "painel.html"), js_api=Api(),
                          width=1200, height=820, min_size=(720, 520))
    webview.start()
