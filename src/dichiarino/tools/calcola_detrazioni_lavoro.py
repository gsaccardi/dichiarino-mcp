"""MCP tool: calcola_detrazione_lavoro_dipendente."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.detrazioni_lavoro import (
    calcola_detrazione_lavoro_dipendente,
    calcola_solo_cuneo_fiscale_2025,
)
from dichiarino.types import TipoReddito


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_detrazione_lavoro(
        reddito_complessivo: float,
        giorni_lavoro: int = 365,
        tipo_reddito: str = "lavoro_dipendente",
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Calcola la detrazione per lavoro dipendente, pensione o redditi assimilati.

        Per il 2025 include automaticamente il taglio cuneo fiscale (L. 207/2024):
        - Reddito <= 20.000€: bonus graduato (7.1% / 5.3% / 4.8%)
        - Reddito 20.001-32.000€: ulteriore detrazione fissa di 1.000€
        - Reddito 32.001-40.000€: detrazione decrescente fino a 0 a 40.000€

        Args:
            reddito_complessivo: Reddito complessivo in euro.
            giorni_lavoro: Giorni di lavoro/pensione nell'anno (1-366). Default: 365.
            tipo_reddito: "lavoro_dipendente" | "pensione" | "lavoro_assimilato". Default: lavoro_dipendente.
            anno: Anno di imposta. Supportati: 2023, 2024, 2025. Default: 2025.
        """
        try:
            tipo = TipoReddito(tipo_reddito)
        except ValueError:
            return {
                "errore": (
                    f"Tipo reddito '{tipo_reddito}' non valido. "
                    "Valori ammessi: lavoro_dipendente, pensione, lavoro_assimilato."
                )
            }

        try:
            detrazione = calcola_detrazione_lavoro_dipendente(
                reddito_complessivo, giorni_lavoro, tipo, anno
            )
            bonus_65 = (
                tipo != TipoReddito.PENSIONE
                and anno in (2024, 2025)
                and 25_000 < reddito_complessivo <= 35_000
            )

            result: dict[str, Any] = {
                "reddito_complessivo": reddito_complessivo,
                "giorni_lavoro": giorni_lavoro,
                "tipo_reddito": tipo_reddito,
                "anno": anno,
                "detrazione_totale": detrazione,
                "include_bonus_65_euro": bonus_65,
            }

            if anno == 2025 and tipo != TipoReddito.PENSIONE:
                cuneo = calcola_solo_cuneo_fiscale_2025(reddito_complessivo, giorni_lavoro)
                result["taglio_cuneo_fiscale_2025"] = cuneo

            result["nota"] = (
                "Detrazione calcolata secondo art. 13 TUIR. "
                + ("Include taglio cuneo fiscale 2025 (L. 207/2024). " if anno == 2025 else "")
                + "Si applica a riduzione dell'IRPEF lorda."
            )
            return result
        except ValueError as e:
            return {"errore": str(e)}
