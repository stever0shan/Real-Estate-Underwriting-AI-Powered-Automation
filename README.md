
# 🧾 Automated Real Estate Underwriting Pipeline

This project takes messy Offering Memorandums (PDFs) from real estate deals and transforms them into clean, structured Excel underwriting models — powered by AI and smart table extraction.

---

## 🚀 What It Does

- 📄 Reads PDFs (even scanned image-based ones)
- 🔍 Extracts key fields like Monthly Rent, NOI, Cap Rate, Units
- 🤖 Uses GPT-3.5 fallback if keyword matching fails
- 📊 Pulls rent tables into a "Unit Mix" Excel tab
- 🧠 Logs what was guessed by AI vs confidently matched
- 📁 Writes to real New Construction / Value Add Excel templates

---

## 🧠 How It Works

### 1. `automate_underwriting.py` — Main Controller
Runs the full pipeline: OCR fallback, field extraction, table parsing, Excel writing.

### 2. `keyword_matcher.py` — Keyword + Regex Field Extractor
Extracts:
- `monthly_rent`
- `NOI`
- `cap_rate`
- `total_units`
- `purchase_price`
- `loan_amount`
- `developer_equity`

### 3. `ai_fallback.py` — GPT-3.5 Assistant
If fields are missing, GPT is prompted with:
> "What is the developer equity?"  
Returns structured answers.

### 4. `ocr_fallback.py` — Handles Scanned PDFs
If no text is found in the PDF, OCR kicks in using `pytesseract` + `pdf2image`.

### 5. `table_extractor.py` — Finds Tables with Camelot
Finds all tables in the PDF and filters for rent/unit tables.

### 6. `unit_mix_writer.py` — Adds “Unit Mix” Excel Tab
Cleans and writes valid rent tables to a second tab in Excel.

### 7. `excel_writer.py` — Fills Excel Template
Uses OpenPyXL to populate either:
- `New Construction Template.xlsx`
- `Value Add Template.xlsx`

---

## 📋 Sample Output

- Excel sheet with populated fields
- `"Unit Mix"` tab with rent breakdown
- Confidence report (AI fallback vs match)

---

## 📂 Project Structure

```
underwriting_automation/
├── automate_underwriting.py
├── keyword_matcher.py
├── ai_fallback.py
├── ocr_fallback.py
├── table_extractor.py
├── unit_mix_writer.py
├── excel_writer.py
├── New Construction Template.xlsx
├── Value Add Template.xlsx
├── output/
└── test_docs/
```

---

## 📈 System Diagram

<img width="940" height="443" alt="image" src="https://github.com/user-attachments/assets/faffb1aa-4bb0-4f40-8217-b8ea4e87472d" />


---

## ✅ Ready to Use

```
python automate_underwriting.py test_docs/lawton_om.pdf
```

---
📌 The sample OM is used for educational/demo purposes only. All copyrights and trademarks belong to their respective owners. No commercial use intended.
📌 These templates are shared for educational/demo purposes only. All cell mappings and formulas are representative and do not constitute financial advice.
Built for scale. Human-ready, AI-augmented.
