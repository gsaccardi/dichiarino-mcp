"""MCP tool: lista_documenti and genera_checklist."""

from __future__ import annotations

from typing import Any

from mcp.server.fastmcp import FastMCP

from dichiarino.data.limiti_detrazioni import LIMITI_PER_ANNO
from dichiarino.types import TipoSpesa

_DOCUMENTI_PER_SPESA: dict[str, list[str]] = {
    TipoSpesa.SPESE_SANITARIE.value: [
        "Fatture/ricevute fiscali del medico o struttura sanitaria",
        "Scontrini farmacia (fiscali, con codice fiscale)",
        "Fatture dispositivi medici (con marcatura CE)",
        "Certificato medico per spese di assistenza specifica",
    ],
    TipoSpesa.SPESE_VETERINARIE.value: [
        "Fatture veterinario",
        "Scontrini farmacia veterinaria",
    ],
    TipoSpesa.MUTUO_PRIMA_CASA.value: [
        "Contratto di mutuo ipotecario",
        "Quietanza di pagamento degli interessi passivi (rilasciata dalla banca)",
        "Atto di acquisto dell'immobile",
        "Dichiarazione della banca sugli interessi passivi pagati nell'anno",
    ],
    TipoSpesa.RISTRUTTURAZIONE.value: [
        "Fatture dei lavori (intestate al contribuente)",
        "Bonifico bancario 'parlante' per ristrutturazioni (con codice fiscale e partita IVA ditta)",
        "Comunicazione inizio lavori (per lavori > 51.645€)",
        "Asseverazione tecnica (se richiesta)",
        "Visura catastale dell'immobile",
    ],
    TipoSpesa.RISPARMIO_ENERGETICO.value: [
        "Fatture dei lavori",
        "Bonifico bancario 'parlante'",
        "Asseverazione tecnica del professionista",
        "Attestato di Prestazione Energetica (APE) prima e dopo i lavori",
        "Comunicazione all'ENEA entro 90 giorni dal fine lavori",
    ],
    TipoSpesa.ISTRUZIONE_UNIVERSITA.value: [
        "Ricevute pagamento tasse universitarie",
        "Certificato di iscrizione all'università",
        "Per università private: confronto con tasse ateneo statale della stessa area",
    ],
    TipoSpesa.ISTRUZIONE_SCUOLA.value: [
        "Ricevute pagamento rette/mense/gite scolastiche",
        "Fatture per libri di testo (se detraibili)",
        "Dichiarazione della scuola",
    ],
    TipoSpesa.ASSICURAZIONE_VITA.value: [
        "Quietanza di pagamento del premio assicurativo",
        "Polizza assicurativa (per verifica tipologia)",
    ],
    TipoSpesa.CONTRIBUTI_PREVIDENZIALI.value: [
        "Ricevute versamento contributi (es. F24, bollettini INPS)",
        "CU del datore (se trattenuti in busta paga)",
        "Estratto conto previdenziale INPS",
    ],
    TipoSpesa.EROGAZIONI_LIBERALI_ONLUS.value: [
        "Ricevuta della donazione rilasciata dall'ente beneficiario",
        "Estratto conto bancario / bonifico",
        "Codice fiscale dell'ente beneficiario",
    ],
    TipoSpesa.EROGAZIONI_LIBERALI_PARTITI.value: [
        "Ricevuta della donazione rilasciata dal partito",
        "Estratto conto bancario (le donazioni devono avvenire tramite banca/posta)",
    ],
    TipoSpesa.SPESE_FUNEBRI.value: [
        "Fattura dell'agenzia funebre",
        "Documento che attesta il decesso del familiare",
    ],
    TipoSpesa.CANONI_AFFITTO_STUDENTI.value: [
        "Contratto di affitto intestato allo studente",
        "Ricevute di pagamento del canone",
        "Certificato di iscrizione all'università",
        "Prova della distanza > 100km dalla residenza",
    ],
    TipoSpesa.BONUS_MOBILI.value: [
        "Fatture acquisto mobili/elettrodomestici (classe A+ o superiore)",
        "Estratto conto / bonifico bancario",
        "Documentazione ristrutturazione collegata",
    ],
    TipoSpesa.SUPERBONUS.value: [
        "Fatture dei lavori trainanti e trainati",
        "Bonifico bancario 'parlante'",
        "Asseverazione tecnica del progettista abilitato",
        "Visto di conformità del CAF/professionista",
        "APE pre e post intervento",
        "Comunicazione ENEA",
    ],
}


def register(mcp: FastMCP) -> None:
    @mcp.tool()
    def lista_documenti_spesa(tipo_spesa: str) -> dict[str, Any]:
        """Restituisce la lista dei documenti necessari per una specifica tipologia di spesa.

        Utile per preparare la documentazione prima di recarsi al CAF o compilare il 730.

        Args:
            tipo_spesa: Tipo di spesa (es. "spese_sanitarie", "mutuo_prima_casa").

        Valori ammessi: spese_sanitarie, spese_veterinarie, mutuo_prima_casa,
            ristrutturazione, risparmio_energetico, istruzione_universita, istruzione_scuola,
            assicurazione_vita, contributi_previdenziali, erogazioni_liberali_onlus,
            erogazioni_liberali_partiti, spese_funebri, canoni_affitto_studenti,
            bonus_mobili, superbonus
        """
        documenti = _DOCUMENTI_PER_SPESA.get(tipo_spesa)
        if documenti is None:
            return {
                "errore": f"Tipo spesa '{tipo_spesa}' non riconosciuto.",
                "tipi_ammessi": list(_DOCUMENTI_PER_SPESA.keys()),
            }
        limite = LIMITI_PER_ANNO[max(LIMITI_PER_ANNO.keys())].get(TipoSpesa(tipo_spesa))
        return {
            "tipo_spesa": tipo_spesa,
            "documenti_necessari": documenti,
            "regole": limite.note if limite else "",
        }

    @mcp.tool()
    def genera_checklist_730(
        ha_lavoro_dipendente: bool = True,
        ha_pensione: bool = False,
        ha_immobili: bool = False,
        ha_terreni: bool = False,
        ha_coniuge_a_carico: bool = False,
        ha_figli_under_21: bool = False,
        ha_figli_over_21_a_carico: bool = False,
        ha_spese_sanitarie: bool = False,
        ha_mutuo_prima_casa: bool = False,
        ha_ristrutturazione: bool = False,
        ha_investimenti_esteri: bool = False,
        ha_criptovalute: bool = False,
        ha_locazioni_brevi: bool = False,
        ha_plusvalenze_finanziarie: bool = False,
        anno: int = 2025,
    ) -> dict[str, Any]:
        """Genera una checklist personalizzata per la compilazione del 730.

        Basandosi sulla situazione del contribuente, indica quali quadri compilare,
        quali documenti raccogliere e quali scadenze rispettare.

        Args:
            ha_lavoro_dipendente: Ha redditi da lavoro dipendente.
            ha_pensione: Ha redditi da pensione.
            ha_immobili: Possiede fabbricati/immobili (inclusa abitazione principale).
            ha_terreni: Possiede terreni.
            ha_coniuge_a_carico: Ha coniuge fiscalmente a carico.
            ha_figli_under_21: Ha figli under 21 (coperti da Assegno Unico, non detraibili).
            ha_figli_over_21_a_carico: Ha figli ≥21 anni fiscalmente a carico.
            ha_spese_sanitarie: Ha spese mediche da detrarre.
            ha_mutuo_prima_casa: Ha mutuo per prima casa (interessi detraibili).
            ha_ristrutturazione: Ha effettuato lavori di ristrutturazione.
            ha_investimenti_esteri: Ha conti o investimenti all'estero.
            ha_criptovalute: Possiede criptovalute/cripto-attività.
            ha_locazioni_brevi: Ha affittato immobili per brevi periodi (Airbnb, ecc.).
            ha_plusvalenze_finanziarie: Ha ceduto titoli/partecipazioni nell'anno.
            anno: Anno di imposta. Default: 2024.
        """
        quadri_necessari: list[str] = ["Frontespizio"]
        documenti: list[str] = ["Documento di identità", "Codice fiscale"]
        avvisi: list[str] = []

        if ha_lavoro_dipendente or ha_pensione:
            quadri_necessari.append("Quadro C - Redditi da lavoro dipendente/pensione")
            documenti.append("Certificazione Unica (CU) del datore di lavoro / INPS")

        if ha_immobili:
            quadri_necessari.append("Quadro B - Redditi dei fabbricati")
            documenti.extend(
                ["Visura catastale degli immobili", "Contratti di locazione (se presenti)"]
            )

        if ha_terreni:
            quadri_necessari.append("Quadro A - Redditi dei terreni")
            documenti.append("Visura catastale dei terreni")

        if ha_coniuge_a_carico or ha_figli_over_21_a_carico:
            quadri_necessari.append("Frontespizio - Sezione familiari a carico")
            documenti.append("Codice fiscale del coniuge/figli a carico")

        if ha_figli_under_21:
            avvisi.append(
                "⚠️ I figli under 21 NON generano detrazione nel 730 (dal 2022 "
                "sono coperti dall'Assegno Unico Universale - AUU)."
            )

        spese_quadro_e: list[str] = []
        if ha_spese_sanitarie:
            spese_quadro_e.append("spese sanitarie (franchigia 129,11€)")
            documenti.extend(["Fatture/ricevute mediche", "Scontrini farmacia con CF"])
        if ha_mutuo_prima_casa:
            spese_quadro_e.append("interessi mutuo prima casa (max 4.000€)")
            documenti.extend(
                [
                    "Quietanza interessi passivi dalla banca",
                    "Contratto di mutuo",
                ]
            )
        if ha_ristrutturazione:
            spese_quadro_e.append("ristrutturazione edilizia (50% su max 96.000€)")
            documenti.extend(
                [
                    "Fatture lavori + bonifici 'parlanti'",
                    "Comunicazione all'Agenzia delle Entrate (se lavori > 51.645€)",
                ]
            )

        if spese_quadro_e:
            quadri_necessari.append(f"Quadro E - Oneri: {', '.join(spese_quadro_e)}")

        if ha_investimenti_esteri or ha_criptovalute:
            quadri_necessari.append("Quadro W - Investimenti e attività estere / cripto-attività")
            if ha_investimenti_esteri:
                documenti.append("Estratti conto bancari esteri")
            if ha_criptovalute:
                documenti.append("Estratti conto exchange crypto (importo in EUR al 31/12)")
                avvisi.append(
                    "⚠️ Le criptovalute vanno dichiarate sempre nel Quadro W. "
                    "Le plusvalenze > 2.000€ sono tassate al 26% nel Quadro T."
                )

        if ha_locazioni_brevi:
            quadri_necessari.append("Quadro L - Locazioni brevi (cedolare secca 26%/21%)")
            documenti.extend(
                [
                    "Estratti conto portali online (Airbnb, Booking, ecc.)",
                    "Certificazione ritenute trattenute dal portale (21%)",
                ]
            )

        if ha_plusvalenze_finanziarie:
            quadri_necessari.append("Quadro T - Plusvalenze finanziarie (nuovo 2025)")
            documenti.extend(
                [
                    "Rendiconto titoli / prospetto fiscale della banca",
                    "Documentazione acquisto e vendita titoli",
                ]
            )

        scadenza_accesso = f"1 maggio {anno + 1}"
        scadenza_invio_caf = f"30 settembre {anno + 1}"
        scadenza_invio_diretto = f"30 settembre {anno + 1}"

        return {
            "anno": anno,
            "quadri_da_compilare": quadri_necessari,
            "documenti_da_raccogliere": list(dict.fromkeys(documenti)),
            "avvisi_importanti": avvisi,
            "scadenze": {
                "accesso_precompilato": scadenza_accesso,
                "invio_tramite_caf_o_professionista": scadenza_invio_caf,
                "invio_diretto_online": scadenza_invio_diretto,
            },
            "nota": (
                "Checklist generata per il Modello 730 precompilato. "
                "Accedi al tuo 730 precompilato su: "
                "https://www.agenziaentrate.gov.it/portale/la-dichiarazione-precompilata"
            ),
        }
