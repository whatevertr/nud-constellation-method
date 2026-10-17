"""
guarda.py · o hook de antes da ferramenta (PreToolUse) da Era 4: cada agente fica fora das casas de quem está acima dele.
v1.0.0 · 17/10/2026 · tars (Claude), o thinker do NUD · guardião.

As regras (lidas do guarda.json, aqui do lado):
  - a sessão principal (sem agente) e o agente do topo (o thinker) passam livres;
  - cada agente da lista fica fora das casas dos agentes ACIMA dele (o manager fora da casa do thinker;
    o worker fora das casas do thinker e do manager);
  - um agente que NÃO está na lista (um subagente qualquer, um que vai existir) fica fora de TODAS as casas;
  - git que muda coisa (commit, push, branch...) só pro agente do topo;
  - apagar de verdade, pra nenhum agente: o que sai vai pro _to_delete;
  - apagar recursivo numa junção ou link é barrado sempre (atravessa o link e apaga a fonte).

O que ela é: um quebra-molas, não uma parede. Ela lê o que está escrito no pedido da ferramenta: segura o acidente
e o acesso ingênuo. Se ela quebrar, deixa passar (fail-open); um programa que o agente roda pode ler o que quiser;
e nada disso evita prompt injection. A parede de verdade é rodar o agente num sandbox ou container.

Agente novo: ponha o nome no guarda.json E os casos dele no teste_guarda.py, rode o teste (tem que dar tudo OK)
e só então ligue o agente.
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
GALAXY = os.path.dirname(AQUI)

GIT_MUTADOR = re.compile(r"\bgit\s+(commit|push|branch|checkout|switch|merge|rebase|reset|tag|add|init|restore|revert|cherry-pick|stash|clean|rm|mv)\b", re.I)
APAGAR = re.compile(r"(^|[\s;&|(])(rm|rmdir|del|erase|rd|remove-item|unlink|shred)(\s|$)", re.I)
RECURSIVO = re.compile(r"(remove-item\b[^;&|]*-r(ecurse)?\b|\brm\s+(-[a-z]*r[a-z]*\b)|\b(rmdir|rd)\b[^;&|]*\s/s\b)", re.I)


def negar(motivo):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": "deny", "permissionDecisionReason": motivo}}, ensure_ascii=False))
    sys.exit(0)


def norm(s):
    return str(s).replace("\\", "/").lower()


def config():
    """A ordem do guarda.json é a hierarquia: o primeiro é o topo. Se o arquivo faltar ou quebrar,
    vale o mais seguro: só a sessão principal passa livre, e todo agente fica fora de todas as casas."""
    try:
        with open(os.path.join(AQUI, "guarda.json"), encoding="utf-8") as f:
            agentes = json.load(f)["agentes"]
        return [(a["nome"].lower(), a["casa"]) for a in agentes]
    except (OSError, ValueError, KeyError, TypeError, AttributeError):
        return []


def e_link(p):
    try:
        return bool(getattr(os.lstat(p), "st_file_attributes", 0) & 0x400) or os.path.islink(p)
    except OSError:
        return False


def link_dentro(p, limite=3000):
    n = 0
    for raiz, dirs, _ in os.walk(p):
        for d in dirs:
            n += 1
            if e_link(os.path.join(raiz, d)):
                return os.path.join(raiz, d)
            if n > limite:
                return None
    return None


def main():
    try:
        pedido = json.load(sys.stdin)
    except ValueError:
        sys.exit(0)
    agente = (pedido.get("agent_type") or "").lower()
    ti = pedido.get("tool_input") or {}
    cmd = str(ti.get("command", ""))
    alvo = " ".join(norm(ti.get(k, "")) for k in ("file_path", "path", "pattern", "command", "notebook_path"))
    cwd = norm(pedido.get("cwd", ""))

    # 1. apagar recursivo numa junção/link: barrado pra todo mundo, inclusive a sessão principal
    if RECURSIVO.search(cmd):
        for parte in re.findall(r"\"[^\"]+\"|'[^']+'|\S+", cmd):
            c = parte.strip("'\"")
            if len(c) > 2 and os.path.exists(c):
                if e_link(c):
                    negar(f"Apagar recursivo numa junção/link atravessa o link e apaga a fonte. Pra tirar só a junção, remova o link, não o conteúdo ('{c}').")
                if os.path.isdir(c) and link_dentro(c):
                    negar(f"Tem junção/link dentro de '{c}': o apagar recursivo atravessaria e apagaria a fonte.")

    if not agente:
        sys.exit(0)   # a sessão principal: as permissões do settings.json cobrem o resto

    # 2. apagar de verdade: nenhum agente
    if APAGAR.search(cmd):
        negar("Apagar de verdade, não: mova pro _to_delete/ da galaxy. Só a pessoa esvazia.")

    agentes = config()
    nomes = [n for n, _ in agentes]
    if agentes and agente == nomes[0]:
        sys.exit(0)   # o topo (o thinker) passa livre

    # 3. as casas que ficam fora: as de quem está acima; agente fora da lista (ou sem config) fica fora de todas
    if agente in nomes:
        fora = [casa for _, casa in agentes[:nomes.index(agente)]]
    else:
        fora = [casa for _, casa in agentes] or ["module_"]
    for casa in fora:
        pedaco = norm(casa).strip("/")
        caminho_casa = norm(os.path.join(GALAXY, "station", casa))
        if pedaco and pedaco in alvo:
            negar(f"Este agente não entra na casa '{casa}' (a guarda segue a hierarquia: cada agente fica fora das casas de quem está acima).")
        # busca a partir de uma pasta-mãe da casa (grep/glob na galaxy inteira) também entraria na casa
        if pedido.get("tool_name") in ("Grep", "Glob"):
            raiz = norm(ti.get("path") or cwd)
            if raiz and caminho_casa.startswith(raiz.rstrip("/") + "/"):
                negar(f"Busca a partir de '{raiz}' entraria na casa '{casa}'. Busque a partir de uma pasta que não contenha a casa.")

    # 4. git que muda coisa: só o topo
    if GIT_MUTADOR.search(cmd):
        negar("git que muda coisa (commit, push, branch...) é só do agente do topo, com o sim da pessoa. git status/diff/log continuam livres.")
    sys.exit(0)


if __name__ == "__main__":
    main()
