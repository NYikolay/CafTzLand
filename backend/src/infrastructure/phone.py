import phonenumbers
from phonenumbers import NumberParseException

REGION = "BY"


def normalize_belarus_phone(raw: str) -> str:
    try:
        parsed = phonenumbers.parse(raw, REGION)
    except NumberParseException as exc:
        raise ValueError("phone number cannot be parsed") from exc
    if not phonenumbers.is_valid_number_for_region(parsed, REGION):
        raise ValueError("phone number is not valid for Belarus")
    return phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.E164)
