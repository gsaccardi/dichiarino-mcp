"""Integration tests: verify all tools and resources are reachable via the MCP server."""

from __future__ import annotations

import pytest

from dichiarino.server import create_server


@pytest.fixture
def mcp():  # type: ignore[no-untyped-def]
    return create_server()


class TestServerTools:
    def test_server_creates_without_error(self, mcp) -> None:  # type: ignore[no-untyped-def]
        assert mcp is not None
        assert mcp.name == "dichiarino"

    def test_all_expected_tools_registered(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tool_names = {t.name for t in mcp._tool_manager.list_tools()}
        expected = {
            "calcola_irpef",
            "calcola_detrazione_lavoro",
            "calcola_detrazioni_familiari_tool",
            "calcola_oneri",
            "verifica_spesa_detraibile",
            "valida_codice_fiscale_tool",
            "calcola_risultato_dichiarazione",
            "guida_quadro",
            "lista_documenti_spesa",
            "genera_checklist_730",
            "calcola_addizionale_regionale_tool",
            "analizza_certificazione_unica",
        }
        missing = expected - tool_names
        assert not missing, f"Missing tools: {missing}"

    def test_calcola_irpef_basic(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        tool = tools["calcola_irpef"]
        result = tool.fn(reddito_complessivo=30_000, anno=2024)
        assert "irpef_lorda" in result
        assert result["irpef_lorda"] > 0

    def test_calcola_irpef_negative_returns_error(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_irpef"].fn(reddito_complessivo=-100, anno=2024)
        assert "errore" in result

    def test_valida_cf_valid(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["valida_codice_fiscale_tool"].fn(codice_fiscale="RSSMRA85T10A562S")
        assert result["valido"] is True

    def test_valida_cf_invalid(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["valida_codice_fiscale_tool"].fn(codice_fiscale="INVALID000000000")
        assert result["valido"] is False

    def test_guida_quadro_c(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["guida_quadro"].fn(quadro="C")
        assert result["quadro"] == "C"
        assert "titolo" in result

    def test_guida_quadro_invalid(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["guida_quadro"].fn(quadro="Z")
        assert "errore" in result

    def test_calcola_risultato_rimborso(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        # 2025: reddito=30k, irpef_lorda≈7140, det_lavoro≈1801+1000(cuneo)=2801, irpef_netta≈4339
        result = tools["calcola_risultato_dichiarazione"].fn(
            reddito_complessivo=30_000,
            irpef_trattenuta=7_000,
            regione="lombardia",
            anno=2025,
        )
        assert "esito" in result
        assert result["saldo"] < 0
        assert result["esito"] == "RIMBORSO"

    def test_calcola_risultato_debito(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_risultato_dichiarazione"].fn(
            reddito_complessivo=30_000,
            irpef_trattenuta=100,
            regione="lombardia",
            anno=2024,
        )
        assert result["esito"] == "DEBITO"

    def test_genera_checklist(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["genera_checklist_730"].fn(
            ha_lavoro_dipendente=True,
            ha_immobili=True,
            ha_spese_sanitarie=True,
        )
        assert "quadri_da_compilare" in result
        assert "documenti_da_raccogliere" in result
        assert any("C" in q for q in result["quadri_da_compilare"])
        assert any("B" in q for q in result["quadri_da_compilare"])

    def test_addizionale_regionale_tool(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_addizionale_regionale_tool"].fn(
            reddito_complessivo=30_000, regione="lombardia"
        )
        assert "addizionale" in result
        assert float(result["addizionale"]) > 0

    def test_calcola_oneri_sanitarie(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_oneri"].fn(
            reddito_complessivo=30_000,
            spese=[{"tipo": "spese_sanitarie", "importo": 500}],
        )
        assert "totale_detrazione_irpef" in result
        # 500 - 129.11 = 370.89 × 19% ≈ 70.47
        assert float(result["totale_detrazione_irpef"]) == pytest.approx(
            (500 - 129.11) * 0.19, rel=1e-2
        )

    def test_verifica_spesa_detraibile(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["verifica_spesa_detraibile"].fn(tipo_spesa="mutuo_prima_casa")
        assert result["detraibile"] is True
        assert result["tetto_massimo"] == 4_000.0

    def test_analizza_cu_ok(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["analizza_certificazione_unica"].fn(
            reddito_lordo=30_000,
            imponibile_previdenziale=29_000,
            irpef_trattenuta=4_000,
            addizionale_regionale_trattenuta=500,
            addizionale_comunale_trattenuta=200,
            giorni_lavoro=365,
        )
        assert "stato" in result
        assert result["anomalie"] == []


class TestServerTools2025:
    def test_calcola_irpef_2025_same_brackets(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        r2024 = tools["calcola_irpef"].fn(reddito_complessivo=40_000, anno=2024)
        r2025 = tools["calcola_irpef"].fn(reddito_complessivo=40_000, anno=2025)
        assert r2024["irpef_lorda"] == r2025["irpef_lorda"]

    def test_calcola_detrazione_lavoro_2025_includes_cuneo(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_detrazione_lavoro"].fn(reddito_complessivo=30_000, anno=2025)
        assert "taglio_cuneo_fiscale_2025" in result
        assert result["taglio_cuneo_fiscale_2025"]["importo"] == pytest.approx(1_000.0)

    def test_calcola_detrazione_lavoro_2025_bonus_under_20k(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_detrazione_lavoro"].fn(reddito_complessivo=15_000, anno=2025)
        cuneo = result["taglio_cuneo_fiscale_2025"]
        assert cuneo["tipo"] == "bonus_busta_paga"
        assert cuneo["importo"] > 0

    def test_calcola_detrazione_lavoro_2024_no_cuneo(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_detrazione_lavoro"].fn(reddito_complessivo=30_000, anno=2024)
        assert "taglio_cuneo_fiscale_2025" not in result

    def test_default_anno_is_2025(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_irpef"].fn(reddito_complessivo=30_000)
        assert result["anno"] == 2025

    def test_calcola_oneri_2025_superbonus_65(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_oneri"].fn(
            reddito_complessivo=30_000,
            spese=[{"tipo": "superbonus", "importo": 96_000.0}],
            anno=2025,
        )
        assert result["totale_detrazione_irpef"] == pytest.approx(62_400.0, abs=0.01)

    def test_calcola_addizionale_2025_uses_own_data(self, mcp) -> None:  # type: ignore[no-untyped-def]
        tools = {t.name: t for t in mcp._tool_manager.list_tools()}
        result = tools["calcola_addizionale_regionale_tool"].fn(
            reddito_complessivo=30_000, regione="lombardia", anno=2025
        )
        assert result.get("aliquota") == pytest.approx(0.0173)
        assert float(result["addizionale"]) > 0
