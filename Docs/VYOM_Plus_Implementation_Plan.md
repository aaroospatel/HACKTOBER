# VYOM+ — End-to-End AI-Powered GST Invoice Intelligence System
## 🏆 Full AI-Agent Implementation Plan

> **Hacktober Fest 4 — Problem Statement 3**
> Built for qualifier submission (Part 1) and final hackathon presentation (Part 2).
> This plan is structured so an AI agent can implement it **phase by phase** on user command.

---

## 📋 Table of Contents

1. [Project Overview & Core Philosophy](#1-project-overview--core-philosophy)
2. [Technology Stack (Final)](#2-technology-stack-final)
3. [Repository Structure](#3-repository-structure)
4. [Universal Invoice JSON Schema](#4-universal-invoice-json-schema)
5. [Part 1 — Qualifier Demo Backend](#part-1--qualifier-demo-backend)
   - [Phase 1: Project Setup](#phase-1-project-setup)
   - [Phase 2: Pydantic Schemas & Database Models](#phase-2-pydantic-schemas--database-models)
   - [Phase 3: Document Processing Pipelines](#phase-3-document-processing-pipelines)
   - [Phase 4: AI Extraction Engine](#phase-4-ai-extraction-engine)
   - [Phase 5: GST + Math Validation Engine](#phase-5-gst--math-validation-engine)
   - [Phase 6: Confidence Engine](#phase-6-confidence-engine)
   - [Phase 7: FastAPI Endpoints & Export](#phase-7-fastapi-endpoints--export)
   - [Phase 8: Basic Streamlit UI (Demo)](#phase-8-basic-streamlit-ui-demo)
   - [Phase 9: README & Qualifier Submission](#phase-9-readme--qualifier-submission)
6. [Part 2 — Full Polished Project](#part-2--full-polished-project)
   - [Phase 10: Next.js Frontend Setup](#phase-10-nextjs-frontend-setup)
   - [Phase 11: Dashboard Page](#phase-11-dashboard-page)
   - [Phase 12: Upload Page](#phase-12-upload-page)
   - [Phase 13: Documents List Page](#phase-13-documents-list-page)
   - [Phase 14: Invoice Review Page](#phase-14-invoice-review-page)
   - [Phase 15: Analytics Page](#phase-15-analytics-page)
   - [Phase 16: Human-in-the-Loop Review UI](#phase-16-human-in-the-loop-review-ui)
   - [Phase 17: Advanced Features](#phase-17-advanced-features)
   - [Phase 18: Testing Dataset & Evaluation](#phase-18-testing-dataset--evaluation)
   - [Phase 19: Deployment](#phase-19-deployment)
   - [Phase 20: Final Polish & Presentation Assets](#phase-20-final-polish--presentation-assets)
7. [User-Supplied Resources Checklist](#user-supplied-resources-checklist)
8. [Agent Command Reference](#agent-command-reference)

---

## 1. Project Overview & Core Philosophy

### What VYOM+ Does

```
Document (any format)
        ↓
File Type Detection
        ↓
Document Processing (format-specific pipeline)
        ↓
OCR / Vision AI (for images/scanned PDFs)
        ↓
Invoice Understanding (AI extraction)
        ↓
Structured JSON (Universal Schema)
        ↓
GST + Mathematical Validation (deterministic rules)
        ↓
Confidence Scoring (multi-signal)
        ↓
Human Review (when confidence < 70%)
        ↓
Validated Financial Record
        ↓
JSON / CSV / Excel Export
```

### Core Principle
> **AI extracts. Deterministic code validates. Confidence decides. Humans resolve uncertainty.**

VYOM+ is NOT just an OCR tool. It is a **document intelligence platform** that:
- Understands invoice structure semantically
- Validates mathematically and against GST rules
- Knows when it might be wrong (confidence)
- Allows humans to correct uncertain fields
- Produces machine-readable output for downstream accounting

### Supported Input Formats
| Format | Pipeline |
|--------|----------|
| `.xlsx` | Pandas tabular parser |
| `.csv` | Pandas tabular parser |
| `.pdf` (digital) | PyMuPDF text extraction → AI |
| `.pdf` (scanned) | PyMuPDF → image render → Vision AI |
| `.jpg` / `.jpeg` | Image preprocessing → Vision AI |
| `.png` | Image preprocessing → Vision AI |

---

## 2. Technology Stack (Final)

| Layer | Technology | Why |
|-------|-----------|-----|
| **Backend** | Python 3.11 + FastAPI | Fast async API, great DX |
| **AI — LLM** | Google Gemini 1.5 Flash (via `google-generativeai`) | Free tier, multimodal, vision capable, strong JSON output |
| **AI — Fallback** | OpenAI GPT-4o-mini (optional, if user has key) | Backup vision model |
| **OCR** | Tesseract (pytesseract) + PaddleOCR | Free, local OCR for preprocessing |
| **Image Processing** | OpenCV + Pillow | Preprocessing, deskew, enhance |
| **PDF Processing** | PyMuPDF (fitz) | Extract text from digital PDFs, render pages |
| **Tabular** | Pandas + OpenPyXL | Excel/CSV parsing |
| **Validation** | Pydantic v2 | Strict schema validation |
| **Database** | SQLite (Part 1) → PostgreSQL/Supabase (Part 2) | SQLAlchemy ORM |
| **Part 1 UI** | Streamlit | Fast demo UI for qualifier |
| **Part 2 Frontend** | Next.js 14 + React + TypeScript | Production-grade SaaS UI |
| **Part 2 Styling** | Tailwind CSS | Fast, responsive design |
| **Export** | JSON + CSV + OpenPyXL (Excel) | Multi-format output |
| **Deployment Backend** | Render / Railway (Part 2) | Free tier deployment |
| **Deployment Frontend** | Vercel (Part 2) | Free Next.js hosting |

### Why Gemini Flash (Primary AI Choice)
- Completely **free tier** available — no API cost issue for hackathon
- **Multimodal** — can process images, PDFs, and text natively
- Excellent at **structured JSON extraction**
- Supports **system instructions** for strict extraction prompts
- The agent will ask user for Gemini API key before Phase 4

---

## 3. Repository Structure

```
vyom-invoice-ai/                          ← Root of project
│
├── backend/                              ← Python FastAPI backend
│   ├── app/
│   │   ├── main.py                       ← FastAPI app entry point
│   │   ├── config.py                     ← Environment config
│   │   │
│   │   ├── routers/
│   │   │   ├── upload.py                 ← POST /api/upload
│   │   │   ├── invoice.py                ← GET/PUT /api/documents/...
│   │   │   └── export.py                 ← GET /api/documents/{id}/json|csv|excel
│   │   │
│   │   ├── services/
│   │   │   ├── file_router.py            ← Detects file type, routes to processor
│   │   │   ├── excel_processor.py        ← .xlsx pipeline
│   │   │   ├── csv_processor.py          ← .csv pipeline
│   │   │   ├── pdf_processor.py          ← PDF pipeline (digital + scanned)
│   │   │   ├── image_processor.py        ← Image preprocessing (OpenCV)
│   │   │   ├── ocr_service.py            ← Tesseract / PaddleOCR wrapper
│   │   │   ├── ai_extractor.py           ← Gemini vision/text extraction
│   │   │   ├── validator.py              ← GST + math validation rules
│   │   │   ├── confidence.py             ← Multi-signal confidence engine
│   │   │   └── exporter.py               ← JSON/CSV/Excel export
│   │   │
│   │   ├── schemas/
│   │   │   └── invoice.py                ← Pydantic models (universal schema)
│   │   │
│   │   ├── database/
│   │   │   ├── models.py                 ← SQLAlchemy ORM models
│   │   │   ├── crud.py                   ← DB create/read/update operations
│   │   │   └── database.py               ← DB connection setup
│   │   │
│   │   └── utils/
│   │       ├── helpers.py                ← Utility functions
│   │       └── gst_rules.py              ← GST rate tables, state codes
│   │
│   ├── demo_ui/
│   │   └── streamlit_app.py              ← Part 1: Streamlit demo UI
│   │
│   ├── requirements.txt
│   ├── .env.example
│   └── README_backend.md
│
├── frontend/                             ← Next.js frontend (Part 2)
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx                      ← Dashboard /
│   │   ├── upload/
│   │   │   └── page.tsx                  ← /upload
│   │   ├── documents/
│   │   │   ├── page.tsx                  ← /documents (list)
│   │   │   └── [id]/
│   │   │       └── page.tsx              ← /documents/[id] (detail/review)
│   │   └── analytics/
│   │       └── page.tsx                  ← /analytics
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx
│   │   │   └── Sidebar.tsx
│   │   ├── dashboard/
│   │   │   ├── StatsCards.tsx
│   │   │   ├── RecentDocuments.tsx
│   │   │   └── DocumentTypePieChart.tsx
│   │   ├── upload/
│   │   │   ├── UploadBox.tsx
│   │   │   └── ProcessingSteps.tsx
│   │   ├── invoice/
│   │   │   ├── InvoiceViewer.tsx         ← Left panel: original document
│   │   │   ├── InvoiceFields.tsx         ← Right panel: extracted fields
│   │   │   ├── LineItemsTable.tsx
│   │   │   ├── GSTSummary.tsx
│   │   │   ├── ValidationPanel.tsx
│   │   │   ├── ConfidenceBadge.tsx
│   │   │   └── HumanReviewPanel.tsx
│   │   ├── export/
│   │   │   └── ExportButtons.tsx
│   │   └── analytics/
│   │       ├── AccuracyByTypeChart.tsx
│   │       └── ConfidenceHistogram.tsx
│   │
│   ├── lib/
│   │   ├── api.ts                        ← API client (axios/fetch)
│   │   └── types.ts                      ← TypeScript types (mirror of Pydantic)
│   │
│   ├── public/
│   │   └── logo.svg
│   │
│   ├── tailwind.config.ts
│   ├── tsconfig.json
│   ├── next.config.ts
│   └── package.json
│
├── sample_invoices/                      ← Test data (user provides)
│   ├── printed/
│   ├── handwritten/
│   ├── digital_pdf/
│   ├── scanned_pdf/
│   ├── excel/
│   └── csv/
│
├── docs/
│   ├── architecture.md
│   └── api_reference.md
│
├── .gitignore
└── README.md                             ← Main README for submission
```

---

## 4. Universal Invoice JSON Schema

Every document — regardless of format — must produce this exact structure:

```json
{
  "document": {
    "id": "uuid-v4",
    "filename": "invoice_001.jpg",
    "document_type": "invoice",
    "source_type": "image",
    "upload_time": "2026-10-07T01:15:00Z",
    "page_count": 1
  },

  "supplier": {
    "name": "ABC Enterprises",
    "gstin": "27ABCDE1234F1Z5",
    "address": "Nagpur, Maharashtra",
    "state_code": "27"
  },

  "buyer": {
    "name": "XYZ Pvt Ltd",
    "gstin": "27AAAAA1234A1Z1",
    "address": "Mumbai, Maharashtra",
    "state_code": "27"
  },

  "invoice": {
    "invoice_number": "INV-1023",
    "invoice_date": "2026-10-04",
    "place_of_supply": "Maharashtra",
    "reverse_charge": false,
    "irn": null,
    "supply_type": "intra-state"
  },

  "items": [
    {
      "description": "Laptop",
      "hsn_sac": "8471",
      "quantity": 2,
      "unit": "PCS",
      "unit_price": 50000.0,
      "discount": 0.0,
      "taxable_value": 100000.0,
      "gst_rate": 18,
      "cgst": 9000.0,
      "sgst": 9000.0,
      "igst": 0.0,
      "cess": 0.0,
      "total": 118000.0
    }
  ],

  "tax": {
    "taxable_amount": 100000.0,
    "cgst": 9000.0,
    "sgst": 9000.0,
    "igst": 0.0,
    "cess": 0.0,
    "round_off": 0.0,
    "total_tax": 18000.0
  },

  "totals": {
    "subtotal": 100000.0,
    "total_discount": 0.0,
    "grand_total": 118000.0,
    "amount_in_words": "One Lakh Eighteen Thousand Rupees Only"
  },

  "validation": {
    "status": "valid",
    "gstin_supplier_valid": true,
    "gstin_buyer_valid": true,
    "tax_calculation_valid": true,
    "line_items_valid": true,
    "grand_total_valid": true,
    "supply_type_consistent": true,
    "errors": [],
    "warnings": []
  },

  "confidence": {
    "overall": 0.96,
    "invoice_number": 0.97,
    "invoice_date": 0.98,
    "supplier_name": 0.95,
    "supplier_gstin": 0.99,
    "buyer_name": 0.94,
    "buyer_gstin": 0.99,
    "items": 0.92,
    "quantities": 0.91,
    "unit_prices": 0.93,
    "total": 0.99,
    "review_required": false,
    "low_confidence_fields": []
  }
}
```

---

# PART 1 — QUALIFIER DEMO BACKEND

> **Goal:** Working Python backend + Streamlit demo UI that processes all 5 file types and produces validated JSON output. Sufficient to write a strong README and submit for qualifier.

---

## Phase 1: Project Setup

### Agent Instructions
> **Command to user:** "Start Phase 1: Project Setup"
> **Agent will:** Create folder structure, virtual environment, install all dependencies, create config files.

### Steps

**1.1 — Create root folder and structure**
```bash
# Run from: c:\Users\LOQ\Desktop\HACKTOBER
mkdir vyom-invoice-ai
cd vyom-invoice-ai
mkdir backend frontend sample_invoices docs
mkdir backend\app backend\app\routers backend\app\services
mkdir backend\app\schemas backend\app\database backend\app\utils
mkdir backend\demo_ui
mkdir sample_invoices\printed sample_invoices\handwritten
mkdir sample_invoices\digital_pdf sample_invoices\scanned_pdf
mkdir sample_invoices\excel sample_invoices\csv
```

**1.2 — Create Python virtual environment**
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```

**1.3 — Install all backend dependencies**
```bash
pip install fastapi uvicorn[standard] python-multipart
pip install pandas openpyxl
pip install pillow opencv-python
pip install pymupdf
pip install pydantic pydantic-settings
pip install python-dotenv
pip install google-generativeai
pip install pytesseract
pip install paddlepaddle paddleocr
pip install sqlalchemy aiosqlite
pip install python-jose httpx
pip install streamlit
pip install reportlab fpdf2
pip install qrcode[pil] pyzbar
pip install pytest httpx
```

> **⚠️ Agent Note:** After running pip installs, ask user: *"Do you want to also use OpenAI as a fallback AI? If yes, provide your OpenAI API key."*
> If user says no, only Gemini will be used (recommended for free tier).

**1.4 — Create `.env.example`**
```
GEMINI_API_KEY=your_gemini_api_key_here
OPENAI_API_KEY=your_openai_api_key_here_optional
DATABASE_URL=sqlite:///./vyom_invoices.db
UPLOAD_DIR=./uploads
ENVIRONMENT=development
```

**1.5 — Create `requirements.txt`**
(Agent generates from pip freeze after installs)

**1.6 — Create `backend/app/config.py`**
```python
from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    gemini_api_key: str
    openai_api_key: str = ""
    database_url: str = "sqlite:///./vyom_invoices.db"
    upload_dir: str = "./uploads"
    environment: str = "development"
    max_file_size_mb: int = 20
    confidence_threshold_high: float = 0.90
    confidence_threshold_review: float = 0.70

    class Config:
        env_file = ".env"

settings = Settings()
```

### Input
- User's project directory

### Output
- Full folder structure
- Virtual environment with all packages
- Config files ready

### User Action Required
> 🔑 **"Please provide your Google Gemini API key."**
> Get it free at: https://aistudio.google.com/app/apikey
> Create a `.env` file in `backend/` with `GEMINI_API_KEY=your_key_here`

---

## Phase 2: Pydantic Schemas & Database Models

### Agent Instructions
> **Command to user:** "Start Phase 2: Schemas and Database"
> **Agent will:** Create all Pydantic models and SQLAlchemy database models.

### 2.1 — `backend/app/schemas/invoice.py`

Full Pydantic schema implementing the universal invoice JSON structure:

```python
from pydantic import BaseModel, Field, validator
from typing import Optional, List, Literal
from datetime import datetime
import uuid

class DocumentInfo(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    filename: str
    document_type: str = "invoice"
    source_type: Literal["excel", "csv", "pdf_digital", "pdf_scanned", "image"]
    upload_time: datetime = Field(default_factory=datetime.utcnow)
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
    supplier: PartyInfo = PartyInfo()
    buyer: PartyInfo = PartyInfo()
    invoice: InvoiceMeta = InvoiceMeta()
    items: List[LineItem] = []
    tax: TaxSummary = TaxSummary()
    totals: Totals = Totals()
    validation: ValidationResult = ValidationResult()
    confidence: ConfidenceScores = ConfidenceScores()

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
```

### 2.2 — `backend/app/database/models.py`

SQLAlchemy ORM models for SQLite:

```python
from sqlalchemy import Column, String, Float, Boolean, Integer, DateTime, Text, JSON
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(String, primary_key=True)
    filename = Column(String, nullable=False)
    file_type = Column(String)         # xlsx, csv, pdf, image
    source_type = Column(String)       # excel, csv, pdf_digital, pdf_scanned, image
    upload_time = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="processing")  # processing, valid, warning, needs_review, invalid
    overall_confidence = Column(Float, default=0.0)
    raw_json = Column(Text)            # Full InvoiceRecord JSON string
    page_count = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.utcnow)

class InvoiceModel(Base):
    __tablename__ = "invoices"
    id = Column(String, primary_key=True)
    document_id = Column(String, nullable=False)
    invoice_number = Column(String)
    invoice_date = Column(String)
    supplier_name = Column(String)
    supplier_gstin = Column(String)
    buyer_name = Column(String)
    buyer_gstin = Column(String)
    place_of_supply = Column(String)
    supply_type = Column(String)
    subtotal = Column(Float)
    total_tax = Column(Float)
    grand_total = Column(Float)
    validation_status = Column(String)
    validation_errors = Column(JSON, default=list)
    validation_warnings = Column(JSON, default=list)

class InvoiceItemModel(Base):
    __tablename__ = "invoice_items"
    id = Column(Integer, primary_key=True, autoincrement=True)
    invoice_id = Column(String, nullable=False)
    description = Column(String)
    hsn_sac = Column(String)
    quantity = Column(Float)
    unit_price = Column(Float)
    taxable_value = Column(Float)
    gst_rate = Column(Float)
    cgst = Column(Float)
    sgst = Column(Float)
    igst = Column(Float)
    total = Column(Float)
```

### 2.3 — `backend/app/database/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from app.config import settings

engine = create_engine(settings.database_url, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

### Input
- Phase 1 complete (folders exist)

### Output
- `schemas/invoice.py` — Full Pydantic model hierarchy
- `database/models.py` — SQLAlchemy tables
- `database/database.py` — Connection setup

---

## Phase 3: Document Processing Pipelines

### Agent Instructions
> **Command to user:** "Start Phase 3: Document Processing Pipelines"
> **Agent will:** Implement all 5 format-specific processors and the file router.

### 3.1 — `backend/app/utils/gst_rules.py`

```python
# Indian GST state codes
STATE_CODES = {
    "01": "Jammu & Kashmir", "02": "Himachal Pradesh", "03": "Punjab",
    "04": "Chandigarh", "05": "Uttarakhand", "06": "Haryana",
    "07": "Delhi", "08": "Rajasthan", "09": "Uttar Pradesh",
    "10": "Bihar", "11": "Sikkim", "12": "Arunachal Pradesh",
    "13": "Nagaland", "14": "Manipur", "15": "Mizoram",
    "16": "Tripura", "17": "Meghalaya", "18": "Assam",
    "19": "West Bengal", "20": "Jharkhand", "21": "Odisha",
    "22": "Chhattisgarh", "23": "Madhya Pradesh", "24": "Gujarat",
    "26": "Dadra and Nagar Haveli and Daman and Diu",
    "27": "Maharashtra", "28": "Andhra Pradesh", "29": "Karnataka",
    "30": "Goa", "31": "Lakshadweep", "32": "Kerala",
    "33": "Tamil Nadu", "34": "Puducherry", "35": "Andaman and Nicobar Islands",
    "36": "Telangana", "37": "Andhra Pradesh (new)"
}

# Valid GST rates (%)
VALID_GST_RATES = {0, 0.1, 0.25, 1, 1.5, 3, 5, 6, 7.5, 12, 18, 28}

# GSTIN format regex
GSTIN_PATTERN = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'

# Column name mapping for Excel/CSV normalization
COLUMN_MAPPING = {
    "invoice no": "invoice_number", "invoice number": "invoice_number",
    "inv no": "invoice_number", "bill no": "invoice_number",
    "date": "invoice_date", "invoice date": "invoice_date",
    "bill date": "invoice_date",
    "gstin": "supplier_gstin", "seller gstin": "supplier_gstin",
    "vendor gstin": "supplier_gstin",
    "buyer gstin": "buyer_gstin", "customer gstin": "buyer_gstin",
    "seller": "supplier_name", "vendor": "supplier_name",
    "supplier": "supplier_name", "from": "supplier_name",
    "buyer": "buyer_name", "customer": "buyer_name", "to": "buyer_name",
    "item": "description", "product": "description",
    "particulars": "description", "goods": "description",
    "qty": "quantity", "quantity": "quantity",
    "rate": "unit_price", "price": "unit_price", "unit price": "unit_price",
    "hsn": "hsn_sac", "sac": "hsn_sac", "hsn/sac": "hsn_sac",
    "gst rate": "gst_rate", "tax rate": "gst_rate",
    "cgst": "cgst", "sgst": "sgst", "igst": "igst",
    "taxable value": "taxable_value", "taxable amount": "taxable_value",
    "total": "total", "amount": "total", "grand total": "grand_total",
}
```

### 3.2 — `backend/app/services/file_router.py`

**Input:** Uploaded file (bytes + filename)
**Output:** Calls correct processor, returns `InvoiceRecord`

```python
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

async def route_file(file: UploadFile, file_bytes: bytes) -> dict:
    """
    Detect file type and route to correct processor.
    Returns InvoiceRecord as dict.
    """
    filename = file.filename.lower()
    ext = filename.rsplit(".", 1)[-1] if "." in filename else ""

    if ext not in SUPPORTED_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file format: .{ext}. Supported: xlsx, csv, pdf, jpg, jpeg, png"
        )

    file_type = SUPPORTED_TYPES[ext]

    if file_type == "excel":
        return await process_excel(file_bytes, file.filename)
    elif file_type == "csv":
        return await process_csv(file_bytes, file.filename)
    elif file_type == "pdf":
        return await process_pdf(file_bytes, file.filename)
    elif file_type == "image":
        return await process_image(file_bytes, file.filename)
```

### 3.3 — `backend/app/services/excel_processor.py`

**Input:** Excel file bytes + filename
**Output:** `InvoiceRecord` dict (no AI needed — rule-based column mapping)

```python
import pandas as pd
import io
import uuid
from datetime import datetime
from app.utils.gst_rules import COLUMN_MAPPING
from app.schemas.invoice import InvoiceRecord, DocumentInfo, PartyInfo, InvoiceMeta, LineItem, TaxSummary, Totals

async def process_excel(file_bytes: bytes, filename: str) -> dict:
    df = pd.read_excel(io.BytesIO(file_bytes), engine="openpyxl")
    return _process_tabular(df, filename, "excel")

def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Lowercase, strip, replace spaces, map to canonical names."""
    df.columns = (
        df.columns
        .str.lower()
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    rename_map = {}
    for col in df.columns:
        if col in COLUMN_MAPPING:
            rename_map[col] = COLUMN_MAPPING[col]
    return df.rename(columns=rename_map)

def _process_tabular(df: pd.DataFrame, filename: str, source_type: str) -> dict:
    df = _normalize_columns(df)
    df = df.dropna(how="all")

    # Extract invoice-level fields (from first row or dedicate header rows)
    first_row = df.iloc[0] if len(df) > 0 else {}

    def get_field(field_name, row=first_row):
        return str(row[field_name]).strip() if field_name in row and pd.notna(row[field_name]) else None

    # Build line items from all rows
    items = []
    for _, row in df.iterrows():
        item = LineItem(
            description=get_field("description", row),
            hsn_sac=get_field("hsn_sac", row),
            quantity=_safe_float(row.get("quantity")),
            unit_price=_safe_float(row.get("unit_price")),
            taxable_value=_safe_float(row.get("taxable_value")),
            gst_rate=_safe_float(row.get("gst_rate")),
            cgst=_safe_float(row.get("cgst")),
            sgst=_safe_float(row.get("sgst")),
            igst=_safe_float(row.get("igst")),
            total=_safe_float(row.get("total")),
        )
        if item.description:  # only add rows that have at least a description
            items.append(item)

    grand_total = _safe_float(df.get("grand_total", pd.Series([None])).dropna().iloc[0] if "grand_total" in df else None)

    record = InvoiceRecord(
        document=DocumentInfo(
            id=str(uuid.uuid4()),
            filename=filename,
            source_type=source_type,
        ),
        supplier=PartyInfo(
            name=get_field("supplier_name"),
            gstin=get_field("supplier_gstin"),
        ),
        buyer=PartyInfo(
            name=get_field("buyer_name"),
            gstin=get_field("buyer_gstin"),
        ),
        invoice=InvoiceMeta(
            invoice_number=get_field("invoice_number"),
            invoice_date=get_field("invoice_date"),
        ),
        items=items,
        totals=Totals(grand_total=grand_total),
    )
    return record.model_dump()

def _safe_float(val) -> float | None:
    try:
        return float(val)
    except (TypeError, ValueError):
        return None
```

### 3.4 — `backend/app/services/csv_processor.py`

```python
import pandas as pd
import io
from .excel_processor import _process_tabular

async def process_csv(file_bytes: bytes, filename: str) -> dict:
    # Try multiple encodings
    for encoding in ["utf-8", "latin-1", "cp1252"]:
        try:
            df = pd.read_csv(io.BytesIO(file_bytes), encoding=encoding)
            return _process_tabular(df, filename, "csv")
        except UnicodeDecodeError:
            continue
    raise ValueError("Could not decode CSV with any supported encoding")
```

### 3.5 — `backend/app/services/image_processor.py`

**Input:** Raw image bytes
**Output:** Preprocessed PIL Image objects (multiple versions for AI)

```python
import cv2
import numpy as np
from PIL import Image
import io
from typing import Tuple

def preprocess_image(image_bytes: bytes) -> dict:
    """
    Returns multiple preprocessed versions of the image.
    The AI extractor will use the best version.
    """
    # Decode image
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image")

    results = {}

    # Original (just resized if too large)
    results["original"] = _resize_if_needed(img)

    # Grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    results["grayscale"] = gray

    # Enhanced contrast (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    results["enhanced"] = enhanced

    # Denoised
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    results["denoised"] = denoised

    # Adaptive threshold (good for printed text, NOT handwriting)
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    results["threshold"] = thresh

    # Deskewed version
    results["deskewed"] = _deskew(gray)

    return results

def _resize_if_needed(img: np.ndarray, max_dim: int = 2000) -> np.ndarray:
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)))
    return img

def _deskew(gray: np.ndarray) -> np.ndarray:
    """Correct image rotation using Hough line transform."""
    try:
        edges = cv2.Canny(gray, 50, 150, apertureSize=3)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100)
        if lines is None:
            return gray
        angles = []
        for rho, theta in lines[:, 0]:
            angle = (theta - np.pi / 2) * 180 / np.pi
            if abs(angle) < 45:
                angles.append(angle)
        if not angles:
            return gray
        median_angle = np.median(angles)
        if abs(median_angle) < 0.5:
            return gray
        h, w = gray.shape
        M = cv2.getRotationMatrix2D((w // 2, h // 2), median_angle, 1.0)
        return cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except Exception:
        return gray

def cv2_to_pil(img_array: np.ndarray) -> Image.Image:
    """Convert OpenCV image to PIL Image for Gemini."""
    if len(img_array.shape) == 2:  # grayscale
        return Image.fromarray(img_array)
    return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

def pil_to_bytes(pil_img: Image.Image, format: str = "JPEG") -> bytes:
    buf = io.BytesIO()
    pil_img.save(buf, format=format, quality=95)
    return buf.getvalue()

def analyze_image_quality(img: np.ndarray) -> dict:
    """Analyze image quality to determine best preprocessing."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
    brightness = gray.mean()
    contrast = gray.std()
    return {
        "blur_score": blur_score,
        "is_blurry": blur_score < 100,
        "brightness": brightness,
        "is_dark": brightness < 80,
        "contrast": contrast,
        "quality": "high" if blur_score > 300 else "medium" if blur_score > 100 else "low"
    }
```

### 3.6 — `backend/app/services/pdf_processor.py`

**Input:** PDF bytes
**Output:** `InvoiceRecord` dict

```python
import fitz  # PyMuPDF
import io
from PIL import Image
from .image_processor import preprocess_image, cv2_to_pil, pil_to_bytes
from .ai_extractor import extract_from_text, extract_from_image

async def process_pdf(file_bytes: bytes, filename: str) -> dict:
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    page_images = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        pages_text.append(text)

        # Render page to image for scanned PDFs
        mat = fitz.Matrix(2, 2)  # 2x zoom for higher quality
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        page_images.append(img_bytes)

    # Determine if it's a digital or scanned PDF
    total_text = " ".join(pages_text)
    is_digital = len(total_text.strip()) > 100  # arbitrary threshold

    if is_digital:
        # Digital PDF: use text extraction + AI
        result = await extract_from_text(
            text=total_text,
            filename=filename,
            source_type="pdf_digital",
            page_count=len(doc)
        )
    else:
        # Scanned PDF: use vision AI on rendered images
        # Combine all page images into one extraction call
        result = await extract_from_image(
            image_bytes=page_images[0],  # primary: first page
            filename=filename,
            source_type="pdf_scanned",
            additional_pages=page_images[1:],
            page_count=len(doc)
        )

    doc.close()
    return result
```

### Input (Phase 3)
- Phase 1 & 2 complete

### Output
- All 5 processor files functional
- File router that correctly routes based on extension

---

## Phase 4: AI Extraction Engine

### Agent Instructions
> **Command to user:** "Start Phase 4: AI Extraction Engine"
> **⚠️ User Action Required BEFORE this phase:** Provide Gemini API key in `.env` file.

### 4.1 — The AI Extraction Prompt

This is the critical prompt given to Gemini for invoice extraction.

**For image/scanned PDFs:**
```
You are an expert GST invoice document intelligence system for India.
Your task is to extract all financial and tax information from this invoice image.

CRITICAL RULES:
1. Extract ONLY what is visible. Do NOT invent or guess any values.
2. If a field is not visible or unreadable, return null for that field.
3. Preserve invoice numbers, GSTINs, and HSN/SAC codes EXACTLY as written.
4. Extract ALL line items — do not skip any.
5. Extract CGST, SGST, and IGST separately.
6. Return confidence scores (0.0 to 1.0) for fields you are uncertain about.
7. For handwritten content, be extra careful with digits: 0/O, 1/I, 5/S, 8/B.

Return ONLY valid JSON matching this exact schema (no markdown, no explanation):
{schema}
```

**For digital text:**
```
You are an expert GST invoice data extraction system for India.
The following text was extracted from a PDF invoice.
Your task is to structure this into the required JSON schema.

RULES:
1. Extract ONLY information explicitly present in the text.
2. If a field is absent, return null.
3. Preserve all numbers, GSTINs, and codes exactly.
4. Return ONLY valid JSON matching this schema:
{schema}

INVOICE TEXT:
{text}
```

### 4.2 — `backend/app/services/ai_extractor.py`

```python
import google.generativeai as genai
from PIL import Image
import io
import json
import re
import uuid
from datetime import datetime
from app.config import settings
from app.schemas.invoice import InvoiceRecord, DocumentInfo

# Configure Gemini
genai.configure(api_key=settings.gemini_api_key)

EXTRACTION_SCHEMA = """
{
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
    "invoice_number": 1.0, "invoice_date": 1.0,
    "supplier_name": 1.0, "supplier_gstin": 1.0,
    "buyer_name": 1.0, "buyer_gstin": 1.0,
    "items": 1.0, "quantities": 1.0, "unit_prices": 1.0, "total": 1.0
  }
}
"""

IMAGE_PROMPT = f"""You are an expert GST invoice document intelligence system for India.
Extract all financial and GST information from this invoice image.

CRITICAL RULES:
1. Extract ONLY what is clearly visible. Do NOT invent values.
2. If unreadable, return null.
3. Preserve invoice numbers, GSTINs, HSN/SAC codes EXACTLY as written.
4. Extract ALL line items.
5. Return confidence scores 0.0-1.0 for uncertain fields.
6. For handwritten digits watch: 0 vs O, 1 vs I, 5 vs S, 8 vs B.

Return ONLY valid JSON (no markdown, no explanation):
{EXTRACTION_SCHEMA}"""

TEXT_PROMPT_TEMPLATE = """You are an expert GST invoice data extraction system.
Structure this invoice text into the required JSON schema.

RULES:
1. Extract ONLY information present in the text.
2. Missing fields → null.
3. Preserve all numbers and codes exactly.

Return ONLY valid JSON:
{schema}

INVOICE TEXT:
{text}"""

async def extract_from_image(
    image_bytes: bytes,
    filename: str,
    source_type: str,
    additional_pages: list = None,
    page_count: int = 1
) -> dict:
    """Extract invoice data from image using Gemini Vision."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Prepare content parts
    content_parts = [IMAGE_PROMPT]

    # Add primary image
    pil_img = Image.open(io.BytesIO(image_bytes))
    content_parts.append(pil_img)

    # Add additional pages if multi-page PDF
    if additional_pages:
        for page_bytes in additional_pages[:5]:  # limit to 5 extra pages
            content_parts.append(Image.open(io.BytesIO(page_bytes)))

    response = model.generate_content(content_parts)
    extracted = _parse_ai_response(response.text)

    return _build_invoice_record(extracted, filename, source_type, page_count)

async def extract_from_text(
    text: str,
    filename: str,
    source_type: str,
    page_count: int = 1
) -> dict:
    """Extract invoice data from text using Gemini."""
    model = genai.GenerativeModel("gemini-1.5-flash")

    prompt = TEXT_PROMPT_TEMPLATE.format(
        schema=EXTRACTION_SCHEMA,
        text=text[:8000]  # token limit safety
    )

    response = model.generate_content(prompt)
    extracted = _parse_ai_response(response.text)

    return _build_invoice_record(extracted, filename, source_type, page_count)

def _parse_ai_response(response_text: str) -> dict:
    """Parse Gemini response, extracting JSON even if wrapped in markdown."""
    text = response_text.strip()

    # Remove markdown code blocks if present
    text = re.sub(r"```json\s*", "", text)
    text = re.sub(r"```\s*", "", text)
    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        # Try to find JSON object in the text
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            try:
                return json.loads(match.group())
            except json.JSONDecodeError:
                pass
    return {}  # Return empty dict if parsing fails

def _build_invoice_record(extracted: dict, filename: str, source_type: str, page_count: int) -> dict:
    """Build a full InvoiceRecord dict from extracted AI data."""
    from app.schemas.invoice import (
        InvoiceRecord, DocumentInfo, PartyInfo, InvoiceMeta,
        LineItem, TaxSummary, Totals, ConfidenceScores
    )

    supplier_data = extracted.get("supplier", {}) or {}
    buyer_data = extracted.get("buyer", {}) or {}
    invoice_data = extracted.get("invoice", {}) or {}
    items_data = extracted.get("items", []) or []
    tax_data = extracted.get("tax", {}) or {}
    totals_data = extracted.get("totals", {}) or {}
    conf_data = extracted.get("confidence", {}) or {}

    items = [LineItem(**{k: v for k, v in item.items() if k in LineItem.model_fields}) for item in items_data]

    # Determine supply type
    supplier_gstin = supplier_data.get("gstin") or ""
    buyer_gstin = buyer_data.get("gstin") or ""
    supply_type = "unknown"
    if len(supplier_gstin) >= 2 and len(buyer_gstin) >= 2:
        supply_type = "intra-state" if supplier_gstin[:2] == buyer_gstin[:2] else "inter-state"

    record = InvoiceRecord(
        document=DocumentInfo(
            id=str(uuid.uuid4()),
            filename=filename,
            source_type=source_type,
            upload_time=datetime.utcnow(),
            page_count=page_count,
        ),
        supplier=PartyInfo(**{k: v for k, v in supplier_data.items() if k in PartyInfo.model_fields}),
        buyer=PartyInfo(**{k: v for k, v in buyer_data.items() if k in PartyInfo.model_fields}),
        invoice=InvoiceMeta(
            **{k: v for k, v in invoice_data.items() if k in InvoiceMeta.model_fields},
            supply_type=supply_type,
        ),
        items=items,
        tax=TaxSummary(**{k: v for k, v in tax_data.items() if k in TaxSummary.model_fields}),
        totals=Totals(**{k: v for k, v in totals_data.items() if k in Totals.model_fields}),
        confidence=ConfidenceScores(**{k: v for k, v in conf_data.items() if k in ConfidenceScores.model_fields}),
    )
    return record.model_dump()
```

### 4.3 — Update `image_processor.py` to call AI extractor

After preprocessing, the image processor calls `ai_extractor.extract_from_image`:

```python
# Add to image_processor.py
from .ai_extractor import extract_from_image

async def process_image(image_bytes: bytes, filename: str) -> dict:
    """Full image processing pipeline."""
    quality = analyze_image_quality(...)

    preprocessed = preprocess_image(image_bytes)

    # Choose best version based on quality analysis
    if quality["quality"] == "high":
        best_img = preprocessed["original"]
    elif quality["is_dark"]:
        best_img = preprocessed["enhanced"]
    else:
        best_img = preprocessed["deskewed"]

    best_bytes = pil_to_bytes(cv2_to_pil(best_img))

    result = await extract_from_image(
        image_bytes=best_bytes,
        filename=filename,
        source_type="image",
    )
    return result
```

### Input (Phase 4)
- Gemini API key in `.env`

### Output
- AI extraction working for images, scanned PDFs, and digital PDFs

---

## Phase 5: GST + Math Validation Engine

### Agent Instructions
> **Command to user:** "Start Phase 5: Validation Engine"
> **Agent will:** Implement deterministic GST and math validation rules.

### 5.1 — `backend/app/services/validator.py`

**Input:** `InvoiceRecord` dict
**Output:** `InvoiceRecord` dict with `validation` field populated

```python
import re
from typing import dict
from app.utils.gst_rules import GSTIN_PATTERN, VALID_GST_RATES, STATE_CODES

ROUNDING_TOLERANCE = 2.0  # ₹2 tolerance for rounding differences

def validate_invoice(record: dict) -> dict:
    """
    Run all validation checks on an InvoiceRecord dict.
    Updates the validation field in-place.
    """
    errors = []
    warnings = []

    supplier_gstin = record.get("supplier", {}).get("gstin")
    buyer_gstin = record.get("buyer", {}).get("gstin")
    items = record.get("items", [])
    tax = record.get("tax", {})
    totals = record.get("totals", {})
    invoice = record.get("invoice", {})

    # --- GSTIN Validation ---
    supplier_gstin_valid = _validate_gstin(supplier_gstin)
    buyer_gstin_valid = _validate_gstin(buyer_gstin)

    if supplier_gstin:
        if not supplier_gstin_valid:
            errors.append(f"Supplier GSTIN '{supplier_gstin}' has invalid format")
        else:
            # Populate state_code
            record["supplier"]["state_code"] = supplier_gstin[:2]
    else:
        warnings.append("Supplier GSTIN is missing")

    if buyer_gstin:
        if not buyer_gstin_valid:
            errors.append(f"Buyer GSTIN '{buyer_gstin}' has invalid format")
        else:
            record["buyer"]["state_code"] = buyer_gstin[:2]
    else:
        warnings.append("Buyer GSTIN is missing")

    # --- Supply type consistency ---
    supply_type_consistent = True
    if supplier_gstin_valid and buyer_gstin_valid:
        same_state = supplier_gstin[:2] == buyer_gstin[:2]
        supply_type = invoice.get("supply_type", "unknown")
        cgst = tax.get("cgst", 0) or 0
        igst = tax.get("igst", 0) or 0

        if same_state and igst > 0 and cgst == 0:
            warnings.append("Intra-state transaction but IGST charged instead of CGST+SGST")
            supply_type_consistent = False
        elif not same_state and cgst > 0 and igst == 0:
            warnings.append("Inter-state transaction but CGST+SGST charged instead of IGST")
            supply_type_consistent = False

    # --- Line Item Validation ---
    line_items_valid = True
    calculated_subtotal = 0.0
    for i, item in enumerate(items):
        qty = item.get("quantity")
        price = item.get("unit_price")
        taxable = item.get("taxable_value")
        discount = item.get("discount", 0) or 0
        gst_rate = item.get("gst_rate")
        cgst = item.get("cgst")
        sgst = item.get("sgst")
        igst = item.get("igst")
        total = item.get("total")

        # qty × price − discount ≈ taxable_value
        if qty is not None and price is not None and taxable is not None:
            expected_taxable = qty * price - discount
            if abs(expected_taxable - taxable) > ROUNDING_TOLERANCE:
                warnings.append(
                    f"Item {i+1} '{item.get('description', '')}': "
                    f"qty×price={expected_taxable:.2f} ≠ taxable_value={taxable:.2f}"
                )
                line_items_valid = False

        # GST rate validation
        if gst_rate is not None and gst_rate not in VALID_GST_RATES:
            warnings.append(f"Item {i+1}: Unusual GST rate {gst_rate}%")

        # Tax amount validation
        if taxable is not None and gst_rate is not None:
            expected_tax = taxable * gst_rate / 100
            if cgst is not None and sgst is not None:
                actual_tax = cgst + sgst
                if abs(actual_tax - expected_tax) > ROUNDING_TOLERANCE:
                    errors.append(
                        f"Item {i+1}: Expected tax ₹{expected_tax:.2f}, "
                        f"CGST+SGST=₹{actual_tax:.2f}"
                    )
            elif igst is not None:
                if abs(igst - expected_tax) > ROUNDING_TOLERANCE:
                    errors.append(
                        f"Item {i+1}: Expected IGST ₹{expected_tax:.2f}, got ₹{igst:.2f}"
                    )

        if taxable:
            calculated_subtotal += taxable

    # --- Tax Totals Validation ---
    tax_calculation_valid = True
    tax_taxable = tax.get("taxable_amount")
    tax_cgst = tax.get("cgst", 0) or 0
    tax_sgst = tax.get("sgst", 0) or 0
    tax_igst = tax.get("igst", 0) or 0
    tax_cess = tax.get("cess", 0) or 0
    tax_total = tax.get("total_tax")

    if tax_taxable and calculated_subtotal:
        if abs(tax_taxable - calculated_subtotal) > ROUNDING_TOLERANCE:
            warnings.append(
                f"Invoice taxable amount ₹{tax_taxable:.2f} ≠ "
                f"sum of line items ₹{calculated_subtotal:.2f}"
            )

    if tax_total:
        expected_total_tax = tax_cgst + tax_sgst + tax_igst + tax_cess
        if abs(expected_total_tax - tax_total) > ROUNDING_TOLERANCE:
            errors.append(
                f"Total tax ₹{tax_total:.2f} ≠ CGST+SGST+IGST+Cess=₹{expected_total_tax:.2f}"
            )
            tax_calculation_valid = False

    # --- Grand Total Validation ---
    grand_total_valid = True
    grand_total = totals.get("grand_total")
    round_off = tax.get("round_off", 0) or 0

    if grand_total and tax_taxable and tax_total:
        expected_grand = tax_taxable + tax_total + round_off
        if abs(expected_grand - grand_total) > ROUNDING_TOLERANCE:
            warnings.append(
                f"Grand total ₹{grand_total:.2f} ≠ "
                f"taxable+tax ₹{expected_grand:.2f} "
                f"(difference: ₹{abs(expected_grand - grand_total):.2f})"
            )
            grand_total_valid = False

    # --- Required Fields Check ---
    if not record.get("invoice", {}).get("invoice_number"):
        warnings.append("Invoice number is missing")
    if not record.get("invoice", {}).get("invoice_date"):
        warnings.append("Invoice date is missing")

    # --- Determine Overall Status ---
    if errors:
        status = "invalid" if len(errors) > 2 else "needs_review"
    elif warnings:
        status = "warning"
    else:
        status = "valid"

    record["validation"] = {
        "status": status,
        "gstin_supplier_valid": supplier_gstin_valid,
        "gstin_buyer_valid": buyer_gstin_valid,
        "tax_calculation_valid": tax_calculation_valid,
        "line_items_valid": line_items_valid,
        "grand_total_valid": grand_total_valid,
        "supply_type_consistent": supply_type_consistent,
        "errors": errors,
        "warnings": warnings,
    }
    return record

def _validate_gstin(gstin: str | None) -> bool:
    if not gstin:
        return False
    gstin = gstin.strip().upper()
    if not re.match(GSTIN_PATTERN, gstin):
        return False
    if gstin[:2] not in STATE_CODES:
        return False
    return True
```

### Input (Phase 5)
- `InvoiceRecord` dict from any processor

### Output
- `validation` field fully populated with:
  - `status`: valid / warning / needs_review / invalid
  - Specific boolean flags per check
  - `errors[]` — critical problems
  - `warnings[]` — minor inconsistencies

---

## Phase 6: Confidence Engine

### Agent Instructions
> **Command to user:** "Start Phase 6: Confidence Engine"

### 6.1 — `backend/app/services/confidence.py`

**Input:** `InvoiceRecord` dict (with AI confidence scores and validation results)
**Output:** Updated `InvoiceRecord` dict with final confidence scores

```python
from app.config import settings

def calculate_confidence(record: dict) -> dict:
    """
    Multi-signal confidence calculation.
    Combines: AI extraction confidence + format validation + math validation
    """
    conf = record.get("confidence", {})
    validation = record.get("validation", {})

    # Signals from validation
    gstin_s_valid = validation.get("gstin_supplier_valid", False)
    gstin_b_valid = validation.get("gstin_buyer_valid", False)
    tax_valid = validation.get("tax_calculation_valid", True)
    items_valid = validation.get("line_items_valid", True)
    total_valid = validation.get("grand_total_valid", True)

    # Boost or penalize AI confidence based on validation
    def _adjust(ai_conf: float | None, validation_passes: bool, weight: float = 0.3) -> float:
        base = ai_conf if ai_conf is not None else 0.5
        if validation_passes:
            return min(1.0, base + weight * (1.0 - base))
        else:
            return max(0.0, base - weight * base)

    final = {
        "invoice_number": _adjust(conf.get("invoice_number"), True),
        "invoice_date": _adjust(conf.get("invoice_date"), True),
        "supplier_name": _adjust(conf.get("supplier_name"), True),
        "supplier_gstin": _adjust(conf.get("supplier_gstin"), gstin_s_valid, 0.5),
        "buyer_name": _adjust(conf.get("buyer_name"), True),
        "buyer_gstin": _adjust(conf.get("buyer_gstin"), gstin_b_valid, 0.5),
        "items": _adjust(conf.get("items"), items_valid, 0.4),
        "quantities": _adjust(conf.get("quantities"), items_valid, 0.4),
        "unit_prices": _adjust(conf.get("unit_prices"), items_valid, 0.4),
        "total": _adjust(conf.get("total"), total_valid, 0.5),
    }

    # Penalize for validation errors
    error_count = len(validation.get("errors", []))
    warning_count = len(validation.get("warnings", []))
    penalty = error_count * 0.1 + warning_count * 0.03

    # Calculate overall confidence
    field_weights = {
        "invoice_number": 1.5, "invoice_date": 1.5,
        "supplier_gstin": 2.0, "buyer_gstin": 2.0,
        "items": 1.5, "total": 2.0,
        "supplier_name": 1.0, "buyer_name": 1.0,
        "quantities": 1.2, "unit_prices": 1.2,
    }

    total_weight = sum(field_weights.values())
    weighted_sum = sum(final.get(f, 0.5) * w for f, w in field_weights.items())
    overall = max(0.0, min(1.0, weighted_sum / total_weight - penalty))

    # Determine low confidence fields
    low_conf_fields = [f for f, v in final.items() if v < settings.confidence_threshold_review]

    final["overall"] = round(overall, 3)
    final["review_required"] = overall < settings.confidence_threshold_review or len(low_conf_fields) > 0
    final["low_confidence_fields"] = low_conf_fields

    record["confidence"] = final
    return record
```

### Confidence Thresholds (configurable in `.env`)
| Threshold | Action |
|-----------|--------|
| `> 0.90` | ✅ Auto-approved — High confidence |
| `0.70 – 0.90` | ⚠️ Warning — Flag for review |
| `< 0.70` | 🔴 Human review required |

---

## Phase 7: FastAPI Endpoints & Export

### Agent Instructions
> **Command to user:** "Start Phase 7: FastAPI Endpoints and Export"

### 7.1 — `backend/app/main.py`

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import upload, invoice, export
from app.database.database import create_tables
import os

app = FastAPI(
    title="VYOM+ Invoice Intelligence API",
    version="1.0.0",
    description="AI-powered GST invoice processing system"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Restrict in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(upload.router, prefix="/api")
app.include_router(invoice.router, prefix="/api")
app.include_router(export.router, prefix="/api")

@app.on_event("startup")
async def startup():
    os.makedirs("uploads", exist_ok=True)
    create_tables()

@app.get("/")
def root():
    return {"message": "VYOM+ Invoice Intelligence API", "status": "running"}

@app.get("/health")
def health():
    return {"status": "healthy"}
```

### 7.2 — `backend/app/routers/upload.py`

**Endpoint:** `POST /api/upload`

```python
from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.file_router import route_file
from app.services.validator import validate_invoice
from app.services.confidence import calculate_confidence
import uuid

router = APIRouter()

@router.post("/upload")
async def upload_invoice(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Upload an invoice document.
    Accepts: .xlsx, .csv, .pdf, .jpg, .jpeg, .png
    Returns: Processed InvoiceRecord with validation and confidence.
    """
    MAX_SIZE = 20 * 1024 * 1024  # 20MB
    file_bytes = await file.read()

    if len(file_bytes) > MAX_SIZE:
        raise HTTPException(status_code=413, detail="File too large. Max 20MB.")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    # 1. Route and extract
    record = await route_file(file, file_bytes)

    # 2. Validate
    record = validate_invoice(record)

    # 3. Confidence
    record = calculate_confidence(record)

    # 4. Save to database
    crud.save_document(db, record)

    return record
```

### 7.3 — `backend/app/routers/invoice.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.validator import validate_invoice
from app.services.confidence import calculate_confidence
from app.schemas.invoice import HumanCorrectionRequest
import json

router = APIRouter()

@router.get("/documents")
def list_documents(db: Session = Depends(get_db)):
    """Get all processed documents."""
    return crud.get_all_documents(db)

@router.get("/documents/{doc_id}")
def get_document(doc_id: str, db: Session = Depends(get_db)):
    """Get a specific document by ID."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return json.loads(doc.raw_json)

@router.put("/documents/{doc_id}")
def apply_correction(
    doc_id: str,
    correction: HumanCorrectionRequest,
    db: Session = Depends(get_db)
):
    """Apply human correction to a field, then revalidate."""
    doc = crud.get_document(db, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    record = json.loads(doc.raw_json)

    # Apply correction using dot-path notation
    record = _apply_correction(record, correction.field_path, correction.corrected_value)

    # Revalidate and recalculate confidence
    record = validate_invoice(record)
    record = calculate_confidence(record)

    # Save updated record
    crud.update_document(db, doc_id, record)
    return record

def _apply_correction(record: dict, field_path: str, value: str) -> dict:
    """Apply a correction using dot-path notation like 'supplier.gstin'."""
    parts = field_path.split(".")
    obj = record
    for part in parts[:-1]:
        obj = obj.get(part, {})
    # Try to coerce to number if possible
    try:
        obj[parts[-1]] = float(value)
    except ValueError:
        obj[parts[-1]] = value
    return record

@router.get("/stats")
def get_stats(db: Session = Depends(get_db)):
    """Dashboard statistics."""
    return crud.get_stats(db)
```

### 7.4 — `backend/app/routers/export.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from app.database.database import get_db
from app.database import crud
from app.services.exporter import export_json, export_csv, export_excel
import json

router = APIRouter()

@router.get("/documents/{doc_id}/json")
def download_json(doc_id: str, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc: raise HTTPException(404, "Not found")
    record = json.loads(doc.raw_json)
    content = export_json(record)
    return StreamingResponse(
        iter([content]),
        media_type="application/json",
        headers={"Content-Disposition": f"attachment; filename={doc_id}.json"}
    )

@router.get("/documents/{doc_id}/csv")
def download_csv(doc_id: str, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc: raise HTTPException(404, "Not found")
    record = json.loads(doc.raw_json)
    content = export_csv(record)
    return StreamingResponse(
        iter([content]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename={doc_id}.csv"}
    )

@router.get("/documents/{doc_id}/excel")
def download_excel(doc_id: str, db: Session = Depends(get_db)):
    doc = crud.get_document(db, doc_id)
    if not doc: raise HTTPException(404, "Not found")
    record = json.loads(doc.raw_json)
    content = export_excel(record)
    return StreamingResponse(
        iter([content]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f"attachment; filename={doc_id}.xlsx"}
    )
```

### 7.5 — `backend/app/services/exporter.py`

```python
import json
import csv
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment

def export_json(record: dict) -> str:
    return json.dumps(record, indent=2, default=str, ensure_ascii=False)

def export_csv(record: dict) -> str:
    output = io.StringIO()
    writer = csv.writer(output)

    # Header info
    inv = record.get("invoice", {})
    supplier = record.get("supplier", {})
    buyer = record.get("buyer", {})

    writer.writerow(["Invoice Number", inv.get("invoice_number", "")])
    writer.writerow(["Invoice Date", inv.get("invoice_date", "")])
    writer.writerow(["Supplier", supplier.get("name", ""), "GSTIN", supplier.get("gstin", "")])
    writer.writerow(["Buyer", buyer.get("name", ""), "GSTIN", buyer.get("gstin", "")])
    writer.writerow([])
    writer.writerow(["Description", "HSN/SAC", "Qty", "Unit", "Rate", "Discount", "Taxable", "GST%", "CGST", "SGST", "IGST", "Total"])

    for item in record.get("items", []):
        writer.writerow([
            item.get("description", ""), item.get("hsn_sac", ""),
            item.get("quantity", ""), item.get("unit", ""),
            item.get("unit_price", ""), item.get("discount", 0),
            item.get("taxable_value", ""), item.get("gst_rate", ""),
            item.get("cgst", ""), item.get("sgst", ""), item.get("igst", ""),
            item.get("total", ""),
        ])

    writer.writerow([])
    totals = record.get("totals", {})
    tax = record.get("tax", {})
    writer.writerow(["Grand Total", totals.get("grand_total", "")])
    writer.writerow(["Total Tax", tax.get("total_tax", "")])

    return output.getvalue()

def export_excel(record: dict) -> bytes:
    wb = openpyxl.Workbook()

    # Sheet 1: Invoice Summary
    ws1 = wb.active
    ws1.title = "Invoice"
    _write_invoice_sheet(ws1, record)

    # Sheet 2: Line Items
    ws2 = wb.create_sheet("Items")
    _write_items_sheet(ws2, record)

    # Sheet 3: Validation
    ws3 = wb.create_sheet("Validation")
    _write_validation_sheet(ws3, record)

    # Sheet 4: Confidence
    ws4 = wb.create_sheet("Confidence")
    _write_confidence_sheet(ws4, record)

    buf = io.BytesIO()
    wb.save(buf)
    return buf.getvalue()

def _write_invoice_sheet(ws, record: dict):
    header_font = Font(bold=True)
    inv = record.get("invoice", {})
    supplier = record.get("supplier", {})
    buyer = record.get("buyer", {})
    totals = record.get("totals", {})
    tax = record.get("tax", {})

    rows = [
        ("Invoice Number", inv.get("invoice_number")),
        ("Invoice Date", inv.get("invoice_date")),
        ("Place of Supply", inv.get("place_of_supply")),
        ("Supply Type", inv.get("supply_type")),
        ("", ""),
        ("SUPPLIER", ""),
        ("Name", supplier.get("name")),
        ("GSTIN", supplier.get("gstin")),
        ("Address", supplier.get("address")),
        ("", ""),
        ("BUYER", ""),
        ("Name", buyer.get("name")),
        ("GSTIN", buyer.get("gstin")),
        ("Address", buyer.get("address")),
        ("", ""),
        ("TOTALS", ""),
        ("Subtotal", totals.get("subtotal")),
        ("Total Tax", tax.get("total_tax")),
        ("Grand Total", totals.get("grand_total")),
        ("Amount in Words", totals.get("amount_in_words")),
    ]
    for r, (label, value) in enumerate(rows, 1):
        ws.cell(r, 1, label).font = header_font
        ws.cell(r, 2, value)

def _write_items_sheet(ws, record: dict):
    headers = ["#", "Description", "HSN/SAC", "Qty", "Unit", "Rate", "Discount", "Taxable", "GST%", "CGST", "SGST", "IGST", "Cess", "Total"]
    for c, h in enumerate(headers, 1):
        cell = ws.cell(1, c, h)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor="1E3A5F")
        cell.font = Font(bold=True, color="FFFFFF")

    for r, item in enumerate(record.get("items", []), 2):
        ws.cell(r, 1, r - 1)
        ws.cell(r, 2, item.get("description"))
        ws.cell(r, 3, item.get("hsn_sac"))
        ws.cell(r, 4, item.get("quantity"))
        ws.cell(r, 5, item.get("unit"))
        ws.cell(r, 6, item.get("unit_price"))
        ws.cell(r, 7, item.get("discount", 0))
        ws.cell(r, 8, item.get("taxable_value"))
        ws.cell(r, 9, item.get("gst_rate"))
        ws.cell(r, 10, item.get("cgst"))
        ws.cell(r, 11, item.get("sgst"))
        ws.cell(r, 12, item.get("igst"))
        ws.cell(r, 13, item.get("cess"))
        ws.cell(r, 14, item.get("total"))

def _write_validation_sheet(ws, record: dict):
    val = record.get("validation", {})
    ws.cell(1, 1, "Status").font = Font(bold=True)
    ws.cell(1, 2, val.get("status"))
    ws.cell(2, 1, "Errors").font = Font(bold=True)
    for i, e in enumerate(val.get("errors", []), 3):
        ws.cell(i, 1, f"ERROR {i-2}")
        ws.cell(i, 2, e)
    offset = 3 + len(val.get("errors", []))
    ws.cell(offset, 1, "Warnings").font = Font(bold=True)
    for i, w in enumerate(val.get("warnings", []), offset + 1):
        ws.cell(i, 1, f"WARNING {i-offset}")
        ws.cell(i, 2, w)

def _write_confidence_sheet(ws, record: dict):
    conf = record.get("confidence", {})
    ws.cell(1, 1, "Field").font = Font(bold=True)
    ws.cell(1, 2, "Confidence").font = Font(bold=True)
    ws.cell(1, 3, "Status").font = Font(bold=True)
    skip = {"overall", "review_required", "low_confidence_fields"}
    for r, (field, value) in enumerate(conf.items(), 2):
        if field in skip or not isinstance(value, (int, float)):
            continue
        ws.cell(r, 1, field)
        ws.cell(r, 2, f"{value:.1%}")
        ws.cell(r, 3, "✅ High" if value >= 0.90 else "⚠️ Review" if value >= 0.70 else "🔴 Human Review")
```

### 7.6 — `backend/app/database/crud.py`

```python
from sqlalchemy.orm import Session
from .models import DocumentModel, InvoiceModel, InvoiceItemModel
import json, uuid

def save_document(db: Session, record: dict):
    doc_id = record["document"]["id"]
    doc = DocumentModel(
        id=doc_id,
        filename=record["document"]["filename"],
        file_type=record["document"]["source_type"],
        source_type=record["document"]["source_type"],
        status=record["validation"]["status"],
        overall_confidence=record["confidence"]["overall"],
        raw_json=json.dumps(record, default=str),
        page_count=record["document"].get("page_count", 1),
    )
    db.add(doc)
    db.commit()

def get_document(db: Session, doc_id: str):
    return db.query(DocumentModel).filter(DocumentModel.id == doc_id).first()

def get_all_documents(db: Session):
    docs = db.query(DocumentModel).order_by(DocumentModel.created_at.desc()).all()
    return [
        {
            "id": d.id, "filename": d.filename, "file_type": d.file_type,
            "status": d.status, "confidence": d.overall_confidence,
            "upload_time": str(d.upload_time), "page_count": d.page_count,
        }
        for d in docs
    ]

def update_document(db: Session, doc_id: str, record: dict):
    doc = get_document(db, doc_id)
    if doc:
        doc.raw_json = json.dumps(record, default=str)
        doc.status = record["validation"]["status"]
        doc.overall_confidence = record["confidence"]["overall"]
        db.commit()

def get_stats(db: Session) -> dict:
    total = db.query(DocumentModel).count()
    valid = db.query(DocumentModel).filter(DocumentModel.status == "valid").count()
    review = db.query(DocumentModel).filter(
        DocumentModel.status.in_(["needs_review", "warning"])
    ).count()
    avg_conf = db.query(DocumentModel).with_entities(
        db.query(DocumentModel.overall_confidence).scalar
    ).scalar() or 0.0
    from sqlalchemy import func
    avg_conf_result = db.query(func.avg(DocumentModel.overall_confidence)).scalar() or 0.0
    return {
        "total_documents": total,
        "validated": valid,
        "needs_review": review,
        "average_confidence": round(avg_conf_result, 3),
        "invalid": total - valid - review,
    }
```

---

## Phase 8: Basic Streamlit UI (Demo)

### Agent Instructions
> **Command to user:** "Start Phase 8: Streamlit Demo UI"
> **Agent will:** Create a functional demo UI for qualifier submission.

### 8.1 — `backend/demo_ui/streamlit_app.py`

The Streamlit app will:
1. Show file upload widget (drag and drop)
2. Call the FastAPI backend
3. Show processing steps live
4. Display extracted fields, validation, confidence
5. Show export buttons (JSON, CSV)

**Key UI sections:**
- Sidebar: navigation and API status
- Upload section: file uploader + processing animation
- Results section:
  - Left: original file preview (image/PDF)
  - Right: extracted data table
- Validation panel: errors/warnings with color coding
- Confidence panel: field-level confidence bars
- Export section: download buttons

**Run command:**
```bash
# From backend/ directory with venv active:
# Start FastAPI first:
uvicorn app.main:app --reload --port 8000

# In second terminal:
streamlit run demo_ui/streamlit_app.py
```

---

## Phase 9: README & Qualifier Submission

### Agent Instructions
> **Command to user:** "Start Phase 9: README and Submission Prep"
> **Agent will:** Write the complete README.md for the project.

### README.md Structure

```markdown
# VYOM+ — End-to-End AI-Powered GST Invoice Intelligence System

> "OCR alone reads documents. VYOM+ turns documents into trustworthy financial records."

## 🏆 Hacktober Fest 4 | Problem Statement 3

## What is VYOM+?
[Project description]

## Architecture Diagram
[Text-art architecture from the implementation guide]

## Supported Formats
[Table of all 5 formats]

## Key Features
- Multi-format support
- Vision AI extraction
- Deterministic GST validation
- Confidence scoring
- Human-in-the-loop review
- Multi-format export

## Technology Stack
[Full stack table]

## Getting Started
[Setup instructions]

## API Documentation
[All endpoints]

## Sample Output
[Sample JSON]

## Demo
[Instructions to run demo]
```

---

# PART 2 — FULL POLISHED PROJECT

> **Goal:** Enterprise-grade SaaS-style full-stack application with Next.js frontend, polished UI, complete features, and deployment.

---

## Phase 10: Next.js Frontend Setup

### Agent Instructions
> **Command to user:** "Start Phase 10: Next.js Frontend Setup"

### Steps

**10.1 — Initialize Next.js project**
```bash
cd vyom-invoice-ai/frontend
npx create-next-app@latest . --typescript --tailwind --app --no-git
```

**10.2 — Install additional dependencies**
```bash
npm install axios react-dropzone lucide-react recharts
npm install @radix-ui/react-dialog @radix-ui/react-progress
npm install react-pdf
npm install framer-motion
npm install sonner   # toast notifications
```

**10.3 — Configure `tailwind.config.ts`**
Custom dark navy + purple accent color theme matching VYOM+ branding.

**10.4 — Create `lib/api.ts`**
Axios instance pointing to FastAPI backend with all typed API calls.

**10.5 — Create `lib/types.ts`**
TypeScript interfaces mirroring all Pydantic models.

---

## Phase 11: Dashboard Page

### Route: `/`

**UI Elements:**
- Top stats bar: Total Documents | Validated | Needs Review | Avg Confidence
- Recent Documents table with: filename, type icon, confidence badge, status badge, date
- Document type distribution pie chart (Recharts)
- Processing quality by type bar chart

**Design:**
- Dark navy `#0F172A` background
- Card component: `bg-slate-800 rounded-xl shadow-lg`
- Purple accent `#7C3AED` for CTAs
- Status badges: green (valid), yellow (warning), red (review/invalid)

---

## Phase 12: Upload Page

### Route: `/upload`

**UI Elements:**
1. **Drag-and-drop zone** — Animated border, accepts all 5 formats
2. **File type indicator** — Shows detected type after selection
3. **Processing animation** — Shows live pipeline steps:
   - ✓ File identified
   - ✓ Document quality analyzed
   - ✓ OCR / Vision extraction started
   - ✓ Invoice fields extracted
   - ✓ GST validated
   - ✓ Confidence calculated
4. **Redirect** — After processing, auto-redirect to `/documents/{id}`

---

## Phase 13: Documents List Page

### Route: `/documents`

**UI Elements:**
- Search bar
- Filter by: status, file type, date range
- Table/grid view toggle
- Each document card: filename, confidence bar, status badge, date, view button

---

## Phase 14: Invoice Review Page

### Route: `/documents/[id]`

**Two-column layout:**

**Left Panel — Original Document Viewer**
- PDF viewer (react-pdf) with page navigation
- Image viewer for JPG/PNG
- For Excel/CSV: tabular preview

**Right Panel — Extracted Data**
- Invoice metadata (number, date, place of supply)
- Supplier & Buyer info with GSTIN validation badge
- Line items table (editable if review_required)
- GST summary breakdown
- Grand total
- Validation panel (errors/warnings color coded)
- Confidence section (per-field bars with color indicators)
- Export buttons: JSON | CSV | Excel

---

## Phase 15: Analytics Page

### Route: `/analytics`

**Charts:**
1. Documents processed over time (line chart)
2. Document type distribution (pie)
3. Validation status distribution (donut)
4. Average confidence by document type (bar)
5. Accuracy metrics table (from test dataset)

---

## Phase 16: Human-in-the-Loop Review UI

### Route: `/documents/[id]` (review mode)

**When `review_required = true`:**
- Show alert banner: "⚠️ {N} fields require human verification"
- For each low-confidence field:
  ```
  Supplier GSTIN — 61% confidence
  AI extracted: 27ABCDE1234F1Z5
  [27ABCDE1234F1Z5          ] ← editable input
  [Accept] [Edit & Revalidate]
  ```
- After all corrections: "Revalidate Invoice" button
- Revalidation updates: validation status, confidence, all calculated fields

---

## Phase 17: Advanced Features

### Agent Instructions
> **Command to user:** "Start Phase 17: Advanced Features"
> Implement these after core is working.

### 17.1 — QR Code Support
- Use `pyzbar` to detect and decode QR codes in invoice images
- Compare QR-decoded GSTIN/amount against AI-extracted values
- Show "QR Verified ✓" badge if they match

### 17.2 — Duplicate Invoice Detection
- Before saving, check DB for matching: invoice_number + supplier_gstin + invoice_date
- If match found: show "⚠️ Possible Duplicate" warning

### 17.3 — Invoice Anomaly Detection
Detect and flag:
- Unusual GST rates
- CGST+SGST ≠ total GST
- Taxable × rate ≠ tax amount
- Grand total mismatch > ₹5
- Missing mandatory fields

### 17.4 — Multi-page PDF handling
- Process all pages together
- Combine extracted data across pages
- Store `source_pages: [1, 2, 3]` per line item

### 17.5 — Batch Upload
- Allow uploading multiple files at once
- Show progress for each file
- Summary results table after batch completes

---

## Phase 18: Testing Dataset & Evaluation

### Agent Instructions
> **Command to user:** "Start Phase 18: Testing and Evaluation"
> **User action required:** Provide sample invoice files.

### 18.1 — Dataset Requirements

The user needs to collect:
| Type | Count | How to get |
|------|-------|-----------|
| Printed invoices (JPG/PNG) | 10 | Scan or photograph printed GST invoices |
| Digital PDFs | 10 | Download GST invoice PDFs from anywhere |
| Handwritten invoices (JPG) | 10 | Write mock GST invoices, photograph them |
| Poor quality images | 5 | Low-light, blurry, angled photos |
| Excel files | 5 | GST invoice data in .xlsx format |
| CSV files | 5 | Invoice data in .csv format |

### 18.2 — Sample Data the Agent Will Create

For Excel/CSV testing, the agent will create:
- `sample_invoices/excel/sample_gst_invoice.xlsx` — 10 sample GST invoice rows
- `sample_invoices/csv/sample_gst_invoices.csv` — Same data in CSV
- `sample_invoices/digital_pdf/` — Agent generates synthetic PDF invoices using fpdf2

### 18.3 — Evaluation Script

Agent creates `backend/evaluate.py`:
- Processes all sample invoices
- Compares extracted vs ground truth
- Reports per-field accuracy
- Generates accuracy table for README/presentation

---

## Phase 19: Deployment

### Agent Instructions
> **Command to user:** "Start Phase 19: Deployment"

### 19.1 — Backend Deployment (Render)

1. Agent creates `backend/Dockerfile`:
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

2. Agent creates `render.yaml`:
```yaml
services:
  - type: web
    name: vyom-backend
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
    envVars:
      - key: GEMINI_API_KEY
        sync: false
      - key: DATABASE_URL
        sync: false
```

3. User sets `GEMINI_API_KEY` in Render environment variables.

### 19.2 — Database Migration (Part 2)

Replace SQLite with PostgreSQL:
- User creates free Supabase project
- Agent updates `DATABASE_URL` to PostgreSQL connection string
- Agent updates SQLAlchemy engine (remove `check_same_thread`)

### 19.3 — Frontend Deployment (Vercel)

1. Agent creates `frontend/.env.local`:
```
NEXT_PUBLIC_API_URL=https://vyom-backend.onrender.com
```

2. User deploys to Vercel:
```bash
npx vercel --prod
```

---

## Phase 20: Final Polish & Presentation Assets

### Agent Instructions
> **Command to user:** "Start Phase 20: Final Polish and Presentation"

### 20.1 — Demo Invoices

Agent creates ready-to-use demo invoices:
- `sample_invoices/demo_printed.pdf` — Clean printed GST invoice (fpdf2)
- `sample_invoices/demo_excel.xlsx` — Excel invoice with multiple line items
- `sample_invoices/demo_csv.csv` — CSV format

### 20.2 — Demo Flow for Presentation

**Judge Demo Sequence:**

| Step | Action | Expected Result |
|------|--------|----------------|
| 1 | Open VYOM+ dashboard | Show stats cards and recent documents |
| 2 | Upload `demo_printed.pdf` | Watch processing animation |
| 3 | View extracted invoice | 98%+ confidence, all fields |
| 4 | Download JSON | Full structured JSON |
| 5 | Upload `demo_excel.xlsx` | Tabular data processed |
| 6 | Upload handwritten invoice | Lower confidence, review flags |
| 7 | Correct uncertain field | Revalidate, confidence improves |
| 8 | Show Analytics page | Charts and accuracy metrics |

### 20.3 — Architecture Diagram

Agent creates `docs/architecture.md` with mermaid diagram of the full system.

### 20.4 — Final README Update

Add:
- Live demo link
- Screenshot gallery
- Evaluation results table
- Architecture diagram (mermaid)
- Team information

---

## User-Supplied Resources Checklist

> The AI agent will ask for these at the appropriate phase:

| Resource | When Needed | Where to Get |
|----------|------------|--------------|
| 🔑 **Gemini API Key** | Phase 4 | https://aistudio.google.com/app/apikey (Free) |
| 📄 **Sample printed invoices** | Phase 18 | Scan/photo any GST invoice |
| ✍️ **Handwritten invoices** | Phase 18 | Write mock invoice, photograph it |
| 📊 **Sample Excel/CSV** | Phase 18 | Agent creates templates |
| 🌐 **Render account** | Phase 19 | https://render.com (Free tier) |
| 🌐 **Vercel account** | Phase 19 | https://vercel.com (Free tier) |
| 🗃️ **Supabase account** (optional) | Phase 19 | https://supabase.com (Free tier) |

---

## Agent Command Reference

Use these commands to trigger each phase:

| Command | What Happens |
|---------|-------------|
| `"Start Phase 1: Project Setup"` | Creates folder structure, venv, installs dependencies |
| `"Start Phase 2: Schemas and Database"` | Creates Pydantic models and DB models |
| `"Start Phase 3: Document Processing Pipelines"` | Creates all 5 format processors |
| `"Start Phase 4: AI Extraction Engine"` | Creates Gemini extractor (needs API key) |
| `"Start Phase 5: Validation Engine"` | Creates GST + math validator |
| `"Start Phase 6: Confidence Engine"` | Creates multi-signal confidence scorer |
| `"Start Phase 7: FastAPI Endpoints and Export"` | Creates all API endpoints + export |
| `"Start Phase 8: Streamlit Demo UI"` | Creates qualifier demo UI |
| `"Start Phase 9: README and Submission Prep"` | Writes complete README |
| `"Start Phase 10: Next.js Frontend Setup"` | Initializes Next.js app |
| `"Start Phase 11: Dashboard Page"` | Builds dashboard with stats |
| `"Start Phase 12: Upload Page"` | Builds upload with animation |
| `"Start Phase 13: Documents List Page"` | Builds document browser |
| `"Start Phase 14: Invoice Review Page"` | Builds full review page |
| `"Start Phase 15: Analytics Page"` | Builds analytics charts |
| `"Start Phase 16: Human-in-the-Loop Review UI"` | Builds correction interface |
| `"Start Phase 17: Advanced Features"` | QR, duplicates, anomalies, batch |
| `"Start Phase 18: Testing and Evaluation"` | Creates test data, evaluation script |
| `"Start Phase 19: Deployment"` | Dockerfile, Render config, Vercel |
| `"Start Phase 20: Final Polish and Presentation"` | Demo invoices, final README, arch diagram |

---

## Quick Start (Part 1 — Qualifier)

```bash
# 1. Clone/Navigate to project
cd c:\Users\LOQ\Desktop\HACKTOBER\vyom-invoice-ai\backend

# 2. Activate virtual environment
venv\Scripts\activate

# 3. Set environment variables
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# 4. Start FastAPI backend
uvicorn app.main:app --reload --port 8000

# 5. Start Streamlit demo UI (new terminal)
venv\Scripts\activate
streamlit run demo_ui/streamlit_app.py

# 6. Open browser
# FastAPI docs: http://localhost:8000/docs
# Streamlit demo: http://localhost:8501
```

---

> **Implementation Principle:**
> Build Phase 1–9 first. Get a working end-to-end pipeline. Test with real invoices. Then move to Part 2 (Phase 10–20) for the polished frontend and deployment.
>
> **Core Philosophy:** *AI extracts. Deterministic code validates. Confidence decides. Humans resolve uncertainty.*
