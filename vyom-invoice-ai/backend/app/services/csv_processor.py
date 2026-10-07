import pandas as pd
import io
from .excel_processor import _process_tabular

async def process_csv(file_bytes: bytes, filename: str) -> dict:
    """Parse CSV files with multiple encoding fallbacks into Universal InvoiceRecord."""
    for encoding in ["utf-8", "utf-8-sig", "latin-1", "cp1252", "iso-8859-1"]:
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
            return _process_tabular(df, filename, "csv")
        except (UnicodeDecodeError, Exception):
            continue
    raise ValueError("Could not decode CSV with any supported encoding.")
