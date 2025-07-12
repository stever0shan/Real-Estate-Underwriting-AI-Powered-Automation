import sys
import os
import pdfplumber
from keyword_matcher import keyword_extract
from ai_fallback import ai_fill_fields
from excel_writer import fill_excel
from table_extractor import extract_tables_from_pdf
from ocr_fallback import extract_text_with_ocr  
from unit_mix_writer import add_unit_mix_tab


def load_text_from_pdf(path):
    with pdfplumber.open(path) as pdf:
        text = "\n".join(page.extract_text() or '' for page in pdf.pages)

    if text.strip():  #  Return if text was successfully extracted
        return text

    # OCR fallback if no text is found
    return extract_text_with_ocr(path)

def detect_deal_type(text):
    if "ground up" in text.lower() or "construction loan" in text.lower():
        return "new_construction"
    elif "renovation" in text.lower() or "value add" in text.lower():
        return "value_add"
    return "value_add"  # fallback

def main(pdf_path):
    #  Step 1: Extract raw text from the PDF
    raw_text = load_text_from_pdf(pdf_path)

    #  Step 2: Extract tables using Camelot and save to CSV
    tables = extract_tables_from_pdf(pdf_path, output_csv_path="output/rent_tables.csv")


    #  Step 3: Extract fields via keyword matcher
    extracted = keyword_extract(raw_text)

    #  Step 4: Fallback to GPT for missing fields
    missing = [k for k, v in extracted.items() if v == "NEEDS_REVIEW"]
    if missing:
        ai_filled = ai_fill_fields(raw_text, missing)
        extracted.update(ai_filled)
    else:
        ai_filled = {}  # ensure it's always defined

    print(" Final extracted fields:")
    for k, v in extracted.items():
        print(f"  {k}: {v}")
        
    print("\n Confidence Report:")
    for k, v in extracted.items():
        source = "AI (fallback)" if k in ai_filled else "Keyword Match"
        print(f"  {k}: {source}")

    #  Step 5: Choose template
    deal_type = detect_deal_type(raw_text)
    if deal_type == "new_construction":
        template = "New Construction Template.xlsx"
    else:
        template = "Value Add Template.xlsx"

    #  Step 6: Fill and save Excel
    output_filename = os.path.join("output", os.path.basename(pdf_path).replace(".pdf", "_output.xlsx"))
    fill_excel(template, output_filename, extracted)
    add_unit_mix_tab(output_filename, tables)

    print(f"\n Excel saved as: {output_filename}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python automate_underwriting.py test_docs/yourfile.pdf")
    else:
        os.makedirs("output", exist_ok=True)
        main(sys.argv[1])
