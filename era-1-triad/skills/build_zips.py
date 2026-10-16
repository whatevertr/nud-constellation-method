"""Regenera o .zip de cada skill desta pasta. Rode depois de qualquer mudanca numa skill.
Uso: python era-1-triad/skills/build_zips.py   (de qualquer lugar). Barras normais (/) dentro do zip, para abrir em Mac/Linux/Windows.
Licenca: MIT."""
import os, zipfile
HERE = os.path.dirname(os.path.abspath(__file__))
for name in sorted(os.listdir(HERE)):
    src = os.path.join(HERE, name)
    if not os.path.isdir(src) or not os.path.isfile(os.path.join(src, "SKILL.md")):
        continue
    out = os.path.join(HERE, name + ".zip")
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src):
            dirs[:] = [d for d in dirs if not d.startswith(".")]
            for f in sorted(files):
                if f.startswith("."):
                    continue
                full = os.path.join(root, f)
                arc = os.path.relpath(full, HERE).replace(os.sep, "/")
                z.write(full, arc)
    print("ok", os.path.basename(out))
