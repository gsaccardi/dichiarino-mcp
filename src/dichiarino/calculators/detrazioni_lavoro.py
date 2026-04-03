"""Detrazione per lavoro dipendente, pensione e assimilati - tax years 2023-2025.

References:
  - 2024: art. 13 TUIR, modificato dal D.Lgs. 216/2023 (riforma IRPEF 2024)
  - 2025: art. 13 TUIR + Legge 207/2024 (taglio cuneo fiscale), art. 1 cc. 4-9
"""

from __future__ import annotations

from dichiarino.types import TipoReddito


def calcola_detrazione_lavoro_dipendente(
    reddito_complessivo: float,
    giorni_lavoro: int = 365,
    tipo_reddito: TipoReddito = TipoReddito.LAVORO_DIPENDENTE,
    anno: int = 2025,
) -> float:
    """Compute the work-income tax credit (detrazione lavoro dipendente).

    For 2025, includes the taglio cuneo fiscale (L. 207/2024) as an additional
    benefit modelled as IRPEF reduction:
      - Reddito <= 20.000€: graduated bonus (7.1% / 5.3% / 4.8%)
      - Reddito 20.001-40.000€: additional detrazione (€1.000 flat or decreasing)

    Args:
        reddito_complessivo: Total taxable income in EUR.
        giorni_lavoro: Days of employment in the tax year (1-366).
        tipo_reddito: Type of income (lavoro dipendente, pensione, assimilato).
        anno: Tax year. Supported: 2023, 2024, 2025. Default: 2025.

    Returns:
        Detrazione amount in EUR (rounded to 2 decimal places).

    Raises:
        ValueError: For invalid inputs or unsupported year.
    """
    if reddito_complessivo < 0:
        raise ValueError("Il reddito complessivo non può essere negativo.")
    if not 1 <= giorni_lavoro <= 366:
        raise ValueError("I giorni di lavoro devono essere compresi tra 1 e 366.")
    if anno not in (2023, 2024, 2025):
        raise ValueError(f"Anno {anno} non supportato per questa detrazione.")

    rapporto_giorni = giorni_lavoro / 365

    if tipo_reddito == TipoReddito.PENSIONE:
        detrazione = _detrazione_pensione_2024(reddito_complessivo)
        # Pension detrazioni formula unchanged between 2024 and 2025
    else:
        detrazione = _detrazione_lavoro_2024(reddito_complessivo)

    detrazione = detrazione * rapporto_giorni

    if anno in (2024, 2025) and tipo_reddito != TipoReddito.PENSIONE:
        # Bonus aggiuntivo 65€ per redditi tra 25.001€ e 35.000€ (art. 13 c. 1-bis TUIR)
        if 25_000 < reddito_complessivo <= 35_000:
            detrazione += 65.0

    if anno == 2025 and tipo_reddito != TipoReddito.PENSIONE:
        # Taglio cuneo fiscale 2025 (L. 207/2024, art. 1 cc. 4-9)
        detrazione += _calcola_cuneo_fiscale_2025(reddito_complessivo) * rapporto_giorni

    return round(max(detrazione, 0.0), 2)


def calcola_solo_cuneo_fiscale_2025(
    reddito_complessivo: float,
    giorni_lavoro: int = 365,
) -> dict[str, float | str]:
    """Compute the taglio cuneo fiscale 2025 component separately.

    Useful to show the benefit breakdown to the user.

    Args:
        reddito_complessivo: Total taxable income in EUR.
        giorni_lavoro: Days worked (1-366), for pro-rating.

    Returns:
        Dict with bonus_busta_paga (<=20k) or detrazione_irpef (20k-40k) and total.
    """
    if reddito_complessivo < 0:
        raise ValueError("Il reddito complessivo non può essere negativo.")

    rapporto = min(giorni_lavoro, 366) / 365
    totale = round(_calcola_cuneo_fiscale_2025(reddito_complessivo) * rapporto, 2)

    if reddito_complessivo <= 20_000:
        return {
            "tipo": "bonus_busta_paga",
            "importo": totale,
            "nota": (
                "Bonus taglio cuneo fiscale 2025 (non tassabile): "
                f"{totale:.2f}€ - riduce l'IRPEF dovuta."
            ),
        }
    if reddito_complessivo <= 40_000:
        return {
            "tipo": "detrazione_irpef",
            "importo": totale,
            "nota": (f"Ulteriore detrazione IRPEF 2025 per taglio cuneo fiscale: {totale:.2f}€."),
        }
    return {
        "tipo": "nessun_beneficio",
        "importo": 0.0,
        "nota": "Reddito oltre 40.000€: nessun beneficio taglio cuneo fiscale 2025.",
    }


def _calcola_cuneo_fiscale_2025(reddito: float) -> float:
    """Taglio cuneo fiscale benefit amount (Legge 207/2024, art. 1 cc. 4-9).

    Two mechanisms:
      1. Reddito <= 20.000€: graduated bonus (treated as tax reduction)
         - Up to 8.500€: 7.1%
         - 8.501-15.000€: 5.3% on excess
         - 15.001-20.000€: 4.8% on excess
      2. Reddito 20.001-40.000€: additional IRPEF detrazione
         - 20.001-32.000€: flat €1.000
         - 32.001-40.000€: €1.000 × (40.000 - reddito) / 8.000
    """
    if reddito <= 0:
        return 0.0

    if reddito <= 20_000:
        bonus = 0.071 * min(reddito, 8_500)
        bonus += 0.053 * max(0.0, min(reddito, 15_000) - 8_500)
        bonus += 0.048 * max(0.0, min(reddito, 20_000) - 15_000)
        return bonus

    if reddito <= 32_000:
        return 1_000.0

    if reddito <= 40_000:
        return 1_000.0 * ((40_000 - reddito) / 8_000)

    return 0.0


def _detrazione_lavoro_2024(reddito: float) -> float:
    """Detrazione lavoro dipendente e assimilati 2024/2025 (art. 13 c. 1 TUIR)."""
    if reddito <= 0:
        return 1_955.0
    if reddito <= 15_000:
        return max(1_955.0, 690.0)
    if reddito <= 28_000:
        return 1_910.0 + 1_190.0 * ((28_000 - reddito) / (28_000 - 15_000))
    if reddito <= 50_000:
        return 1_910.0 * ((50_000 - reddito) / (50_000 - 28_000))
    return 0.0


def _detrazione_pensione_2024(reddito: float) -> float:
    """Detrazione per redditi di pensione 2024/2025 (art. 13 c. 3 TUIR)."""
    if reddito <= 0:
        return 1_955.0
    if reddito <= 8_500:
        return max(1_955.0, 713.0)
    if reddito <= 28_000:
        return 700.0 + 1_255.0 * ((28_000 - reddito) / (28_000 - 8_500))
    if reddito <= 50_000:
        return 700.0 * ((50_000 - reddito) / (50_000 - 28_000))
    return 0.0
