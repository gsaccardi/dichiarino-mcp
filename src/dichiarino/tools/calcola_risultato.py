"""MCP tool: calcola_risultato_dichiarazione (rimborso / debito)."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.calculators.addizionali import calcola_addizionale_regionale
from dichiarino.calculators.detrazioni_familiari import calcola_detrazioni_familiari
from dichiarino.calculators.detrazioni_lavoro import calcola_detrazione_lavoro_dipendente
from dichiarino.calculators.irpef import calcola_irpef_lorda
from dichiarino.calculators.oneri import calcola_oneri_detraibili
from dichiarino.types import (
    FamiliareACarico,
    RegioneItaliana,
    RisultatoDichiarazione,
    SpesaDetraibile,
    TipoFamiliare,
    TipoReddito,
    TipoSpesa,
)


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def calcola_risultato_dichiarazione(
        reddito_complessivo: float,
        irpef_trattenuta: float,
        giorni_lavoro: int = 365,
        tipo_reddito: str = "lavoro_dipendente",
        regione: str = "lombardia",
        familiari: list[dict[str, Any]] | None = None,
        spese: list[dict[str, Any]] | None = None,
        oneri_deducibili_totale: float = 0.0,
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Calcola il risultato finale della dichiarazione 730: rimborso o debito IRPEF.

        Combina IRPEF lorda, tutte le detrazioni spettanti e le ritenute già versate
        per determinare se il contribuente riceverà un rimborso o dovrà pagare un saldo.

        Args:
            reddito_complessivo: Reddito complessivo in euro.
            irpef_trattenuta: IRPEF già trattenuta dal sostituto d'imposta (da CU).
            giorni_lavoro: Giorni di lavoro nell'anno (default 365).
            tipo_reddito: "lavoro_dipendente" | "pensione" | "lavoro_assimilato".
            regione: Regione di residenza (es. "lombardia"). Default: "lombardia".
            familiari: Lista familiari a carico (vedi calcola_detrazioni_familiari).
            spese: Lista spese Quadro E (vedi calcola_oneri).
            oneri_deducibili_totale: Totale oneri già deducibili (riduce reddito imponibile).
            anno: Anno di imposta. Default: 2024.
        """
        try:
            tipo = TipoReddito(tipo_reddito)
            reg = RegioneItaliana(regione)
        except ValueError as e:
            return {"errore": str(e)}

        try:
            # Adjust reddito for deductions that reduce taxable base
            reddito_imponibile = max(0.0, reddito_complessivo - oneri_deducibili_totale)

            irpef_res = calcola_irpef_lorda(reddito_imponibile, anno)
            irpef_lorda = irpef_res.irpef_lorda

            det_lavoro = calcola_detrazione_lavoro_dipendente(
                reddito_imponibile, giorni_lavoro, tipo, anno
            )

            familiari_list: list[FamiliareACarico] = []
            if familiari:
                for f in familiari:
                    familiari_list.append(
                        FamiliareACarico(
                            tipo=TipoFamiliare(f.get("tipo", "altro")),
                            mesi_a_carico=int(f.get("mesi_a_carico", 12)),
                            percentuale_carico=float(f.get("percentuale_carico", 1.0)),
                            eta_inferiore_21=bool(f.get("eta_inferiore_21", False)),
                        )
                    )
            det_familiari_res = calcola_detrazioni_familiari(
                familiari_list, reddito_imponibile, anno
            )
            det_familiari = float(det_familiari_res["totale"])

            spese_list: list[SpesaDetraibile] = []
            if spese:
                for s in spese:
                    spese_list.append(
                        SpesaDetraibile(tipo=TipoSpesa(s["tipo"]), importo=float(s["importo"]))
                    )
            oneri_res = calcola_oneri_detraibili(spese_list, reddito_imponibile, anno)
            det_oneri = oneri_res["totale_detrazione_irpef"]

            irpef_netta = max(0.0, irpef_lorda - det_lavoro - det_familiari - float(det_oneri))

            addizionale_res = calcola_addizionale_regionale(reddito_imponibile, reg, anno)
            addizionale_regionale = float(addizionale_res["addizionale"])

            # saldo: positive = debito (you owe), negative = rimborso (you get back)
            saldo = round(irpef_netta - irpef_trattenuta, 2)

            risultato = RisultatoDichiarazione(
                irpef_lorda=irpef_lorda,
                detrazione_lavoro=det_lavoro,
                detrazioni_familiari=float(det_familiari),
                detrazioni_oneri=float(det_oneri),
                oneri_deducibili=oneri_deducibili_totale,
                addizionale_regionale=addizionale_regionale,
                irpef_netta=irpef_netta,
                irpef_trattenuta=irpef_trattenuta,
                saldo=saldo,
                anno=anno,
            )

            esito = "RIMBORSO" if saldo < 0 else ("DEBITO" if saldo > 0 else "PAREGGIO")

            return {
                "anno": risultato.anno,
                "reddito_complessivo": reddito_complessivo,
                "reddito_imponibile": round(reddito_imponibile, 2),
                "irpef_lorda": risultato.irpef_lorda,
                "detrazione_lavoro": risultato.detrazione_lavoro,
                "detrazioni_familiari": risultato.detrazioni_familiari,
                "detrazioni_oneri": risultato.detrazioni_oneri,
                "irpef_netta": risultato.irpef_netta,
                "addizionale_regionale": risultato.addizionale_regionale,
                "irpef_trattenuta": risultato.irpef_trattenuta,
                "saldo": risultato.saldo,
                "esito": esito,
                "nota": (
                    f"Saldo {esito}: "
                    + (
                        f"rimborso di {abs(saldo):.2f}€"
                        if saldo < 0
                        else f"debito di {saldo:.2f}€"
                        if saldo > 0
                        else "nessun rimborso né debito"
                    )
                    + ". L'addizionale regionale è separata e non inclusa nel saldo IRPEF principale."
                ),
            }
        except (ValueError, KeyError) as e:
            return {"errore": str(e)}
