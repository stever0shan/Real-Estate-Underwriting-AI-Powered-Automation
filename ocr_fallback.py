# ocr_fallback.py
from pdf2image import convert_from_path
from pytesseract import image_to_string

def extract_text_with_ocr(pdf_path):
    try:
        print(" Running OCR fallback...")
        images = convert_from_path(pdf_path)
        full_text = "\n".join([image_to_string(img) for img in images])
        return full_text
    except Exception as e:
        print(f" OCR failed: {e}")
        return ""
