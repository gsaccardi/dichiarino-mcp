"""Core domain types for Dichiarino."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum, StrEnum


class AnnoFiscale(int, Enum):
    """Supported tax years (anno di imposta, not anno della dichiarazione)."""

    Y2025 = 2025
    Y2024 = 2024
    Y2023 = 2023


class TipoReddito(StrEnum):
    LAVORO_DIPENDENTE = "lavoro_dipendente"
    PENSIONE = "pensione"
    LAVORO_ASSIMILATO = "lavoro_assimilato"


class TipoFamiliare(StrEnum):
    CONIUGE = "coniuge"
    FIGLIO = "figlio"
    ALTRO = "altro"


class RegioneItaliana(StrEnum):
    ABRUZZO = "abruzzo"
    BASILICATA = "basilicata"
    CALABRIA = "calabria"
    CAMPANIA = "campania"
    EMILIA_ROMAGNA = "emilia_romagna"
    FRIULI_VENEZIA_GIULIA = "friuli_venezia_giulia"
    LAZIO = "lazio"
    LIGURIA = "liguria"
    LOMBARDIA = "lombardia"
    MARCHE = "marche"
    MOLISE = "molise"
    PIEMONTE = "piemonte"
    PUGLIA = "puglia"
    SARDEGNA = "sardegna"
    SICILIA = "sicilia"
    TOSCANA = "toscana"
    TRENTINO_ALTO_ADIGE = "trentino_alto_adige"
    UMBRIA = "umbria"
    VALLE_D_AOSTA = "valle_d_aosta"
    VENETO = "veneto"


class TipoSpesa(StrEnum):
    """Expense categories for Quadro E."""

    SPESE_SANITARIE = "spese_sanitarie"
    SPESE_VETERINARIE = "spese_veterinarie"
    MUTUO_PRIMA_CASA = "mutuo_prima_casa"
    RISTRUTTURAZIONE = "ristrutturazione"
    RISPARMIO_ENERGETICO = "risparmio_energetico"
    ISTRUZIONE_UNIVERSITA = "istruzione_universita"
    ISTRUZIONE_SCUOLA = "istruzione_scuola"
    ASSICURAZIONE_VITA = "assicurazione_vita"
    ASSICURAZIONE_INFORTUNI = "assicurazione_infortuni"
    CONTRIBUTI_PREVIDENZIALI = "contributi_previdenziali"
    EROGAZIONI_LIBERALI_ONLUS = "erogazioni_liberali_onlus"
    EROGAZIONI_LIBERALI_PARTITI = "erogazioni_liberali_partiti"
    SPESE_FUNEBRI = "spese_funebri"
    CANONI_AFFITTO_STUDENTI = "canoni_affitto_studenti"
    BONUS_MOBILI = "bonus_mobili"
    SUPERBONUS = "superbonus"


@dataclass
class ScaglioneFiscale:
    min_reddito: float
    max_reddito: float | None  # None = no upper limit
    aliquota: float  # e.g. 0.23 for 23%


@dataclass
class FamiliareACarico:
    tipo: TipoFamiliare
    mesi_a_carico: int = 12  # 1-12
    percentuale_carico: float = 1.0  # 0.5 for 50% shared
    eta_inferiore_21: bool = False  # for children
    eta_inferiore_3: bool = False  # for children under 3


@dataclass
class SpesaDetraibile:
    tipo: TipoSpesa
    importo: float
    note: str = ""


@dataclass
class DatiCertificazioneUnica:
    """Key fields from Certificazione Unica (CU)."""

    reddito_lordo: float
    imponibile_previdenziale: float
    irpef_trattenuta: float
    addizionale_regionale_trattenuta: float
    addizionale_comunale_trattenuta: float
    giorni_lavoro: int
    tipo_reddito: TipoReddito = TipoReddito.LAVORO_DIPENDENTE


@dataclass
class RisultatoIRPEF:
    reddito_complessivo: float
    irpef_lorda: float
    breakdown_scaglioni: list[dict[str, float]] = field(default_factory=list)
    anno: int = 2025


@dataclass
class RisultatoDichiarazione:
    irpef_lorda: float
    detrazione_lavoro: float
    detrazioni_familiari: float
    detrazioni_oneri: float
    oneri_deducibili: float
    addizionale_regionale: float
    irpef_netta: float
    irpef_trattenuta: float
    saldo: float  # negative = rimborso, positive = debito
    anno: int = 2025
