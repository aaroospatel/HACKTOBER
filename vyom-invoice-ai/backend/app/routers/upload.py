from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.file_router import route_file
from app.services.validator import validate_invoice
from app.services.confidence import calculate_confidence
from app.config import settings
import os
import uuid

router = APIRouter(tags=["Upload"])

@router.post("/upload")
async def upload_invoice(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload and process an invoice document in any supported format.
    Accepts: .xlsx, .xls, .csv, .pdf, .jpg, .jpeg, .png
    Returns: Fully extracted, validated, and confidence-scored InvoiceRecord JSON.
    """
    max_bytes = getattr(settings, "max_file_size_mb", 20) * 1024 * 1024
    file_bytes = await file.read()

    if len(file_bytes) > max_bytes:
        raise HTTPException(status_code=413, detail=f"File exceeds maximum allowed size of {settings.max_file_size_mb}MB.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    # Save physical copy for audit and UI view
    os.makedirs(settings.upload_dir, exist_ok=True)
    saved_filename = f"{uuid.uuid4()}_{file.filename}"
    saved_path = os.path.join(settings.upload_dir, saved_filename)
    try:
        with open(saved_path, "wb") as f:
            f.write(file_bytes)
    except Exception:
        saved_path = None

    # 1. Route and extract
    record = await route_file(file.filename, file_bytes)

    # 2. Deterministic validation
    record = validate_invoice(record)

    # 3. Multi-signal confidence calculation
    record = calculate_confidence(record)

    # 4. Save to database
    crud.save_document(db, record, file_path=saved_path)

    return record
