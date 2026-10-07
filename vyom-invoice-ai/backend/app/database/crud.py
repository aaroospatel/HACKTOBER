from sqlalchemy.orm import Session
from sqlalchemy import func
from .models import DocumentModel, InvoiceModel, InvoiceItemModel
from typing import Dict, Any, List, Optional
import json

def save_document(db: Session, record: dict, file_path: Optional[str] = None) -> DocumentModel:
    """Save newly processed invoice record into documents, invoices, and invoice_items tables."""
    doc_info = record.get("document") or {}
    val = record.get("validation") or {}
    conf = record.get("confidence") or {}
    inv = record.get("invoice") or {}
    supp = record.get("supplier") or {}
    buy = record.get("buyer") or {}
    tot = record.get("totals") or {}
    tax = record.get("tax") or {}

    doc_id = doc_info.get("id")
    raw_json_str = json.dumps(record, default=str, ensure_ascii=False)

    doc = DocumentModel(
        id=doc_id,
        filename=doc_info.get("filename", "unknown"),
        file_type=doc_info.get("source_type", "image"),
        source_type=doc_info.get("source_type", "image"),
        file_path=file_path,
        status=val.get("status", "needs_review"),
        overall_confidence=float(conf.get("overall", 0.0)),
        raw_json=raw_json_str,
        page_count=int(doc_info.get("page_count", 1))
    )
    doc = db.merge(doc)

    invoice_entry = InvoiceModel(
        id=f"inv_{doc_id}",
        document_id=doc_id,
        invoice_number=inv.get("invoice_number"),
        invoice_date=inv.get("invoice_date"),
        supplier_name=supp.get("name"),
        supplier_gstin=supp.get("gstin"),
        buyer_name=buy.get("name"),
        buyer_gstin=buy.get("gstin"),
        place_of_supply=inv.get("place_of_supply"),
        supply_type=inv.get("supply_type"),
        subtotal=tot.get("subtotal"),
        total_tax=tax.get("total_tax"),
        grand_total=tot.get("grand_total"),
        validation_status=val.get("status"),
        validation_errors=val.get("errors", []),
        validation_warnings=val.get("warnings", [])
    )
    invoice_entry = db.merge(invoice_entry)

    # Line items
    db.query(InvoiceItemModel).filter(InvoiceItemModel.invoice_id == invoice_entry.id).delete()
    for item in record.get("items", []):
        db_item = InvoiceItemModel(
            invoice_id=invoice_entry.id,
            description=item.get("description"),
            hsn_sac=item.get("hsn_sac"),
            quantity=item.get("quantity"),
            unit_price=item.get("unit_price"),
            taxable_value=item.get("taxable_value"),
            gst_rate=item.get("gst_rate"),
            cgst=item.get("cgst"),
            sgst=item.get("sgst"),
            igst=item.get("igst"),
            total=item.get("total")
        )
        db.add(db_item)

    db.commit()
    db.refresh(doc)
    return doc

def get_document(db: Session, doc_id: str) -> Optional[DocumentModel]:
    return db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()

def get_all_documents(db: Session, status: Optional[str] = None) -> List[dict]:
    query = db.query(DocumentModel)
    if status:
        query = query.filter(DocumentModel.status == status)
    docs = query.order_by(DocumentModel.created_at.desc()).all()
    
    results = []
    for d in docs:
        inv_record = json.loads(d.raw_json) if d.raw_json else {}
        results.append({
            "id": d.id,
            "filename": d.filename,
            "file_type": d.file_type,
            "source_type": d.source_type,
            "status": d.status,
            "confidence": d.overall_confidence,
            "upload_time": str(d.upload_time),
            "page_count": d.page_count,
            "invoice_number": inv_record.get("invoice", {}).get("invoice_number"),
            "supplier_name": inv_record.get("supplier", {}).get("name"),
            "grand_total": inv_record.get("totals", {}).get("grand_total")
        })
    return results

def update_document(db: Session, doc_id: str, record: dict) -> Optional[DocumentModel]:
    doc = get_document(db, doc_id)
    if doc:
        val = record.get("validation") or {}
        conf = record.get("confidence") or {}
        doc.raw_json = json.dumps(record, default=str, ensure_ascii=False)
        doc.status = val.get("status", "needs_review")
        doc.overall_confidence = float(conf.get("overall", 0.0))
        db.commit()
        db.refresh(doc)
    return doc

def get_stats(db: Session) -> dict:
    total = db.query(DocumentModel).count()
    valid = db.query(DocumentModel).filter(DocumentModel.status == "valid").count()
    review = db.query(DocumentModel).filter(
        DocumentModel.status.in_(["needs_review", "warning"])
    ).count()
    avg_conf = db.query(func.avg(DocumentModel.overall_confidence)).scalar() or 0.0
    return {
        "total_documents": total,
        "validated": valid,
        "needs_review": review,
        "average_confidence": round(float(avg_conf), 3),
        "invalid": max(0, total - valid - review),
    }
