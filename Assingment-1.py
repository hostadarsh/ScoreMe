import fitz
import pandas as pd
import re

pdf_file = "test3.pdf"
output_excel = "extracted_bank_statement.xlsx"


def extract_text_from_pdf(pdf_path):
    text_data = []
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text_data.append(page.get_text("text"))
    return "\n".join(text_data)

def parse_transactions(text):
    transactions = []
    
    transaction_pattern = re.compile(
        r"(\d{2}-[A-Za-z]{3}-\d{4})\s+([\w\s.-]+)\s+([,\d]+.\d{2})\s+([,\d]+.\d{2}[A-Za-z]+)"
    )

    matches = transaction_pattern.findall(text)
    
    for match in matches:
        date, description, amount, balance = match
        transactions.append({
            "Date": date,
            "Description": description.strip(),
            "Transaction Amount": amount.replace(",", ""),
            "Balance": balance.replace(",", ""),
        })

    return transactions

text_data = extract_text_from_pdf(pdf_file)


transactions = parse_transactions(text_data)


df = pd.DataFrame(transactions)


df.to_excel(output_excel, index=False)

print(f"Bank statement extracted and saved to {output_excel}")
    