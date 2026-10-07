from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, Text, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime, timezone

Base = declarative_base()

class DocumentModel(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String)         # xlsx, csv, pdf, image
    source_type = Column(String)       # excel, csv, pdf_digital, pdf_scanned, image
    file_path = Column(String, nullable=True)
    upload_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    status = Column(String, default="processing")  # processing, valid, warning, needs_review, invalid
    overall_confidence = Column(Float, default=0.0)
    raw_json = Column(Text)            # Full InvoiceRecord JSON string
    page_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class InvoiceModel(Base):
    __tablename__ = "invoices"
    
    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False, index=True)
    invoice_number = Column(String, nullable=True)
    invoice_date = Column(String, nullable=True)
    supplier_name = Column(String, nullable=True)
    supplier_gstin = Column(String, nullable=True)
    buyer_name = Column(String, nullable=True)
    buyer_gstin = Column(String, nullable=True)
    place_of_supply = Column(String, nullable=True)
    supply_type = Column(String, nullable=True)
    subtotal = Column(Float, nullable=True)
    total_tax = Column(Float, nullable=True)
    grand_total = Column(Float, nullable=True)
    validation_status = Column(String, nullable=True)
    validation_errors = Column(JSON, default=list)
    validation_warnings = Column(JSON, default=list)

class InvoiceItemModel(Base):
    __tablename__ = "invoice_items"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(String, nullable=False, index=True)
    description = Column(String, nullable=True)
    hsn_sac = Column(String, nullable=True)
    quantity = Column(Float, nullable=True)
    unit_price = Column(Float, nullable=True)
    taxable_value = Column(Float, nullable=True)
    gst_rate = Column(Float, nullable=True)
    cgst = Column(Float, nullable=True)
    sgst = Column(Float, nullable=True)
    igst = Column(Float, nullable=True)
    total = Column(Float, nullable=True)
