# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import re

ORCAMENTO = 750_000
FORA = re.compile(
    r"\.(png|jpe?g|gif|ico|svg|webp|bmp|pdf|zip|gz|tar|7z|exe|dll|bin|so|woff2?|ttf|eot|mp3|mp4|wav|pt|pth|safetensors|onnx|pkl|npy|npz|parquet|ipynb|min\.js|min\.css)$"
    r"|(^|/)\.DS_Store$|(^|/)(package-lock\.json|yarn\.lock|poetry\.lock|Pipfile\.lock|uv\.lock|pnpm-lock\.yaml)$",
    re.I,
)
DOC = re.compile(r"\.(md|txt|rst)$|(^|/)LICEN[SC]E[^/]*$|(^|/)NOTICE[^/]*$", re.I)
DEPLOY = re.compile(r"^\.github/|(^|/)(deployments?|deploy|k8s|kubernetes|helm|monitoring)/|(^|/)Dockerfile[^/]*$|(^|/)docker-compose[^/]*$", re.I)
EXEMPLO = re.compile(r"(^|/)(examples?|exemplo[^/]*|samples?|demos?)/", re.I)
TESTE = re.compile(r"(^|/)(tests?|testing|__tests__)/|(^|/)(test_[^/]+|[^/]+_test\.[a-z]+|conftest\.py|pytest\.ini)$", re.I)
CONFIG = re.compile(r"\.(json|ya?ml|toml|ini|cfg|conf|env|example)$|(^|/)\.[^/]+$|(^|/)Makefile$", re.I)
ORDEM = ("doc", "fonte", "config", "deploy", "teste", "exemplo")


def classe(caminho):
    if FORA.search(caminho):
        return "fora"
    if DOC.search(caminho):
        return "doc"
    if TESTE.search(caminho):
        return "teste"
    if EXEMPLO.search(caminho):
        return "exemplo"
    if DEPLOY.search(caminho):
        return "deploy"
    if CONFIG.search(caminho):
        return "config"
    return "fonte"


def selecionar(arquivos):
    sit, total = {}, 0
    por = {c: [] for c in ORDEM}
    for caminho, tam in arquivos:
        c = classe(caminho)
        if c == "fora":
            sit[caminho] = "fora_da_regra"
        else:
            por[c].append((caminho, tam))
    for c in ORDEM:
        for caminho, tam in sorted(por[c], key=lambda x: (x[1], x[0])):
            if total + tam <= ORCAMENTO:
                sit[caminho] = "incluido"
                total += tam
            else:
                sit[caminho] = "omitido_orcamento"
    return sit, total
