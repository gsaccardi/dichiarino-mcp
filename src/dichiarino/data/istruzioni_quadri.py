"""Quadro descriptions and instructions for each section of Modello 730/2025."""

from __future__ import annotations

ISTRUZIONI_QUADRI: dict[str, dict[str, str]] = {
    "A": {
        "titolo": "Redditi dei Terreni",
        "descrizione": (
            "Quadro A raccoglie i redditi fondiari derivanti da terreni situati nel territorio "
            "italiano. Si compilano i dati catastali (Comune, foglio, particella), la qualità "
            "colturale, la rendita catastale e l'eventuale affitto."
        ),
        "campi_principali": (
            "• Rendita catastale del terreno\n"
            "• Comune del terreno\n"
            "• Utilizzo: terreno non affittato (codice 1), affittato (codice 2), "
            "a conduzione diretta (codice 3)\n"
            "• Quote di possesso (%)\n"
            "• Canone di affitto (se affittato)"
        ),
        "note": (
            "Dal 2020 si applica la rivalutazione dell'80% sulla rendita catastale dei terreni. "
            "I terreni agricoli posseduti da coltivatori diretti/IAP sono esclusi dall'IRPEF."
        ),
        "documenti_necessari": "Visura catastale, contratti di affitto se presenti.",
    },
    "B": {
        "titolo": "Redditi dei Fabbricati",
        "descrizione": (
            "Quadro B riguarda i redditi fondiari di fabbricati e altri immobili a uso "
            "abitativo o non abitativo situati in Italia. Include la prima casa (non tassata "
            "ma da dichiarare), altri immobili, immobili concessi in locazione."
        ),
        "campi_principali": (
            "• Rendita catastale\n"
            "• Utilizzo: abitazione principale (cod. 1), altro uso (cod. 2), "
            "locazione ordinaria (cod. 3), cedolare secca (cod. 8)\n"
            "• Canone di locazione annuo\n"
            "• Giorni di utilizzo\n"
            "• Percentuale di possesso"
        ),
        "note": (
            "L'abitazione principale non è soggetta a IRPEF (è esclusa dalla base imponibile). "
            "Per le locazioni con cedolare secca le aliquote sono 21% (ordinaria) o 10% "
            "(canone concordato in comuni ad alta tensione abitativa)."
        ),
        "documenti_necessari": (
            "Visura catastale, contratti di locazione, comunicazione cedolare secca (RLI)."
        ),
    },
    "C": {
        "titolo": "Redditi da Lavoro Dipendente e Assimilati",
        "descrizione": (
            "Quadro C raccoglie i redditi da lavoro dipendente, pensione e redditi assimilati "
            "(es. collaborazioni coordinate e continuative, borse di studio). I dati provengono "
            "principalmente dalla Certificazione Unica (CU) rilasciata dal datore di lavoro."
        ),
        "campi_principali": (
            "• Reddito di lavoro dipendente (punto 1 CU)\n"
            "• Ritenute IRPEF subite (punto 21 CU)\n"
            "• Addizionale regionale trattenuta (punto 22 CU)\n"
            "• Addizionale comunale acconto/saldo (punti 23-24 CU)\n"
            "• Giorni di lavoro nell'anno\n"
            "• Codice fiscale del sostituto d'imposta"
        ),
        "note": (
            "In caso di più CU (es. cambio lavoro) compilare più righe del Quadro C. "
            "Il 730 precompilato include già i dati da tutte le CU trasmesse."
        ),
        "documenti_necessari": "Certificazione Unica (CU) del datore di lavoro/ente pensionistico.",
    },
    "D": {
        "titolo": "Altri Redditi",
        "descrizione": (
            "Quadro D include redditi non rientranti in altri quadri: redditi da capitale "
            "(dividendi, interessi), redditi diversi (plusvalenze non finanziarie, proventi "
            "da attività commerciali occasionali, redditi di lavoro autonomo occasionale)."
        ),
        "campi_principali": (
            "• Tipo di reddito (codice)\n"
            "• Importo del reddito\n"
            "• Ritenute subite\n"
            "• Codice fiscale del soggetto che ha corrisposto il reddito"
        ),
        "note": (
            "I dividendi da partecipazioni qualificate e non qualificate hanno trattamenti "
            "fiscali diversi. Le plusvalenze finanziarie sono ora nel Quadro T (dal 2025)."
        ),
        "documenti_necessari": (
            "Estratti conto bancari, contratti, certificazioni del soggetto erogante."
        ),
    },
    "E": {
        "titolo": "Oneri e Spese Detraibili/Deducibili",
        "descrizione": (
            "Quadro E è il quadro delle detrazioni e deduzioni: spese mediche, interessi "
            "su mutui, contributi previdenziali, premi assicurativi, spese per istruzione, "
            "ristrutturazioni, erogazioni liberali e molti altri oneri."
        ),
        "campi_principali": (
            "• Codice spesa (identifica il tipo di onere)\n"
            "• Importo della spesa\n"
            "• Codice fiscale del beneficiario (per alcune voci)\n"
            "• Numero rata (per bonus pluriennali come ristrutturazioni)"
        ),
        "note": (
            "Dal 2024, per redditi > 50.000€ si applica una riduzione di 260€ "
            "sulle detrazioni al 19% (escluse le spese sanitarie). "
            "Il precompilato include già spese sanitarie e veterinarie dal Sistema Tessera Sanitaria."
        ),
        "documenti_necessari": (
            "Fatture e ricevute spese mediche, contratto mutuo e quietanza interessi, "
            "ricevute contributi previdenziali, fatture ristrutturazione, ecc."
        ),
    },
    "F": {
        "titolo": "Acconti, Ritenute, Eccedenze e Altri Dati",
        "descrizione": (
            "Quadro F raccoglie dati non riconducibili ad altri quadri: acconti IRPEF versati, "
            "ritenute su redditi a tassazione separata, eccedenze da precedenti dichiarazioni, "
            "dati per il calcolo dell'acconto IRPEF dell'anno successivo."
        ),
        "campi_principali": (
            "• Acconti IRPEF (primo e secondo acconto)\n"
            "• Ritenute su redditi a tassazione separata\n"
            "• Eccedenza IRPEF anno precedente\n"
            "• Codice per metodo di calcolo acconto (storico/previsionale)"
        ),
        "note": "Generalmente compilato automaticamente dal CAF o dal precompilato.",
        "documenti_necessari": ("F24 di versamento acconti, dichiarazione anno precedente."),
    },
    "G": {
        "titolo": "Crediti d'Imposta",
        "descrizione": (
            "Quadro G raccoglie i crediti d'imposta spettanti: credito per redditi prodotti "
            "all'estero (art. 165 TUIR), crediti per imposte sostitutive, crediti da bonus "
            "fiscali (es. bonus affitti, crediti da precedenti dichiarazioni)."
        ),
        "campi_principali": (
            "• Tipo di credito (codice)\n"
            "• Importo del credito\n"
            "• Anno di riferimento\n"
            "• Imposta estera pagata (per crediti esteri)"
        ),
        "note": (
            "Il credito per imposte pagate all'estero evita la doppia imposizione. "
            "Non può eccedere la quota di IRPEF italiana relativa al reddito estero."
        ),
        "documenti_necessari": (
            "Certificazione imposta estera pagata, documentazione bonus spettanti."
        ),
    },
    "I": {
        "titolo": "Imposte da Compensare",
        "descrizione": (
            "Quadro I indica le eccedenze di imposta che il contribuente intende "
            "utilizzare in compensazione (tramite F24) anziché ricevere a rimborso."
        ),
        "campi_principali": ("• Codice tributo da compensare\n• Importo da compensare"),
        "note": (
            "Opzione alternativa al rimborso IRPEF. Le eccedenze possono essere usate "
            "per compensare altri tributi (es. IMU, bollo auto) tramite F24."
        ),
        "documenti_necessari": "Nessun documento specifico aggiuntivo.",
    },
    "K": {
        "titolo": "Comunicazione dell'Amministratore di Condominio",
        "descrizione": (
            "Quadro K è compilato dagli amministratori di condominio per comunicare "
            "all'Agenzia delle Entrate i dati dei lavori condominiali e i relativi importi "
            "attribuibili a ciascun condòmino (es. ristrutturazioni, ecobonus)."
        ),
        "campi_principali": (
            "• Codice fiscale del condominio\n"
            "• Tipo di intervento\n"
            "• Importo complessivo dei lavori\n"
            "• Quota attribuita al dichiarante"
        ),
        "note": "Rilevante per i condòmini che vogliono detrarre quote di lavori condominiali.",
        "documenti_necessari": (
            "Comunicazione dell'amministratore di condominio con dettaglio quote pro-capite."
        ),
    },
    "L": {
        "titolo": "Ulteriori Dati Fiscali",
        "descrizione": (
            "Quadro L contiene dati ulteriori: casi particolari (residenti all'estero, "
            "canoni di locazione agevolati, dati per la determinazione dell'acconto "
            "cedolare secca, redditi da locazioni brevi)."
        ),
        "campi_principali": (
            "• Redditi da locazioni brevi (Airbnb, Booking, ecc.)\n"
            "• Dati per residenti all'estero iscritti AIRE\n"
            "• Dati per soggetti non residenti"
        ),
        "note": (
            "Le locazioni brevi (max 30 giorni) sono soggette a cedolare secca 26% "
            "(21% se prima casa). I portali online applicano una ritenuta del 21%."
        ),
        "documenti_necessari": (
            "Estratti conto portali online (Airbnb, Booking), contratti di locazione breve."
        ),
    },
    "M": {
        "titolo": "Redditi a Tassazione Separata e Imposta Sostitutiva",
        "descrizione": (
            "Quadro M (nuovo dal 2025) raccoglie i redditi assoggettati a tassazione separata "
            "o a imposta sostitutiva: TFR, arretrati di lavoro dipendente, indennità di fine "
            "rapporto, rivalutazioni di terreni/partecipazioni, redditi percepiti da eredi."
        ),
        "campi_principali": (
            "• Tipo di reddito a tassazione separata (codice evento)\n"
            "• Importo percepito\n"
            "• Anno di maturazione\n"
            "• Ritenute già subite\n"
            "• Imposta sostitutiva versata (per rivalutazioni)"
        ),
        "note": (
            "Il TFR è generalmente tassato dal sostituto d'imposta; in alcuni casi "
            "il contribuente deve indicarlo per il conguaglio. "
            "La rivalutazione dei terreni richiede perizia giurata e versamento dell'imposta sostitutiva."
        ),
        "documenti_necessari": (
            "CU (punti relativi a TFR/arretrati), atto di perizia giurata per rivalutazione, "
            "F24 imposta sostitutiva versata."
        ),
    },
    "T": {
        "titolo": "Plusvalenze di Natura Finanziaria",
        "descrizione": (
            "Quadro T (nuovo dal 2025) raccoglie le plusvalenze derivanti da cessione di "
            "partecipazioni, titoli, valute, criptovalute e altri strumenti finanziari "
            "soggetti a imposta sostitutiva (26%) o a tassazione ordinaria."
        ),
        "campi_principali": (
            "• Tipo di plusvalenza (codice)\n"
            "• Data operazione\n"
            "• Corrispettivo di cessione\n"
            "• Costo/valore di acquisto\n"
            "• Plusvalenza imponibile\n"
            "• Imposta sostitutiva dovuta\n"
            "• Minusvalenze pregresse compensabili"
        ),
        "note": (
            "Partecipazioni qualificate: tassazione ordinaria IRPEF. "
            "Partecipazioni non qualificate: imposta sostitutiva 26%. "
            "Criptovalute: imposta sostitutiva 26% sulle plusvalenze > 2.000€ nell'anno."
        ),
        "documenti_necessari": (
            "Rendiconto titoli della banca/intermediario, contratti di acquisto e vendita, "
            "estratti conto exchange per criptovalute."
        ),
    },
    "W": {
        "titolo": "Investimenti e Attività Estere (IVAFE/IVIE)",
        "descrizione": (
            "Quadro W (ex RW) è il quadro del monitoraggio fiscale: obbligatorio per chi "
            "detiene investimenti o attività finanziarie all'estero. Serve anche per calcolare "
            "IVAFE (imposta su attività finanziarie estere) e IVIE (immobili esteri)."
        ),
        "campi_principali": (
            "• Tipo di attività estera (codice)\n"
            "• Paese estero (codice)\n"
            "• Valore iniziale e finale dell'investimento\n"
            "• Criterio di determinazione del valore\n"
            "• IVAFE/IVIE dovuta\n"
            "• Cripto-attività detenute"
        ),
        "note": (
            "Obbligo di compilazione anche se il valore è inferiore a 15.000€ "
            "(la soglia è solo per il versamento IVAFE). "
            "Dal 2023 le criptovalute vanno sempre dichiarate in Quadro W."
        ),
        "documenti_necessari": (
            "Estratti conto bancari esteri, rendiconto intermediari esteri, "
            "estratti conto exchange crypto."
        ),
    },
}
