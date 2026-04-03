"""Oneri detraibili e deducibili - Quadro E calculator."""

from __future__ import annotations

from typing import Any

from dichiarino.data.limiti_detrazioni import LIMITI_PER_ANNO
from dichiarino.types import SpesaDetraibile, TipoSpesa


def calcola_oneri_detraibili(
    spese: list[SpesaDetraibile],
    reddito_complessivo: float,
    anno: int = 2025,
) -> dict[str, Any]:
    """Compute total detraibile/deducibile amounts for Quadro E expenses.

    Args:
        spese: List of expenses with type and amount.
        reddito_complessivo: Taxpayer's total income (used for high-income cap).
        anno: Tax year. Supported: 2024, 2025.

    Returns:
        Dict with per-category breakdown, totale_detrazione_irpef, totale_deducibile.
    """
    if anno not in LIMITI_PER_ANNO:
        raise ValueError(f"Anno {anno} non ancora supportato.")

    limiti = LIMITI_PER_ANNO[anno]

    totale_detrazione = 0.0
    totale_deducibile = 0.0
    totale_detrazioni_19_non_sanitarie = 0.0
    dettaglio: list[dict[str, Any]] = []

    # Group spese sanitarie for franchigia aggregation
    sanitarie_totale = sum(s.importo for s in spese if s.tipo == TipoSpesa.SPESE_SANITARIE)

    seen_sanitarie = False

    for spesa in spese:
        limite = limiti.get(spesa.tipo)
        if limite is None:
            dettaglio.append(
                {
                    "tipo": spesa.tipo,
                    "importo": spesa.importo,
                    "detrazione": 0.0,
                    "note": "Tipo spesa non riconosciuto.",
                }
            )
            continue

        if limite.deducibile:
            # Reduces taxable income
            base = min(spesa.importo, limite.tetto_massimo or spesa.importo)
            totale_deducibile += base
            dettaglio.append(
                {
                    "tipo": spesa.tipo,
                    "importo": spesa.importo,
                    "deducibile": round(base, 2),
                    "note": limite.note,
                }
            )
            continue

        # Aggregate all spese sanitarie under a single franchigia
        if spesa.tipo == TipoSpesa.SPESE_SANITARIE:
            if seen_sanitarie:
                continue
            seen_sanitarie = True
            importo_effettivo = sanitarie_totale
        else:
            importo_effettivo = spesa.importo

        base = importo_effettivo - limite.franchigia
        if base <= 0:
            dettaglio.append(
                {
                    "tipo": spesa.tipo,
                    "importo": importo_effettivo,
                    "detrazione": 0.0,
                    "note": f"Sotto la franchigia di {limite.franchigia:.2f}€.",
                }
            )
            continue

        if limite.tetto_massimo is not None:
            base = min(base, limite.tetto_massimo)

        detrazione = round(base * limite.aliquota, 2)
        totale_detrazione += detrazione
        # Track 19% detrazioni (excluding sanitarie) for high-income cap
        if limite.aliquota == 0.19 and spesa.tipo != TipoSpesa.SPESE_SANITARIE:
            totale_detrazioni_19_non_sanitarie += detrazione
        dettaglio.append(
            {
                "tipo": spesa.tipo,
                "importo": importo_effettivo,
                "base_detraibile": round(base, 2),
                "aliquota": limite.aliquota,
                "detrazione": detrazione,
                "note": limite.note,
            }
        )

    # High-income cap: for redditi > 50.000€, reduce 19% detrazioni by 260€
    # (excluding spese sanitarie - art. 15 c. 3-bis TUIR as per D.Lgs. 216/2023)
    if reddito_complessivo > 50_000:
        riduzione = min(260.0, totale_detrazioni_19_non_sanitarie)
        totale_detrazione = max(0.0, totale_detrazione - riduzione)

    return {
        "dettaglio": dettaglio,
        "totale_detrazione_irpef": round(totale_detrazione, 2),
        "totale_deducibile": round(totale_deducibile, 2),
    }
