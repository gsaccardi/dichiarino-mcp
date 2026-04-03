"""Unit tests for addizionali regionali calculator."""

from __future__ import annotations

import pytest

from dichiarino.calculators.addizionali import calcola_addizionale_regionale
from dichiarino.types import RegioneItaliana


class TestAddizionaleRegionale:
    def test_lombardia(self) -> None:
        result = calcola_addizionale_regionale(30_000, RegioneItaliana.LOMBARDIA)
        expected = 30_000 * 0.0173
        assert float(result["addizionale"]) == pytest.approx(expected, rel=1e-4)

    def test_valle_d_aosta_lowest(self) -> None:
        result = calcola_addizionale_regionale(30_000, RegioneItaliana.VALLE_D_AOSTA)
        assert float(result["aliquota"]) == pytest.approx(0.007)

    def test_calabria_highest(self) -> None:
        result = calcola_addizionale_regionale(30_000, RegioneItaliana.CALABRIA)
        assert float(result["aliquota"]) == pytest.approx(0.023)

    def test_zero_income(self) -> None:
        result = calcola_addizionale_regionale(0.0, RegioneItaliana.LOMBARDIA)
        assert float(result["addizionale"]) == 0.0

    def test_exemption_threshold_basilicata(self) -> None:
        # Basilicata has exemption threshold of 12.000€
        below = calcola_addizionale_regionale(11_000, RegioneItaliana.BASILICATA)
        above = calcola_addizionale_regionale(20_000, RegioneItaliana.BASILICATA)
        assert float(below["addizionale"]) == 0.0
        assert float(above["addizionale"]) > 0.0

    def test_exemption_threshold_sardegna(self) -> None:
        below = calcola_addizionale_regionale(14_000, RegioneItaliana.SARDEGNA)
        assert float(below["addizionale"]) == 0.0

    def test_negative_income_raises(self) -> None:
        with pytest.raises(ValueError, match="negativo"):
            calcola_addizionale_regionale(-1, RegioneItaliana.LOMBARDIA)

    def test_unsupported_year_raises(self) -> None:
        with pytest.raises(ValueError, match="non ancora supportato"):
            calcola_addizionale_regionale(30_000, RegioneItaliana.LOMBARDIA, anno=2022)

    def test_result_contains_expected_keys(self) -> None:
        result = calcola_addizionale_regionale(30_000, RegioneItaliana.LAZIO)
        for key in ("regione", "aliquota", "soglia_esenzione", "imponibile", "addizionale", "note"):
            assert key in result

    def test_all_regions_covered(self) -> None:
        for regione in RegioneItaliana:
            result = calcola_addizionale_regionale(30_000, regione)
            assert float(result["addizionale"]) >= 0.0

    def test_anno_2025_uses_correct_data(self) -> None:
        result_2024 = calcola_addizionale_regionale(30_000, RegioneItaliana.LOMBARDIA, anno=2024)
        result_2025 = calcola_addizionale_regionale(30_000, RegioneItaliana.LOMBARDIA, anno=2025)
        # Rates are the same for 2025 Lombardia but data path is now independent
        assert result_2024["aliquota"] == result_2025["aliquota"]
        assert result_2025["addizionale"] == result_2024["addizionale"]

    def test_anno_2025_default(self) -> None:
        # Default anno should now be 2025
        result = calcola_addizionale_regionale(30_000, RegioneItaliana.LAZIO)
        assert result["aliquota"] == pytest.approx(0.0173)
