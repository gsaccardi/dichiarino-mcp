---
name: checklist-documenti-730
description: >
  Generate a personalised checklist of documents needed to compile the Italian Modello
  730. Based on the user's situation (income types, family status, home ownership,
  deductible expenses), produces a complete list of what to gather before filing.
  Covers CU (Certificazione Unica), property documents, medical receipts, mortgage
  statements, school fees, insurance policies, and more. Use this skill when a user
  wants to know what documents they need for their 730, or wants to prepare before
  visiting a CAF or commercialista.
license: Apache-2.0
compatibility: >
  Works best with the Dichiarino MCP server (tool: genera_checklist_730). Can also
  produce a standalone checklist via embedded rules.
metadata:
  domain: italian-tax
  form: modello-730
  author: dichiarino
---

# Checklist Documenti 730

Generate a **personalised document checklist** for the Modello 730 Precompilato.

## When to activate

Activate when the user:
- Asks "Quali documenti mi servono per il 730?"
- Wants to prepare before going to a CAF
- Is not sure if they need to file, and wants to see what applies to them
- Needs a per-category breakdown of documents

---

## Step-by-step instructions

### 1 - Profile the user's situation

Ask (or infer from context):

| Question | Why it matters |
|----------|---------------|
| Lavoratore dipendente / autonomo / pensionato? | Determines which CU / quadri apply |
| Prima casa in proprietà? | Abitazione principale exemptions, IMU |
| Mutuo sulla casa? | Interessi passivi detraibili (Quadro E7) |
| Figli / coniuge a carico? | Detrazioni familiari, asilo nido, sport |
| Spese mediche nel 2024/2025? | Quadro E spese sanitarie |
| Affittato immobili? | Quadro B, cedolare secca |
| Investimenti / conti esteri? | Quadro W |
| Altro reddito (freelance, collaborazioni)? | Quadro D |

### 2 - Use Dichiarino MCP (if available)

```
genera_checklist_730(
  ha_reddito_lavoro=True,
  ha_immobili=True,
  ha_mutuo=True,
  tipi_spese=["spese_sanitarie", "istruzione"],
  ha_familiari_a_carico=True
)
→ Returns: categorised document list
```

### 3 - Build the checklist manually

Use [assets/CHECKLIST_TEMPLATE.md](assets/CHECKLIST_TEMPLATE.md) as the base.
Tick/include sections based on user's answers.

---

## Minimum always-required documents

Every taxpayer needs:
- [ ] **Documento d'identità** (carta d'identità o passaporto)
- [ ] **Tessera sanitaria / codice fiscale**
- [ ] **IBAN** (per accredito rimborso)
- [ ] **Modello 730 dell'anno precedente** (se disponibile)

---

## Conditional document groups

### If lavoratore dipendente / pensionato
- [ ] **Certificazione Unica (CU)** rilasciata dal datore di lavoro / INPS
  - Contains: reddito, ritenute IRPEF, addizionali, contributi

### If autonomo / libero professionista
- [ ] CU da committenti (se co.co.co. / occasionale)
- [ ] Registro incassi e pagamenti o contabilità semplificata
- [ ] Fatture emesse e ricevute nell'anno

### If immobile in proprietà
- [ ] **Visura catastale** (rendita catastale)
- [ ] F24 IMU pagato (se non prima casa)
- [ ] Contratti d'affitto (se locato)

### If mutuo prima casa
- [ ] **Attestato interessi passivi** dalla banca (anno fiscale)
- [ ] Atto di mutuo (anno del contratto)
- [ ] Rogito notarile (per prima casa)

### If spese sanitarie
- [ ] Scontrini parlanti (con codice fiscale) da farmacia
- [ ] Ricevute / fatture da medici, dentisti, specialisti
- [ ] Fatture per ausili medici (occhiali, protesi) con prescrizione

### If figli a carico (≥ 21 anni)
- [ ] Codice fiscale dei figli
- [ ] Reddito del figlio (< €2.840,51 lordo per essere a carico)

### If spese istruzione
- [ ] Ricevute tasse universitarie / scolastiche
- [ ] Ricevute asilo nido (con CF del bambino)
- [ ] Ricevute attività sportiva (ragazzi 5–18 anni)

### If donazioni
- [ ] Ricevuta / attestato dell'ente beneficiario
- [ ] Bonifico tracciabile

---

## Output format

Present the checklist grouped by category, with checkboxes.  
Add at the end: *"Porta tutti gli originali + una copia al CAF. I documenti vanno conservati per 5 anni."*
