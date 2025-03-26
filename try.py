import fitz

pdf_file = "test3.pdf"
doc = fitz.open(pdf_file)

for page_num, page in enumerate(doc, start=1):
    text = page.get_text("text")
    print(f"\n--- Page {page_num} Text ---\n")
    print(text)
