class DateError(Exception):
    """Raised when the `date` field is missing or malformed."""


class FileError(Exception):
    """Raised when the `file` field is missing or not a .tsv."""
