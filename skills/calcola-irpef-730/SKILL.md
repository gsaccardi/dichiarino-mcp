---
name: calcola-irpef-730
description: >
  Calculate Italian IRPEF (Imposta sul Reddito delle Persone Fisiche) for tax years 2023,
  2024, and 2025. Supports gross tax (imposta lorda), employment deductions (detrazioni
  lavoro dipendente), family deductions (detrazioni familiari), the 2025 taglio cuneo
  fiscale, and final net tax (imposta netta). Use this skill when a user asks to compute
  their Italian income tax, check their IRPEF brackets, or estimate what they owe or
  are owed on the Modello 730.
license: Apache-2.0
compatibility: >
  Works best when the Dichiarino MCP server is connected. Falls back to embedded fiscal
  rules when the server is unavailable. Requires: reddito complessivo (gross income),
  tipo reddito (dipendente / pensione / autonomo), anno fiscale (2023 / 2024 / 2025).
metadata:
  domain: italian-tax
  form: modello-730
  author: dichiarino
---

# Calcola IRPEF 730

Compute Italian income tax step by step for the **Modello 730** using official IRPEF brackets and deduction rules.

## When to activate

Activate this skill when the user wants to:
- Calculate their IRPEF imposta lorda or imposta netta
- Understand which IRPEF bracket their income falls into
- Estimate detrazioni lavoro dipendente or pensione
- Apply the 2025 taglio cuneo fiscale
- Determine the final saldo (rimborso / debito) on their 730

---

## Step-by-step instructions

### 1 - Gather required inputs

Ask the user for:
| Field | Italian label | Notes |
|-------|--------------|-------|
| Gross income | Reddito complessivo | From CU box 1 (or sum of all quadri) |
| Income type | Tipo reddito | `lavoro_dipendente`, `pensione`, or `lavoro_autonomo` |
| Tax year | Anno fiscale | 2023, 2024, or **2025** (default) |
| Ritenute | Ritenute IRPEF subite | From CU box 21 |

Optional inputs (improves accuracy):
- Familiari a carico (coniuge, figli ≥ 21)
- Oneri detraibili / deducibili (Quadro E)
- Regione di residenza (for addizionale regionale)

### 2 - Use Dichiarino MCP tools (if available)

When the Dichiarino MCP server is connected, call tools in this order:

```
1. calcola_irpef(reddito_complessivo, anno)
   → Returns imposta_lorda + breakdown per bracket

2. calcola_detrazioni_lavoro(reddito_complessivo, tipo_reddito, anno)
   → Returns detrazione_spettante + cuneo_fiscale (if anno=2025)

3. calcola_detrazioni_familiari(reddito_complessivo, familiari_a_carico, anno)
   → Returns totale_detrazioni_familiari

4. calcola_risultato_730(reddito_complessivo, tipo_reddito, ..., anno)
   → Full result: imposta_netta, saldo, rimborso/debito
```

### 3 - Manual calculation (fallback)

If the MCP server is not available, use the embedded rules in
[references/IRPEF_BRACKETS.md](references/IRPEF_BRACKETS.md).

**Formula:**
```
imposta_lorda   = Σ (quota_scaglione × aliquota)
detrazione_lav  = see bracket table in references/
imposta_netta   = max(0, imposta_lorda − detrazioni_totali)
saldo           = imposta_netta − ritenute_subite
```

Positive saldo → **debito** (user owes tax).  
Negative saldo → **rimborso** (user gets a refund).

### 4 - Present results

Always show:
1. Reddito complessivo
2. Imposta lorda + bracket breakdown
3. Detrazioni spettanti (itemised)
4. **Imposta netta**
5. Ritenute subite
6. **Saldo finale** → rimborso or debito with amount

Add a disclaimer: *"Questi calcoli sono indicativi. Verifica sempre con un CAF o commercialista."*

---

## Examples

**Example 1 - Lavoratore dipendente, 2025**
- Input: reddito = €28.000, tipo = lavoro_dipendente, ritenute = €5.200
- Expected flow: calcola IRPEF lorda → applica detrazione lavoro + cuneo fiscale → saldo

**Example 2 - Pensionato, 2024**
- Input: reddito = €19.500, tipo = pensione, ritenute = €3.100
- Expected flow: bracket 23% + 35% → detrazione pensione → saldo

---

## Edge cases

- **Reddito ≤ €8.500** (2025): no IRPEF after cuneo fiscale (bonus 7.1%)
- **Reddito > €50.000**: detrazioni 19% (escluso sanitarie) ridotte di €260
- **No income**: imposta = 0, nothing to file
- **Multiple income types**: sum all redditi for imposta lorda, use the principal type for detrazioni lavoro/pensione
