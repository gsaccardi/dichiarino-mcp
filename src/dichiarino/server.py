"""Dichiarino MCP Server - server setup and tool/resource registration."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

from dichiarino.resources import risorse
from dichiarino.tools import (
    analizza_cu,
    calcola_addizionale_regionale,
    calcola_detrazioni_familiari,
    calcola_detrazioni_lavoro,
    calcola_irpef,
    calcola_oneri,
    calcola_risultato,
    checklist_documenti,
    guida_quadro,
    valida_codice_fiscale,
)

_DESCRIPTION = """
Dichiarino - Il tuo assistente fiscale intelligente per il 730 precompilato 🇮🇹

Aiuta nella compilazione del Modello 730 precompilato attraverso:
- Calcolo IRPEF, detrazioni e addizionali regionali
- Validazione del codice fiscale
- Guida quadro per quadro
- Analisi della Certificazione Unica (CU)
- Verifica detraibilità delle spese
- Generazione checklist personalizzata

Anno fiscale supportato: 2023, 2024, 2025 (Modello 730/2024, 730/2025, 730/2026).
Nessun dato personale viene memorizzato o trasmesso.

⚠️ AVVISO IMPORTANTE: I calcoli e le informazioni fiscali forniti da questo
strumento hanno finalità esclusivamente informative e di supporto. Non
costituiscono consulenza fiscale o legale professionale. Prima di presentare
qualsiasi dichiarazione dei redditi, verifica sempre i valori con un
professionista qualificato (CAF, commercialista, consulente del lavoro) o
direttamente con l'Agenzia delle Entrate. Gli autori non si assumono alcuna
responsabilità per errori, omissioni o variazioni normative successive.
""".strip()


def create_server() -> FastMCP:
    """Create and configure the Dichiarino MCP server."""
    mcp = FastMCP("dichiarino", instructions=_DESCRIPTION)

    # Register tools
    calcola_irpef.register(mcp)
    calcola_detrazioni_lavoro.register(mcp)
    calcola_detrazioni_familiari.register(mcp)
    calcola_oneri.register(mcp)
    valida_codice_fiscale.register(mcp)
    calcola_risultato.register(mcp)
    guida_quadro.register(mcp)
    checklist_documenti.register(mcp)
    calcola_addizionale_regionale.register(mcp)
    analizza_cu.register(mcp)

    # Register resources
    risorse.register(mcp)

    return mcp
