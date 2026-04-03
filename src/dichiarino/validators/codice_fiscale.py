"""Italian Codice Fiscale (CF) validator and parser.

Implements the full algorithm defined by the Ministero dell'Economia e delle Finanze,
including the check-character (16th character) computation.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Month codes
_MESI: dict[str, int] = {
    "A": 1,
    "B": 2,
    "C": 3,
    "D": 4,
    "E": 5,
    "H": 6,
    "L": 7,
    "M": 8,
    "P": 9,
    "R": 10,
    "S": 11,
    "T": 12,
}

# Odd-position character values for check digit
_ODD_VALUES: dict[str, int] = {
    "0": 1,
    "1": 0,
    "2": 5,
    "3": 7,
    "4": 9,
    "5": 13,
    "6": 15,
    "7": 17,
    "8": 19,
    "9": 21,
    "A": 1,
    "B": 0,
    "C": 5,
    "D": 7,
    "E": 9,
    "F": 13,
    "G": 15,
    "H": 17,
    "I": 19,
    "J": 21,
    "K": 2,
    "L": 4,
    "M": 18,
    "N": 20,
    "O": 11,
    "P": 3,
    "Q": 6,
    "R": 8,
    "S": 12,
    "T": 14,
    "U": 16,
    "V": 10,
    "W": 22,
    "X": 25,
    "Y": 24,
    "Z": 23,
}

# Even-position character values (0-based index)
_EVEN_VALUES: dict[str, int] = {
    **{str(i): i for i in range(10)},
    **{chr(ord("A") + i): i for i in range(26)},
}

_CF_PATTERN = re.compile(r"^[A-Z]{6}\d{2}[ABCDEHLMPRST]\d{2}[A-Z]\d{3}[A-Z]$")


@dataclass
class CodiceFiscaleInfo:
    codice_fiscale: str
    valido: bool
    errore: str | None = None
    sesso: str | None = None  # "M" or "F"
    anno_nascita: int | None = None  # 2-digit year (ambiguous century)
    mese_nascita: int | None = None
    giorno_nascita: int | None = None
    codice_comune: str | None = None  # Belfiore code (4 chars)


def valida_codice_fiscale(cf: str) -> CodiceFiscaleInfo:
    """Validate and parse an Italian codice fiscale.

    Args:
        cf: The codice fiscale string (case-insensitive, spaces stripped).

    Returns:
        CodiceFiscaleInfo with validation result and parsed fields.
    """
    cf = cf.strip().upper().replace(" ", "")

    if len(cf) != 16:
        return CodiceFiscaleInfo(cf, False, f"Lunghezza non valida: {len(cf)} (attesa: 16).")

    if not _CF_PATTERN.match(cf):
        return CodiceFiscaleInfo(
            cf,
            False,
            "Formato non valido. Il codice fiscale deve seguire il pattern: AAABBB00A00A000A",
        )

    # Validate check character
    expected_check = _calcola_carattere_controllo(cf[:15])
    if cf[15] != expected_check:
        return CodiceFiscaleInfo(
            cf,
            False,
            f"Carattere di controllo non valido: atteso '{expected_check}', trovato '{cf[15]}'.",
        )

    # Parse fields
    anno_2digit = int(cf[6:8])
    mese_code = cf[8]
    mese = _MESI.get(mese_code)
    giorno_raw = int(cf[9:11])

    if giorno_raw > 40:
        sesso = "F"
        giorno = giorno_raw - 40
    else:
        sesso = "M"
        giorno = giorno_raw

    codice_comune = cf[11:15]

    return CodiceFiscaleInfo(
        codice_fiscale=cf,
        valido=True,
        sesso=sesso,
        anno_nascita=anno_2digit,
        mese_nascita=mese,
        giorno_nascita=giorno,
        codice_comune=codice_comune,
    )


def _calcola_carattere_controllo(cf15: str) -> str:
    """Compute the 16th (check) character from the first 15 characters."""
    total = 0
    for i, char in enumerate(cf15):
        # Positions are 1-indexed; odd positions use _ODD_VALUES
        if (i + 1) % 2 == 1:
            total += _ODD_VALUES[char]
        else:
            total += _EVEN_VALUES[char]
    return chr(ord("A") + (total % 26))
