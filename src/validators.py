import re

FORMATION_PATTERN = re.compile(r"^\d-\d-\d$")

# Allows letters, numbers, spaces, apostrophes, hyphens and dots (simple safe filter)
SEARCH_PATTERN = re.compile(r"^[A-Za-z0-9 .'\-]+$")


def validate_formation(formation: str) -> bool:
    """
    Validate a football formation like '3-5-2'.
    Returns True if valid, otherwise False.
    """
    return bool(FORMATION_PATTERN.match(formation))


def validate_search_text(text: str) -> bool:
    """
    Validate user search input to avoid weird characters.
    Returns True if valid, otherwise False.
    """
    text = text.strip()
    if not text:
        return False
    return bool(SEARCH_PATTERN.match(text))