from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.validator import validate_invoice
from app.services.confidence import calculate_confidence
from app.schemas.invoice import HumanCorrectionRequest
from typing import Optional, List
import json

router = APIRouter(tags=["Invoices & Documents"])

@router.get("/documents")
def list_documents(
    status: Optional[str] = Query(None, description="Filter by status: valid, warning, needs_review, invalid"),
    db: Session = Depends(get_db)
):
    """Retrieve all processed invoice documents."""
    return crud.get_all_documents(db, status=status)

@router.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    """Retrieve the full Universal InvoiceRecord JSON for a specific document ID."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")
    return json.loads(doc.raw_json)

def _apply_nested_correction(record: dict, field_path: str, value: str) -> dict:
    """Safely apply a human correction using dot-notation path like 'supplier.gstin'."""
    parts = field_path.split(".")
    target = record
    for part in parts[:-1]:
        if "[" in part and "]" in part:
            # Handle array index like items[0]
            arr_name, idx_str = part[:-1].split("[")
            target = target.get(arr_name, [])[int(idx_str)]
        else:
            if part not in target or not isinstance(target[part], dict):
                target[part] = {}
            target = target[part]

    last_key = parts[-1]
    # Attempt type conversions
    try:
        if "." in value:
            target[last_key] = float(value)
        else:
            target[last_key] = int(value)
    except (ValueError, TypeError):
        if value.lower() in ("true", "false"):
            target[last_key] = value.lower() == "true"
        elif value.lower() in ("null", "none"):
            target[last_key] = None
        else:
            target[last_key] = value

    return record

@router.put("/documents/{doc_id}")
def apply_correction(
    doc_id: str,
    correction: HumanCorrectionRequest,
    db: Session = Depends(get_db)
):
    """
    Human-in-the-Loop review endpoint.
    Applies an operator correction to any field, triggers immediate deterministic revalidation,
    recalculates confidence scores, and updates the database record.
    """
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    record = json.loads(doc.raw_json)

    # 1. Apply correction
    record = _apply_nested_correction(record, correction.field_path, correction.corrected_value)

    # 2. Re-validate
    record = validate_invoice(record)

    # 3. Recalculate confidence
    record = calculate_confidence(record)

    # 4. Update in database
    crud.update_document(db, doc_id, record)

    return record

@router.get("/stats")
def get_dashboard_stats(db: Session = Depends(get_db)):
    """Retrieve system analytics and processing statistics."""
    return crud.get_stats(db)
