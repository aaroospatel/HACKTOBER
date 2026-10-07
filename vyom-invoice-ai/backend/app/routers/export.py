from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import Response, StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.exporter import export_json, export_csv, export_excel
import json
import io

router = APIRouter(tags=["Export"])

@router.get("/documents/{doc_id}/json")
@router.get("/documents/{doc_id}/export/json")
def download_json(doc_id: str, db: Session = Depends(get_db)):
    """Export standardized machine-readable JSON for a document."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    record = json.loads(doc.raw_json)
    json_str = export_json(record)
    return Response(
        content=json_str,
        media_type="application/json",
        headers={"Content-Disposition": f'attachment; filename="{doc_id}.json"'}
    )

@router.get("/documents/{doc_id}/csv")
@router.get("/documents/{doc_id}/export/csv")
def download_csv(doc_id: str, db: Session = Depends(get_db)):
    """Export invoice and line items as CSV."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    record = json.loads(doc.raw_json)
    csv_str = export_csv(record)
    return Response(
        content=csv_str,
        media_type="text/csv",
        headers={"Content-Disposition": f'attachment; filename="{doc_id}.csv"'}
    )

@router.get("/documents/{doc_id}/excel")
@router.get("/documents/{doc_id}/export/excel")
def download_excel(doc_id: str, db: Session = Depends(get_db)):
    """Export multi-tab workbook as Microsoft Excel (.xlsx)."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found.")

    record = json.loads(doc.raw_json)
    excel_bytes = export_excel(record)
    return Response(
        content=excel_bytes,
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{doc_id}.xlsx"'}
    )
