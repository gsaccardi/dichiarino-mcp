"""MCP tool: valida_codice_fiscale."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.validators.codice_fiscale import valida_codice_fiscale


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def valida_codice_fiscale_tool(codice_fiscale: str) -> dict[str, Any]:
        """Valida un codice fiscale italiano e ne estrae i dati anagrafici codificati.

        Verifica: formato, lunghezza, carattere di controllo (16° carattere).
        Restituisce sesso, anno/mese/giorno di nascita (da codice) e codice comune.

        Args:
            codice_fiscale: Codice fiscale da validare (case-insensitive, spazi ignorati).
        """
        info = valida_codice_fiscale(codice_fiscale)
        result: dict[str, Any] = {
            "codice_fiscale": info.codice_fiscale,
            "valido": info.valido,
        }
        if not info.valido:
            result["errore"] = info.errore
        else:
            result["sesso"] = info.sesso
            result["anno_nascita_2cifre"] = info.anno_nascita
            result["mese_nascita"] = info.mese_nascita
            result["giorno_nascita"] = info.giorno_nascita
            result["codice_comune_belfiore"] = info.codice_comune
            result["nota"] = (
                "L'anno di nascita è espresso con 2 cifre (ambiguità di secolo). "
                "Il codice comune (Belfiore) identifica il Comune o lo Stato estero di nascita."
            )
        return result
