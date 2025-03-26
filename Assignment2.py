import pdfplumber
import pandas as pd

pdf_path = "test3.pdf"

data = []

with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        ext_txt = page.extract_text()
        
        if ext_txt:
            lines = ext_txt.split("\n")
            for line in lines:
                
                columns = list(filter(None, line.split("  ")))
                data.append(columns)

df = pd.DataFrame(data)


df.to_excel("output.xlsx", index=False, header=False)

print("✅ Data extracted and saved to output.xlsx")
