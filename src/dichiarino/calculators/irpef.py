"""IRPEF gross tax calculation."""

from __future__ import annotations

from dichiarino.data.aliquote_irpef import SCAGLIONI_PER_ANNO
from dichiarino.types import RisultatoIRPEF, ScaglioneFiscale


def calcola_irpef_lorda(reddito_complessivo: float, anno: int = 2025) -> RisultatoIRPEF:
    """Compute gross IRPEF for a given total income and tax year.

    Args:
        reddito_complessivo: Total taxable income in EUR (must be >= 0).
        anno: Tax year (anno di imposta). Defaults to 2024.

    Returns:
        RisultatoIRPEF with gross IRPEF and per-bracket breakdown.

    Raises:
        ValueError: If the tax year is not supported or income is negative.
    """
    if reddito_complessivo < 0:
        raise ValueError("Il reddito complessivo non può essere negativo.")
    if anno not in SCAGLIONI_PER_ANNO:
        raise ValueError(
            f"Anno fiscale {anno} non supportato. "
            f"Anni disponibili: {sorted(SCAGLIONI_PER_ANNO.keys())}"
        )

    scaglioni = SCAGLIONI_PER_ANNO[anno]
    irpef_totale = 0.0
    breakdown: list[dict[str, float]] = []

    for scaglione in scaglioni:
        imposta, base = _imposta_scaglione(reddito_complessivo, scaglione)
        irpef_totale += imposta
        if base > 0:
            breakdown.append(
                {
                    "min": scaglione.min_reddito,
                    "max": scaglione.max_reddito or float("inf"),
                    "aliquota": scaglione.aliquota,
                    "base_imponibile": round(base, 2),
                    "imposta": round(imposta, 2),
                }
            )

    return RisultatoIRPEF(
        reddito_complessivo=reddito_complessivo,
        irpef_lorda=round(irpef_totale, 2),
        breakdown_scaglioni=breakdown,
        anno=anno,
    )


def _imposta_scaglione(reddito: float, scaglione: ScaglioneFiscale) -> tuple[float, float]:
    """Return (tax, taxable_base) for one bracket."""
    if reddito <= scaglione.min_reddito:
        return 0.0, 0.0
    cap = scaglione.max_reddito if scaglione.max_reddito is not None else reddito
    base = min(reddito, cap) - scaglione.min_reddito
    return base * scaglione.aliquota, base
