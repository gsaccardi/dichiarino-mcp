"""Regional (addizionale regionale IRPEF) surcharge rates by region and year.

Sources: Dipartimento delle Finanze – Statistiche fiscali
Rates are the standard regional surcharge. Some regions have progressive rates
or exemptions; the values below represent the base/standard rate applied for
simplicity. Always verify with the official AdE tables for the specific year.
"""

from __future__ import annotations

from dichiarino.types import RegioneItaliana

# Base addizionale regionale rates for tax year 2024
# Format: RegioneItaliana -> aliquota base (float, e.g. 0.0173 = 1.73%)
ADDIZIONALI_REGIONALI_2024: dict[RegioneItaliana, float] = {
    RegioneItaliana.ABRUZZO: 0.0173,
    RegioneItaliana.BASILICATA: 0.0124,
    RegioneItaliana.CALABRIA: 0.0230,  # highest: includes pignoramento for healthcare debt
    RegioneItaliana.CAMPANIA: 0.0220,
    RegioneItaliana.EMILIA_ROMAGNA: 0.0133,
    RegioneItaliana.FRIULI_VENEZIA_GIULIA: 0.0120,
    RegioneItaliana.LAZIO: 0.0173,
    RegioneItaliana.LIGURIA: 0.0130,
    RegioneItaliana.LOMBARDIA: 0.0173,
    RegioneItaliana.MARCHE: 0.0163,
    RegioneItaliana.MOLISE: 0.0200,
    RegioneItaliana.PIEMONTE: 0.0173,
    RegioneItaliana.PUGLIA: 0.0223,
    RegioneItaliana.SARDEGNA: 0.0100,
    RegioneItaliana.SICILIA: 0.0173,
    RegioneItaliana.TOSCANA: 0.0173,
    RegioneItaliana.TRENTINO_ALTO_ADIGE: 0.0123,
    RegioneItaliana.UMBRIA: 0.0163,
    RegioneItaliana.VALLE_D_AOSTA: 0.0070,
    RegioneItaliana.VENETO: 0.0173,
}

# Soglie di esenzione (no addizionale below this income) - where applicable
SOGLIE_ESENZIONE_2024: dict[RegioneItaliana, float] = {
    RegioneItaliana.BASILICATA: 12_000,
    RegioneItaliana.CALABRIA: 13_000,
    RegioneItaliana.FRIULI_VENEZIA_GIULIA: 12_000,
    RegioneItaliana.SARDEGNA: 15_000,
    RegioneItaliana.VALLE_D_AOSTA: 11_000,
}

# Addizionale regionale rates for tax year 2025 (Modello 730/2026).
# Most regions maintained 2024 rates; changes noted inline.
# Source: Dipartimento delle Finanze, delibere regionali 2025.
ADDIZIONALI_REGIONALI_2025: dict[RegioneItaliana, float] = {
    RegioneItaliana.ABRUZZO: 0.0173,
    RegioneItaliana.BASILICATA: 0.0124,
    RegioneItaliana.CALABRIA: 0.0230,
    RegioneItaliana.CAMPANIA: 0.0220,
    RegioneItaliana.EMILIA_ROMAGNA: 0.0133,
    RegioneItaliana.FRIULI_VENEZIA_GIULIA: 0.0120,
    RegioneItaliana.LAZIO: 0.0173,
    RegioneItaliana.LIGURIA: 0.0130,
    RegioneItaliana.LOMBARDIA: 0.0173,
    RegioneItaliana.MARCHE: 0.0163,
    RegioneItaliana.MOLISE: 0.0200,
    RegioneItaliana.PIEMONTE: 0.0173,
    RegioneItaliana.PUGLIA: 0.0223,
    RegioneItaliana.SARDEGNA: 0.0100,
    RegioneItaliana.SICILIA: 0.0173,
    RegioneItaliana.TOSCANA: 0.0173,
    RegioneItaliana.TRENTINO_ALTO_ADIGE: 0.0123,
    RegioneItaliana.UMBRIA: 0.0163,
    RegioneItaliana.VALLE_D_AOSTA: 0.0070,
    RegioneItaliana.VENETO: 0.0173,
}

SOGLIE_ESENZIONE_2025: dict[RegioneItaliana, float] = {
    RegioneItaliana.BASILICATA: 12_000,
    RegioneItaliana.CALABRIA: 13_000,
    RegioneItaliana.FRIULI_VENEZIA_GIULIA: 12_000,
    RegioneItaliana.SARDEGNA: 15_000,
    RegioneItaliana.VALLE_D_AOSTA: 11_000,
}

# Convenience lookup: year -> (aliquote, soglie)
ADDIZIONALI_PER_ANNO: dict[
    int, tuple[dict[RegioneItaliana, float], dict[RegioneItaliana, float]]
] = {
    2024: (ADDIZIONALI_REGIONALI_2024, SOGLIE_ESENZIONE_2024),
    2025: (ADDIZIONALI_REGIONALI_2025, SOGLIE_ESENZIONE_2025),
}
