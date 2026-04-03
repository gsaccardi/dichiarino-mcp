"""Unit tests for IRPEF calculator."""

from __future__ import annotations

import pytest

from dichiarino.calculators.irpef import calcola_irpef_lorda


class TestCalcolaIrpefLorda:
    def test_zero_income(self) -> None:
        result = calcola_irpef_lorda(0.0)
        assert result.irpef_lorda == 0.0
        assert result.breakdown_scaglioni == []

    def test_first_bracket_only(self) -> None:
        # 20.000€ → entirely in 23% bracket
        result = calcola_irpef_lorda(20_000)
        assert result.irpef_lorda == pytest.approx(4_600.0)
        assert len(result.breakdown_scaglioni) == 1
        assert result.breakdown_scaglioni[0]["aliquota"] == 0.23

    def test_at_first_bracket_boundary(self) -> None:
        result = calcola_irpef_lorda(28_000)
        expected = 28_000 * 0.23
        assert result.irpef_lorda == pytest.approx(expected)

    def test_second_bracket(self) -> None:
        # 40.000€: 28.000 × 23% + 12.000 × 35%
        result = calcola_irpef_lorda(40_000)
        expected = 28_000 * 0.23 + 12_000 * 0.35
        assert result.irpef_lorda == pytest.approx(expected, rel=1e-4)
        assert len(result.breakdown_scaglioni) == 2

    def test_third_bracket(self) -> None:
        # 60.000€: 28.000 × 23% + 22.000 × 35% + 10.000 × 43%
        result = calcola_irpef_lorda(60_000)
        expected = 28_000 * 0.23 + 22_000 * 0.35 + 10_000 * 0.43
        assert result.irpef_lorda == pytest.approx(expected, rel=1e-4)
        assert len(result.breakdown_scaglioni) == 3

    def test_at_50k_boundary(self) -> None:
        result = calcola_irpef_lorda(50_000)
        expected = 28_000 * 0.23 + 22_000 * 0.35
        assert result.irpef_lorda == pytest.approx(expected)

    def test_anno_2023(self) -> None:
        # 2023: 4 brackets. 20.000€: 15.000×23% + 5.000×25%
        result = calcola_irpef_lorda(20_000, anno=2023)
        expected = 15_000 * 0.23 + 5_000 * 0.25
        assert result.irpef_lorda == pytest.approx(expected)
        assert result.anno == 2023

    def test_negative_income_raises(self) -> None:
        with pytest.raises(ValueError, match="negativo"):
            calcola_irpef_lorda(-100)

    def test_unsupported_year_raises(self) -> None:
        with pytest.raises(ValueError, match="non supportato"):
            calcola_irpef_lorda(30_000, anno=2000)

    def test_breakdown_fields(self) -> None:
        result = calcola_irpef_lorda(40_000)
        for entry in result.breakdown_scaglioni:
            assert "min" in entry
            assert "max" in entry
            assert "aliquota" in entry
            assert "base_imponibile" in entry
            assert "imposta" in entry

    def test_anno_2025_same_brackets_as_2024(self) -> None:
        # 2025 brackets are identical to 2024
        result_2024 = calcola_irpef_lorda(40_000, anno=2024)
        result_2025 = calcola_irpef_lorda(40_000, anno=2025)
        assert result_2025.irpef_lorda == result_2024.irpef_lorda
        assert result_2025.anno == 2025
