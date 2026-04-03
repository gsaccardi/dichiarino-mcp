---
name: verifica-codice-fiscale
description: >
  Validate, decode, and explain an Italian codice fiscale (fiscal code). Checks format,
  extracts surname, name, birth date, gender, and municipality of birth, and verifies
  the check digit. Detects common errors (transposed characters, wrong check digit,
  omocodia variants). Use this skill when a user provides a codice fiscale and wants
  to verify it is correct, understand what it encodes, or diagnose a mismatch with
  their personal data.
license: Apache-2.0
compatibility: >
  Works best with the Dichiarino MCP server connected (tool: valida_codice_fiscale).
  Standalone validation logic is embedded in this skill.
metadata:
  domain: italian-tax
  form: modello-730
  author: dichiarino
---

# Verifica Codice Fiscale

Validate and decode an Italian **codice fiscale** (16-character alphanumeric fiscal code).

## When to activate

Activate when a user:
- Asks "Il mio codice fiscale è corretto?"
- Provides a CF and wants to know what it encodes
- Gets a mismatch error when submitting their 730
- Needs to check a dependent family member's CF

---

## Structure of the codice fiscale

```
S S S N N N A A D D D C C C C X
│ │ │ │ │ │ │ │ │ │ │ │ │ │ │ └─ Check character (1)
│ │ │ │ │ │ │ │ │ │ └─────────── Codice comune nascita (4)
│ │ │ │ │ │ │ │ └─────────────── Giorno nascita + sesso (2)
│ │ │ │ │ │ └───────────────── Mese nascita (1 letter)
│ │ │ │ │ └─────────────────── Anno nascita (2 digits)
│ │ │ └───────────────────── Nome consonants (3)
└─────────────────────────── Cognome consonants (3)
```

**Total: 16 characters** - uppercase letters and digits.

---

## Step-by-step validation

### 1 - Use Dichiarino MCP (if available)

```
valida_codice_fiscale(codice_fiscale="RSSMRA85M01H501Z")
→ Returns: valid (bool), sesso, data_nascita, codice_comune, errors
```

### 2 - Manual validation (fallback)

**Step 2a - Format check**
- Must be exactly 16 characters
- Regex: `^[A-Z]{6}[0-9LMNPQRSTUV]{2}[ABCDEHLMPRST]{1}[0-9LMNPQRSTUV]{2}[A-Z]{1}[0-9LMNPQRSTUV]{3}[A-Z]{1}$`

**Step 2b - Decode each field**

| Pos | Field | How to read |
|-----|-------|-------------|
| 0–2 | Cognome | 3 consonants; if < 3 consonants, fill with vowels then X |
| 3–5 | Nome | If ≥ 4 consonants: take 1st, 3rd, 4th. Else: consonants then vowels then X |
| 6–7 | Anno nascita | Last 2 digits of birth year |
| 8 | Mese nascita | Letter code (see table below) |
| 9–10 | Giorno + sesso | Day 01–31 = male; day 41–71 = female (day − 40) |
| 11–14 | Codice comune | Starts with letter for Italian comuni; Z+3 digits for foreign countries |
| 15 | Carattere controllo | Computed from positions 0–14 |

**Month letter codes:**
A=Gen, B=Feb, C=Mar, D=Apr, E=Mag, H=Giu, L=Lug, M=Ago, P=Set, R=Ott, S=Nov, T=Dic

**Step 2c - Verify the check digit** (position 15)

Odd positions (1,3,5,…): use odd-position lookup table.  
Even positions (0,2,4,…): face value (0→0, A→0, B→1 … Z→25).  
Sum all 16 partial values → check = `chr(ord('A') + (total % 26))`

See [references/CHECK_DIGIT.md](references/CHECK_DIGIT.md) for the full lookup tables.

---

## Presenting results

Always show:
1. ✅ / ❌ **Validity** (with reason if invalid)
2. Decoded fields: surname hint, name hint, birth date, gender (M/F), comune/nazione
3. Any detected **omocodia** substitution (digits replaced with letters)
4. Suggested fix if invalid

---

## Common errors

| Error | Cause | Fix |
|-------|-------|-----|
| Wrong check digit | Typo anywhere in the CF | Re-derive from personal data |
| Day > 40 reported as male | Encoding is correct - female day = day+40 | Inform user it's normal |
| Omocodia variant | Comune has duplicate CFs; Agenzia Entrate substitutes digits with letters | Both variants are valid |
| Foreign-born | Codice comune = Z + 3 digits (Belcalis table) | Not an error |
