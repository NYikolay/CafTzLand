import pytest

from infrastructure.phone import normalize_belarus_phone

VALID = [
    "+375291234567",
    "+375 (29) 123-45-67",
    "+375 29 123 45 67",
    "375291234567",
    "80291234567",
    "29 123-45-67",
]

INVALID = [
    "",
    "12345",
    "залупа",
    "+79001234567",
    "+375111234567",
]


@pytest.mark.parametrize("raw", VALID)
def test_normalizes_belarus_mobile(raw: str) -> None:
    assert normalize_belarus_phone(raw) == "+375291234567"


@pytest.mark.parametrize("raw", INVALID)
def test_rejects_invalid_numbers(raw: str) -> None:
    with pytest.raises(ValueError, match="phone number"):
        normalize_belarus_phone(raw)
