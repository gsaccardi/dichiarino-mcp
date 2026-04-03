"""Addizionale regionale IRPEF calculator."""

from __future__ import annotations

from dichiarino.data.addizionali_regionali import ADDIZIONALI_PER_ANNO
from dichiarino.types import RegioneItaliana


def calcola_addizionale_regionale(
    reddito_complessivo: float,
    regione: RegioneItaliana,
    anno: int = 2025,
) -> dict[str, float | str]:
    """Compute the regional IRPEF surcharge (addizionale regionale).

    Args:
        reddito_complessivo: Total taxable income in EUR.
        regione: Italian region.
        anno: Tax year. Supported: 2024, 2025.

    Returns:
        Dict with aliquota, soglia_esenzione, imponibile, addizionale.

    Raises:
        ValueError: For unsupported year or negative income.
    """
    if anno not in ADDIZIONALI_PER_ANNO:
        raise ValueError(f"Anno {anno} non ancora supportato.")
    if reddito_complessivo < 0:
        raise ValueError("Il reddito complessivo non può essere negativo.")

    aliquote, soglie = ADDIZIONALI_PER_ANNO[anno]
    aliquota = aliquote[regione]
    soglia = soglie.get(regione, 0.0)

    if reddito_complessivo <= soglia:
        return {
            "regione": regione.value,
            "aliquota": aliquota,
            "soglia_esenzione": soglia,
            "imponibile": 0.0,
            "addizionale": 0.0,
            "note": f"Reddito sotto la soglia di esenzione ({soglia:.0f}€). Nessuna addizionale.",
        }

    imponibile = reddito_complessivo - soglia
    addizionale = round(imponibile * aliquota, 2)

    return {
        "regione": regione.value,
        "aliquota": aliquota,
        "soglia_esenzione": soglia,
        "imponibile": round(imponibile, 2),
        "addizionale": addizionale,
        "note": (
            f"Addizionale regionale {regione.value.replace('_', ' ').title()}: "
            f"{aliquota * 100:.2f}% su {imponibile:.2f}€."
        ),
    }
