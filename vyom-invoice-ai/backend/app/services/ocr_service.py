import pytesseract
from PIL import Image
import numpy as np
from typing import Dict, Any, Optional

def extract_text_from_image(image: Any) -> str:
    """
    Extract raw text using Tesseract OCR.
    Handles PIL Images and OpenCV numpy arrays.
    Gracefully catches TesseractNotFound errors.
    """
    try:
        if isinstance(image, np.ndarray):
            # Convert BGR/Grayscale to RGB for PIL
            if len(image.shape) == 2:
                pil_img = Image.fromarray(image)
            else:
                import cv2
                pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_img = image

        text = pytesseract.image_to_string(pil_img, config='--psm 6')
        return text.strip()
    except pytesseract.TesseractNotFoundError:
        return ""
    except Exception:
        return ""

def get_ocr_confidence_data(image: Any) -> Dict[str, Any]:
    """
    Extract OCR word-level bounding boxes and confidence scores.
    """
    try:
        if isinstance(image, np.ndarray):
            if len(image.shape) == 2:
                pil_img = Image.fromarray(image)
            else:
                import cv2
                pil_img = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        else:
            pil_img = image

        data = pytesseract.image_to_data(pil_img, output_type=pytesseract.Output.DICT)
        confs = [float(c) for c in data.get('conf', []) if str(c).isdigit() and float(c) > 0]
        avg_conf = (sum(confs) / len(confs)) / 100.0 if confs else 0.5
        return {
            "average_confidence": round(avg_conf, 2),
            "word_count": len(confs),
            "raw_text": pytesseract.image_to_string(pil_img).strip()
        }
    except Exception:
        return {
            "average_confidence": 0.5,
            "word_count": 0,
            "raw_text": ""
        }
