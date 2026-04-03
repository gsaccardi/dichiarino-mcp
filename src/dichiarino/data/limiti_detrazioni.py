"""Limits and rules for deductible/deductible expenses - tax years 2024-2025.

Source: Agenzia delle Entrate - Modello 730/2025 and 730/2026 istruzioni, TUIR aggiornato.
Key 2025 changes (Legge di Bilancio 2025, L. 207/2024):
  - Ristrutturazione: 50%/96k → 36%/48k (prima casa); 30%/48k (altri immobili).
  - Superbonus: 70% → 65%.
  - Risparmio energetico (Ecobonus): 65% → 50% for most interventions.
  - Bonus mobili: cap unchanged at 5.000€.
  - All other limits unchanged.
"""

from __future__ import annotations

from dataclasses import dataclass

from dichiarino.types import TipoSpesa


@dataclass(frozen=True)
class LimiteDetrazione:
    aliquota: float  # e.g. 0.19 = 19%
    tetto_massimo: float | None  # max deductible base; None = unlimited
    franchigia: float = 0.0  # non-deductible floor (e.g. 129.11 for medical)
    note: str = ""
    deducibile: bool = False  # True = reduces reddito imponibile instead of tax


# Detrazioni al 19% (from IRPEF) - Quadro E
# NB: for redditi > 50.000€ a franchigia of 260€ applies on the total 19% deductions
# (excluding spese sanitarie per D.Lgs. 216/2023)
LIMITI_DETRAZIONI_2024: dict[TipoSpesa, LimiteDetrazione] = {
    TipoSpesa.SPESE_SANITARIE: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=None,
        franchigia=129.11,
        note="Franchigia 129,11€. Detraibili al 19% sull'importo eccedente la franchigia.",
    ),
    TipoSpesa.SPESE_VETERINARIE: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=550.00,
        franchigia=129.11,
        note="Tetto massimo 550€, franchigia 129,11€.",
    ),
    TipoSpesa.MUTUO_PRIMA_CASA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=4_000.00,
        note="Interessi passivi su mutuo prima casa: max 4.000€.",
    ),
    TipoSpesa.RISTRUTTURAZIONE: LimiteDetrazione(
        aliquota=0.50,
        tetto_massimo=96_000.00,
        note="Detrazione 50% su max 96.000€. Rate in 10 anni.",
    ),
    TipoSpesa.RISPARMIO_ENERGETICO: LimiteDetrazione(
        aliquota=0.65,
        tetto_massimo=100_000.00,
        note="Ecobonus 65% (o 50% per alcune tipologie). Rate in 10 anni.",
    ),
    TipoSpesa.ISTRUZIONE_UNIVERSITA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=None,
        note=(
            "Tasse universitarie (pubbliche: intero importo; private: limite pari alle "
            "tasse degli atenei statali della stessa area geografica)."
        ),
    ),
    TipoSpesa.ISTRUZIONE_SCUOLA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=800.00,
        note="Spese scolastiche (dall'infanzia alla secondaria): max 800€ per figlio.",
    ),
    TipoSpesa.ASSICURAZIONE_VITA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=530.00,
        note="Premi assicurazione vita/invalidità: max 530€ (o 1.291€ per non autosufficienza).",
    ),
    TipoSpesa.ASSICURAZIONE_INFORTUNI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=530.00,
        note="Incluso nel limite delle assicurazioni vita.",
    ),
    TipoSpesa.CONTRIBUTI_PREVIDENZIALI: LimiteDetrazione(
        aliquota=1.0,
        tetto_massimo=5_164.57,
        deducibile=True,
        note="Contributi previdenziali/assistenziali: deducibili dal reddito (non detrazione).",
    ),
    TipoSpesa.EROGAZIONI_LIBERALI_ONLUS: LimiteDetrazione(
        aliquota=0.30,
        tetto_massimo=30_000.00,
        note="Donazioni a ONLUS/ETS: 30% su max 30.000€.",
    ),
    TipoSpesa.EROGAZIONI_LIBERALI_PARTITI: LimiteDetrazione(
        aliquota=0.26,
        tetto_massimo=30_000.00,
        franchigia=30.00,
        note="Donazioni a partiti politici: 26% su importo tra 30€ e 30.000€.",
    ),
    TipoSpesa.SPESE_FUNEBRI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=1_550.00,
        note="Spese funebri per familiari: max 1.550€ per decesso.",
    ),
    TipoSpesa.CANONI_AFFITTO_STUDENTI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=2_633.00,
        note=(
            "Canoni di locazione per studenti universitari fuori sede "
            "(almeno 100km dalla residenza): max 2.633€."
        ),
    ),
    TipoSpesa.BONUS_MOBILI: LimiteDetrazione(
        aliquota=0.50,
        tetto_massimo=5_000.00,
        note="Bonus mobili/grandi elettrodomestici connesso a ristrutturazione: 50% su max 5.000€.",
    ),
    TipoSpesa.SUPERBONUS: LimiteDetrazione(
        aliquota=0.70,
        tetto_massimo=96_000.00,
        note="Superbonus 70% (2024) per lavori trainanti. Rate in 4 anni.",
    ),
}

# Tax year 2025 (Modello 730/2026) - Legge di Bilancio 2025 (L. 207/2024).
# Changes vs 2024:
#   - Ristrutturazione: 36%/48k (prima casa) - use this as the standard rate.
#     For altri immobili the rate is 30%/48k; users should verify with their CAF.
#   - Risparmio energetico: 50% for most interventions (was 65%).
#   - Superbonus: 65% (was 70%).
#   - Everything else: unchanged.
LIMITI_DETRAZIONI_2025: dict[TipoSpesa, LimiteDetrazione] = {
    TipoSpesa.SPESE_SANITARIE: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=None,
        franchigia=129.11,
        note="Franchigia 129,11€. Detraibili al 19% sull'importo eccedente la franchigia.",
    ),
    TipoSpesa.SPESE_VETERINARIE: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=550.00,
        franchigia=129.11,
        note="Tetto massimo 550€, franchigia 129,11€.",
    ),
    TipoSpesa.MUTUO_PRIMA_CASA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=4_000.00,
        note="Interessi passivi su mutuo prima casa: max 4.000€.",
    ),
    TipoSpesa.RISTRUTTURAZIONE: LimiteDetrazione(
        aliquota=0.36,
        tetto_massimo=48_000.00,
        note=(
            "Detrazione 36% su max 48.000€ (abitazione principale) - L. 207/2024. "
            "Per altri immobili: 30% su max 48.000€. Rate in 10 anni."
        ),
    ),
    TipoSpesa.RISPARMIO_ENERGETICO: LimiteDetrazione(
        aliquota=0.50,
        tetto_massimo=100_000.00,
        note="Ecobonus 50% per la maggior parte degli interventi - L. 207/2024. Rate in 10 anni.",
    ),
    TipoSpesa.ISTRUZIONE_UNIVERSITA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=None,
        note=(
            "Tasse universitarie (pubbliche: intero importo; private: limite pari alle "
            "tasse degli atenei statali della stessa area geografica)."
        ),
    ),
    TipoSpesa.ISTRUZIONE_SCUOLA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=800.00,
        note="Spese scolastiche (dall'infanzia alla secondaria): max 800€ per figlio.",
    ),
    TipoSpesa.ASSICURAZIONE_VITA: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=530.00,
        note="Premi assicurazione vita/invalidità: max 530€ (o 1.291€ per non autosufficienza).",
    ),
    TipoSpesa.ASSICURAZIONE_INFORTUNI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=530.00,
        note="Incluso nel limite delle assicurazioni vita.",
    ),
    TipoSpesa.CONTRIBUTI_PREVIDENZIALI: LimiteDetrazione(
        aliquota=1.0,
        tetto_massimo=5_164.57,
        deducibile=True,
        note="Contributi previdenziali/assistenziali: deducibili dal reddito (non detrazione).",
    ),
    TipoSpesa.EROGAZIONI_LIBERALI_ONLUS: LimiteDetrazione(
        aliquota=0.30,
        tetto_massimo=30_000.00,
        note="Donazioni a ONLUS/ETS: 30% su max 30.000€.",
    ),
    TipoSpesa.EROGAZIONI_LIBERALI_PARTITI: LimiteDetrazione(
        aliquota=0.26,
        tetto_massimo=30_000.00,
        franchigia=30.00,
        note="Donazioni a partiti politici: 26% su importo tra 30€ e 30.000€.",
    ),
    TipoSpesa.SPESE_FUNEBRI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=1_550.00,
        note="Spese funebri per familiari: max 1.550€ per decesso.",
    ),
    TipoSpesa.CANONI_AFFITTO_STUDENTI: LimiteDetrazione(
        aliquota=0.19,
        tetto_massimo=2_633.00,
        note=(
            "Canoni di locazione per studenti universitari fuori sede "
            "(almeno 100km dalla residenza): max 2.633€."
        ),
    ),
    TipoSpesa.BONUS_MOBILI: LimiteDetrazione(
        aliquota=0.50,
        tetto_massimo=5_000.00,
        note="Bonus mobili/grandi elettrodomestici connesso a ristrutturazione: 50% su max 5.000€.",
    ),
    TipoSpesa.SUPERBONUS: LimiteDetrazione(
        aliquota=0.65,
        tetto_massimo=96_000.00,
        note="Superbonus 65% (2025) per lavori trainanti - L. 207/2024. Rate in 4 anni.",
    ),
}

# Convenience lookup: year -> limits dict
LIMITI_PER_ANNO: dict[int, dict[TipoSpesa, LimiteDetrazione]] = {
    2024: LIMITI_DETRAZIONI_2024,
    2025: LIMITI_DETRAZIONI_2025,
}
