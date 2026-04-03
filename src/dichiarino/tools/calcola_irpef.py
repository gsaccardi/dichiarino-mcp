"""MCP tool: calcola_irpef."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.irpef import calcola_irpef_lorda


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_irpef(reddito_complessivo: float, anno: int = 2025) -> dict[str, Any]:
        """Calcola l'IRPEF lorda per un dato reddito complessivo e anno fiscale.

        Utilizza gli scaglioni ufficiali (2024-2025: 23%/35%/43% - riforma IRPEF L. 207/2024).
        Restituisce l'imposta totale e il dettaglio per scaglione.

        Args:
            reddito_complessivo: Reddito complessivo in euro (>= 0).
            anno: Anno di imposta. Supportati: 2023, 2024, 2025. Default: 2025.
        """
        try:
            risultato = calcola_irpef_lorda(reddito_complessivo, anno)
            return {
                "anno": risultato.anno,
                "reddito_complessivo": risultato.reddito_complessivo,
                "irpef_lorda": risultato.irpef_lorda,
                "breakdown_scaglioni": risultato.breakdown_scaglioni,
                "nota": (
                    f"IRPEF lorda calcolata con gli scaglioni {anno}. "
                    "Sottrarre le detrazioni spettanti per ottenere l'IRPEF netta."
                ),
            }
        except ValueError as e:
            return {"errore": str(e)}
