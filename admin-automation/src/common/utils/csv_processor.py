import csv
import io
from typing import Any, Dict, List
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CSVProcessor:
    def __init__(self, file, delimiter: str = "\t") -> None:
        self.file = file
        self.delimiter = delimiter

    def read_and_clean(self) -> List[Dict[str, Any]]:
        """
        Reads the CSV/TSV from the provided file-like, normalizes
        header names and cell values, and returns a list of row‑dicts.
        """
        data = self.file.read().decode("utf-8")
        stream = io.StringIO(data)
        reader = csv.DictReader(stream, delimiter=self.delimiter)
        return self._clean_csv_content(reader)

    def _clean_csv_content(self, reader: csv.DictReader) -> List[Dict[str, Any]]:
        if reader.fieldnames is None:
            return []
        reader.fieldnames = [
            col.strip().lower().replace(" ", "_") for col in reader.fieldnames
        ]

        rows: List[Dict[str, Any]] = []
        for row in reader:
            cleaned = {
                key: (val.strip().lower() if isinstance(val, str) else val)
                for key, val in row.items()
            }
            rows.append(cleaned)
        return rows
