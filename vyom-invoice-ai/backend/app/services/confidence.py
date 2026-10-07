from typing import Dict, Any, List, Optional
from app.config import settings

def _adjust(ai_conf: Optional[float], validation_passes: bool, weight: float = 0.3) -> float:
    """
    Boost or penalize AI extraction confidence based on deterministic validation.
    """
    base = float(ai_conf) if ai_conf is not None else 0.90
    if validation_passes:
        # Boost towards 1.0
        return min(1.0, round(base + weight * (1.0 - base), 3))
    else:
        # Penalize downwards
        return max(0.0, round(base - weight * base, 3))

def calculate_confidence(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Multi-Signal Confidence Scoring Algorithm.
    Combines:
      - Multi-modal AI / OCR extraction confidence
      - Deterministic GST syntax validity
      - Mathematical and accounting reconciliation checks
    Returns the updated record with comprehensive confidence metrics.
    """
    conf = record.get("confidence") or {}
    validation = record.get("validation") or {}

    # Validation signals
    gstin_s_valid = validation.get("gstin_supplier_valid", False)
    gstin_b_valid = validation.get("gstin_buyer_valid", False)
    tax_valid = validation.get("tax_calculation_valid", True)
    items_valid = validation.get("line_items_valid", True)
    total_valid = validation.get("grand_total_valid", True)
    supply_type_valid = validation.get("supply_type_consistent", True)

    final: Dict[str, float] = {
        "invoice_number": _adjust(conf.get("invoice_number"), True, 0.1),
        "invoice_date": _adjust(conf.get("invoice_date"), True, 0.1),
        "supplier_name": _adjust(conf.get("supplier_name"), True, 0.1),
        "supplier_gstin": _adjust(conf.get("supplier_gstin"), gstin_s_valid, 0.5),
        "buyer_name": _adjust(conf.get("buyer_name"), True, 0.1),
        "buyer_gstin": _adjust(conf.get("buyer_gstin"), gstin_b_valid, 0.5),
        "items": _adjust(conf.get("items"), items_valid, 0.4),
        "quantities": _adjust(conf.get("quantities"), items_valid, 0.3),
        "unit_prices": _adjust(conf.get("unit_prices"), items_valid, 0.3),
        "total": _adjust(conf.get("total"), total_valid, 0.5),
    }

    # Error and warning penalties
    errors = validation.get("errors", [])
    warnings = validation.get("warnings", [])
    penalty = (len(errors) * 0.12) + (len(warnings) * 0.03)

    # Statutory field weighting
    field_weights = {
        "supplier_gstin": 2.0,
        "buyer_gstin": 2.0,
        "total": 2.0,
        "invoice_number": 1.5,
        "invoice_date": 1.5,
        "items": 1.5,
        "quantities": 1.2,
        "unit_prices": 1.2,
        "supplier_name": 1.0,
        "buyer_name": 1.0,
    }

    total_weight = sum(field_weights.values())
    weighted_sum = sum(final.get(field, 0.5) * weight for field, weight in field_weights.items())
    overall = max(0.0, min(1.0, (weighted_sum / total_weight) - penalty))

    threshold_review = getattr(settings, "confidence_threshold_review", 0.70)
    low_confidence_fields = [f for f, v in final.items() if v < threshold_review]

    final_scores = {
        **final,
        "overall": round(overall, 3),
        "review_required": bool(overall < threshold_review or len(low_confidence_fields) > 0 or len(errors) > 0),
        "low_confidence_fields": low_confidence_fields
    }

    record["confidence"] = final_scores
    return record
