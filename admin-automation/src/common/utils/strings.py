from re import Pattern
from datetime import date
from common.constants import SPANISH_MONTHS


def capitalize_phrase(s: str) -> str:
    """Capitalize each word in the input string."""
    return " ".join(word.capitalize() for word in s.split())


def capitalize_list_phrases(list_phrases: list[str]) -> str:
    return [capitalize_phrase(phrase) for phrase in list_phrases]


def parse_names(names: list) -> str:
    capitalzied_names = capitalize_list_phrases(names)
    return "\n- ".join(capitalzied_names)


def extractor_with_regex(pattern: Pattern[str], text: str) -> str:
    """
    Find the first capturing group in `text` that matches `pattern`.

    :param pattern: a pre-compiled regex with at least one capturing group
    :param text: the string to search
    :return: the contents of group(1)
    :raises ValueError: if no match is found
    """
    match = pattern.search(text)
    if not match:
        raise ValueError(f"No match for pattern {pattern.pattern!r}")
    return match.group(1)


def format_spanish_date(iso_date: str) -> str:
    """
    Convert ISO format 'YYYY-MM-DD' into a spanish string
    'DD de MM del YYYY'.
    """
    dt = date.fromisoformat(iso_date)
    dd = f"{dt.day:02d}"
    mm = SPANISH_MONTHS[dt.month]
    yy = dt.year
    return f"{dd} de {mm} del {yy}"
