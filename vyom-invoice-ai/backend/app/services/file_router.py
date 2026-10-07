import os
from fastapi import UploadFile, HTTPException
from .excel_processor import process_excel
from .csv_processor import process_csv
from .pdf_processor import process_pdf
from .image_processor import process_image

SUPPORTED_TYPES = {
    "xlsx": "excel",
    "xls": "excel",
    "csv": "csv",
    "pdf": "pdf",
    "jpg": "image",
    "jpeg": "image",
    "png": "image",
}

def detect_file_type(filename: str) -> str:
    """Return normalized file category from extension."""
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""
    if ext not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: .{ext}. Supported formats: xlsx, xls, csv, pdf, jpg, jpeg, png"
        )
    return SUPPORTED_TYPES[ext]

async def route_file(filename: str, file_bytes: bytes) -> dict:
    """
    Detect file type and route to appropriate pipeline processor.
    Returns the populated InvoiceRecord dictionary.
    """
    file_type = detect_file_type(filename)

    if file_type == "excel":
        return await process_excel(file_bytes, filename)
    elif file_type == "csv":
        return await process_csv(file_bytes, filename)
    elif file_type == "pdf":
        return await process_pdf(file_bytes, filename)
    elif file_type == "image":
        return await process_image(file_bytes, filename)
    else:
        raise HTTPException(status_code=400, detail=f"No processor available for {file_type}")
