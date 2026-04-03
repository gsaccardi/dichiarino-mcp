"""MCP tool: calcola_addizionale_regionale."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.addizionali import calcola_addizionale_regionale
from dichiarino.types import RegioneItaliana


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_addizionale_regionale_tool(
        reddito_complessivo: float,
        regione: str,
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Calcola l'addizionale regionale IRPEF per una specifica regione.

        L'addizionale regionale è un'imposta separata dall'IRPEF, trattenuta dal
        sostituto d'imposta e conguagliata nella dichiarazione.

        Args:
            reddito_complessivo: Reddito complessivo in euro.
            regione: Nome della regione (es. "lombardia", "lazio", "campania").
            anno: Anno di imposta. Default: 2024.

        Regioni disponibili:
            abruzzo, basilicata, calabria, campania, emilia_romagna,
            friuli_venezia_giulia, lazio, liguria, lombardia, marche, molise,
            piemonte, puglia, sardegna, sicilia, toscana, trentino_alto_adige,
            umbria, valle_d_aosta, veneto
        """
        try:
            reg = RegioneItaliana(regione.lower())
        except ValueError:
            return {
                "errore": f"Regione '{regione}' non riconosciuta.",
                "regioni_disponibili": [r.value for r in RegioneItaliana],
            }
        try:
            return calcola_addizionale_regionale(reddito_complessivo, reg, anno)
        except ValueError as e:
            return {"errore": str(e)}
