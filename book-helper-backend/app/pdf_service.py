import fitz  # PyMuPDF

def extract_text_by_page(pdf_path: str) -> list[str]:
    doc = fitz.open(pdf_path)
    pages_text = []
    for i in range(len(doc)):
        page = doc.load_page(i)
        pages_text.append(page.get_text())
    return pages_text
