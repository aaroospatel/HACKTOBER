import pymupdf
import io
from typing import Dict, Any

async def process_pdf(file_bytes: bytes, filename: str) -> dict:
    """
    Process both digital and scanned PDFs.
    Routes digital PDFs to text extraction, and scanned PDFs to vision extraction.
    """
    from .ai_extractor import extract_from_text, extract_from_image

    doc = pymupdf.open(stream=file_bytes, filetype="pdf")
    pages_text = []
    page_images = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        text = page.get_text("text").strip()
        pages_text.append(text)

        # Render page to high-res image for scanned page processing
        mat = pymupdf.Matrix(2, 2)  # 2x zoom for clarity
        pix = page.get_pixmap(matrix=mat)
        img_bytes = pix.tobytes("png")
        page_images.append(img_bytes)

    total_text = "\n".join(pages_text).strip()
    is_digital = len(total_text) > 100

    if is_digital:
        # Digital PDF with selectable text
        result = await extract_from_text(
            text=total_text,
            filename=filename,
            source_type="pdf_digital",
            page_count=len(doc)
        )
    else:
        # Scanned PDF or image-only PDF
        result = await extract_from_image(
            image_bytes=page_images[0] if page_images else b"",
            filename=filename,
            source_type="pdf_scanned",
            additional_pages=page_images[1:] if len(page_images) > 1 else [],
            page_count=len(doc)
        )

    doc.close()
    return result
