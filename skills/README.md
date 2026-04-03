# Dichiarino - Agent Skills

This folder contains [Agent Skills](https://agentskills.io) for the **Dichiarino** 730 tax assistant.
Skills are portable, agent-compatible instruction packages that work with Claude, Cursor, and any
[agentskills.io](https://agentskills.io)-compatible AI tool.

Each skill is self-contained and works **standalone** (embedded fiscal rules) or **enhanced** when
the [Dichiarino MCP server](../README.md) is connected.

---

## Available skills

| Skill | Description |
|-------|-------------|
| [`calcola-irpef-730`](calcola-irpef-730/) | Calculate IRPEF brackets, detrazioni lavoro, and final 730 saldo |
| [`compila-quadro-730`](compila-quadro-730/) | Step-by-step guide to fill in any quadro of the 730 form |
| [`verifica-codice-fiscale`](verifica-codice-fiscale/) | Validate and decode an Italian codice fiscale |
| [`calcola-detrazioni-730`](calcola-detrazioni-730/) | Calculate Quadro E deductions - spese sanitarie, mutuo, istruzione, etc. |
| [`checklist-documenti-730`](checklist-documenti-730/) | Generate a personalised document checklist before filing |
| [`analizza-cu`](analizza-cu/) | Parse and explain a Certificazione Unica (CU) |

---

## Installation

### Claude Code (claude.ai/code)

The easiest way is to add the skills folder as a project context directory so Claude
picks up all `SKILL.md` files automatically:

```bash
# From the repo root - add the skills directory to Claude Code's context
claude --add-dir skills
```

Or, to load a **single skill** for the current session:

```bash
claude --add-dir skills/calcola-irpef-730
```

Alternatively, reference the skill inline inside your project's `CLAUDE.md`:

```markdown
<!-- CLAUDE.md -->
@skills/calcola-irpef-730/SKILL.md
@skills/compila-quadro-730/SKILL.md
```

### Claude Desktop

1. Open **Claude Desktop** → **Settings** → **Developer** → **Edit Config**
   (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS).

2. Add a `userDefinedFiles` entry pointing at the skills you want active:

   ```json
   {
     "userDefinedFiles": [
       "/absolute/path/to/dichiarino-mcp/skills/calcola-irpef-730/SKILL.md",
       "/absolute/path/to/dichiarino-mcp/skills/compila-quadro-730/SKILL.md"
     ]
   }
   ```

3. Restart Claude Desktop. The skills will be injected into every conversation as
   context - Claude will automatically follow the instructions and use the embedded
   fiscal data.

> **Tip:** for the best experience, also connect the [Dichiarino MCP server](../README.md#with-claude-desktop)
> so Claude can call live calculation tools instead of relying solely on embedded rules.

### Cursor

1. Open **Cursor Settings** → **AI** → **Rules for AI** (or add a `.cursorrules` file
   in the repo root).
2. Copy the content of the desired `SKILL.md` file(s) into the rules field, or add an
   `@file` reference:

   ```
   @skills/calcola-irpef-730/SKILL.md
   ```

### Any agentskills.io-compatible agent

Each skill folder contains a valid `SKILL.md` with YAML frontmatter. Point your agent at
any skill directory.

---

## Structure

Each skill follows the [Agent Skills specification](https://agentskills.io/specification):

```
skill-name/
├── SKILL.md          # Metadata + instructions (required)
├── references/       # Detailed reference tables loaded on demand
└── assets/           # Templates and static resources
```

---

## License

Skills are released under the **Apache License 2.0** - see [../LICENSE](../LICENSE).
Any use or redistribution must credit the original repository.
