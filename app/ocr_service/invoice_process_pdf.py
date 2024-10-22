import re
from typing import List, Dict


def extract_invoice_data(recognized_text: List[str]) -> Dict[str, any]:
    # initialize dictionary to hold extracted invoice data
    invoice_data = {
        "markt_name": "",
        "store_address": "",
        "telephone": None,
        "uid_number": None,
        "items": [],
        "total": None,
        "date": None,
        "time": None,
        "payment_method": None,
        "receipt_nr": None,  # Bon-Nr.
        "document_nr": None,  # Beleg-Nr.
        "trace_nr": None,  # Seriennnummer Kasse
        "brand": "REWE",  # Default to REWE
        "markt_id": "",
        "register_number": "",
        "cashier_number": "",
        "discount_used_payback": "",
    }

    # Compile regex patterns to extract data
    trace_nr_pattern = re.compile(r"Trace-Nr\.\s*(\d+)", re.IGNORECASE)
    receipt_nr_pattern = re.compile(r"Bon-Nr\.\s*:\s*(\d+)", re.IGNORECASE)
    document_nr_pattern = re.compile(r"Beleg-Nr\.\s*(\d+)", re.IGNORECASE)
    markt_pattern = re.compile(r"Markt\:\s*(\d+)", re.IGNORECASE)
    kasse_pattern = re.compile(r"Kasse\:\s*(\d+)", re.IGNORECASE)
    bediener_pattern = re.compile(r"Bed\.\s*:\s*(\d+)", re.IGNORECASE)
    item_pattern = re.compile(r"^(.*?)\s([\d,]+\.?\d*)\s([AB])$")
    quantity_price_pattern = re.compile(r"(\d+)\sStk\sx\s([\d,]+\.?\d*)")
    total_pattern = re.compile(r"^SUMME\sEUR\s([\d,]+\.?\d*)$", re.IGNORECASE)
    date_pattern = re.compile(r"(\d{2}\.\d{2}\.\d{4})", re.IGNORECASE)
    time_pattern = re.compile(r"\d{2}\.\d{2}\.\d{4}\s(\d{2}:\d{2})", re.IGNORECASE)
    telephone_pattern = re.compile(r"Tel\.\s(\d{4}\-\d{8})", re.IGNORECASE)
    uid_pattern = re.compile(r"UID\sNr\.\:\s(.*)", re.IGNORECASE)
    payment_pattern = re.compile(r"^Geg\.\s(\w+)\sEUR\s([\d,]+\.?\d*)$", re.IGNORECASE)
    discount_pattern_payback = re.compile(r"PAYBACK Karten-Nr\.\:\s(.*)", re.IGNORECASE)

    """
    Extract address lines,cuz address line have no obvious identification marks，
    so i could only def the line>3 is the position which address located,
    """
    if len(recognized_text) > 3:
        unclean_market_name = recognized_text[1]
        cleaning_market_name_first = unclean_market_name.find(" ")
        cleaning_market_name_last = [unclean_market_name.rindex(" ")][0]
        clean_market_name = unclean_market_name[
            cleaning_market_name_first:cleaning_market_name_last
        ].strip()
        invoice_data["markt_name"] = clean_market_name

        unclean_street_address = recognized_text[2]
        csaf = recognized_text[2].find(" ")
        csal = [recognized_text[2].rindex(" ")][0]
        clean_street_address = unclean_street_address[csaf:csal].strip()
        # clean_street_address = re.sub(r"[\* ]+", "", recognized_text[2]).strip()
        clean_postal_and_city = re.sub(r"[\*xk]+", "", recognized_text[3]).strip()
        postal_and_city_match = re.match(r"(\d{5})\s+(\w+)", clean_postal_and_city)
        if postal_and_city_match:
            formatted_postal_and_city = (
                f"{postal_and_city_match.group(1)} {postal_and_city_match.group(2)}"
            )
        else:
            formatted_postal_and_city = clean_postal_and_city
        invoice_data["store_address"] = (
            f"{clean_street_address}, {formatted_postal_and_city}"
        )

    # Extract information line by line
    current_item = None
    expect_price_line = False
    for line in recognized_text:
        if markt_match := markt_pattern.search(line):
            invoice_data["markt_id"] = markt_match.group(1)
        if kasse_match := kasse_pattern.search(line):
            invoice_data["register_number"] = kasse_match.group(1)
        if bediener_match := bediener_pattern.search(line):
            invoice_data["cashier_number"] = bediener_match.group(1)
        if trace_nr_match := trace_nr_pattern.search(line):
            invoice_data["trace_nr"] = trace_nr_match.group(1)
        if receipt_nr_match := receipt_nr_pattern.search(line):
            invoice_data["receipt_nr"] = receipt_nr_match.group(1)
        if document_nr_match := document_nr_pattern.search(line):
            invoice_data["document_nr"] = document_nr_match.group(1)
        if time_match := time_pattern.search(line):
            invoice_data["time"] = time_match.group(1)
        if uid_match := uid_pattern.search(line):
            invoice_data["uid_number"] = uid_match.group(1)
        if telephone_match := telephone_pattern.search(line):
            invoice_data["telephone"] = telephone_match.group(1)
        if date_match := date_pattern.search(line):
            invoice_data["date"] = date_match.group(1)
        if total_match := total_pattern.search(line):
            invoice_data["total"] = total_match.group(1)
        if item_match := item_pattern.search(line):
            if current_item:
                invoice_data["items"].append(current_item)
            current_item = {
                "description": item_match.group(1).strip(),
                "total_price": item_match.group(2),
                "quantity": 1,
                "unit_price": item_match.group(2),
            }
            expect_price_line = True
        elif expect_price_line and (
            quantity_price_match := quantity_price_pattern.search(line)
        ):
            if current_item:
                current_item["quantity"] = int(quantity_price_match.group(1))
                current_item["unit_price"] = quantity_price_match.group(2)
            expect_price_line = False
        if payment_match := payment_pattern.search(line):
            invoice_data["payment_method"] = payment_match.group(1)
        if discount_card_match := discount_pattern_payback.search(line):
            invoice_data["discount_used_payback"] = (
                "PAYBACK" + discount_card_match.group(1)
            )

    if current_item:
        invoice_data["items"].append(current_item)

    return invoice_data
