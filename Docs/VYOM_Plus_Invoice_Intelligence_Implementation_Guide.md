# VYOM+ — End-to-End AI-Powered GST Invoice Intelligence System

## Hackathon Implementation Guide

> **Goal:** Build a complete document-intelligence platform that accepts Excel, CSV, PDF, JPG/JPEG, and PNG invoice documents, extracts GST and financial information, validates it, assigns confidence, supports human review, and exports standardized machine-readable records.

---

# 1. Product Vision

## VYOM+ Invoice Intelligence

### Tagline

**From messy invoices to validated financial data.**

VYOM+ should not be positioned as merely an OCR application.

The core product is:

```text
Document
   ↓
File Type Detection
   ↓
Document Processing
   ↓
OCR / Vision AI
   ↓
Invoice Understanding
   ↓
Structured JSON
   ↓
GST + Mathematical Validation
   ↓
Confidence Scoring
   ↓
Human Review when Necessary
   ↓
Validated Financial Record
   ↓
JSON / CSV / Excel
```

The central idea is:

> **VYOM+ doesn't simply read invoices. It understands, validates, and knows when it may be wrong.**

---

# 2. Problem Statement Requirements

The system must support:

- Excel (.xlsx)
- CSV
- PDF
- JPEG / JPG
- PNG

The system must:

- Identify input type.
- Route the document through the appropriate pipeline.
- Process Excel/CSV into structured tabular data.
- Process PDFs/images using OCR and/or vision AI.
- Extract invoice, GST, tax, financial, and line-item information.
- Validate extracted values.
- Identify inconsistent or uncertain information.
- Produce machine-readable JSON and/or structured tabular output.
- Provide an interface for uploading documents and inspecting results.
- Perform strongly on printed and digitally generated invoices.
- Give special attention to handwritten GST invoices.

---

# 3. Recommended Technology Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js + React + TypeScript |
| Styling | Tailwind CSS |
| Backend | Python + FastAPI |
| AI | Multimodal Vision LLM |
| OCR | Vision/OCR pipeline |
| Image Processing | OpenCV + Pillow |
| PDF Processing | PyMuPDF |
| Tabular Processing | Pandas + OpenPyXL |
| Validation | Python + Pydantic |
| Database | SQLite for MVP / PostgreSQL for deployment |
| Output | JSON + CSV + XLSX |
| Frontend Deployment | Vercel |
| Backend Deployment | Render / Railway / similar |
| Database Deployment | PostgreSQL / Supabase |

---

# 4. Overall System Architecture

```text
                    ┌──────────────────┐
                    │   Upload Invoice  │
                    │ PDF/JPG/PNG/XLSX  │
                    │       /CSV        │
                    └─────────┬────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │ File Type Router  │
                    └───────┬──────────┘
                            │
          ┌─────────────────┼─────────────────┐
          │                 │                 │
          ▼                 ▼                 ▼
     Excel / CSV       PDF / Digital     JPG / PNG / Scan
          │                 │                 │
          ▼                 ▼                 ▼
    Pandas parser       PDF → images      Image preprocessing
          │                 │                 │
          │                 ▼                 ▼
          │             Vision/OCR       Vision/OCR
          │                 │                 │
          └─────────────────┼─────────────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Invoice AI Extractor│
                 │ Structured JSON     │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ GST Validation      │
                 │ Math Validation      │
                 │ Confidence Scoring   │
                 └──────────┬──────────┘
                            ▼
                 ┌─────────────────────┐
                 │ Human Review        │
                 │ Fix uncertain data  │
                 └──────────┬──────────┘
                            ▼
              ┌────────────────────────────┐
              │ JSON / Excel / CSV Export  │
              └────────────────────────────┘
```

---

# 5. What the Website Should Contain

The website should have at least five major areas:

1. Dashboard
2. Upload
3. Documents
4. Invoice Extraction / Review
5. Analytics

---

# 6. Dashboard

Example:

```text
┌───────────────────────────────────────────────────────────┐
│ VYOM+ Invoice Intelligence                    + Upload     │
├──────────────┬──────────────┬──────────────┬─────────────┤
│ 128          │ 113          │ 15           │ 94.2%       │
│ Documents    │ Validated    │ Review       │ Avg Accuracy│
├──────────────┴──────────────┴──────────────┴─────────────┤
│                                                           │
│ Recent Documents                                          │
│                                                           │
│ invoice_001.pdf     ₹12,450    98%     ✓ Valid            │
│ handwritten.jpg     ₹8,200     74%     ⚠ Review           │
│ sales.xlsx          ₹45,210    100%    ✓ Valid            │
│ invoice_004.png     ₹7,840     91%     ✓ Valid            │
│                                                           │
└───────────────────────────────────────────────────────────┘
```

Dashboard metrics:

- Total documents processed
- Successful extractions
- Documents needing review
- Average confidence
- GST errors detected
- Recent documents
- Document type distribution
- Extraction quality by document type

Only show performance numbers based on your actual evaluation dataset.

---

# 7. Upload Page

Support drag-and-drop:

```text
╔══════════════════════════════════════════╗
║                                          ║
║       Drop your invoice here             ║
║                                          ║
║       or click to browse                 ║
║                                          ║
║  PDF • JPG • PNG • XLSX • CSV            ║
║                                          ║
╚══════════════════════════════════════════╝
```

Processing stages:

```text
invoice.jpg
Handwritten GST Invoice

[ Processing... ]

✓ File identified
✓ Image enhanced
✓ Invoice detected
✓ Data extracted
✓ GST validated
✓ Confidence calculated
```

---

# 8. Extraction Result Page

Use a two-column layout.

Left:

- Original document
- PDF/image viewer
- Page navigation for multi-page PDFs

Right:

- Invoice fields
- Supplier
- Buyer
- Invoice metadata
- Line items
- GST summary
- Totals
- Validation
- Confidence
- Export buttons

Example:

```text
┌─────────────────────┬────────────────────────────────────┐
│                     │ Invoice Information                │
│                     │                                    │
│   ORIGINAL          │ Invoice No: INV-1023               │
│   INVOICE           │ Date: 04/10/2026                   │
│                     │                                    │
│                     │ Supplier                           │
│                     │ ABC Enterprises                    │
│                     │ GSTIN: 27ABCDE1234F1Z5             │
│                     │                                    │
│                     │ Customer                           │
│                     │ XYZ Pvt Ltd                        │
│                     │ GSTIN: 27AAAAA1234A1Z1             │
│                     │                                    │
│                     │ Items                              │
│                     │ Product  Qty Rate GST Amount       │
│                     │ Laptop   2   50000 18% 118000      │
│                     │                                    │
│                     │ Subtotal: ₹100,000                 │
│                     │ CGST: ₹9,000                       │
│                     │ SGST: ₹9,000                       │
│                     │ Total: ₹118,000                    │
└─────────────────────┴────────────────────────────────────┘
```

---

# 9. Confidence Visualization

Every important field should have a confidence score.

Example:

```text
GSTIN:             99% 🟢
Invoice Number:    97% 🟢
Date:              98% 🟢
Quantity:           82% 🟡
Rate:               61% 🔴
```

Suggested thresholds:

```text
> 90%      High confidence
70–90%     Review / warning
< 70%      Human review
```

These thresholds should be tuned against your test dataset.

---

# 10. Project Repository Structure

Recommended structure:

```text
vyom-invoice-ai/
│
├── frontend/
│   ├── app/
│   │   ├── page.tsx
│   │   ├── upload/
│   │   │   └── page.tsx
│   │   ├── documents/
│   │   │   └── page.tsx
│   │   └── documents/
│   │       └── [id]/
│   │           └── page.tsx
│   │
│   ├── components/
│   │   ├── UploadBox.tsx
│   │   ├── ProcessingSteps.tsx
│   │   ├── InvoiceViewer.tsx
│   │   ├── InvoiceFields.tsx
│   │   ├── LineItems.tsx
│   │   ├── ConfidenceBadge.tsx
│   │   ├── ValidationPanel.tsx
│   │   └── ExportButtons.tsx
│   │
│   └── lib/
│       └── api.ts
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   │
│   │   ├── routers/
│   │   │   ├── upload.py
│   │   │   ├── invoice.py
│   │   │   └── export.py
│   │   │
│   │   ├── services/
│   │   │   ├── router.py
│   │   │   ├── excel_processor.py
│   │   │   ├── csv_processor.py
│   │   │   ├── pdf_processor.py
│   │   │   ├── image_processor.py
│   │   │   ├── ocr.py
│   │   │   ├── extractor.py
│   │   │   ├── validator.py
│   │   │   └── confidence.py
│   │   │
│   │   ├── schemas/
│   │   │   └── invoice.py
│   │   │
│   │   ├── database/
│   │   │   └── models.py
│   │   │
│   │   └── utils/
│   │       └── helpers.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── sample_invoices/
│   ├── printed/
│   ├── handwritten/
│   ├── pdf/
│   └── excel/
│
└── README.md
```

---

# 11. Universal Invoice Schema

Regardless of whether the source is:

- Excel
- CSV
- PDF
- JPG
- PNG

everything should eventually become the same standardized JSON structure.

Example:

```json
{
  "document": {
    "filename": "invoice_001.jpg",
    "document_type": "invoice",
    "source_type": "image"
  },

  "supplier": {
    "name": "ABC Enterprises",
    "gstin": "27ABCDE1234F1Z5",
    "address": "Nagpur, Maharashtra"
  },

  "buyer": {
    "name": "XYZ Pvt Ltd",
    "gstin": "27AAAAA1234A1Z1",
    "address": "Mumbai, Maharashtra"
  },

  "invoice": {
    "invoice_number": "INV-1023",
    "invoice_date": "2026-10-04",
    "place_of_supply": "Maharashtra"
  },

  "items": [
    {
      "description": "Laptop",
      "hsn_sac": "8471",
      "quantity": 2,
      "unit": "PCS",
      "unit_price": 50000,
      "taxable_value": 100000,
      "gst_rate": 18,
      "cgst": 9000,
      "sgst": 9000,
      "igst": 0,
      "total": 118000
    }
  ],

  "tax": {
    "taxable_amount": 100000,
    "cgst": 9000,
    "sgst": 9000,
    "igst": 0,
    "cess": 0,
    "total_tax": 18000
  },

  "totals": {
    "subtotal": 100000,
    "grand_total": 118000
  },

  "validation": {
    "status": "valid",
    "errors": [],
    "warnings": []
  },

  "confidence": {
    "overall": 0.96,
    "invoice_number": 0.97,
    "gstin": 0.99,
    "date": 0.98,
    "items": 0.92,
    "total": 0.99
  }
}
```

---

# 12. Pydantic Schema

Create:

```text
backend/app/schemas/invoice.py
```

Example:

```python
from pydantic import BaseModel
from typing import Optional, List


class Supplier(BaseModel):
    name: Optional[str] = None
    gstin: Optional[str] = None
    address: Optional[str] = None


class Buyer(BaseModel):
    name: Optional[str] = None
    gstin: Optional[str] = None
    address: Optional[str] = None


class InvoiceItem(BaseModel):
    description: Optional[str] = None
    hsn_sac: Optional[str] = None
    quantity: Optional[float] = None
    unit: Optional[str] = None
    unit_price: Optional[float] = None
    taxable_value: Optional[float] = None
    gst_rate: Optional[float] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    total: Optional[float] = None


class Invoice(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[str] = None
    place_of_supply: Optional[str] = None


class Tax(BaseModel):
    taxable_amount: Optional[float] = None
    cgst: Optional[float] = None
    sgst: Optional[float] = None
    igst: Optional[float] = None
    cess: Optional[float] = None
    total_tax: Optional[float] = None


class Totals(BaseModel):
    subtotal: Optional[float] = None
    grand_total: Optional[float] = None


class InvoiceRecord(BaseModel):
    supplier: Supplier
    buyer: Buyer
    invoice: Invoice
    items: List[InvoiceItem]
    tax: Tax
    totals: Totals
```

Later extend the schema with validation and confidence information.

---

# 13. Backend Setup

```bash
mkdir vyom-invoice-ai
cd vyom-invoice-ai

mkdir backend
cd backend

python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install fastapi uvicorn python-multipart
pip install pandas openpyxl
pip install pillow opencv-python
pip install pymupdf
pip install pydantic
pip install python-dotenv
pip install openai
```

Run:

```bash
uvicorn app.main:app --reload
```

---

# 14. File Type Router

The router determines which pipeline to use.

```text
xlsx → Excel processor
csv  → CSV processor
pdf  → PDF processor
jpg  → Image processor
jpeg → Image processor
png  → Image processor
```

Conceptually:

```python
if ext == "xlsx":
    return process_excel(file)

elif ext == "csv":
    return process_csv(file)

elif ext == "pdf":
    return process_pdf(file)

elif ext in ["jpg", "jpeg", "png"]:
    return process_image(file)

else:
    raise ValueError("Unsupported file")
```

---

# 15. Excel Processing Pipeline

Excel does not require OCR.

Pipeline:

```text
XLSX
 ↓
Pandas
 ↓
Read sheets
 ↓
Detect headers
 ↓
Normalize columns
 ↓
Map columns
 ↓
Universal invoice schema
```

Example input:

```text
invoice_no | date | seller | gstin | item | qty | rate | tax
```

Normalize to:

```text
invoice_number
invoice_date
supplier
gstin
description
quantity
unit_price
gst_rate
```

Column mapping:

```python
COLUMN_MAPPING = {
    "invoice no": "invoice_number",
    "invoice number": "invoice_number",
    "inv no": "invoice_number",
    "date": "invoice_date",
    "gstin": "gstin",
    "seller": "supplier",
    "vendor": "supplier",
    "item": "description",
    "product": "description",
    "qty": "quantity",
    "rate": "unit_price"
}
```

---

# 16. CSV Processing Pipeline

Pipeline:

```text
CSV
 ↓
Pandas
 ↓
Normalize column names
 ↓
Detect invoice fields
 ↓
Universal schema
```

Example:

```python
df = pd.read_csv(file)

df.columns = (
    df.columns
      .str.lower()
      .str.strip()
      .str.replace(" ", "_")
)
```

Then map columns to the universal schema.

---

# 17. PDF Processing Pipeline

There are two major PDF types.

## Digital PDF

```text
PDF
 ↓
PyMuPDF
 ↓
Extract text
 ↓
AI extraction
 ↓
JSON
```

## Scanned PDF

```text
PDF
 ↓
Render pages
 ↓
Images
 ↓
Image preprocessing
 ↓
Vision/OCR
 ↓
AI extraction
 ↓
JSON
```

The system should automatically distinguish between text-based and scanned PDFs.

---

# 18. Image Preprocessing

Especially important for handwritten invoices.

Pipeline:

```text
Camera photo
 ↓
Resize
 ↓
Grayscale
 ↓
Contrast enhancement
 ↓
Noise removal
 ↓
Deskew
 ↓
Perspective correction
 ↓
OCR / Vision
```

Useful OpenCV operations:

```text
cv2.cvtColor()
cv2.resize()
cv2.GaussianBlur()
cv2.threshold()
cv2.adaptiveThreshold()
```

Do not blindly threshold every image.

For handwriting, aggressive binarization can destroy useful strokes.

Create multiple versions:

```text
image_original
image_enhanced
image_grayscale
image_threshold
```

Use the best version or multiple versions for extraction.

---

# 19. Handwritten Invoice Strategy

Handwritten invoice processing should be a major differentiator.

Do not claim simply:

> "Our OCR recognizes handwriting."

Instead describe the system as:

> **A multi-stage visual document intelligence pipeline with preprocessing, semantic invoice understanding, confidence estimation, and deterministic validation.**

Pipeline:

```text
Handwritten invoice
        │
        ▼
Image quality analysis
        │
        ├── blurry?
        ├── tilted?
        ├── low contrast?
        └── shadows?
        │
        ▼
Adaptive preprocessing
        │
        ▼
Vision model
        │
        ▼
Invoice schema extraction
        │
        ▼
GST/math validation
        │
        ▼
Confidence scoring
        │
        ├── HIGH → automatically approve
        │
        └── LOW → human review
```

The system should explicitly allow uncertainty rather than pretending AI is always correct.

---

# 20. AI Extraction

Give the vision model the invoice image/document and a strict extraction prompt.

Example:

```text
You are an invoice document intelligence system.

Extract financial and GST information from this invoice.

Important rules:

1. Do not invent missing values.
2. If a field cannot be read, return null.
3. Preserve invoice numbers exactly.
4. Extract all line items.
5. Extract GSTINs exactly as visible.
6. Extract HSN/SAC if present.
7. Extract CGST, SGST, IGST and cess separately.
8. Calculate nothing unless explicitly requested.
9. Return the result using the supplied JSON schema.
10. Include confidence values for uncertain fields.
```

Use structured output / JSON schema enforcement where supported.

---

# 21. AI Should Extract; Code Should Validate

Do not use AI for deterministic calculations.

Example:

AI extracts:

```text
quantity = 2
unit_price = 50000
taxable_value = 100000
```

Python checks:

```text
2 × 50,000 = 100,000
```

Then:

```text
GST = 18%

100,000 × 18% = 18,000
```

Then:

```text
CGST = 9,000
SGST = 9,000

Total = 118,000
```

If invoice total is:

```text
128,000
```

report:

```text
⚠ TOTAL MISMATCH

Expected: ₹118,000
Invoice:  ₹128,000
Difference: ₹10,000
```

This is one of the strongest aspects of the project.

---

# 22. GST Validation Engine

Create:

```text
backend/app/services/validator.py
```

Validate:

- GSTIN format
- GST rate
- CGST
- SGST
- IGST
- Cess
- Taxable amount
- Tax totals
- Grand total
- Line-item calculations

## GSTIN

Perform format validation:

```text
length
state code
format
characters
```

Important:

A regex/format check does not prove that a GSTIN is officially registered.

Report:

```text
GSTIN format: VALID
```

rather than:

```text
GSTIN officially verified
```

unless an authorized verification service is actually used.

---

# 23. Tax Validation

If:

```text
Taxable value = ₹10,000
GST = 18%
```

Expected tax:

```text
₹1,800
```

For intra-state:

```text
CGST = ₹900
SGST = ₹900
```

For inter-state:

```text
IGST = ₹1,800
```

Compare these against extracted values.

---

# 24. Line Item Validation

For every item:

```text
quantity × unit price
```

should approximately equal:

```text
taxable value
```

Use a small rounding tolerance.

Example:

```python
abs(calculated - extracted) <= 1
```

Adjust the tolerance according to the invoice currency and rounding behavior.

---

# 25. Invoice Total Validation

Check:

```text
sum(line items)
+ tax
+ additional charges
- discounts
= grand total
```

Example response:

```json
{
  "status": "warning",
  "errors": [
    {
      "field": "grand_total",
      "message": "Grand total does not match calculated total"
    }
  ]
}
```

---

# 26. Confidence Engine

Confidence should combine multiple signals:

```text
Field confidence
        │
        ├── AI extraction confidence
        ├── format validation
        ├── mathematical validation
        └── cross-field consistency
```

Example:

```text
GSTIN

AI confidence             0.97
Format valid              1.00
Cross-field consistency   1.00

Final confidence          0.98
```

For a difficult handwritten field:

```text
Unit price

AI confidence             0.62
Math validation            0.40
Cross-field consistency    0.50

Final confidence           0.51
```

Then:

```text
< 0.70 → Human review
0.70–0.90 → Warning
> 0.90 → Automatically accepted
```

These values should be tuned against real test data.

---

# 27. Human-in-the-Loop Review

If confidence is low, show:

```text
⚠ This field has low confidence.

Unit price

[ 5000              ]

[Accept] [Edit]
```

After correction:

```text
Revalidate
```

Then recalculate:

- Taxable value
- GST
- Total
- Validation status
- Confidence/review status

This turns VYOM+ into a practical accounting workflow.

---

# 28. Explainable Extraction

Add:

```text
Why is this field uncertain?
```

Example:

```text
Unit price

Confidence: 61%

Reason:
The handwritten digit after "5" was partially obscured.

The value was cross-checked against:
• quantity
• taxable value
• GST amount

Recommended review.
```

---

# 29. API Endpoints

Recommended API structure:

```text
POST /api/upload
```

Upload document.

```text
GET /api/documents
```

Get processed documents.

```text
GET /api/documents/{id}
```

Get extracted invoice.

```text
POST /api/documents/{id}/validate
```

Run validation.

```text
PUT /api/documents/{id}
```

Save human corrections.

```text
GET /api/documents/{id}/json
```

Download JSON.

```text
GET /api/documents/{id}/csv
```

Download CSV.

```text
GET /api/documents/{id}/excel
```

Download Excel.

---

# 30. Upload Endpoint Concept

Example:

```python
@app.post("/api/upload")
async def upload_invoice(file: UploadFile):

    filename = file.filename.lower()

    if filename.endswith(".xlsx"):
        result = process_excel(file)

    elif filename.endswith(".csv"):
        result = process_csv(file)

    elif filename.endswith(".pdf"):
        result = process_pdf(file)

    elif filename.endswith((".jpg", ".jpeg", ".png")):
        result = process_image(file)

    else:
        raise HTTPException(
            status_code=400,
            detail="Unsupported file format"
        )

    validated = validate_invoice(result)

    return validated
```

---

# 31. Frontend Setup

Create:

```bash
npx create-next-app@latest frontend
```

Recommended:

```text
TypeScript
Tailwind CSS
App Router
```

Run:

```bash
cd frontend
npm run dev
```

Frontend communicates with the FastAPI backend during development.

---

# 32. Frontend Routes

```text
/
```

Dashboard.

```text
/upload
```

Upload page.

```text
/documents
```

Document list.

```text
/documents/[id]
```

Detailed extraction and review.

---

# 33. SaaS-Style UI

The UI should look like enterprise document-intelligence software, not a basic college project.

Recommended visual style:

- Dark navy / white
- Purple or blue accent
- Cards
- Rounded corners
- Subtle shadows
- Clean typography
- Responsive layout

Header:

```text
VYOM+
Invoice Intelligence

Dashboard   Documents   Analytics
                         Upload
```

---

# 34. Processing Animation

Display real pipeline stages:

```text
Analyzing invoice...

✓ File identified
✓ Document quality checked
✓ Invoice region detected
✓ OCR / Vision extraction completed
✓ GST fields extracted
✓ Line items identified
✓ Mathematical validation completed
✓ Confidence calculated

98% confidence
```

The frontend should reflect actual backend stages where possible instead of showing a fake long animation.

---

# 35. Analytics Dashboard

Example:

```text
Documents processed       1,284
Valid invoices             1,121
Needs review                 163
Average confidence          94.7%
GST mismatches               42
```

Document type chart:

```text
PDF       █████████████
Images    █████████
Excel     █████
CSV       ███
```

Extraction quality:

```text
Printed        97.8%
Digital PDF    99.1%
Handwritten    86.3%
```

Only use actual measured values from your evaluation dataset.

---

# 36. Database Design

For the MVP, SQLite is enough.

For deployment, PostgreSQL is recommended.

## documents

```text
id
filename
file_type
upload_time
status
confidence
created_at
```

## invoices

```text
id
document_id
invoice_number
invoice_date
supplier_name
supplier_gstin
buyer_name
buyer_gstin
subtotal
total_tax
grand_total
validation_status
```

## invoice_items

```text
id
invoice_id
description
hsn_sac
quantity
unit_price
taxable_value
gst_rate
cgst
sgst
igst
total
```

---

# 37. JSON Export

Button:

```text
↓ Download JSON
```

Example:

```json
{
  "invoice_number": "INV-1002",
  "date": "2026-10-04",
  "supplier": {
    "name": "ABC Enterprises",
    "gstin": "27ABCDE1234F1Z5"
  },
  "items": [],
  "tax": {},
  "totals": {},
  "validation": {}
}
```

---

# 38. Excel Export

Create:

```text
invoice.xlsx
```

with:

### Sheet 1 — Invoice

Invoice metadata.

### Sheet 2 — Items

All line items.

### Sheet 3 — Validation

Errors, warnings, and checks.

### Sheet 4 — Confidence

Field-level confidence values.

This gives the output a strong accounting-workflow feel.

---

# 39. Multi-Page Invoice Support

A PDF may contain:

```text
Page 1 → Invoice header
Page 2 → 30 line items
Page 3 → GST summary
```

Do not treat these as three separate invoices.

Pipeline:

```text
PDF
 ↓
Pages
 ↓
Page-level extraction
 ↓
Combine
 ↓
Single invoice
 ↓
Validate
```

Store source pages:

```json
{
  "source_pages": [1, 2, 3]
}
```

---

# 40. Indian GST Fields to Support

Recommended fields:

```text
Invoice number
Invoice date

Supplier name
Supplier GSTIN
Supplier address

Buyer name
Buyer GSTIN
Buyer address

Place of supply

Reverse charge
IRN / e-invoice information if present
QR-related information if present

HSN/SAC
Description
Quantity
Unit
Rate

Discount
Taxable value

CGST
SGST
IGST
Cess

Subtotal
Round-off
Grand total

Amount in words
Payment terms
Bank information if present
```

Do not make every field mandatory. Missing fields should generally become `null` rather than being invented.

---

# 41. QR Code Support

Optional high-value feature:

```text
Invoice image
       ↓
QR detection
       ↓
Decode
       ↓
Extract embedded information
       ↓
Compare against AI extraction
```

Example:

```text
AI GSTIN      = 27ABCDE1234F1Z5
QR GSTIN      = 27ABCDE1234F1Z5

✓ Match
```

QR information can become an independent validation signal.

---

# 42. Three-Source Validation

A strong architecture:

```text
            ┌───────────────┐
            │ Vision / OCR  │
            └───────┬───────┘
                    │
                    ▼
            Extracted invoice
                    │
          ┌─────────┼──────────┐
          ↓         ↓          ↓
       AI data   GST rules   Math rules
          │         │          │
          └─────────┼──────────┘
                    ↓
             Confidence Engine
                    ↓
             Final Record
```

Optional fourth signal:

```text
QR data
```

---

# 43. Duplicate Invoice Detection

Add a future feature:

Store:

```text
invoice number
supplier GSTIN
invoice date
grand total
```

If the same invoice appears again:

```text
⚠ Possible duplicate invoice

Invoice: INV-1023
Supplier: ABC Enterprises
Date: 04/10/2026
Amount: ₹118,000

Existing document found.
```

---

# 44. Invoice Anomaly Detection

Examples:

```text
⚠ Unusual GST rate detected
```

```text
⚠ CGST + SGST ≠ GST
```

```text
⚠ Taxable amount × GST rate ≠ tax amount
```

```text
⚠ Grand total does not match calculated total
```

```text
⚠ Possible duplicate invoice
```

Use deterministic rules wherever possible.

---

# 45. Document Intelligence Pipeline Screen

A dedicated visual pipeline page can show:

```text
                    INVOICE PROCESSING PIPELINE

┌─────────┐
│ Upload  │
└────┬────┘
     ↓
┌─────────────┐
│ File Router │
└────┬────────┘
     ↓
┌───────────────────────┐
│ Document Preprocessor │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ OCR / Vision Model    │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ Invoice Extraction    │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ Schema Normalization  │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ GST Validation        │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ Confidence Engine     │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ Human Review          │
└──────────┬────────────┘
           ↓
┌───────────────────────┐
│ JSON / Excel / CSV    │
└───────────────────────┘
```

---

# 46. Team Division

For a 4-person team:

## Person 1 — AI / Document Processing

Responsible for:

- PDF
- Image
- OCR
- Vision AI
- Extraction
- Handwriting pipeline

## Person 2 — Backend

Responsible for:

- FastAPI
- Database
- Validation
- Export
- APIs

## Person 3 — Frontend

Responsible for:

- Dashboard
- Upload
- Extraction result
- Review interface
- Analytics
- UI polish

## Person 4 — Testing / AI / Presentation

Responsible for:

- Handwritten test dataset
- Evaluation
- Demo invoices
- Testing
- Documentation
- Presentation
- Pitch

---

# 47. Development Order

Do not build everything simultaneously.

## Phase 1 — Basic Website

Build:

```text
Next.js
 ↓
Upload page
 ↓
FastAPI
```

---

## Phase 2 — Excel / CSV

Make:

```text
XLSX
CSV
```

work first.

---

## Phase 3 — Printed Image

Build:

```text
invoice.jpg
 ↓
Vision
 ↓
JSON
```

---

## Phase 4 — PDF

Build:

```text
PDF
 ↓
pages
 ↓
Vision
 ↓
JSON
```

---

## Phase 5 — Validation

Add:

```text
GSTIN
Math
Totals
Tax
```

---

## Phase 6 — Confidence

Add:

```text
field confidence
overall confidence
review status
```

---

## Phase 7 — Handwriting

Optimize:

```text
preprocessing
multi-pass vision
uncertainty
human review
```

---

## Phase 8 — Export

Add:

```text
JSON
CSV
Excel
```

---

## Phase 9 — UI Polish

Add:

```text
dashboard
charts
animations
responsive design
```

---

# 48. What NOT to Build Initially

Avoid:

- User authentication
- Complex microservices
- Kubernetes
- Redis
- Celery
- Custom transformer training
- Fine-tuning an OCR model
- Blockchain
- Mobile app
- Complex accounting integration
- Huge database architecture

For a hackathon, prioritize a reliable working demo.

---

# 49. MVP Definition

The MVP must be able to do:

## Input

```text
handwritten.jpg
```

## Processing

```text
Upload
 ↓
Detect image
 ↓
Preprocess
 ↓
Vision extraction
 ↓
Structured JSON
 ↓
GST validation
 ↓
Confidence
```

## Output

```text
Supplier: ABC Enterprises
GSTIN: 27ABCDE1234F1Z5

Invoice: INV-1002
Date: 04/10/2026

Items:
Laptop × 2
₹50,000 each

Taxable: ₹100,000
CGST: ₹9,000
SGST: ₹9,000

Total: ₹118,000

Confidence: 94%

Status: ✓ VALID
```

---

# 50. Recommended Demo Flow

Use this exact sequence for the hackathon presentation.

## Demo 1 — Printed Invoice

Upload:

```text
printed_invoice.pdf
```

Show:

```text
98% confidence
✓ Valid
```

Then show JSON.

---

## Demo 2 — Excel

Upload:

```text
sales.xlsx
```

Show:

```text
Detected tabular document

✓ Records normalized
✓ GST fields mapped
✓ Records validated
```

Use actual counts from your test file.

---

## Demo 3 — Handwritten Invoice

This should be the hero demo.

Upload a messy handwritten invoice.

Show:

```text
Document quality:
Moderate

Processing...

Vision extraction...
```

Then:

```text
Invoice number        94%
GSTIN                 98%
Date                  91%
Quantity              76% ⚠
Unit price             68% ⚠
```

Then:

```text
⚠ 2 fields require human verification
```

Correct them.

Then:

```text
Recalculate

✓ Taxable amount verified
✓ GST verified
✓ Total verified

Invoice approved.
```

This demonstrates that the system can recognize uncertainty instead of falsely claiming perfect accuracy.

---

# 51. Testing Dataset

Create a real evaluation dataset before the final demo.

Recommended minimum:

```text
10 printed invoices
10 digital PDFs
10 handwritten invoices
5 poor-quality images
5 Excel files
5 CSV files
```

Measure:

```text
Field accuracy
GSTIN accuracy
Invoice number accuracy
Date accuracy
Item accuracy
Quantity accuracy
Price accuracy
Tax accuracy
Total accuracy
```

Especially report:

```text
Printed accuracy
Handwritten accuracy
```

Do not claim a specific accuracy percentage unless it was actually measured.

---

# 52. Architecture for Presentation

Use this on an architecture slide:

```text
                    VYOM+
          INVOICE INTELLIGENCE ENGINE

                         INPUT
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
       XLSX               CSV             PDF/Image
        │                  │                  │
        └──────────────────┼──────────────────┘
                           │
                    FILE CLASSIFIER
                           │
                  DOCUMENT PROCESSOR
                           │
            ┌──────────────┴──────────────┐
            │                             │
      Tabular Parser                Vision Pipeline
            │                             │
            │                     Preprocessing
            │                             │
            │                       OCR / VLM
            │                             │
            └──────────────┬──────────────┘
                           │
                  STRUCTURED EXTRACTION
                           │
                     JSON SCHEMA
                           │
              ┌────────────┼────────────┐
              │            │            │
          GST Rules    Math Rules    Confidence
              │            │            │
              └────────────┼────────────┘
                           │
                    HUMAN REVIEW
                           │
                    FINAL RECORD
                           │
              ┌────────────┼────────────┐
              │            │            │
             JSON         CSV          XLSX
```

---

# 53. Technology Stack Slide

Use:

| Layer | Technology |
|---|---|
| Frontend | Next.js + React + Tailwind |
| Backend | Python + FastAPI |
| AI | Multimodal Vision LLM |
| OCR | Vision/OCR pipeline |
| Image Processing | OpenCV + Pillow |
| PDF | PyMuPDF |
| Tabular | Pandas + OpenPyXL |
| Validation | Python + Pydantic |
| Database | PostgreSQL / SQLite |
| Output | JSON + CSV + XLSX |
| Deployment | Vercel + Render |

---

# 54. Final Architecture

```text
VYOM+
│
├── frontend
│   │
│   ├── Dashboard
│   ├── Upload
│   ├── Documents
│   ├── Invoice Viewer
│   ├── Review
│   └── Analytics
│
├── backend
│   │
│   ├── File Router
│   │
│   ├── Document Processing
│   │   ├── Excel
│   │   ├── CSV
│   │   ├── PDF
│   │   └── Image
│   │
│   ├── AI Extraction
│   │
│   ├── Schema Normalization
│   │
│   ├── GST Validator
│   │
│   ├── Math Validator
│   │
│   ├── Confidence Engine
│   │
│   ├── Human Review
│   │
│   └── Export Engine
│
├── database
│
├── sample_data
│
└── documentation
```

---

# 55. Hackathon Timeline

If you have approximately 1–2 days:

## First 4 hours

```text
Next.js setup
FastAPI setup
Upload
Frontend ↔ Backend connection
```

## Next 4 hours

```text
XLSX
CSV
Image
AI extraction
```

## Next 4 hours

```text
PDF
GST validation
Math validation
JSON schema
```

## Next 4 hours

```text
Confidence
Human review
Export
Database
```

## Final hours

```text
Dashboard
UI polish
Demo invoices
Testing
PPT
Pitch
```

---

# 56. Winning Project Positioning

The project should be presented as:

> **An end-to-end AI-powered GST invoice intelligence platform that transforms heterogeneous invoices into validated, structured financial records.**

Core differentiators:

### 1. Multi-format

```text
PDF ✓
JPG ✓
PNG ✓
XLSX ✓
CSV ✓
```

### 2. Multi-modal

```text
Digital text
Printed
Scanned
Handwritten
```

### 3. Structured extraction

```text
Invoice → JSON
```

### 4. Validation

```text
GST
Tax
Totals
Line items
```

### 5. Uncertainty awareness

```text
High confidence → automatic

Low confidence → human review
```

### 6. Production-like output

```text
JSON
CSV
Excel
```

---

# 57. Core Pitch

Use this as the central message:

> **OCR alone reads documents. VYOM+ turns documents into trustworthy financial records.**

Explain:

```text
OCR alone
    ↓
"₹1O,000"

VYOM+
    ↓
"₹10,000"
    ↓
Check quantity
    ↓
Check taxable value
    ↓
Check GST
    ↓
Check total
    ↓
Confidence = 68%
    ↓
Human verification required
```

This demonstrates the difference between document recognition and document intelligence.

---

# 58. Recommended Implementation Strategy

Build incrementally with this order:

```text
1. Repository
2. FastAPI backend
3. Next.js frontend
4. Upload endpoint
5. File router
6. Universal invoice schema
7. Excel parser
8. CSV parser
9. Image processor
10. Vision extraction
11. PDF processor
12. GST validation
13. Mathematical validation
14. Confidence engine
15. Human review
16. Database
17. JSON export
18. CSV export
19. Excel export
20. Dashboard
21. Analytics
22. Handwriting optimization
23. QR validation
24. Duplicate detection
25. Deployment
```

Do not attempt all 25 features before the basic end-to-end pipeline works.

---

# 59. Final Goal

The final working website should allow a judge to:

```text
1. Open VYOM+
        ↓
2. Upload an invoice
        ↓
3. Watch the document pipeline
        ↓
4. See extracted fields
        ↓
5. Inspect confidence scores
        ↓
6. See GST/math validation
        ↓
7. Correct uncertain fields
        ↓
8. Revalidate
        ↓
9. Download JSON/CSV/Excel
```

The complete experience should feel like:

> **Upload → Understand → Validate → Review → Export**

rather than simply:

> **Upload → OCR → Text**

---

# 60. Final Recommendation

The strongest version of VYOM+ is not the one with the most AI models.

It is the one that demonstrates the most reliable end-to-end workflow.

Prioritize:

1. **Universal schema**
2. **Multi-format support**
3. **Vision-based extraction**
4. **Handwritten invoice handling**
5. **GST validation**
6. **Mathematical validation**
7. **Confidence scoring**
8. **Human-in-the-loop review**
9. **Machine-readable exports**
10. **Clean SaaS-style UI**

The key architectural principle is:

> **AI extracts. Deterministic code validates. Confidence decides. Humans resolve uncertainty.**

That gives VYOM+ a much stronger hackathon story than a simple OCR application.
