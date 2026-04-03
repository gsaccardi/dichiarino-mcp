"""Detrazioni per carichi di famiglia - tax years 2024-2025.

References:
  - art. 12 TUIR, modificato dalla Legge di Bilancio 2022 (addio detrazioni figli
    under 21 → assegno unico) e Legge di Bilancio 2024.
  - Legge 207/2024 (Legge di Bilancio 2025): detrazioni figli a carico spettano
    solo per figli tra 21 e 30 anni (salvo disabilità); oltre i 30 anni solo se disabili.

Key rules (2024/2025):
- Children under 21: no detrazione (covered by Assegno Unico Universale - AUU).
- Children 21-30 (or disabled): detrazione 950€ (income-scaled).
- Coniuge a carico: detrazione 690-800€ (income-scaled).
- Other dependants: detrazione 750€ (income-scaled).
"""

from __future__ import annotations

from dichiarino.types import FamiliareACarico, TipoFamiliare


def calcola_detrazioni_familiari(
    familiari: list[FamiliareACarico],
    reddito_complessivo: float,
    anno: int = 2025,
) -> dict[str, float | str]:
    """Compute total detrazioni per carichi di famiglia.

    Args:
        familiari: List of dependant family members.
        reddito_complessivo: Taxpayer's total taxable income.
        anno: Tax year.

    Returns:
        Dict with per-category amounts and total detrazione.

    Raises:
        ValueError: For unsupported year or invalid inputs.
    """
    if anno not in (2024, 2025):
        raise ValueError(f"Anno {anno} non ancora supportato.")
    if reddito_complessivo < 0:
        raise ValueError("Il reddito complessivo non può essere negativo.")
    totale_coniuge = 0.0
    totale_figli = 0.0
    totale_altri = 0.0

    for familiare in familiari:
        rapporto = (familiare.mesi_a_carico / 12) * familiare.percentuale_carico

        if familiare.tipo == TipoFamiliare.CONIUGE:
            base = _detrazione_coniuge_2024(reddito_complessivo)
            totale_coniuge += base * rapporto

        elif familiare.tipo == TipoFamiliare.FIGLIO:
            if familiare.eta_inferiore_21:
                # No detrazione - covered by Assegno Unico Universale
                continue
            base = _detrazione_figlio_2024(reddito_complessivo)
            totale_figli += base * rapporto

        elif familiare.tipo == TipoFamiliare.ALTRO:
            base = _detrazione_altro_familiare_2024(reddito_complessivo)
            totale_altri += base * rapporto

    totale = totale_coniuge + totale_figli + totale_altri

    return {
        "detrazione_coniuge": round(totale_coniuge, 2),
        "detrazione_figli": round(totale_figli, 2),
        "detrazione_altri": round(totale_altri, 2),
        "totale": round(totale, 2),
    }


def _detrazione_coniuge_2024(reddito: float) -> float:
    """Detrazione per coniuge a carico (art. 12 c. 1 lett. a TUIR)."""
    if reddito <= 15_000:
        return 800.0
    if reddito <= 29_000:
        return 800.0 - 110.0 * ((reddito - 15_000) / (29_000 - 15_000))
    if reddito <= 29_200:
        return 690.0
    if reddito <= 34_700:
        return 700.0
    if reddito <= 35_000:
        return 710.0
    if reddito <= 35_100:
        return 720.0
    if reddito <= 35_200:
        return 710.0
    if reddito <= 40_000:
        return 690.0
    if reddito <= 80_000:
        return 690.0 * ((80_000 - reddito) / (80_000 - 40_000))
    return 0.0


def _detrazione_figlio_2024(reddito: float) -> float:
    """Detrazione per figlio a carico ≥ 21 anni (art. 12 c. 1 lett. c-bis TUIR)."""
    if reddito <= 80_000:
        return 950.0 * ((80_000 - reddito) / 80_000)
    return 0.0


def _detrazione_altro_familiare_2024(reddito: float) -> float:
    """Detrazione per altri familiari a carico (art. 12 c. 1 lett. d TUIR)."""
    if reddito <= 80_000:
        return 750.0 * ((80_000 - reddito) / 80_000)
    return 0.0
