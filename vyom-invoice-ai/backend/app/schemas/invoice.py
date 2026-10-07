from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime, timezone
import uuid

class DocumentInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    document_type: str = "invoice"
    source_type: Literal["excel", "csv", "pdf_digital", "pdf_scanned", "image"]
    upload_time: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    page_count: int = 1

class PartyInfo(BaseModel):
    name: Optional[str] = None
    gstin: Optional[str] = None
    address: Optional[str] = None
    state_code: Optional[str] = None

class InvoiceMeta(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    place_of_supply: Optional[str] = None
    reverse_charge: Optional[bool] = False
    irn: Optional[str] = None
    supply_type: Optional[Literal["intra-state", "inter-state", "unknown"]] = "unknown"

class LineItem(BaseModel):
    description: Optional[str] = None
    hsn_sac: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    discount: Optional[float] = 0.0
    taxable_value: Optional[float] = None
    gst_rate: Optional[float] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    cess: Optional[float] = 0.0
    total: Optional[float] = None

class TaxSummary(BaseModel):
    taxable_amount: Optional[float] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    cess: Optional[float] = 0.0
    round_off: Optional[float] = 0.0
    total_tax: Optional[float] = None

class Totals(BaseModel):
    subtotal: Optional[float] = None
    total_discount: Optional[float] = 0.0
    grand_total: Optional[float] = None
    amount_in_words: Optional[str] = None

class ValidationResult(BaseModel):
    status: Literal["valid", "warning", "needs_review", "invalid"] = "needs_review"
    gstin_supplier_valid: Optional[bool] = None
    gstin_buyer_valid: Optional[bool] = None
    tax_calculation_valid: Optional[bool] = None
    line_items_valid: Optional[bool] = None
    grand_total_valid: Optional[bool] = None
    supply_type_consistent: Optional[bool] = None
    errors: List[str] = []
    warnings: List[str] = []

class ConfidenceScores(BaseModel):
    overall: float = 0.0
    invoice_number: Optional[float] = None
    invoice_date: Optional[float] = None
    supplier_name: Optional[float] = None
    supplier_gstin: Optional[float] = None
    buyer_name: Optional[float] = None
    buyer_gstin: Optional[float] = None
    items: Optional[float] = None
    quantities: Optional[float] = None
    unit_prices: Optional[float] = None
    total: Optional[float] = None
    review_required: bool = False
    low_confidence_fields: List[str] = []

class InvoiceRecord(BaseModel):
    document: DocumentInfo
    supplier: PartyInfo = Field(default_factory=PartyInfo)
    buyer: PartyInfo = Field(default_factory=PartyInfo)
    invoice: InvoiceMeta = Field(default_factory=InvoiceMeta)
    items: List[LineItem] = Field(default_factory=list)
    tax: TaxSummary = Field(default_factory=TaxSummary)
    totals: Totals = Field(default_factory=Totals)
    validation: ValidationResult = Field(default_factory=ValidationResult)
    confidence: ConfidenceScores = Field(default_factory=ConfidenceScores)

# API Request/Response models
class UploadResponse(BaseModel):
    document_id: str
    filename: str
    status: str
    message: str

class HumanCorrectionRequest(BaseModel):
    field_path: str       # e.g., "supplier.gstin", "items[0].unit_price"
    corrected_value: str
    document_id: str

class DocumentSummary(BaseModel):
    id: str
    filename: str
    file_type: Optional[str] = None
    source_type: Optional[str] = None
    upload_time: datetime
    status: str
    overall_confidence: float
    invoice_number: Optional[str] = None
    supplier_name: Optional[str] = None
    grand_total: Optional[float] = None
