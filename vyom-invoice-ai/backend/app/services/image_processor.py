import cv2
import numpy as np
from PIL import Image
import io
from typing import Dict, Any, Optional

def _resize_if_needed(img: np.ndarray, max_dim: int = 2000) -> np.ndarray:
    h, w = img.shape[:2]
    if max(h, w) > max_dim:
        scale = max_dim / max(h, w)
        img = cv2.resize(img, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
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
        median_angle = float(np.median(angles))
        if abs(median_angle) < 0.5:
            return gray
        h, w = gray.shape
        M = cv2.getRotationMatrix2D((w // 2, h // 2), median_angle, 1.0)
        return cv2.warpAffine(gray, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    except Exception:
        return gray

def preprocess_image(image_bytes: bytes) -> Dict[str, np.ndarray]:
    """
    Returns multiple preprocessed versions of the image.
    The AI extractor or OCR will select the most optimal variant.
    """
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not decode image from provided bytes.")

    results: Dict[str, np.ndarray] = {}

    # 1. Resized original
    resized = _resize_if_needed(img)
    results["original"] = resized

    # 2. Grayscale
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    results["grayscale"] = gray

    # 3. Enhanced contrast (CLAHE)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced = clahe.apply(gray)
    results["enhanced"] = enhanced

    # 4. Denoised
    denoised = cv2.fastNlMeansDenoising(gray, h=10)
    results["denoised"] = denoised

    # 5. Adaptive threshold (clean printed text)
    thresh = cv2.adaptiveThreshold(
        denoised, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY, 11, 2
    )
    results["threshold"] = thresh

    # 6. Deskewed
    results["deskewed"] = _deskew(gray)

    return results

def cv2_to_pil(img_array: np.ndarray) -> Image.Image:
    """Convert OpenCV image array to PIL Image."""
    if len(img_array.shape) == 2:  # Grayscale
        return Image.fromarray(img_array)
    return Image.fromarray(cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB))

def pil_to_bytes(pil_img: Image.Image, format: str = "JPEG") -> bytes:
    """Convert PIL Image to byte string."""
    buf = io.BytesIO()
    if pil_img.mode != "RGB" and format.upper() == "JPEG":
        pil_img = pil_img.convert("RGB")
    pil_img.save(buf, format=format, quality=95)
    return buf.getvalue()

def analyze_image_quality(img: np.ndarray) -> Dict[str, Any]:
    """Analyze image quality (blurriness, illumination, contrast)."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) if len(img.shape) == 3 else img
    blur_score = float(cv2.Laplacian(gray, cv2.CV_64F).var())
    brightness = float(gray.mean())
    contrast = float(gray.std())
    return {
        "blur_score": blur_score,
        "is_blurry": blur_score < 100,
        "brightness": brightness,
        "is_dark": brightness < 80,
        "contrast": contrast,
        "quality": "high" if blur_score > 300 else ("medium" if blur_score > 100 else "low")
    }

async def process_image(image_bytes: bytes, filename: str) -> dict:
    """
    Full image processing pipeline:
    Analyzes quality, picks best preprocessed image, then invokes AI extraction.
    """
    from .ai_extractor import extract_from_image

    preprocessed = preprocess_image(image_bytes)
    quality = analyze_image_quality(preprocessed["original"])

    if quality["quality"] == "high":
        best_img = preprocessed["original"]
    elif quality["is_dark"]:
        best_img = preprocessed["enhanced"]
    else:
        best_img = preprocessed["deskewed"]

    best_bytes = pil_to_bytes(cv2_to_pil(best_img))

    return await extract_from_image(
        image_bytes=best_bytes,
        filename=filename,
        source_type="image",
        page_count=1
    )
