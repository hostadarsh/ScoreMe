import pandas as pd
import re

inp_fil = "output.xlsx"
out_file = "cleaned_transactions.xlsx"

df = pd.read_excel(inp_fil, header=None)

data_patt = r"\d{2}-[A-Za-z]{3}-\d{2,4}"  
amt_patt = r"[\d,]+\.\d{2}" 
bal_patt = r"\d{1,3}(?:,\d{3})*\.\d{2}Dr?"  

transactions = []

for row in df[0]:
    match = re.findall(data_patt, str(row))  
    if match:
        date = match[0]  
        details = row.split(date)[-1].strip() 
        
       
        transaction_type = "Unknown"
        if "Cash" in details:
            transaction_type = "Cash Deposit"
        elif "IMPS" in details or "UPI" in details:
            transaction_type = "UPI Transfer"
        elif "NEFT" in details:
            transaction_type = "NEFT Transfer"
        elif "Interest" in details or "Int.Coll" in details:
            transaction_type = "Interest Charged"
        elif "Lien Reversal" in details:
            transaction_type = "Lien Reversal"
        
        
        amounts = re.findall(amt_patt, details)
        if len(amounts) == 3:
            debit, credit, balance = amounts
        elif len(amounts) == 2:
            debit, credit, balance = amounts[0], "", amounts[1]  
        elif len(amounts) == 1:
            debit, credit, balance = "", "", amounts[0]  
        else:
            debit, credit, balance = "", "", ""
        

        transactions.append([date, transaction_type, details, debit, credit, balance])


columns = ["Date", "Transaction Type", "Details", "Debit (₹)", "Credit (₹)", "Balance (₹)"]
df_cleaned = pd.DataFrame(transactions, columns=columns)


df_cleaned.to_excel(out_file, index=False)

print(f"✅ Structured data saved to {out_file}")
