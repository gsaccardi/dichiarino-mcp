"""Unit tests for codice fiscale validator."""

from __future__ import annotations

from dichiarino.validators.codice_fiscale import valida_codice_fiscale


class TestValidaCodiceFiscale:
    # Known valid CF (synthetic test fixtures)
    # RSSMRA85T10A562S = Mario Rossi, 10/12/1985, male, Agrigento (A562)
    # Computed via check-char algorithm: RSSMRA85T50A562W = same data, female (day 50)
    VALID_CF = "RSSMRA85T10A562S"
    VALID_CF_FEMALE = "RSSMRA85T50A562W"  # day 50 = 40+10 → female born on day 10

    def test_valid_cf(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.valido is True
        assert info.errore is None

    def test_valid_cf_female(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF_FEMALE)
        # Female: day raw = 50 (> 40), actual day = 10
        assert info.valido is True
        assert info.sesso == "F"
        assert info.giorno_nascita == 10

    def test_sesso_maschio(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.sesso == "M"

    def test_giorno_nascita(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.giorno_nascita == 10

    def test_mese_nascita(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.mese_nascita == 12  # T = December

    def test_anno_nascita(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.anno_nascita == 85

    def test_codice_comune(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF)
        assert info.codice_comune == "A562"

    def test_case_insensitive(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF.lower())
        assert info.valido is True

    def test_strips_spaces(self) -> None:
        info = valida_codice_fiscale(f"  {self.VALID_CF}  ")
        assert info.valido is True

    def test_wrong_length(self) -> None:
        info = valida_codice_fiscale("RSSMRA85T10A562")
        assert info.valido is False
        assert "Lunghezza" in (info.errore or "")

    def test_wrong_check_char(self) -> None:
        bad = self.VALID_CF[:-1] + ("T" if self.VALID_CF[-1] != "T" else "U")
        info = valida_codice_fiscale(bad)
        assert info.valido is False
        assert "controllo" in (info.errore or "").lower()

    def test_invalid_format(self) -> None:
        info = valida_codice_fiscale("1234567890123456")
        assert info.valido is False

    def test_all_uppercase_output(self) -> None:
        info = valida_codice_fiscale(self.VALID_CF.lower())
        assert info.codice_fiscale == self.VALID_CF
