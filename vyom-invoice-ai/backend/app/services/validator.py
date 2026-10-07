import re
from typing import Dict, Any, Optional
from app.utils.gst_rules import GSTIN_PATTERN, VALID_GST_RATES, STATE_CODES

ROUNDING_TOLERANCE = 2.0  # ₹2 tolerance for rounding differences

def _validate_gstin(gstin: Optional[str]) -> bool:
    """Validate 15-character Indian GSTIN format and state code."""
    if not gstin:
        return False
    gstin = str(gstin).strip().upper()
    if not re.match(GSTIN_PATTERN, gstin):
        return False
    if gstin[:2] not in STATE_CODES:
        return False
    return True

def validate_invoice(record: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute deterministic GST statutory and mathematical consistency checks.
    Updates and returns the invoice record with comprehensive validation results.
    """
    errors = []
    warnings = []

    supplier = record.get("supplier") or {}
    buyer = record.get("buyer") or {}
    invoice = record.get("invoice") or {}
    items = record.get("items") or []
    tax = record.get("tax") or {}
    totals = record.get("totals") or {}

    supplier_gstin = supplier.get("gstin")
    buyer_gstin = buyer.get("gstin")

    # 1. GSTIN Format & State Code Validation
    supplier_gstin_valid = _validate_gstin(supplier_gstin)
    buyer_gstin_valid = _validate_gstin(buyer_gstin)

    if supplier_gstin:
        if not supplier_gstin_valid:
            errors.append(f"Supplier GSTIN '{supplier_gstin}' is invalid (does not match 15-char statutory format or state code).")
        else:
            supplier["state_code"] = str(supplier_gstin)[:2]
    else:
        warnings.append("Supplier GSTIN is missing.")

    if buyer_gstin:
        if not buyer_gstin_valid:
            errors.append(f"Buyer GSTIN '{buyer_gstin}' is invalid (does not match 15-char statutory format or state code).")
        else:
            buyer["state_code"] = str(buyer_gstin)[:2]
    else:
        warnings.append("Buyer GSTIN is missing.")

    # 2. Supply Type Consistency (Intra-State vs Inter-State)
    supply_type_consistent = True
    if supplier_gstin_valid and buyer_gstin_valid:
        same_state = str(supplier_gstin)[:2] == str(buyer_gstin)[:2]
        cgst_val = float(tax.get("cgst") or 0.0)
        sgst_val = float(tax.get("sgst") or 0.0)
        igst_val = float(tax.get("igst") or 0.0)

        if same_state:
            invoice["supply_type"] = "intra-state"
            if igst_val > 0.0 and (cgst_val == 0.0 or sgst_val == 0.0):
                warnings.append("Intra-state supply detected (matching state codes), but IGST was charged instead of CGST + SGST.")
                supply_type_consistent = False
        else:
            invoice["supply_type"] = "inter-state"
            if (cgst_val > 0.0 or sgst_val > 0.0) and igst_val == 0.0:
                warnings.append("Inter-state supply detected (differing state codes), but CGST/SGST was charged instead of IGST.")
                supply_type_consistent = False

    # 3. Line Items Arithmetic Validation
    line_items_valid = True
    calculated_subtotal = 0.0

    for i, item in enumerate(items):
        desc = item.get("description") or f"Item {i+1}"
        qty = item.get("quantity")
        price = item.get("unit_price")
        taxable = item.get("taxable_value")
        discount = float(item.get("discount") or 0.0)
        gst_rate = item.get("gst_rate")
        cgst = item.get("cgst")
        sgst = item.get("sgst")
        igst = item.get("igst")
        item_total = item.get("total")

        # Qty × Rate − Discount ≈ Taxable
        if qty is not None and price is not None and taxable is not None:
            expected_taxable = round(float(qty) * float(price) - discount, 2)
            if abs(expected_taxable - float(taxable)) > ROUNDING_TOLERANCE:
                warnings.append(
                    f"Line Item #{i+1} ('{desc}'): Quantity ({qty}) × Unit Price ({price}) − Discount ({discount}) = Rs. {expected_taxable:.2f}, but extracted Taxable Value is Rs. {float(taxable):.2f}."
                )
                line_items_valid = False

        # GST Rate Verification
        if gst_rate is not None:
            gst_rate_num = float(gst_rate)
            if gst_rate_num not in VALID_GST_RATES:
                warnings.append(f"Line Item #{i+1} ('{desc}'): Unusual or non-standard GST rate: {gst_rate_num}%.")

        # Line Item Tax Amount Verification
        if taxable is not None and gst_rate is not None:
            expected_tax = round(float(taxable) * float(gst_rate) / 100.0, 2)
            if cgst is not None and sgst is not None:
                actual_tax = round(float(cgst) + float(sgst), 2)
                if abs(actual_tax - expected_tax) > ROUNDING_TOLERANCE:
                    errors.append(
                        f"Line Item #{i+1} ('{desc}'): Expected Tax at {gst_rate}% is Rs. {expected_tax:.2f}, but CGST ({cgst}) + SGST ({sgst}) = Rs. {actual_tax:.2f}."
                    )
            elif igst is not None:
                if abs(float(igst) - expected_tax) > ROUNDING_TOLERANCE:
                    errors.append(
                        f"Line Item #{i+1} ('{desc}'): Expected IGST at {gst_rate}% is Rs. {expected_tax:.2f}, but got Rs. {float(igst):.2f}."
                    )

        if taxable is not None:
            calculated_subtotal += float(taxable)

    # 4. Tax Totals Reconciliation
    tax_calculation_valid = True
    tax_taxable = tax.get("taxable_amount")
    tax_cgst = float(tax.get("cgst") or 0.0)
    tax_sgst = float(tax.get("sgst") or 0.0)
    tax_igst = float(tax.get("igst") or 0.0)
    tax_cess = float(tax.get("cess") or 0.0)
    tax_total = tax.get("total_tax")

    if tax_taxable is not None and calculated_subtotal > 0:
        if abs(float(tax_taxable) - calculated_subtotal) > ROUNDING_TOLERANCE:
            warnings.append(
                f"Invoice Taxable Amount Rs. {float(tax_taxable):.2f} does not reconcile with sum of Line Items Rs. {calculated_subtotal:.2f}."
            )

    if tax_total is not None:
        expected_total_tax = round(tax_cgst + tax_sgst + tax_igst + tax_cess, 2)
        if abs(expected_total_tax - float(tax_total)) > ROUNDING_TOLERANCE:
            errors.append(
                f"Total Tax Rs. {float(tax_total):.2f} does not match sum of CGST + SGST + IGST + Cess (Rs. {expected_total_tax:.2f})."
            )
            tax_calculation_valid = False

    # 5. Grand Total Reconciliation
    grand_total_valid = True
    grand_total = totals.get("grand_total")
    round_off = float(tax.get("round_off") or 0.0)

    reconcile_taxable = float(tax_taxable) if tax_taxable is not None else (calculated_subtotal if calculated_subtotal > 0 else None)
    reconcile_tax = float(tax_total) if tax_total is not None else (tax_cgst + tax_sgst + tax_igst + tax_cess)

    if grand_total is not None and reconcile_taxable is not None and reconcile_tax is not None:
        expected_grand = round(reconcile_taxable + reconcile_tax + round_off, 2)
        if abs(expected_grand - float(grand_total)) > ROUNDING_TOLERANCE:
            warnings.append(
                f"Grand Total Rs. {float(grand_total):.2f} differs from Taxable ({reconcile_taxable:.2f}) + Tax ({reconcile_tax:.2f}) + Round-off ({round_off:.2f}) = Rs. {expected_grand:.2f} (diff: Rs. {abs(expected_grand - float(grand_total)):.2f})."
            )
            grand_total_valid = False

    # 6. Essential Invoice Metadata Checks
    if not invoice.get("invoice_number"):
        warnings.append("Invoice Number is missing or unreadable.")
    if not invoice.get("invoice_date"):
        warnings.append("Invoice Date is missing or unreadable.")

    # 7. Final Validation Status Classification
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
