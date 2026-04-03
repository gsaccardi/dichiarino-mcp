# INSTRUCTIONS - How to connect Dichiarino to your AI client

## What is this?

**Dichiarino** is an [MCP (Model Context Protocol)](https://modelcontextprotocol.io) server.
Once connected, any compatible AI client (Claude Desktop, Cursor, Windsurf, VS Code with Copilot, etc.)
gains fiscal intelligence tools for the Italian **Modello 730 Precompilato**.

---

## Prerequisites

1. **Python 3.11+** installed
2. **[uv](https://docs.astral.sh/uv/getting-started/installation/)** installed:
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. This repository cloned to your machine:
   ```bash
   git clone https://github.com/gsaccardi/dichiarino-mcp.git
   cd dichiarino-mcp
   uv sync
   ```

---

## Claude Desktop

### Step 1 - Find the config file

| OS | Path |
|----|------|
| macOS | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Windows | `%APPDATA%\Claude\claude_desktop_config.json` |
| Linux | `~/.config/Claude/claude_desktop_config.json` |

### Step 2 - Add Dichiarino

Open the config file (create it if it doesn't exist) and add:

```json
{
  "mcpServers": {
    "dichiarino": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/dichiarino-mcp",
        "run",
        "dichiarino"
      ]
    }
  }
}
```

> Replace `/ABSOLUTE/PATH/TO/dichiarino-mcp` with your actual path, e.g.
> `/Users/mario/Repos/dichiarino-mcp` on macOS or `C:\Users\mario\Repos\dichiarino-mcp` on Windows.

### Step 3 - Restart Claude Desktop

Quit and reopen Claude Desktop. You should see the 🔌 tools icon in the chat input bar.
Click it to verify **dichiarino** is listed.

---

## Cursor

Open `.cursor/mcp.json` in your project (or `~/.cursor/mcp.json` globally) and add:

```json
{
  "mcpServers": {
    "dichiarino": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/dichiarino-mcp",
        "run",
        "dichiarino"
      ]
    }
  }
}
```

Then open **Cursor Settings → MCP** and verify Dichiarino appears as active.

---

## Windsurf (Codeium)

Open Windsurf settings and navigate to **MCP Servers**. Add a new server:

- **Name:** `dichiarino`
- **Command:** `uv`
- **Args:** `--directory /ABSOLUTE/PATH/TO/dichiarino-mcp run dichiarino`

---

## VS Code + GitHub Copilot (agent mode)

Add to your `.vscode/mcp.json` (or user-level settings):

```json
{
  "servers": {
    "dichiarino": {
      "type": "stdio",
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/dichiarino-mcp",
        "run",
        "dichiarino"
      ]
    }
  }
}
```

Enable MCP in Copilot Chat via the `#tools` selector or agent mode.

---

## Zed Editor

Add to your Zed config (`~/.config/zed/settings.json`):

```json
{
  "context_servers": {
    "dichiarino": {
      "command": {
        "path": "uv",
        "args": [
          "--directory",
          "/ABSOLUTE/PATH/TO/dichiarino-mcp",
          "run",
          "dichiarino"
        ]
      }
    }
  }
}
```

---

## Using uvx (no clone required, once published on PyPI)

If Dichiarino is published to PyPI, you can use it without cloning:

```json
{
  "mcpServers": {
    "dichiarino": {
      "command": "uvx",
      "args": ["dichiarino-mcp"]
    }
  }
}
```

---

## Verifying it works

Once connected, try asking your AI assistant:

```
Calcola l'IRPEF per un reddito di 35.000€ nel 2024.
```

```
Ho speso 800€ dal medico. Quanto posso detrarre nel 730?
```

```
Quali quadri del 730 devo compilare se ho lavoro dipendente e un mutuo?
```

You should see the AI calling Dichiarino tools and returning structured fiscal calculations.

---

## Troubleshooting

**"Server not found" / tools not appearing**
- Make sure the path in `--directory` is absolute and correct
- Run `uv run dichiarino` manually in the repo directory to verify it starts without errors

**"uv command not found"**
- Ensure uv is installed: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Restart your terminal / AI client after installation

**Calculations seem off**
- Dichiarino covers tax year **2024** (Modello 730/2025). Verify you're asking about the correct year.
- Open a GitHub issue: https://github.com/gsaccardi/dichiarino-mcp/issues

---

## Attribution

Per the **Apache License 2.0**:  
If you redistribute Dichiarino or a Derivative Work, you must include the NOTICE file with attribution to the original repository.  
See [LICENSE](LICENSE) and [NOTICE](NOTICE) for full terms.
