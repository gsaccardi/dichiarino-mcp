"""Unit tests for detrazioni familiari calculator."""

from __future__ import annotations

import pytest

from dichiarino.calculators.detrazioni_familiari import calcola_detrazioni_familiari
from dichiarino.types import FamiliareACarico, TipoFamiliare


class TestDetrazioniFamiliari:
    def test_no_familiari(self) -> None:
        result = calcola_detrazioni_familiari([], 30_000)
        assert result["totale"] == 0.0

    def test_coniuge_reddito_basso(self) -> None:
        familiari = [FamiliareACarico(tipo=TipoFamiliare.CONIUGE)]
        result = calcola_detrazioni_familiari(familiari, 10_000)
        assert result["detrazione_coniuge"] == pytest.approx(800.0, rel=1e-4)

    def test_coniuge_reddito_alto(self) -> None:
        familiari = [FamiliareACarico(tipo=TipoFamiliare.CONIUGE)]
        result = calcola_detrazioni_familiari(familiari, 90_000)
        assert result["detrazione_coniuge"] == 0.0

    def test_figlio_under_21_excluded(self) -> None:
        familiari = [FamiliareACarico(tipo=TipoFamiliare.FIGLIO, eta_inferiore_21=True)]
        result = calcola_detrazioni_familiari(familiari, 30_000)
        assert result["detrazione_figli"] == 0.0
        assert result["totale"] == 0.0

    def test_figlio_over_21(self) -> None:
        familiari = [FamiliareACarico(tipo=TipoFamiliare.FIGLIO, eta_inferiore_21=False)]
        result = calcola_detrazioni_familiari(familiari, 30_000)
        expected = 950.0 * ((80_000 - 30_000) / 80_000)
        assert result["detrazione_figli"] == pytest.approx(expected, rel=1e-4)

    def test_altro_familiare(self) -> None:
        familiari = [FamiliareACarico(tipo=TipoFamiliare.ALTRO)]
        result = calcola_detrazioni_familiari(familiari, 20_000)
        expected = 750.0 * ((80_000 - 20_000) / 80_000)
        assert result["detrazione_altri"] == pytest.approx(expected, rel=1e-4)

    def test_partial_months(self) -> None:
        fam_6m = FamiliareACarico(tipo=TipoFamiliare.CONIUGE, mesi_a_carico=6)
        fam_12m = FamiliareACarico(tipo=TipoFamiliare.CONIUGE, mesi_a_carico=12)
        result_6 = calcola_detrazioni_familiari([fam_6m], 10_000)
        result_12 = calcola_detrazioni_familiari([fam_12m], 10_000)
        assert result_6["totale"] == pytest.approx(result_12["totale"] * 0.5, rel=1e-4)

    def test_shared_carico_50_percent(self) -> None:
        fam_50 = FamiliareACarico(tipo=TipoFamiliare.CONIUGE, percentuale_carico=0.5)
        fam_100 = FamiliareACarico(tipo=TipoFamiliare.CONIUGE, percentuale_carico=1.0)
        result_50 = calcola_detrazioni_familiari([fam_50], 10_000)
        result_100 = calcola_detrazioni_familiari([fam_100], 10_000)
        assert result_50["totale"] == pytest.approx(result_100["totale"] * 0.5, rel=1e-4)

    def test_multiple_familiari(self) -> None:
        familiari = [
            FamiliareACarico(tipo=TipoFamiliare.CONIUGE),
            FamiliareACarico(tipo=TipoFamiliare.FIGLIO, eta_inferiore_21=False),
        ]
        result = calcola_detrazioni_familiari(familiari, 30_000)
        assert result["detrazione_coniuge"] > 0
        assert result["detrazione_figli"] > 0

    def test_negative_income_raises(self) -> None:
        with pytest.raises(ValueError, match="negativo"):
            calcola_detrazioni_familiari([], -1)

    def test_unsupported_year_raises(self) -> None:
        with pytest.raises(ValueError, match="non ancora supportato"):
            calcola_detrazioni_familiari([], 30_000, anno=2022)

    def test_anno_2025_same_rules_as_2024(self) -> None:
        # Family deduction rules unchanged between 2024 and 2025
        familiari = [FamiliareACarico(tipo=TipoFamiliare.CONIUGE)]
        result_2024 = calcola_detrazioni_familiari(familiari, 30_000, anno=2024)
        result_2025 = calcola_detrazioni_familiari(familiari, 30_000, anno=2025)
        assert result_2024["totale"] == result_2025["totale"]

    def test_anno_2025_default(self) -> None:
        # Default anno should be 2025
        familiari = [FamiliareACarico(tipo=TipoFamiliare.CONIUGE)]
        result = calcola_detrazioni_familiari(familiari, 30_000)
        assert float(result["totale"]) > 0
