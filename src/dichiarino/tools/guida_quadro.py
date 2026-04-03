"""MCP tool: guida_quadro."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.data.istruzioni_quadri import ISTRUZIONI_QUADRI


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def guida_quadro(quadro: str) -> dict[str, Any]:
        """Fornisce una guida dettagliata per la compilazione di un quadro del Modello 730.

        Spiega cosa va dichiarato, i campi principali, le note importanti e i documenti
        necessari per ogni sezione del modello.

        Args:
            quadro: Lettera del quadro (es. "A", "B", "C", "E", "M", "T", "W").
                    Case-insensitive.

        Quadri disponibili: A, B, C, D, E, F, G, I, K, L, M, T, W
        """
        quadro = quadro.strip().upper()
        istruzioni = ISTRUZIONI_QUADRI.get(quadro)
        if istruzioni is None:
            return {
                "errore": f"Quadro '{quadro}' non trovato.",
                "quadri_disponibili": sorted(ISTRUZIONI_QUADRI.keys()),
            }
        return {
            "quadro": quadro,
            **istruzioni,
        }
