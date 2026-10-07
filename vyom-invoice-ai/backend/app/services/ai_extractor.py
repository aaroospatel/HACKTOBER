import google.generativeai as genai
from PIL import Image
import io
import json
import re
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from app.config import settings
from app.schemas.invoice import (
    InvoiceRecord, DocumentInfo, PartyInfo, InvoiceMeta,
    LineItem, TaxSummary, Totals, ConfidenceScores, ValidationResult
)
from .ocr_service import extract_text_from_image, get_ocr_confidence_data

# Priority list of Gemini vision models
GEMINI_MODELS = [
    "gemini-3.1-flash-lite",
    "gemini-flash-latest",
    "gemini-3.5-flash",
    "gemini-2.5-flash"
]

if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

EXTRACTION_SCHEMA = """{
  "supplier": {"name": null, "gstin": null, "address": null},
  "buyer": {"name": null, "gstin": null, "address": null},
  "invoice": {
    "invoice_number": null,
    "invoice_date": null,
    "place_of_supply": null,
    "reverse_charge": false,
    "irn": null
  },
  "items": [
    {
      "description": null, "hsn_sac": null, "quantity": null,
      "unit": null, "unit_price": null, "discount": 0,
      "taxable_value": null, "gst_rate": null,
      "cgst": null, "sgst": null, "igst": null, "cess": 0, "total": null
    }
  ],
  "tax": {
    "taxable_amount": null, "cgst": null, "sgst": null,
    "igst": null, "cess": 0, "round_off": 0, "total_tax": null
  },
  "totals": {
    "subtotal": null, "grand_total": null, "amount_in_words": null
  },
  "confidence": {
    "invoice_number": 0.95, "invoice_date": 0.95,
    "supplier_name": 0.95, "supplier_gstin": 0.95,
    "buyer_name": 0.95, "buyer_gstin": 0.95,
    "items": 0.90, "quantities": 0.90, "unit_prices": 0.90, "total": 0.95
  }
}"""

IMAGE_PROMPT = f"""You are an expert GST invoice document intelligence system for India.
Extract all financial, tax, party, and line item details from this invoice image.

CRITICAL RULES:
1. Extract ONLY what is visible. Do NOT invent or guess values.
2. If unreadable or missing, return null for that field.
3. Preserve invoice numbers, GSTINs, and HSN/SAC codes EXACTLY as written.
4. Extract ALL line items (description, qty, rate, taxable value, GST rate, CGST, SGST, IGST, total).
5. Extract CGST, SGST, and IGST amounts separately.
6. Return confidence scores (0.0 to 1.0) for fields.
7. For handwritten digits, pay close attention to: 0 vs O, 1 vs I, 5 vs S, 8 vs B.

Return ONLY valid JSON matching this schema (no markdown, no conversational text):
{EXTRACTION_SCHEMA}"""

TEXT_PROMPT_TEMPLATE = """You are an expert GST invoice data extraction system for India.
Structure this invoice text into the required JSON schema.

RULES:
1. Extract ONLY information present in the text.
2. Missing or unmentioned fields must be null.
3. Preserve all numbers, GSTINs, and codes exactly.

Return ONLY valid JSON:
{schema}

INVOICE TEXT:
{text}"""

def _parse_ai_response(response_text: str) -> dict:
    """Parse Gemini response, extracting JSON even if enclosed in markdown code fences."""
    text = response_text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}

def _build_invoice_record(extracted: dict, filename: str, source_type: str, page_count: int = 1) -> dict:
    """Build a full validated InvoiceRecord dict from extracted AI or OCR data."""
    supplier_data = extracted.get("supplier", {}) or {}
    buyer_data = extracted.get("buyer", {}) or {}
    invoice_data = extracted.get("invoice", {}) or {}
    items_data = extracted.get("items", []) or []
    tax_data = extracted.get("tax", {}) or {}
    totals_data = extracted.get("totals", {}) or {}
    conf_data = extracted.get("confidence", {}) or {}

    items = []
    for item in items_data:
        if isinstance(item, dict):
            filtered = {k: v for k, v in item.items() if k in LineItem.model_fields}
            items.append(LineItem(**filtered))

    supplier_gstin = supplier_data.get("gstin") or ""
    buyer_gstin = buyer_data.get("gstin") or ""
    supply_type = "unknown"
    if len(supplier_gstin) >= 2 and len(buyer_gstin) >= 2:
        supply_type = "intra-state" if supplier_gstin[:2] == buyer_gstin[:2] else "inter-state"

    overall_conf = float(conf_data.get("overall", 0.92))

    record = InvoiceRecord(
        document=DocumentInfo(
            id=str(uuid.uuid4()),
            filename=filename,
            source_type=source_type,
            upload_time=datetime.now(timezone.utc),
            page_count=page_count,
        ),
        supplier=PartyInfo(
            name=supplier_data.get("name"),
            gstin=supplier_data.get("gstin"),
            address=supplier_data.get("address"),
            state_code=supplier_gstin[:2] if len(supplier_gstin) >= 2 else None
        ),
        buyer=PartyInfo(
            name=buyer_data.get("name"),
            gstin=buyer_data.get("gstin"),
            address=buyer_data.get("address"),
            state_code=buyer_gstin[:2] if len(buyer_gstin) >= 2 else None
        ),
        invoice=InvoiceMeta(
            invoice_number=invoice_data.get("invoice_number"),
            invoice_date=invoice_data.get("invoice_date"),
            place_of_supply=invoice_data.get("place_of_supply"),
            reverse_charge=invoice_data.get("reverse_charge", False),
            irn=invoice_data.get("irn"),
            supply_type=supply_type,
        ),
        items=items,
        tax=TaxSummary(**{k: v for k, v in tax_data.items() if k in TaxSummary.model_fields}),
        totals=Totals(**{k: v for k, v in totals_data.items() if k in Totals.model_fields}),
        confidence=ConfidenceScores(
            overall=overall_conf,
            invoice_number=conf_data.get("invoice_number", 0.95),
            invoice_date=conf_data.get("invoice_date", 0.95),
            supplier_name=conf_data.get("supplier_name", 0.95),
            supplier_gstin=conf_data.get("supplier_gstin", 0.95),
            buyer_name=conf_data.get("buyer_name", 0.95),
            buyer_gstin=conf_data.get("buyer_gstin", 0.95),
            items=conf_data.get("items", 0.90),
            quantities=conf_data.get("quantities", 0.90),
            unit_prices=conf_data.get("unit_prices", 0.90),
            total=conf_data.get("total", 0.95),
            review_required=overall_conf < 0.70,
            low_confidence_fields=[k for k, v in conf_data.items() if isinstance(v, (int, float)) and v < 0.70]
        ),
    )
    return record.model_dump()

async def extract_from_image(
    image_bytes: bytes,
    filename: str,
    source_type: str,
    additional_pages: list = None,
    page_count: int = 1
) -> dict:
    """Extract invoice data from image using Gemini Vision cascade with OCR fallback."""
    pil_img = Image.open(io.BytesIO(image_bytes))

    if settings.gemini_api_key and not settings.gemini_api_key.startswith("your_"):
        content_parts = [IMAGE_PROMPT, pil_img]
        if additional_pages:
            for p_bytes in additional_pages[:5]:
                content_parts.append(Image.open(io.BytesIO(p_bytes)))

        for model_name in GEMINI_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(content_parts)
                extracted = _parse_ai_response(response.text)
                if extracted:
                    return _build_invoice_record(extracted, filename, source_type, page_count)
            except Exception:
                continue

    # Fallback to OCR service
    ocr_data = get_ocr_confidence_data(pil_img)
    raw_text = ocr_data.get("raw_text", "")
    return _build_fallback_record(raw_text, filename, source_type, page_count, ocr_data.get("average_confidence", 0.70))

async def extract_from_text(
    text: str,
    filename: str,
    source_type: str,
    page_count: int = 1
) -> dict:
    """Extract invoice data from digital text using Gemini LLM cascade with regex fallback."""
    if settings.gemini_api_key and not settings.gemini_api_key.startswith("your_"):
        prompt = TEXT_PROMPT_TEMPLATE.format(
            schema=EXTRACTION_SCHEMA,
            text=text[:12000]
        )
        for model_name in GEMINI_MODELS:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(prompt)
                extracted = _parse_ai_response(response.text)
                if extracted:
                    return _build_invoice_record(extracted, filename, source_type, page_count)
            except Exception:
                continue

    return _build_fallback_record(text, filename, source_type, page_count, 0.85)

def _build_fallback_record(text: str, filename: str, source_type: str, page_count: int, confidence: float) -> dict:
    """Heuristic fallback extraction from raw text when AI API is unavailable."""
    inv_num_match = re.search(r'(?:invoice|inv|bill)\s*(?:no\.?|#|number)?[:\s]*([A-Z0-9\-\/]+)', text, re.IGNORECASE)
    gstin_matches = re.findall(r'[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]', text)
    date_match = re.search(r'\b(\d{1,2}[\/\-\.]\d{1,2}[\/\-\.]\d{2,4})\b', text)
    total_match = re.search(r'(?:grand\s+total|total\s+amount|total)[\s:₹Rs\.]*([0-9,]+\.?[0-9]*)', text, re.IGNORECASE)

    extracted = {
        "invoice": {
            "invoice_number": inv_num_match.group(1) if inv_num_match else None,
            "invoice_date": date_match.group(1) if date_match else None,
        },
        "supplier": {
            "gstin": gstin_matches[0] if len(gstin_matches) > 0 else None,
        },
        "buyer": {
            "gstin": gstin_matches[1] if len(gstin_matches) > 1 else None,
        },
        "totals": {
            "grand_total": float(total_match.group(1).replace(",", "")) if total_match else None,
        },
        "confidence": {
            "overall": confidence
        }
    }
    return _build_invoice_record(extracted, filename, source_type, page_count)
