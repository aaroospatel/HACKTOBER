import pandas as pd
import io
import uuid
from typing import Optional
from app.utils.gst_rules import COLUMN_MAPPING
from app.schemas.invoice import (
    InvoiceRecord, DocumentInfo, PartyInfo, InvoiceMeta,
    LineItem, TaxSummary, Totals, ConfidenceScores, ValidationResult
)

def _safe_float(val) -> Optional[float]:
    if val is None or pd.isna(val):
        return None
    try:
        # Strip any currency symbols or commas
        clean_val = str(val).replace(",", "").replace("₹", "").replace("$", "").strip()
        return float(clean_val)
    except (TypeError, ValueError):
        return None

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase, strip, collapse whitespace, and map columns to canonical names."""
    df = df.copy()
    cleaned_cols = []
    for col in df.columns:
        c_str = str(col).lower().strip()
        c_str = " ".join(c_str.split())
        cleaned_cols.append(c_str)
    df.columns = cleaned_cols

    rename_map = {}
    for col in df.columns:
        if col in COLUMN_MAPPING:
            rename_map[col] = COLUMN_MAPPING[col]
    return df.rename(columns=rename_map)

def _process_tabular(df: pd.DataFrame, filename: str, source_type: str) -> dict:
    df = _normalize_columns(df)
    df = df.dropna(how="all")

    if len(df) == 0:
        record = InvoiceRecord(
            document=DocumentInfo(
                id=str(uuid.uuid4()),
                filename=filename,
                source_type=source_type,
            )
        )
        return record.model_dump()

    first_row = df.iloc[0]

    def get_field(field_name, row=first_row) -> Optional[str]:
        if field_name in row and pd.notna(row[field_name]):
            val = str(row[field_name]).strip()
            return val if val != "" else None
        return None

    # Build line items
    items = []
    taxable_sum = 0.0
    cgst_sum = 0.0
    sgst_sum = 0.0
    igst_sum = 0.0

    for _, row in df.iterrows():
        desc = get_field("description", row)
        qty = _safe_float(row.get("quantity"))
        rate = _safe_float(row.get("unit_price"))
        taxable = _safe_float(row.get("taxable_value"))
        gst_r = _safe_float(row.get("gst_rate"))
        cg = _safe_float(row.get("cgst"))
        sg = _safe_float(row.get("sgst"))
        ig = _safe_float(row.get("igst"))
        item_tot = _safe_float(row.get("total"))

        # If taxable is missing but qty and rate exist
        if taxable is None and qty is not None and rate is not None:
            taxable = round(qty * rate, 2)

        # Accumulate sums
        if taxable is not None:
            taxable_sum += taxable
        if cg is not None:
            cgst_sum += cg
        if sg is not None:
            sgst_sum += sg
        if ig is not None:
            igst_sum += ig

        # Only append if row represents a genuine item
        if desc or qty or rate or taxable:
            item = LineItem(
                description=desc or "Item",
                hsn_sac=get_field("hsn_sac", row),
                quantity=qty,
                unit=get_field("unit", row) or "NOS",
                unit_price=rate,
                discount=_safe_float(row.get("discount")) or 0.0,
                taxable_value=taxable,
                gst_rate=gst_r,
                cgst=cg,
                sgst=sg,
                igst=ig,
                cess=_safe_float(row.get("cess")) or 0.0,
                total=item_tot or (round(taxable + (cg or 0) + (sg or 0) + (ig or 0), 2) if taxable is not None else None)
            )
            items.append(item)

    # Determine supplier and buyer
    supplier_gstin = get_field("supplier_gstin")
    buyer_gstin = get_field("buyer_gstin")

    # Supply type
    supply_type = "unknown"
    if supplier_gstin and buyer_gstin and len(supplier_gstin) >= 2 and len(buyer_gstin) >= 2:
        supply_type = "intra-state" if supplier_gstin[:2] == buyer_gstin[:2] else "inter-state"

    # Grand total extraction or fallback to sum
    grand_total = None
    if "grand_total" in df:
        valid_gt = df["grand_total"].dropna()
        if len(valid_gt) > 0:
            grand_total = _safe_float(valid_gt.iloc[-1])

    total_tax = round(cgst_sum + sgst_sum + igst_sum, 2)
    if grand_total is None and taxable_sum > 0:
        grand_total = round(taxable_sum + total_tax, 2)

    record = InvoiceRecord(
        document=DocumentInfo(
            id=str(uuid.uuid4()),
            filename=filename,
            source_type=source_type,
        ),
        supplier=PartyInfo(
            name=get_field("supplier_name"),
            gstin=supplier_gstin,
            state_code=supplier_gstin[:2] if supplier_gstin and len(supplier_gstin) >= 2 else None,
        ),
        buyer=PartyInfo(
            name=get_field("buyer_name"),
            gstin=buyer_gstin,
            state_code=buyer_gstin[:2] if buyer_gstin and len(buyer_gstin) >= 2 else None,
        ),
        invoice=InvoiceMeta(
            invoice_number=get_field("invoice_number"),
            invoice_date=get_field("invoice_date"),
            supply_type=supply_type,
        ),
        items=items,
        tax=TaxSummary(
            taxable_amount=round(taxable_sum, 2) if taxable_sum > 0 else None,
            cgst=round(cgst_sum, 2) if cgst_sum > 0 else None,
            sgst=round(sgst_sum, 2) if sgst_sum > 0 else None,
            igst=round(igst_sum, 2) if igst_sum > 0 else None,
            total_tax=total_tax if total_tax > 0 else None,
        ),
        totals=Totals(
            subtotal=round(taxable_sum, 2) if taxable_sum > 0 else None,
            grand_total=grand_total,
        ),
        confidence=ConfidenceScores(
            overall=0.98,
            invoice_number=0.99,
            invoice_date=0.99,
            supplier_name=0.95,
            supplier_gstin=0.99,
            buyer_name=0.95,
            buyer_gstin=0.99,
            items=0.98,
            quantities=0.99,
            unit_prices=0.99,
            total=0.99,
            review_required=False,
            low_confidence_fields=[]
        ),
        validation=ValidationResult(
            status="valid"
        )
    )
    return record.model_dump()

async def process_excel(file_bytes: bytes, filename: str) -> dict:
    """Parse Excel files into Universal InvoiceRecord."""
    df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    return _process_tabular(df, filename, "excel")
