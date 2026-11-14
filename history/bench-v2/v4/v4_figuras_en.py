# Versao publicada (14/11/2026): comentarios e docstrings omitidos e, quando havia, caminhos locais e codigos internos de agentes trocados, para limpeza e privacidade; o original esta carimbado no OpenTimestamps.
import re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
AQUI = Path(__file__).resolve().parent
SRC, OUT = AQUI.parent / "relatorio_final" / "figuras", AQUI.parent / "relatorio_final" / "figuras_en"
OUT.mkdir(parents=True, exist_ok=True)
T = [
    ('Diferença contra a condição "cru", comparada dentro de cada repositório (IC 95%)', 'Difference from the "bare" condition, compared within each repository (95% CI)'),
    ("Diferença contra a condição &quot;cru&quot;, comparada dentro de cada repositório (IC 95%)", "Difference from the &quot;bare&quot; condition, compared within each repository (95% CI)"),
    ("traço = intervalo de 95%; se cruza o zero, a diferença cabe no ruído", "bar = 95% interval; if it crosses zero, the difference is within noise"),
    ("Diferenças contra o cru", "Differences from bare"),
    ("Afirmações contraditas e anuladas, em % das afirmações conferíveis", "Contradicted and unverifiable claims, as % of checkable claims"),
    ("contagem / conferíveis", "counts / checkable"),
    ("O que os laudos afirmam, por capacidade e condição", "What the reviews claim, by capability and condition"),
    ("Cada tipo de afirmação contra o gabarito (todas as condições)", "Each claim type against the reference verdicts (all conditions)"),
    ("Marcas de não-verificação (🍷) por laudo, por modelo e condição", "Non-verification marks (🍷) per review, by model and condition"),
    ("Taças por laudo", "Marks per review"),
    ("🍷/laudo · % com ressalva", "🍷/review · % hedged"),
    ("O desenho do estudo", "Study design"), ("Desenho do estudo", "Study design"),
    ("3 repositórios", "3 repositories"), ("congelados em um commit", "frozen at one commit"),
    ("3 dossiês de texto", "3 text dossiers"), ("iguais para todos", "identical for all models"),
    ("6 modelos × 3 condições × 5", "6 models × 3 conditions × 5"), ("270 avaliações, sem ferramentas", "270 reviews, no tools"),
    ("extração às cegas", "blind extraction"), ("11.832 afirmações", "11,832 claims"),
    ("gabarito (veredito)", "reference verdicts"), ("2 conferidores + amostra com clone + juiz", "2 verifiers + clone sample + judge"),
    ("rótulo de cada afirmação", "label of each claim"), ("juiz cego: modelo, condição, repo", "blind judge: model, condition, repo"),
    ("ressalva (🍷)", "hedge (🍷)"), ("lida no texto do laudo", "read from the review text"),
    ("análise: cada condição comparada com o &quot;cru&quot; dentro do mesmo repositório", "analysis: each condition compared with &quot;bare&quot; within the same repository"),
    ("2 métricas primárias do protocolo + análise exploratória (postura, volume, ressalva)", "2 primary metrics from the protocol + exploratory analysis (stance, volume, hedging)"),
    ("graves reais (p.p.)", "serious real findings (pp)"), ("falsas (p.p.)", "false claims (pp)"),
    ("afirmações por laudo", "claims per review"), ("pontos por laudo", "points per review"),
    ("anulada com ressalva", "unverifiable, hedged"), ("anulada seca", "unverifiable, unhedged"), ("anulada", "unverifiable"),
    ("inferência declarada", "declared inference"), ("constatação", "neutral statement"), ("verdadeira", "true"), ("parcial", "partial"),
    ("contradita", "contradicted"), ("crítico", "critical"), ("prioridade", "priority"), ("ajuste", "fix"), ("melhoria", "improvement"), ("elogio", "praise"),
    ("MAIORES", "LARGER"), ("COMPACTOS", "COMPACT"), ("maiores", "larger"), ("compactos", "compact"),
    ("conferíveis", "checkable"), ("afirmações", "claims"),
    ("só piso", "floor only"), ("tríade", "triad"), ("cru", "bare"),
]
LEG = re.compile(r'<rect x="[\d.]+" y="32" width="12" height="12" rx="2" fill="(#[0-9a-f]+)"/><text x="[\d.]+" y="42" class="r">([^<]+)</text>')
for f in sorted(SRC.glob("*.svg")):
    s = f.read_text(encoding="utf-8")
    for pt, en in T:
        s = s.replace(pt, en)
    itens = list(LEG.finditer(s))
    if itens and f.name != "fig5_tacas.svg":
        x, novo, fim = 12, [], 0
        for m in itens:
            novo.append(s[fim:m.start()] + f'<rect x="{x}" y="32" width="12" height="12" rx="2" fill="{m.group(1)}"/><text x="{x + 17}" y="42" class="r">{m.group(2)}</text>')
            x += round(32 + 7.4 * len(m.group(2)))
            fim = m.end()
        s = "".join(novo) + s[fim:]
    (OUT / f.name).write_text(s, encoding="utf-8")
print("ok:", sorted(p.name for p in OUT.glob("*.svg")))
