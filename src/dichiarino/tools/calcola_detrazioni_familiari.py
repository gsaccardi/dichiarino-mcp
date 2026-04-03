"""MCP tool: calcola_detrazioni_familiari."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.detrazioni_familiari import calcola_detrazioni_familiari
from dichiarino.types import FamiliareACarico, TipoFamiliare


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_detrazioni_familiari_tool(
        reddito_complessivo: float,
        familiari: list[dict[str, Any]],
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Calcola le detrazioni per carichi di famiglia (coniuge, figli ≥21, altri).

        ATTENZIONE: Dal 2022 le detrazioni per figli UNDER 21 sono state abolite
        e sostituite dall'Assegno Unico Universale (AUU). Questa funzione le esclude.

        Args:
            reddito_complessivo: Reddito complessivo del dichiarante in euro.
            familiari: Lista di familiari a carico. Ogni elemento è un dict con:
                - tipo: "coniuge" | "figlio" | "altro"
                - mesi_a_carico: mesi di carico nell'anno (1-12, default 12)
                - percentuale_carico: quota di carico (0.5 o 1.0, default 1.0)
                - eta_inferiore_21: true se figlio under 21 (default false)
            anno: Anno di imposta. Default: 2024.

        Esempi familiari:
            [{"tipo": "coniuge"}, {"tipo": "figlio", "eta_inferiore_21": false}]
        """
        try:
            lista: list[FamiliareACarico] = []
            for f in familiari:
                lista.append(
                    FamiliareACarico(
                        tipo=TipoFamiliare(f.get("tipo", "altro")),
                        mesi_a_carico=int(f.get("mesi_a_carico", 12)),
                        percentuale_carico=float(f.get("percentuale_carico", 1.0)),
                        eta_inferiore_21=bool(f.get("eta_inferiore_21", False)),
                    )
                )
            risultato = calcola_detrazioni_familiari(lista, reddito_complessivo, anno)
            risultato["nota"] = (
                "Detrazioni calcolate secondo art. 12 TUIR. "
                "I figli under 21 non generano detrazione (coperti da Assegno Unico Universale)."
            )
            return risultato
        except (ValueError, KeyError) as e:
            return {"errore": str(e)}
