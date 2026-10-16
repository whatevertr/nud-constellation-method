# INSTALL.md: Era 4 of the Constellation Method
*Written for the AI that will install the method for a person. If you are the person, you can read it too: there is no secret here. Built for Claude Code (desktop app or terminal). Tested from scratch on Windows on 2026-10-16. The template's file contents are in Brazilian Portuguese; the Portuguese version of this guide is `INSTALAR.md`.*

## Before installing: talk first
Read the repository's thesis and talk with the person: how they work, what they do with AI, where they get stuck. Say honestly whether it is worth it.

**The method asks for attention, not maintenance.** In Era 4, the agent does the recording (through the registrar) and the hooks deliver the context. What stays with the person is checking what the AI delivers and closing the day with a summary. For someone who works with AI every day and wants more quality and continuity, this is the lightest era. For one-off use, or for someone who won't check anything, it still weighs more than it helps. If you try it, start small.

## What comes in this package
```
cosmos\                         the root: rules that apply to every agent
└─ galaxy_exemplo\              one universe of work, with a single Tars
   ├─ station\module_thinker\   the thinker's home: CLAUDE.md (its profile card and way of working),
   │                            diary\ (the diary), galley\ (the search into the past),
   │                            .claude\settings.json (the hooks)
   ├─ missions\                 the work; one example mission, with lab\storage|output|tasks
   ├─ matrix\                   the skills (context skills and craft skills)
   ├─ tools\                    registrar, reader, the 3 hooks, slicer and searcher (the galley)
   ├─ _to_delete\               the trash (only the person empties it)
   └─ _archived\                what is finished, kept
```
**The two memories:**
- **work memory** is the **log** (`log.jsonl`, written only by `registrar.py`): what was done, what was decided, and what is left;
- **companionship memory** is the **diary** (`diary\`): a first-person record of what it was like to work together that day.

**The hooks that deliver both, on their own:**
- **arrival** (`hook_chegada.py`): when the session opens, it delivers the last summary, the tasks and the missions;
- **soul** (`hook_alma.py`): it delivers the last diary entry. "Soul" is the method's name for this: what the agent receives on waking about who it is and how you two work together. It is text, written and read; it is not a promise of consciousness;
- **mission** (`hook_mission.py`): when the agent touches a mission, it delivers that mission's summary.

**The galley:** the search into the past (old diaries and records). It works **with nothing installed** (keyword search). With [Ollama](https://ollama.com) and the `qwen3-embedding:0.6b` model, it also searches by meaning, and results improve. If Ollama doesn't answer, it falls back to keyword search on its own.

## Step by step
1. **Where it lives.** The recommended place is `C:\Users\<person's name>\cosmos` (on Mac or Linux, `~/cosmos`): inside the person's own folder, outside synced folders (OneDrive and the like sync in the middle of the work and confuse the agents), with no spaces or accents in the path. Copy the `modelo\cosmos\` folder there.
2. **Python.** The tools use only the standard library of Python 3.10 or newer. Find the full path of the machine's executable (on Windows, `where python` or `py -0p`; watch out for the Microsoft Store shortcut, which opens the store instead of Python). Always use the full path.
3. **The placeholders.** Replace in every `.md` and `.json`:
   - `{PYTHON}` → the Python path (in `settings.json`, with forward slashes `/`);
   - `{COSMOS}` → the path of the `cosmos` folder (in `settings.json`, with forward slashes `/`);
   - `{AAAA-MM-DD}` → today's date (year-month-day);
   - `{nome da pessoa}` (the person's name), `{como ela prefere trabalhar}` (how they prefer to work) and the other `{…}` → with the person, in conversation.
4. **The names.** If the person wants, rename `galaxy_exemplo` and `module_thinker` (and update the paths in `settings.json` and in the home's `CLAUDE.md`). The `thinker:` field in the header is the name the log uses: choose it now, because it doesn't change later.
5. **The profile card.** Fill in the header of `module_thinker\CLAUDE.md` with the person. The example diary can be deleted (or replaced) on the first day: the thinker writes the first real diary entry when closing the day.
6. **The first record.** Run, from the home folder:
   ```
   "{PYTHON}" "{COSMOS}\galaxy_exemplo\tools\registrar.py" "{COSMOS}\galaxy_exemplo\station\module_thinker" --por thinker --tipo nota --tag organizacao --txt "First line: installation done."
   ```
   It must answer `REGISTRADO`.

## How to know it worked
1. Open a new Claude Code session **with the home folder** (`module_thinker`) as the working folder.
2. In its first reply, the thinker must mention the **`=== CHEGADA (hook, Era 4) ===`** block (arrival) and the **`=== ALMA ===`** block (soul). If they came, continued memory is on.
3. Ask it to record a task in `minha-primeira-mission` and then to search the galley. If both work, it is installed.

**If the arrival block didn't come:** check the Python path in `settings.json` (full path, forward slashes `/`), and whether the session was opened in the home folder (the hooks live in its `.claude\settings.json`).

**On Codex (or another agent):** every folder has an `AGENTS.md` that points to the `CLAUDE.md` next to it, so the rules arrive. The hooks (arrival, soul, mission) were tested only on Claude Code; on another agent, ask it to run, on opening, `"{PYTHON}" "{COSMOS}\galaxy_exemplo\tools\leitor.py" chegada "{COSMOS}\galaxy_exemplo\station\module_thinker"`.

## What this package doesn't bring
- **The agent profile** (`.claude\agents\<name>.md`, the soul that goes along into every session), **on purpose**: the profile is born from the Triad, written with the person, from how they work. A ready-made profile would belong to someone else.
- **The guard** (a hook that keeps each agent out of areas that aren't its own): every person has their own areas; a generic version comes later.
- **The dashboard app** (the view of missions, tasks and indicators): in a later delivery.

## One last thing
If, after talking, you think the method doesn't serve this person, say so. That is the method working too.
