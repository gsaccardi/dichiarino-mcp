---
name: calcola-detrazioni-730
description: >
  Calculate Italian tax deductions (detrazioni e deduzioni) for the Modello 730,
  specifically Quadro E (oneri detraibili and oneri deducibili). Covers spese sanitarie,
  interessi sul mutuo, spese istruzione, premi assicurativi, donazioni, spese funebri,
  spese veterinarie, and more. Applies the correct percentage (19% or other), spending
  limits (massimali), franchise thresholds (franchigie), and the >€50.000 income cap.
  Use this skill when a user wants to know if a specific expense is deductible, how much
  they can deduct, or needs help filling in Quadro E of their 730.
license: Apache-2.0
compatibility: >
  Works best with the Dichiarino MCP server (tools: calcola_oneri_detraibili,
  verifica_spesa_detraibile). Embedded rules cover all 2024/2025 limits.
metadata:
  domain: italian-tax
  form: modello-730
  author: dichiarino
---

# Calcola Detrazioni 730

Calculate tax deductions for **Quadro E** of the Modello 730 Precompilato.

## When to activate

Activate when the user asks:
- "Posso detrarre la spesa dal dentista?"
- "Quanto posso detrarre di interessi sul mutuo?"
- "Ho pagato €1.500 di spese mediche, quanto mi ritorna?"
- "Come funziona la detrazione per i figli a scuola?"

---

## Deduction mechanics

There are two types of fiscal benefits in Quadro E:

| Type | Italian | Mechanism |
|------|---------|-----------|
| **Detrazioni** | Oneri detraibili | Reduce **imposta lorda** by a % of the expense |
| **Deduzioni** | Oneri deducibili | Reduce **reddito complessivo** (before IRPEF) |

Most expenses are **detrazioni al 19%**. A few are deducibili (e.g., contributi previdenziali).

---

## Step-by-step instructions

### 1 - Identify the expense type

Ask the user what they spent money on. Map it to a `TipoSpesa`:

| Spesa | TipoSpesa | Note |
|-------|----------|------|
| Medico, farmacia, analisi | `spese_sanitarie` | Franchigia €129,11 |
| Dentista | `spese_sanitarie` | Same as above |
| Occhiali / lenti (con ricetta) | `spese_sanitarie` | Max €464 for devices |
| Interessi mutuo prima casa | `interessi_mutuo_prima_casa` | Max €4.000 |
| Interessi altri mutui | `interessi_mutuo_altri` | Max €2.066 |
| Asilo nido | `asilo_nido` | Max €632/child |
| Istruzione scolastica | `istruzione` | Max €800 |
| Università | `istruzione_universitaria` | No cap |
| Abbonamento trasporti | `abbonamento_trasporti` | Max €250 |
| Premi RC auto | `premi_assicurazione_rischio_morte` | RC auto NOT deductible |
| Premi vita/infortuni | `premi_assicurazione_rischio_morte` | Max €530 |
| Attività sportiva ragazzi | `sport_ragazzi` | Max €210/child, età 5–18 |
| Veterinario | `spese_veterinarie` | Max €550, franchigia €129,11 |
| Affitto studenti fuori sede | `affitto_studenti` | Max €2.633 |
| Donazioni ONLUS/ETS | `erogazioni_onlus` | 30%, max €30.000 |
| Spese funebri | `spese_funebri` | Max €1.550/decesso |

### 2 - Use Dichiarino MCP (if available)

```
verifica_spesa_detraibile(tipo_spesa="spese_sanitarie", importo=500.0)
→ Returns: detraibile (bool), percentuale, massimale, importo_detraibile, note

calcola_oneri_detraibili(spese=[...], reddito_complessivo=28000, anno=2025)
→ Returns: totale_detrazione, per_spesa breakdown, note
```

### 3 - Manual calculation

```
detrazione = min(spesa - franchigia, massimale) × percentuale
```

For `spese_sanitarie`:
```
detrazione = max(0, totale_sanitarie - 129.11) × 19%
```

**Income cap (reddito > €50.000):**
All 19% detrazioni *except* spese sanitarie are reduced by €260.

### 4 - Present results

Show per-expense:
- Importo versato
- Importo detraibile (after franchigia and cap)
- Detrazione spettante (€)
- Rigo Quadro E dove inserirlo

Then show totale detrazioni Quadro E.

---

## Common questions

**"Posso detrarre i farmaci da banco?"**
→ Yes, if purchased with pagamento tracciabile (bancomat/carta). Keep the receipt (scontrino parlante con CF).

**"Ho pagato in contanti dal medico, vale?"**
→ Spese sanitarie are exempt from the tracciability requirement. Cash payments are valid.

**"Il mio reddito è €60.000 - cambio qualcosa?"**
→ Yes: all 19% detrazioni except spese sanitarie are reduced by €260.

**"Mutuo cointestato con il coniuge"**
→ Each co-owner deducts their share of interest (e.g., 50% each). Max €4.000 applies per-person.

---

## Full limits table

See [references/DETRAZIONI.md](references/DETRAZIONI.md) for all massimali and percentuali.
