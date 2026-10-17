# station: as casas dos agentes
- **Um `module_[nome]\` por agente.** Casa nova nasce do molde `tools\moldes\esqueleto_modulo.md`: muda só o cabeçalho e a seção "Só seu".
- **O cabeçalho do `CLAUDE.md` do módulo é a ficha do agente.** O `thinker:` é o nome que o log usa (`--por`): não muda depois que o módulo nasce, senão o histórico se perde.
- **Os hooks** (chegada, alma, mission) moram em `tools\` e se ligam no `.claude\settings.json` de cada casa. Eles rodam quando a sessão começa, volta ou é compactada.
- **A guarda** (`tools\guarda.py`) roda antes de toda ferramenta: cada agente fica fora das casas de quem está acima dele, e agente que ela não conhece fica fora de todas. **Agente novo, antes de ligar:** (1) o nome e a casa dele no `tools\guarda.json`, na posição da hierarquia; (2) os casos dele no `tools\teste_guarda.py`; (3) rodar o teste, que tem que dar tudo OK.
