---
name: analizza-cu
description: >
  Parse, explain, and summarise an Italian Certificazione Unica (CU) - the annual
  income and tax certificate issued by employers and INPS to employees, pensioners,
  and self-employed workers. Maps each box number to its meaning, extracts the key
  figures needed for the 730 (reddito, ritenute, addizionali, detrazioni applicate),
  and flags anomalies or missing data. Use this skill when a user has their CU and
  wants to understand it, verify it, or extract the values to fill in the 730.
license: Apache-2.0
compatibility: >
  Works best with the Dichiarino MCP server (tool: analizza_certificazione_unica).
  Embedded CU field mapping covers the standard CU 2024/2025 layout.
metadata:
  domain: italian-tax
  form: modello-730
  author: dichiarino
---

# Analizza Certificazione Unica (CU)

Parse and explain the **Certificazione Unica** - the employer/INPS income certificate needed to file the Modello 730.

## When to activate

Activate when the user:
- Uploads or pastes CU data and asks "Cosa significa questo campo?"
- Asks "Dove trovo il mio reddito sulla CU?"
- Reports that the pre-filled 730 shows different values from their CU
- Has received multiple CUs (e.g., two employers) and needs to reconcile them

---

## What is the CU?

The **Certificazione Unica** (formerly CUD) is issued by:
- **Datori di lavoro** (employers) - for employees
- **INPS / enti previdenziali** - for pensioners and benefit recipients
- **Committenti** - for co.co.co. / lavoro autonomo

It must be sent to the Agenzia delle Entrate by **16 March** each year, and given to the taxpayer by **31 March**.

---

## Step-by-step instructions

### 1 - Use Dichiarino MCP (if available)

```
analizza_certificazione_unica(
  reddito_lavoro_dipendente=35000,
  ritenute_irpef=6800,
  ritenute_addizionale_regionale=350,
  anno=2025
)
→ Returns: summary, quadro_c_values, note, anomalie
```

### 2 - Map CU boxes to 730 fields

Use [references/CU_CAMPI.md](references/CU_CAMPI.md) for the complete box mapping.

Key fields to extract:

| CU Box | Description | → 730 field |
|--------|-------------|-------------|
| **1** | Reddito lavoro dipendente / pensione | → Quadro C, rigo C1 |
| **4** | Reddito co.co.co. / assimilati | → Quadro C, rigo C3 |
| **21** | Ritenute IRPEF | → Quadro C, rigo C9 / Quadro F, rigo F2 |
| **22** | Ritenute IRPEF per redditi co.co.co. | → Quadro F, rigo F2 |
| **23** | Addizionale regionale trattenuta | → Quadro C, rigo C10 |
| **24** | Addizionale regionale saldo dovuto | → calculated field |
| **25** | Addizionale comunale acconto | → Quadro C, rigo C11 |
| **26** | Addizionale comunale saldo | → Quadro C, rigo C12 |
| **43** | Acconto cedolare secca | → Quadro C, rigo C13 |
| **101** | Contributi previdenziali a carico lavoratore | → Quadro E, rigo E21 |
| **361** | Detrazioni per lavoro dipendente applicate | → verify vs. calculated |
| **362** | Detrazioni per familiari a carico applicate | → verify vs. calculated |

### 3 - Check for anomalies

Flag these automatically:
- Box 1 = 0 but Box 21 > 0 → ritenute senza reddito (unusual)
- Box 361 > expected detrazione lavoro → employer may have over-applied detractions
- Box 1 >> expected for the sector → possible error
- Multiple CUs with overlapping periods → sum redditi, check total ritenute

### 4 - Summarise for the user

Provide a clear plain-language summary:
```
📋 La tua CU 2025 - Riepilogo
────────────────────────────
Datore di lavoro: [name if provided]
Reddito percepito:      €35.000,00
IRPEF trattenuta:        €6.800,00
Addiz. regionale:          €350,00
Addiz. comunale acc.:      €120,00

Da inserire nel 730:
• Quadro C, rigo C1:  €35.000
• Quadro C, rigo C9:   €6.800
• Quadro C, rigo C10:    €350
```

---

## Multiple CUs (same year, different employers)

If the user has more than one CU:
1. Sum all **Box 1** values → single C1 entry
2. Sum all **Box 21** values → single C9 entry
3. Attach all CUs to the 730
4. Check that total months ≤ 12 (unless job change mid-year)

---

## Common questions

**"Il mio datore non mi ha dato la CU - cosa faccio?"**
→ The employer is legally required to provide it by 31 March. Contact them first; if unresponsive, file a complaint with the ITL (Ispettorato del Lavoro).

**"La CU pre-compila già la mia dichiarazione?"**
→ Yes - the Agenzia delle Entrate receives the CU directly. The 730 precompilato will have Box 1 and Box 21 already filled. Always verify they match your paper CU.

**"Ho ricevuto la CU ma sono un dipendente part-time con più datori"**
→ You will have one CU per datore. Sum all C1 values; the 730 precompilato should already aggregate them.
