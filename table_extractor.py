import camelot

def extract_tables_from_pdf(pdf_path, output_csv_path="rent_tables.csv"):
    try:
        print(f" Extracting tables from: {pdf_path}")
        tables = camelot.read_pdf(pdf_path, pages='all')
        if tables:
            tables.export(output_csv_path, f="csv")
            print(f" Exported {len(tables)} table(s) to {output_csv_path}")
            return tables
        else:
            print(" No tables found.")
            return []
    except Exception as e:
        print(f" Camelot error: {e}")
        return []
