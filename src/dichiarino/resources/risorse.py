"""MCP resources for Dichiarino."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from dichiarino.data.addizionali_regionali import ADDIZIONALI_PER_ANNO
from dichiarino.data.aliquote_irpef import SCAGLIONI_PER_ANNO
from dichiarino.data.istruzioni_quadri import ISTRUZIONI_QUADRI
from dichiarino.data.limiti_detrazioni import LIMITI_PER_ANNO
from dichiarino.types import TipoSpesa


def register(mcp: FastMCP) -> None:
    @mcp.resource("dichiarino://aliquote/{anno}")
    def aliquote_irpef(anno: str) -> str:
        """Tabella scaglioni e aliquote IRPEF per l'anno fiscale specificato."""
        try:
            anno_int = int(anno)
        except ValueError:
            return f"Anno non valido: {anno}"
        scaglioni = SCAGLIONI_PER_ANNO.get(anno_int)
        if scaglioni is None:
            anni = sorted(SCAGLIONI_PER_ANNO.keys())
            return f"Anno {anno} non supportato. Anni disponibili: {anni}"
        lines = [f"## Scaglioni IRPEF {anno_int}\n"]
        for s in scaglioni:
            max_str = f"{s.max_reddito:,.0f}€" if s.max_reddito else "oltre"
            lines.append(f"- Da {s.min_reddito:,.0f}€ a {max_str}: **{s.aliquota * 100:.0f}%**")
        return "\n".join(lines)

    @mcp.resource("dichiarino://quadri/{nome}")
    def istruzioni_quadro(nome: str) -> str:
        """Istruzioni complete per la compilazione di un quadro del Modello 730."""
        quadro = nome.strip().upper()
        info = ISTRUZIONI_QUADRI.get(quadro)
        if info is None:
            disponibili = ", ".join(sorted(ISTRUZIONI_QUADRI.keys()))
            return f"Quadro '{quadro}' non trovato. Disponibili: {disponibili}"
        return (
            f"# Quadro {quadro} - {info['titolo']}\n\n"
            f"## Descrizione\n{info['descrizione']}\n\n"
            f"## Campi principali\n{info['campi_principali']}\n\n"
            f"## Note\n{info['note']}\n\n"
            f"## Documenti necessari\n{info['documenti_necessari']}"
        )

    @mcp.resource("dichiarino://scadenze/{anno}")
    def scadenze_730(anno: str) -> str:
        """Scadenze principali per la dichiarazione 730 dell'anno specificato."""
        try:
            anno_int = int(anno)
        except ValueError:
            return f"Anno non valido: {anno}"
        anno_dich = anno_int + 1  # declaration year is income year + 1
        return (
            f"## Scadenze Modello 730/{anno_dich} (redditi {anno_int})\n\n"
            f"| Data | Adempimento |\n"
            f"|------|-------------|\n"
            f"| 1° maggio {anno_dich} | Disponibilità 730 precompilato online |\n"
            f"| 31 maggio {anno_dich} | Termine per modifiche senza responsabilità del CAF |\n"
            f"| 30 giugno {anno_dich} | Termine consegna al sostituto d'imposta |\n"
            f"| 30 settembre {anno_dich} | **Scadenza invio 730** (diretto o tramite CAF) |\n"
            f"| 30 novembre {anno_dich} | Prima rata acconto IRPEF anno successivo |\n\n"
            f"ℹ️ Accedi al 730 precompilato: "
            f"https://www.agenziaentrate.gov.it/portale/la-dichiarazione-precompilata"
        )

    @mcp.resource("dichiarino://regioni")
    def addizionali_regionali() -> str:
        """Tabella addizionali regionali IRPEF per l'anno più recente disponibile."""
        anno_corrente = max(ADDIZIONALI_PER_ANNO.keys())
        aliquote_2025, _ = ADDIZIONALI_PER_ANNO[anno_corrente]
        lines = [f"## Addizionali Regionali IRPEF {anno_corrente}\n"]
        lines.append("| Regione | Aliquota |")
        lines.append("|---------|----------|")
        for regione, aliquota in sorted(aliquote_2025.items(), key=lambda x: x[0].value):
            lines.append(f"| {regione.value.replace('_', ' ').title()} | {aliquota * 100:.2f}% |")
        lines.append(
            "\n⚠️ Le aliquote sono indicative (base). Alcune regioni applicano aliquote progressive "
            "o esenzioni per redditi bassi. Verificare sempre con le tabelle ufficiali AdE."
        )
        return "\n".join(lines)

    @mcp.resource("dichiarino://detrazioni")
    def limiti_detrazioni() -> str:
        """Tabella limiti e aliquote per tutte le tipologie di detrazioni/deduzioni per l'anno più recente disponibile."""
        anno_corrente = max(LIMITI_PER_ANNO.keys())
        lines = [f"## Limiti Detrazioni e Deduzioni {anno_corrente} (Quadro E)\n"]
        lines.append("| Tipo Spesa | Aliquota | Tetto Max | Franchigia | Tipo |")
        lines.append("|-----------|----------|-----------|------------|------|")
        for tipo in TipoSpesa:
            limite = LIMITI_PER_ANNO[anno_corrente].get(tipo)
            if limite is None:
                continue
            tipo_str = "Deduzione" if limite.deducibile else "Detrazione"
            tetto = f"{limite.tetto_massimo:,.0f}€" if limite.tetto_massimo else "nessun limite"
            franchigia = f"{limite.franchigia:.2f}€" if limite.franchigia > 0 else "-"
            lines.append(
                f"| {tipo.value} | {limite.aliquota * 100:.0f}% | {tetto} | {franchigia} | {tipo_str} |"
            )
        return "\n".join(lines)
