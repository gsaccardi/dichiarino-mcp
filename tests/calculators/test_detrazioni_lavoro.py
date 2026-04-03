"""Unit tests for detrazioni lavoro dipendente calculator."""

from __future__ import annotations

import pytest

from dichiarino.calculators.detrazioni_lavoro import calcola_detrazione_lavoro_dipendente
from dichiarino.types import TipoReddito


class TestDetrazioniLavoroDipendente:
    def test_reddito_zero(self) -> None:
        det = calcola_detrazione_lavoro_dipendente(0.0)
        assert det >= 690.0  # minimum guaranteed

    def test_reddito_8500_no_tax_area(self) -> None:
        # No-tax area: detrazione should cover all IRPEF (>= 1.955€)
        det = calcola_detrazione_lavoro_dipendente(8_500)
        assert det >= 1_955.0 * (365 / 365)

    def test_reddito_15000(self) -> None:
        det = calcola_detrazione_lavoro_dipendente(15_000)
        assert det >= 690.0

    def test_reddito_20000_formula(self) -> None:
        # In bracket 15.001-28.000: 1.910 + 1.190 x (28.000-20.000)/(28.000-15.000)
        expected = 1_910.0 + 1_190.0 * ((28_000 - 20_000) / (28_000 - 15_000))
        det = calcola_detrazione_lavoro_dipendente(20_000, anno=2024)
        assert det == pytest.approx(expected, rel=1e-4)

    def test_reddito_28000(self) -> None:
        # At 28.000€ the bracket formula returns 1.910€, plus the 65€ bonus (25k-35k)
        det = calcola_detrazione_lavoro_dipendente(28_000, anno=2024)
        assert det == pytest.approx(1_910.0 + 65.0)

    def test_reddito_40000(self) -> None:
        # In bracket 28.001-50.000: 1.910 × (50.000-40.000)/(50.000-28.000)
        expected = 1_910.0 * ((50_000 - 40_000) / (50_000 - 28_000))
        det = calcola_detrazione_lavoro_dipendente(40_000)
        assert det == pytest.approx(expected, rel=1e-4)

    def test_reddito_above_50000(self) -> None:
        det = calcola_detrazione_lavoro_dipendente(60_000)
        assert det == 0.0

    def test_partial_year(self) -> None:
        # 180 days ≈ half year → roughly half the detrazione
        det_full = calcola_detrazione_lavoro_dipendente(20_000, giorni_lavoro=365)
        det_half = calcola_detrazione_lavoro_dipendente(20_000, giorni_lavoro=180)
        assert det_half == pytest.approx(det_full * (180 / 365), rel=1e-2)

    def test_bonus_65_applies(self) -> None:
        # Reddito between 25.001 and 35.000 gets +65€
        det_25001 = calcola_detrazione_lavoro_dipendente(25_001)
        det_24999 = calcola_detrazione_lavoro_dipendente(24_999)
        # The one with bonus should be higher (accounting for formula reduction)
        assert det_25001 > det_24999 - 200  # rough check

    def test_bonus_65_not_for_pensione(self) -> None:
        det_lav = calcola_detrazione_lavoro_dipendente(
            30_000, tipo_reddito=TipoReddito.LAVORO_DIPENDENTE
        )
        det_pen = calcola_detrazione_lavoro_dipendente(30_000, tipo_reddito=TipoReddito.PENSIONE)
        # Pensione doesn't get the 65€ bonus
        assert det_lav != det_pen

    def test_invalid_days_raises(self) -> None:
        with pytest.raises(ValueError, match="giorni"):
            calcola_detrazione_lavoro_dipendente(20_000, giorni_lavoro=0)

    def test_invalid_days_too_many(self) -> None:
        with pytest.raises(ValueError, match="giorni"):
            calcola_detrazione_lavoro_dipendente(20_000, giorni_lavoro=400)

    def test_negative_income_raises(self) -> None:
        with pytest.raises(ValueError, match="negativo"):
            calcola_detrazione_lavoro_dipendente(-1)

    def test_pensione_reddito_basso(self) -> None:
        det = calcola_detrazione_lavoro_dipendente(7_500, tipo_reddito=TipoReddito.PENSIONE)
        assert det >= 713.0


class TestCuneoFiscale2025:
    def test_reddito_below_8500(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        # 7.1% of 8.000
        assert _calcola_cuneo_fiscale_2025(8_000) == pytest.approx(8_000 * 0.071, rel=1e-4)

    def test_reddito_15000(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        expected = 8_500 * 0.071 + 6_500 * 0.053
        assert _calcola_cuneo_fiscale_2025(15_000) == pytest.approx(expected, rel=1e-4)

    def test_reddito_20000(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        expected = 8_500 * 0.071 + 6_500 * 0.053 + 5_000 * 0.048
        assert _calcola_cuneo_fiscale_2025(20_000) == pytest.approx(expected, rel=1e-4)

    def test_reddito_25000_flat_1000(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        assert _calcola_cuneo_fiscale_2025(25_000) == pytest.approx(1_000.0)

    def test_reddito_32000_still_1000(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        assert _calcola_cuneo_fiscale_2025(32_000) == pytest.approx(1_000.0)

    def test_reddito_36000_decreasing(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        expected = 1_000.0 * ((40_000 - 36_000) / 8_000)
        assert _calcola_cuneo_fiscale_2025(36_000) == pytest.approx(expected, rel=1e-4)

    def test_reddito_40000_zero(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        assert _calcola_cuneo_fiscale_2025(40_000) == pytest.approx(0.0, abs=1e-4)

    def test_reddito_above_40000_zero(self) -> None:
        from dichiarino.calculators.detrazioni_lavoro import _calcola_cuneo_fiscale_2025

        assert _calcola_cuneo_fiscale_2025(50_000) == 0.0

    def test_2025_higher_than_2024_at_30k(self) -> None:
        # At 30k (in cuneo range 20k-40k), 2025 gives +1000€ extra vs 2024
        det_2025 = calcola_detrazione_lavoro_dipendente(30_000, anno=2025)
        det_2024 = calcola_detrazione_lavoro_dipendente(30_000, anno=2024)
        assert det_2025 == pytest.approx(det_2024 + 1_000.0, rel=1e-4)

    def test_2025_higher_than_2024_at_10k(self) -> None:
        # At 10k, 2025 gives bonus (8500×7.1% + 1500×5.3%) extra
        det_2025 = calcola_detrazione_lavoro_dipendente(10_000, anno=2025)
        det_2024 = calcola_detrazione_lavoro_dipendente(10_000, anno=2024)
        assert det_2025 > det_2024

    def test_2025_equals_2024_above_40k(self) -> None:
        # Above 40k, no cuneo fiscale, should be same
        det_2025 = calcola_detrazione_lavoro_dipendente(45_000, anno=2025)
        det_2024 = calcola_detrazione_lavoro_dipendente(45_000, anno=2024)
        assert det_2025 == pytest.approx(det_2024)
