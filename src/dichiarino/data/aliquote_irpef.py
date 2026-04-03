"""IRPEF rates and brackets by tax year."""

from __future__ import annotations

from dichiarino.types import ScaglioneFiscale

# IRPEF 2025 - confirmed permanent by Legge di Bilancio 2025 (L. 207/2024)
SCAGLIONI_2025: list[ScaglioneFiscale] = [
    ScaglioneFiscale(min_reddito=0, max_reddito=28_000, aliquota=0.23),
    ScaglioneFiscale(min_reddito=28_000, max_reddito=50_000, aliquota=0.35),
    ScaglioneFiscale(min_reddito=50_000, max_reddito=None, aliquota=0.43),
]

# IRPEF 2024 - Legge di Bilancio 2024 (D.Lgs. 216/2023)
# Three brackets after reform (previously four)
SCAGLIONI_2024: list[ScaglioneFiscale] = [
    ScaglioneFiscale(min_reddito=0, max_reddito=28_000, aliquota=0.23),
    ScaglioneFiscale(min_reddito=28_000, max_reddito=50_000, aliquota=0.35),
    ScaglioneFiscale(min_reddito=50_000, max_reddito=None, aliquota=0.43),
]

# IRPEF 2023 - four brackets
SCAGLIONI_2023: list[ScaglioneFiscale] = [
    ScaglioneFiscale(min_reddito=0, max_reddito=15_000, aliquota=0.23),
    ScaglioneFiscale(min_reddito=15_000, max_reddito=28_000, aliquota=0.25),
    ScaglioneFiscale(min_reddito=28_000, max_reddito=50_000, aliquota=0.35),
    ScaglioneFiscale(min_reddito=50_000, max_reddito=None, aliquota=0.43),
]

SCAGLIONI_PER_ANNO: dict[int, list[ScaglioneFiscale]] = {
    2025: SCAGLIONI_2025,
    2024: SCAGLIONI_2024,
    2023: SCAGLIONI_2023,
}
