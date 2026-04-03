<div align="center">

<img src="site/assets/logo-icon.svg" alt="Dichiarino icon" width="100"/><br/>

<img src="site/assets/logo.svg" alt="Dichiarino" width="520"/>


[![CI](https://github.com/gsaccardi/dichiarino-mcp/actions/workflows/ci.yml/badge.svg)](https://github.com/gsaccardi/dichiarino-mcp/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: Apache 2.0](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](LICENSE)
[![MCP](https://img.shields.io/badge/MCP-compatible-brightgreen.svg)](https://modelcontextprotocol.io)

An MCP (Model Context Protocol) server that acts as an intelligent assistant for compiling the Italian **Modello 730 Precompilato** - the pre-filled annual income tax return.

</div>

---

## What is Dichiarino?

Dichiarino is an [MCP server](https://modelcontextprotocol.io) that gives any compatible AI assistant (Claude Desktop, Cursor, etc.) deep knowledge of the Italian tax system and calculation tools for the 730 form. It embeds official fiscal rules, IRPEF rates, and deduction limits so the AI can guide you through your annual tax return.

> **Note:** The Agenzia delle Entrate provides no public API for the 730 precompilato. Dichiarino works as a knowledge + calculation engine - it cannot submit your return for you. Always verify results with a qualified professional (CAF, commercialista, consulente del lavoro).

## Features

| Tool | Description |
|------|-------------|
| `calcola_irpef` | IRPEF lorda from income + year (2024: 23%/35%/43%) |
| `calcola_detrazione_lavoro` | Work income tax credit - formula per bracket + €65 bonus |
| `calcola_detrazioni_familiari_tool` | Detrazioni for spouse, children ≥21, other dependants |
| `calcola_oneri` | Quadro E deductions - medical, mortgage, renovation, university… |
| `verifica_spesa_detraibile` | Is this expense deductible? Which quadro? How much? |
| `valida_codice_fiscale_tool` | Validate + parse Italian codice fiscale (check digit algorithm) |
| `calcola_risultato_dichiarazione` | Full 730 result - **rimborso** or **debito** |
| `guida_quadro` | Step-by-step guide for any Quadro (A–W, M, T) |
| `lista_documenti_spesa` | Documents needed for a specific expense type |
| `genera_checklist_730` | Personalised compilation checklist |
| `calcola_addizionale_regionale_tool` | Regional IRPEF surcharge for all 20 Italian regions |
| `analizza_certificazione_unica` | Validate CU (Certificazione Unica) fields for consistency |

**Resources:**
- `dichiarino://aliquote/{anno}` - IRPEF brackets and rates  
- `dichiarino://quadri/{nome}` - Full instructions for each Quadro  
- `dichiarino://scadenze/{anno}` - Key deadlines  
- `dichiarino://regioni` - Regional surcharge table  
- `dichiarino://detrazioni` - Full deduction limits table  

## Agent Skills

In addition to the MCP server, Dichiarino ships a set of portable **[Agent Skills](https://agentskills.io)**
in the [`skills/`](skills/) folder - standalone instruction packages compatible with Claude, Cursor,
and any agentskills.io-supported tool. They work without the MCP server but are enhanced when it is connected.

| Skill | When to use |
|-------|------------|
| [`calcola-irpef-730`](skills/calcola-irpef-730/) | Compute IRPEF, brackets, detrazioni lavoro, 2025 cuneo fiscale |
| [`compila-quadro-730`](skills/compila-quadro-730/) | Fill in any quadro of the 730 form step by step |
| [`verifica-codice-fiscale`](skills/verifica-codice-fiscale/) | Validate and decode a codice fiscale |
| [`calcola-detrazioni-730`](skills/calcola-detrazioni-730/) | Calculate Quadro E deductions and limits |
| [`checklist-documenti-730`](skills/checklist-documenti-730/) | Generate a personalised document checklist |
| [`analizza-cu`](skills/analizza-cu/) | Parse and explain a Certificazione Unica (CU) |

See [`skills/README.md`](skills/README.md) for installation instructions.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

## Installation

```bash
# Clone the repo
git clone https://github.com/gsaccardi/dichiarino-mcp.git
cd dichiarino-mcp

# Install with uv
uv sync
```

## Usage

### With Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "dichiarino": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/dichiarino-mcp",
        "run",
        "dichiarino"
      ]
    }
  }
}
```

### With Cursor or other MCP clients

Add to `.cursor/mcp.json` (project) or `~/.cursor/mcp.json` (global):

```json
{
  "mcpServers": {
    "dichiarino": {
      "command": "uv",
      "args": ["--directory", "/path/to/dichiarino-mcp", "run", "dichiarino"]
    }
  }
}
```

### Run directly

```bash
uv run dichiarino
# or
uv run python -m dichiarino.main
```

## Example Interactions

Once connected to Claude Desktop:

```
You: Quanto IRPEF devo pagare su un reddito di 35.000€?

Claude: [calls calcola_irpef + calcola_detrazione_lavoro]
        IRPEF lorda: 8.890€
        Detrazione lavoro: 1.565€ + bonus 65€
        IRPEF netta stimata: 7.260€
```

```
You: Ho speso 1.200€ dal medico quest'anno. Cosa posso detrarre?

Claude: [calls calcola_oneri]
        Spese sanitarie: 1.200€ - franchigia 129,11€ = 1.070,89€ x 19% = 203,47€
        Documenti necessari: fatture mediche, scontrini farmacia con CF
```

```
You: Quali quadri devo compilare? Ho lavoro dipendente, mutuo, e figli under 21.

Claude: [calls genera_checklist_730]
        Quadri: Frontespizio, C (lavoro), E (mutuo 19% su max 4.000€)
        ⚠️ I figli under 21 non generano detrazione - coperti dall'Assegno Unico Universale
        Documenti: CU datore, quietanza interessi banca, contratto mutuo
```

## Development

```bash
# Install dev dependencies
uv sync --dev

# Run tests
uv run pytest

# Lint
uv run ruff check src/ tests/

# Type check
uv run mypy src/
```

## Project Structure

```
src/dichiarino/
├── main.py              # Entry point
├── server.py            # MCP server setup + registration
├── types.py             # Domain types
├── calculators/         # Pure calculation functions
│   ├── irpef.py
│   ├── detrazioni_lavoro.py
│   ├── detrazioni_familiari.py
│   ├── oneri.py
│   └── addizionali.py
├── validators/
│   └── codice_fiscale.py
├── data/                # Static fiscal data (2024)
│   ├── aliquote_irpef.py
│   ├── addizionali_regionali.py
│   ├── limiti_detrazioni.py
│   └── istruzioni_quadri.py
├── tools/               # MCP tool handlers
└── resources/           # MCP resource handlers

tests/
├── calculators/         # Unit tests for fiscal math
├── validators/          # Codice fiscale tests
└── integration/         # Full MCP server integration tests
```

## Tax Year Coverage

| Anno di imposta | Modello | Status |
|----------------|---------|--------|
| 2025 | 730/2026 | ✅ Fully supported (default) |
| 2024 | 730/2025 | ✅ Fully supported |
| 2023 | 730/2024 | ✅ IRPEF brackets supported |

## Attribution

This project is licensed under the **Apache License 2.0**.
If you redistribute this software or a Derivative Work, you must include the
[NOTICE](NOTICE) file and retain the following attribution:

> Powered by Dichiarino - https://github.com/gsaccardi/dichiarino-mcp

See [LICENSE](LICENSE) and [NOTICE](NOTICE) for full terms.

## Disclaimer

The fiscal calculations provided are for informational purposes only and do not constitute professional tax or legal advice. Always verify your tax return with a qualified professional before submission. The authors accept no liability for errors or changes in fiscal legislation.

---

<div align="center">
Made with ❤️ for Italian taxpayers
</div>
