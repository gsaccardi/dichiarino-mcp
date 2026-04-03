"""Unit tests for Quadro E oneri calculator."""

from __future__ import annotations

import pytest

from dichiarino.calculators.oneri import calcola_oneri_detraibili
from dichiarino.types import SpesaDetraibile, TipoSpesa


class TestOneriBase:
    def test_empty_spese(self) -> None:
        result = calcola_oneri_detraibili([], reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] == 0.0
        assert result["totale_deducibile"] == 0.0
        assert result["dettaglio"] == []

    def test_unsupported_year_raises(self) -> None:
        with pytest.raises(ValueError, match="non ancora supportato"):
            calcola_oneri_detraibili([], reddito_complessivo=30_000, anno=2000)


class TestSpeseSanitarie:
    def test_above_franchigia(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=1_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        # 1000 - 129.11 = 870.89; 870.89 * 0.19 = 165.4691 → 165.47
        assert result["totale_detrazione_irpef"] == pytest.approx(165.47, abs=0.01)

    def test_below_franchigia(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=100.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] == 0.0
        det = result["dettaglio"][0]
        assert det["detrazione"] == 0.0
        assert "franchigia" in det["note"].lower()

    def test_exactly_at_franchigia(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=129.11)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] == 0.0

    def test_multiple_sanitarie_aggregated(self) -> None:
        """Multiple medical expenses should be aggregated under a single franchigia."""
        spese = [
            SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=200.0),
            SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=300.0),
        ]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        # Total sanitarie = 500; 500 - 129.11 = 370.89; 370.89 * 0.19 = 70.4691 → 70.47
        assert result["totale_detrazione_irpef"] == pytest.approx(70.47, abs=0.01)
        # Only one detail entry for sanitarie (aggregated)
        sanitarie_entries = [
            d for d in result["dettaglio"] if d["tipo"] == TipoSpesa.SPESE_SANITARIE
        ]
        assert len(sanitarie_entries) == 1


class TestTettoMassimo:
    def test_spese_veterinarie_capped(self) -> None:
        """Veterinary expenses: tetto 550€, franchigia 129.11€."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_VETERINARIE, importo=1_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        # 1000 - 129.11 = 870.89; capped to min(870.89, 550) = 550; 550 * 0.19 = 104.50
        assert result["totale_detrazione_irpef"] == pytest.approx(104.50, abs=0.01)

    def test_mutuo_prima_casa_capped(self) -> None:
        """Mortgage: tetto 4000€, no franchigia."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=6_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        # Capped to 4000; 4000 * 0.19 = 760
        assert result["totale_detrazione_irpef"] == pytest.approx(760.0, abs=0.01)

    def test_mutuo_below_tetto(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=2_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] == pytest.approx(380.0, abs=0.01)


class TestDeducibile:
    def test_contributi_previdenziali_deducibili(self) -> None:
        """Previdenziali are deducibili (reduce income, not IRPEF)."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.CONTRIBUTI_PREVIDENZIALI, importo=3_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_deducibile"] == pytest.approx(3_000.0)
        assert result["totale_detrazione_irpef"] == 0.0

    def test_contributi_capped_at_tetto(self) -> None:
        """Previdenziali capped at 5164.57€."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.CONTRIBUTI_PREVIDENZIALI, importo=10_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_deducibile"] == pytest.approx(5_164.57, abs=0.01)


class TestNonStandardRates:
    def test_ristrutturazione_50_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.RISTRUTTURAZIONE, importo=20_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000, anno=2024)
        assert result["totale_detrazione_irpef"] == pytest.approx(10_000.0, abs=0.01)

    def test_risparmio_energetico_65_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.RISPARMIO_ENERGETICO, importo=10_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000, anno=2024)
        assert result["totale_detrazione_irpef"] == pytest.approx(6_500.0, abs=0.01)

    def test_erogazioni_onlus_30_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.EROGAZIONI_LIBERALI_ONLUS, importo=1_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] == pytest.approx(300.0, abs=0.01)


class TestHighIncomeCap:
    """The 260€ cap for redditi > 50.000€ applies only to 19% detrazioni, excluding sanitarie."""

    def test_cap_applies_to_19_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=4_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=60_000)
        # Mutuo: 4000 * 0.19 = 760; cap: 760 - 260 = 500
        assert result["totale_detrazione_irpef"] == pytest.approx(500.0, abs=0.01)

    def test_cap_does_not_apply_below_50k(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=4_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=49_000)
        assert result["totale_detrazione_irpef"] == pytest.approx(760.0, abs=0.01)

    def test_cap_excludes_sanitarie(self) -> None:
        """Only sanitarie: 260€ cap should NOT reduce the total."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=5_000.0)]
        result_high = calcola_oneri_detraibili(spese, reddito_complessivo=60_000)
        result_low = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        # Sanitarie are excluded from the cap, so both should be equal
        assert result_high["totale_detrazione_irpef"] == result_low["totale_detrazione_irpef"]

    def test_cap_does_not_affect_non_19_detrazioni(self) -> None:
        """50% ristrutturazione (2024) should NOT be reduced by the 260€ cap."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.RISTRUTTURAZIONE, importo=20_000.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=60_000, anno=2024)
        # No 19% non-sanitarie detrazioni → riduzione = 0
        assert result["totale_detrazione_irpef"] == pytest.approx(10_000.0, abs=0.01)

    def test_cap_mixed_spese(self) -> None:
        """Mix of 19% + non-19% (2024): cap only reduces the 19% portion."""
        spese = [
            SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=4_000.0),  # 19% → 760
            SpesaDetraibile(tipo=TipoSpesa.RISTRUTTURAZIONE, importo=20_000.0),  # 50% → 10000
        ]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=60_000, anno=2024)
        # Cap reduces only the 19% mutuo part: 760 - 260 = 500; total = 500 + 10000 = 10500
        assert result["totale_detrazione_irpef"] == pytest.approx(10_500.0, abs=0.01)

    def test_cap_limited_to_19_amount(self) -> None:
        """When 19% detrazioni < 260€, cap is limited to the 19% amount."""
        spese = [SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=500.0)]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=60_000)
        # Mutuo: 500 * 0.19 = 95; cap: min(260, 95) = 95; total = 95 - 95 = 0
        assert result["totale_detrazione_irpef"] == pytest.approx(0.0, abs=0.01)


class TestMultipleSpese:
    def test_mixed_detraibile_and_deducibile(self) -> None:
        spese = [
            SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=1_000.0),
            SpesaDetraibile(tipo=TipoSpesa.CONTRIBUTI_PREVIDENZIALI, importo=2_000.0),
        ]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert result["totale_detrazione_irpef"] > 0
        assert result["totale_deducibile"] == pytest.approx(2_000.0)

    def test_dettaglio_has_all_entries(self) -> None:
        spese = [
            SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=500.0),
            SpesaDetraibile(tipo=TipoSpesa.MUTUO_PRIMA_CASA, importo=2_000.0),
            SpesaDetraibile(tipo=TipoSpesa.CONTRIBUTI_PREVIDENZIALI, importo=1_000.0),
        ]
        result = calcola_oneri_detraibili(spese, reddito_complessivo=30_000)
        assert len(result["dettaglio"]) == 3


class TestOneri2025:
    def test_superbonus_2025_is_65_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SUPERBONUS, importo=96_000.0)]
        result_2024 = calcola_oneri_detraibili(spese, 30_000, anno=2024)
        result_2025 = calcola_oneri_detraibili(spese, 30_000, anno=2025)
        # 2024: 70% of 96k = 67200; 2025: 65% of 96k = 62400
        assert result_2024["totale_detrazione_irpef"] == pytest.approx(67_200.0, abs=0.01)
        assert result_2025["totale_detrazione_irpef"] == pytest.approx(62_400.0, abs=0.01)

    def test_ristrutturazione_2025_lower_rate_and_cap(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.RISTRUTTURAZIONE, importo=96_000.0)]
        result_2024 = calcola_oneri_detraibili(spese, 30_000, anno=2024)
        result_2025 = calcola_oneri_detraibili(spese, 30_000, anno=2025)
        # 2024: 50% of 96k = 48000; 2025: 36% of 48k = 17280
        assert result_2024["totale_detrazione_irpef"] == pytest.approx(48_000.0, abs=0.01)
        assert result_2025["totale_detrazione_irpef"] == pytest.approx(17_280.0, abs=0.01)

    def test_risparmio_energetico_2025_is_50_percent(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.RISPARMIO_ENERGETICO, importo=10_000.0)]
        result_2024 = calcola_oneri_detraibili(spese, 30_000, anno=2024)
        result_2025 = calcola_oneri_detraibili(spese, 30_000, anno=2025)
        # 2024: 65% of 10k = 6500; 2025: 50% of 10k = 5000
        assert result_2024["totale_detrazione_irpef"] == pytest.approx(6_500.0, abs=0.01)
        assert result_2025["totale_detrazione_irpef"] == pytest.approx(5_000.0, abs=0.01)

    def test_sanitarie_unchanged_2025(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SPESE_SANITARIE, importo=1_000.0)]
        result_2024 = calcola_oneri_detraibili(spese, 30_000, anno=2024)
        result_2025 = calcola_oneri_detraibili(spese, 30_000, anno=2025)
        assert result_2024["totale_detrazione_irpef"] == result_2025["totale_detrazione_irpef"]

    def test_default_anno_is_2025(self) -> None:
        spese = [SpesaDetraibile(tipo=TipoSpesa.SUPERBONUS, importo=96_000.0)]
        result = calcola_oneri_detraibili(spese, 30_000)
        # Default 2025: 65% of 96k
        assert result["totale_detrazione_irpef"] == pytest.approx(62_400.0, abs=0.01)
