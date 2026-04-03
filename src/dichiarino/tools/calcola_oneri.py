"""MCP tool: calcola_oneri (detraibili and deducibili - Quadro E)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.oneri import calcola_oneri_detraibili
from dichiarino.data.limiti_detrazioni import LIMITI_PER_ANNO
from dichiarino.types import SpesaDetraibile, TipoSpesa


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_oneri(
        reddito_complessivo: float,
        spese: list[dict[str, Any]],
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Calcola detrazioni e deduzioni per le spese del Quadro E (oneri e spese).

        Gestisce spese sanitarie (franchigia 129,11€), mutuo prima casa, ristrutturazioni,
        università, assicurazioni, contributi previdenziali, donazioni e molto altro.

        Per redditi > 50.000€ applica automaticamente la riduzione di 260€ sulle
        detrazioni al 19% (escluse le spese sanitarie).

        Args:
            reddito_complessivo: Reddito complessivo in euro.
            spese: Lista di spese. Ogni elemento è un dict con:
                - tipo: tipo di spesa (vedi valori ammessi)
                - importo: importo in euro
                - note: note opzionali (default "")
            anno: Anno di imposta. Default: 2024.

        Valori ammessi per tipo:
            spese_sanitarie, spese_veterinarie, mutuo_prima_casa, ristrutturazione,
            risparmio_energetico, istruzione_universita, istruzione_scuola,
            assicurazione_vita, assicurazione_infortuni, contributi_previdenziali,
            erogazioni_liberali_onlus, erogazioni_liberali_partiti, spese_funebri,
            canoni_affitto_studenti, bonus_mobili, superbonus
        """
        try:
            lista: list[SpesaDetraibile] = []
            for s in spese:
                lista.append(
                    SpesaDetraibile(
                        tipo=TipoSpesa(s["tipo"]),
                        importo=float(s["importo"]),
                        note=str(s.get("note", "")),
                    )
                )
            risultato = calcola_oneri_detraibili(lista, reddito_complessivo, anno)
            risultato["nota"] = (
                "Detrazioni calcolate secondo art. 15 e seguenti TUIR. "
                "Le spese sanitarie hanno una franchigia di 129,11€. "
                "I contributi previdenziali sono dedotti dal reddito imponibile."
            )
            return risultato
        except (ValueError, KeyError) as e:
            return {
                "errore": str(e),
                "tipi_ammessi": [t.value for t in TipoSpesa],
            }

    @mcp.tool()
    def verifica_spesa_detraibile(tipo_spesa: str) -> dict[str, Any]:
        """Verifica se una spesa è detraibile/deducibile e con quali regole.

        Args:
            tipo_spesa: Tipo di spesa da verificare (es. "spese_sanitarie").
        """
        try:
            tipo = TipoSpesa(tipo_spesa)
        except ValueError:
            return {
                "detraibile": False,
                "errore": f"Tipo spesa '{tipo_spesa}' non riconosciuto.",
                "tipi_ammessi": [t.value for t in TipoSpesa],
            }

        limite = LIMITI_PER_ANNO[max(LIMITI_PER_ANNO.keys())].get(tipo)
        if limite is None:
            return {"detraibile": False, "nota": "Nessuna detrazione disponibile per questo tipo."}
        return {
            "tipo": tipo_spesa,
            "detraibile": not limite.deducibile,
            "deducibile": limite.deducibile,
            "aliquota_detrazione": limite.aliquota if not limite.deducibile else None,
            "tetto_massimo": limite.tetto_massimo,
            "franchigia": limite.franchigia if limite.franchigia > 0 else None,
            "note": limite.note,
        }
