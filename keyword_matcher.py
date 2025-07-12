import re

RENT_KEYWORDS = [
    "monthly rent", "avg rent", "average rent", "effective rent",
    "rent per unit", "in-place rent", "contract rent",
    "rental income", "gross potential rent", "base rent",
    "annual rent", "total rent", "scheduled rent", "pro forma rent"
]

NOI_KEYWORDS = [
    "net operating income", "noi", "current noi",
    "stabilized noi", "pro forma noi", "estimated noi",
    "projected net income", "income after expenses"
]

CAP_RATE_KEYWORDS = [
    "cap rate", "capitalization rate", "stabilized cap rate",
    "market cap rate", "exit cap rate", "going-in cap"
]

UNITS_KEYWORDS = [
    "total units", "number of units", "unit count",
    "units", "apartment units", "residential units", "unit mix",
    "442-unit", "442 units", "unit configuration"
]

PURCHASE_PRICE_KEYWORDS = [
    "purchase price", "asking price", "sale price", "offering price", "price"
]

LOAN_AMOUNT_KEYWORDS = [
    "loan amount", "loan size", "principal", "construction loan", "loan proceeds"
]

DEVELOPER_EQUITY_KEYWORDS = [
    "developer equity", "owner equity", "equity contribution", "sponsor equity", "developer cash"
]

def extract_value(text, keywords, field=None):
    lines = text.lower().splitlines()
    for line in lines:
        for kw in keywords:
            if kw in line:
                # Special case: convert annual rent to monthly rent
                if field == "monthly_rent" and "annual rent" in line:
                    match = re.search(r"\$?[\d,.]+", line)
                    if match:
                        annual = float(match.group().replace("$", "").replace(",", ""))
                        return f"${round(annual / 12):,}"

                # Regular match
                match = re.search(r"\$?[\d,.]+%?", line)
                if match:
                    val = match.group().strip()

                    # Avoid false match like "737 N LaSalle"
                    if field == "NOI":
                        if "la salle" in line or "address" in line or "location" in line:
                            continue
                        if match:
                            num_only = re.sub(r"[^\d]", "", match.group())
                            if len(num_only) <= 4:  # e.g., 737
                                continue
                    return val
    return None

def keyword_extract(text):
    data = {}
    data["monthly_rent"] = extract_value(text, RENT_KEYWORDS, field="monthly_rent") or "NEEDS_REVIEW"
    data["NOI"] = extract_value(text, NOI_KEYWORDS, field="NOI") or "NEEDS_REVIEW"
    data["cap_rate"] = extract_value(text, CAP_RATE_KEYWORDS, field="cap_rate") or "NEEDS_REVIEW"
    data["total_units"] = extract_value(text, UNITS_KEYWORDS, field="total_units") or "NEEDS_REVIEW"
    data["purchase_price"] = extract_value(text, PURCHASE_PRICE_KEYWORDS, field="purchase_price") or "NEEDS_REVIEW"
    data["loan_amount"] = extract_value(text, LOAN_AMOUNT_KEYWORDS, field="loan_amount") or "NEEDS_REVIEW"
    data["developer_equity"] = extract_value(text, DEVELOPER_EQUITY_KEYWORDS, field="developer_equity") or "NEEDS_REVIEW"
    return data
