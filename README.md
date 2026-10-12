<p align="right"><a href="README.pt-BR.md">🇧🇷 Português</a></p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/banner-night.svg">
  <img alt="Constellation Method: one human, three agents, context that steers everything" src="assets/banner-day.svg">
</picture>

# Constellation Method

Method for managing several areas and projects from a minimum context that steers everything, with agents in three angles of function.

---

## What it is

It is a way to organize context so AI can help me manage my life. I started simple: markdown files inside projects in the provider's interface, which the instance read at the start of each job. I documented it here as it scaled. Today I have a system I designed to be model-agnostic — I've run it on the platforms I've tested (Claude Code, Hermes, Codex) — and I manage my whole life from three agent functions: thinker, manager and worker. This is how I use it and it works for me; if you try it somewhere else, I'd genuinely like to hear how it went. It's transforming my life. It gives me more autonomy and capacity to create, and it made me a healthier person.

I still have a lot to improve and learn, so improvements will always arrive in this repository. Here I explain how to install and start using my agents and my method of context flow for whatever you want: managing a life, a project, or an annoying task from your job.

## Minimum context

Everything starts from minimum context, split into three documents. Each one organizes a type of information the instance needs to work in a managerial way. If you want to use it in just a one-off project, use a project in your provider's app (Claude Cowork, for example): the three documents go into the project configuration, and that's it. It is simple and functional. **To scale, with management and continued memory**, these same three documents are the minimum the platform needs to configure an agent: the manual becomes the rules of conduct, the door becomes the project's memory, and the function becomes the agent's profile. Guardrails (what it cannot run, where it cannot write) and hooks (what is blocked before it happens) sit on top of this, as platform configuration, not as text. Where each piece lives on each platform is in [`ONDE_CONFIGURAR.md`](ONDE_CONFIGURAR.md).

Three documents, three layers:

- **the door** (`start_here`): where the instance enters. The topic, the goal, why it matters now = context of the goal;
- **the manual** (`how_to_work_with_me`): how your head works. Your criteria for collaboration = context of human/AI communication;
- **the function** (`agents/`), **thinker**/**manager**/**worker**, or analysis/audit/execution = context of what is indispensable for meeting the goal.

## Agents

In a small job, inside an app project, the task is one-off: it is either analysis, or checking, or execution. You choose one agent and use only that one. To manage, the three work in layers within the same project, and what reaches you is just the result, ready for the decision. What makes me confident enough to let the agents manage is the floor each one carries: I work with a lot of data analysis and research, I need layers of checking, and they work exactly like this:

- **Operationalized execution** (worker): takes the task with clean context, to reduce the bias of whoever designed the process — that's how I set it up.
- **Audit check** (manager): checks what came back against what was agreed.
- **Analytical check** (thinker): stresses the hypothesis before it becomes a decision, and plans the next one.

The floor and the guardrails the three carry are explained in [`METODO.md`](METODO.md).

## How to use

1. **Download the skills.** They are in the [`skills/`](skills/) folder: each one as an open folder and as a `.zip` ready to upload to your app. The folder's `README` explains the installation.
2. **`nud-como-trabalhar-comigo`**: install it or paste it into the chat. The instance will ask questions; answer honestly. This document is what establishes the common ground for communication between you and your agents.
3. **`nud-comece-aqui`**: helps you explain your goal. It works for a project folder, a one-off task, or a specific goal (a wedding party, for example). It ensures the minimum context of a goal.
4. **`nud-agentes`**: the context of the method. It installs in the instance the capacity to help you set up your way of working, whether in an app project or at scale, and it brings the profiles of the three agents inside it. It will ask for the two documents generated above to understand what kind of configuration you need.

**Example in Claude Cowork (September 2026):** the manual goes in *Settings → General → Instructions for Claude* (applies to all conversations) or in the project's *Instructions*; the door goes in the project's *Instructions*, and the goal can also go into the project's memory (the `claude` folder, which the instance creates when you ask and which only shows up in the interface once there is something inside it); the agent's profile goes in *Settings → Cowork* (the instructions that apply to all Cowork sessions) or in the project's *Instructions*. Field names change over time; the logic stays the same: manual = how you work, door = what the project is, function = the instance's role.

## Where to use

The minimum context fits in a single folder, inside your app's project. Context at scale needs a folder structure on your computer. Once set up, it does not move or get deleted, it only grows: the configurations and guardrails point to these paths. That is what keeps the instance always calibrated in context and able to manage the topics.

```
Documents/
└── vault_[name]/
    ├── _to_delete/                 ← pre-trash: nothing is deleted for good
    ├── projects/
    │   └── project_[name]/
    │       └── start_here.md       ← the project's door
    ├── neighborhood/               ← one home per agent
    │   ├── home_thinker/
    │   │   └── memory/             ← states
    │   ├── home_manager/
    │   └── home_worker/
    └── work_tables/
        └── work_table_[project]/   ← handoff between agents
            ├── _task/
            ├── _output/
            └── _states/
```

What each piece does: the **home** (`home_[agent]`) is where each agent is bound, and in some services the folder ties to the agent's identifier; the **work_table** is where one agent delivers and another picks up; the **memory** keeps the states of where the work stopped; the **pre-trash** avoids deletion and allows recovery; and `start_here.md` sits in the project folder.


<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/context-flow-night.svg">
  <img alt="Context flow: from the providers to the cycle of the three agents, and back to you" src="assets/context-flow-day.svg">
</picture>

## Dig deeper

- [`METODO.md`](METODO.md): the epistemic floor, the guardrails, the two rules of honesty, what rung the method is on and what it leans on.
- [`ONDE_CONFIGURAR.md`](ONDE_CONFIGURAR.md): where each layer lives on each platform (Claude Code, Hermes, Codex).
- [`MANIFESTO.md`](MANIFESTO.md): where this came from.
- [`cronologia/`](cronologia/): the trail of the method, by eras.
- [`DEVLOG.md`](DEVLOG.md): what changed, when, and what the check knocked down.

## License

- **Method, templates and texts:** [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)
- **Any code or script:** MIT.
