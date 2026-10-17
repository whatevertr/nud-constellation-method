"""Regenera o .zip de cada skill desta pasta e da instaladora na raiz do repositorio. Rode depois de qualquer mudanca numa skill.
Uso: python era-1-triad/skills/build_zips.py   (de qualquer lugar). Barras normais (/) dentro do zip, para abrir em Mac/Linux/Windows.
Cada zip fica ao lado da pasta da skill.
Licenca: MIT."""
import os, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(os.path.dirname(HERE))   # a raiz do repositorio (onde mora a nud-install-constellation-method)

def skills_em(pasta):
    for name in sorted(os.listdir(pasta)):
        src = os.path.join(pasta, name)
        if os.path.isdir(src) and os.path.isfile(os.path.join(src, "SKILL.md")):
            yield pasta, name, src

for pasta, name, src in list(skills_em(HERE)) + list(skills_em(RAIZ)):
    out = os.path.join(pasta, name + ".zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in sorted(files):
                if f.startswith("."):
                    continue
                full = os.path.join(root, f)
                arc = os.path.relpath(full, pasta).replace(os.sep, "/")
                z.write(full, arc)
    print("ok", os.path.relpath(out, RAIZ).replace(os.sep, "/"))
