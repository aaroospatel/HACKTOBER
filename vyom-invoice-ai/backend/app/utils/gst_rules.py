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
    "36": "Telangana", "37": "Andhra Pradesh (new)", "38": "Ladakh",
    "97": "Other Territory", "99": "Centre Jurisdiction"
}

# Standard Indian GST rates (%)
VALID_GST_RATES = {0, 0.1, 0.25, 1, 1.5, 3, 5, 6, 7.5, 12, 18, 28}

# GSTIN format regex (15-character alphanumeric)
GSTIN_PATTERN = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$'

# Column name mapping for Excel/CSV normalization
COLUMN_MAPPING = {
    "invoice no": "invoice_number", "invoice number": "invoice_number",
    "inv no": "invoice_number", "bill no": "invoice_number", "invoice_no": "invoice_number",
    "date": "invoice_date", "invoice date": "invoice_date", "invoice_date": "invoice_date",
    "bill date": "invoice_date",
    "gstin": "supplier_gstin", "seller gstin": "supplier_gstin",
    "vendor gstin": "supplier_gstin", "supplier gstin": "supplier_gstin",
    "buyer gstin": "buyer_gstin", "customer gstin": "buyer_gstin",
    "seller": "supplier_name", "vendor": "supplier_name",
    "supplier": "supplier_name", "from": "supplier_name", "supplier name": "supplier_name",
    "buyer": "buyer_name", "customer": "buyer_name", "to": "buyer_name", "buyer name": "buyer_name",
    "item": "description", "product": "description",
    "particulars": "description", "goods": "description", "item description": "description",
    "qty": "quantity", "quantity": "quantity",
    "rate": "unit_price", "price": "unit_price", "unit price": "unit_price",
    "hsn": "hsn_sac", "sac": "hsn_sac", "hsn/sac": "hsn_sac", "hsn code": "hsn_sac",
    "gst rate": "gst_rate", "tax rate": "gst_rate", "rate of tax": "gst_rate",
    "cgst": "cgst", "cgst amount": "cgst",
    "sgst": "sgst", "sgst amount": "sgst",
    "igst": "igst", "igst amount": "igst",
    "cess": "cess",
    "taxable value": "taxable_value", "taxable amount": "taxable_value", "taxable val": "taxable_value",
    "total": "total", "amount": "total", "grand total": "grand_total", "total amount": "grand_total"
}
