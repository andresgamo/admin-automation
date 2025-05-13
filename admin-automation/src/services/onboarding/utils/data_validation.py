from typing import Any, Dict, Tuple
from common.utils.data_validation import DateError, FileError


def validate_data(data: Dict[str, Any]) -> Tuple[str, Any]:
    """
    Validate that `data` contains:
      - a non‐empty 'date' string
      - a 'file' item whose .filename ends with .tsv and whose .file stream is non‐empty

    Raises:
      DateError if date is missing or blank.
      FileError if file is missing, empty, or not .tsv.

    Returns:
      (date_str, file_item)
    """
    date_obj = data.get("date")
    if not date_obj:
        raise DateError("Missing date")

    file_obj = data.get("file")
    if file_obj is None:
        raise FileError("Missing file")

    filename = getattr(file_obj, "filename", "")
    if not filename.lower().endswith(".tsv"):
        raise FileError("Please upload a .tsv file")

    file_stream = getattr(file_obj, "file", None)
    if not file_stream:
        raise FileError("Uploaded file is empty or unreadable")

    return date_obj.value, file_obj.file
