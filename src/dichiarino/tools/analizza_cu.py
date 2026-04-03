"""MCP tool: analizza_certificazione_unica."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.detrazioni_lavoro import calcola_detrazione_lavoro_dipendente
from dichiarino.calculators.irpef import calcola_irpef_lorda
from dichiarino.types import DatiCertificazioneUnica, TipoReddito


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def analizza_certificazione_unica(
        reddito_lordo: float,
        imponibile_previdenziale: float,
        irpef_trattenuta: float,
        addizionale_regionale_trattenuta: float,
        addizionale_comunale_trattenuta: float,
        giorni_lavoro: int,
        tipo_reddito: str = "lavoro_dipendente",
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Analizza i dati della Certificazione Unica (CU) e rileva eventuali anomalie.

        Verifica la coerenza interna dei dati CU: controlla se l'IRPEF trattenuta
        è plausibile rispetto al reddito dichiarato, e se i giorni di lavoro
        sono nel range corretto.

        Args:
            reddito_lordo: Reddito lordo (punto 1 CU).
            imponibile_previdenziale: Imponibile previdenziale (punto 6 CU).
            irpef_trattenuta: IRPEF trattenuta (punto 21 CU).
            addizionale_regionale_trattenuta: Addizionale regionale trattenuta (punto 22 CU).
            addizionale_comunale_trattenuta: Addizionale comunale (punti 23+24 CU).
            giorni_lavoro: Giorni di lavoro/pensione nell'anno (punto 5 CU).
            tipo_reddito: "lavoro_dipendente" | "pensione" | "lavoro_assimilato".
            anno: Anno di imposta. Default: 2024.
        """
        anomalie: list[str] = []
        avvisi: list[str] = []

        try:
            tipo = TipoReddito(tipo_reddito)
        except ValueError:
            return {"errore": f"Tipo reddito '{tipo_reddito}' non valido."}

        cu = DatiCertificazioneUnica(
            reddito_lordo=reddito_lordo,
            imponibile_previdenziale=imponibile_previdenziale,
            irpef_trattenuta=irpef_trattenuta,
            addizionale_regionale_trattenuta=addizionale_regionale_trattenuta,
            addizionale_comunale_trattenuta=addizionale_comunale_trattenuta,
            giorni_lavoro=giorni_lavoro,
            tipo_reddito=tipo,
        )

        # Validate days
        if not 1 <= cu.giorni_lavoro <= 366:
            anomalie.append(f"Giorni di lavoro non validi: {cu.giorni_lavoro} (attesi 1-366).")

        # Cross-check: imponibile previdenziale should be <= reddito lordo
        if cu.imponibile_previdenziale > cu.reddito_lordo * 1.05:
            anomalie.append(
                "L'imponibile previdenziale supera significativamente il reddito lordo. "
                "Verificare i dati CU."
            )

        # Plausibility check on IRPEF: compute expected and compare
        try:
            irpef_attesa_res = calcola_irpef_lorda(cu.reddito_lordo, anno)
            det_lavoro = calcola_detrazione_lavoro_dipendente(
                cu.reddito_lordo, cu.giorni_lavoro, tipo, anno
            )
        except ValueError as e:
            return {"errore": str(e)}
        irpef_netta_attesa = max(0.0, irpef_attesa_res.irpef_lorda - det_lavoro)

        # Allow ±20% tolerance (employer may have partial year, other income, etc.)
        if irpef_netta_attesa > 0:
            scarto = abs(cu.irpef_trattenuta - irpef_netta_attesa) / irpef_netta_attesa
            if scarto > 0.30:
                avvisi.append(
                    f"L'IRPEF trattenuta ({cu.irpef_trattenuta:.2f}€) differisce "
                    f"del {scarto * 100:.0f}% dall'IRPEF netta stimata "
                    f"({irpef_netta_attesa:.2f}€). Verificare se ci sono altri redditi "
                    f"o detrazioni particolari."
                )

        if cu.irpef_trattenuta < 0:
            anomalie.append("L'IRPEF trattenuta non può essere negativa.")

        return {
            "dati_cu": {
                "reddito_lordo": cu.reddito_lordo,
                "imponibile_previdenziale": cu.imponibile_previdenziale,
                "irpef_trattenuta": cu.irpef_trattenuta,
                "addizionale_regionale_trattenuta": cu.addizionale_regionale_trattenuta,
                "addizionale_comunale_trattenuta": cu.addizionale_comunale_trattenuta,
                "giorni_lavoro": cu.giorni_lavoro,
                "tipo_reddito": tipo_reddito,
            },
            "stima_irpef_netta": round(irpef_netta_attesa, 2),
            "stima_irpef_lorda": irpef_attesa_res.irpef_lorda,
            "stima_detrazione_lavoro": round(det_lavoro, 2),
            "anomalie": anomalie,
            "avvisi": avvisi,
            "stato": "OK" if not anomalie else "ANOMALIE_RILEVATE",
            "nota": (
                f"Analisi di plausibilità basata su IRPEF {anno} e detrazione lavoro dipendente. "
                "La stima non considera altri redditi o detrazioni specifiche."
            ),
        }
