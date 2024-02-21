import pandas as pd
from Pdf_generation.trust_certificate import bill_generation_config
from Pdf_generation.invoice import Invoice_generation_config
from Treasurer.Reply import ReplyConfig
from Pdf_generation.trust_certificate import scannedPdfConverter


file_path=r"Data\80G .pdf"
save_path=r"output.pdf"

scannedPdfConverter(file_path=file_path,save_path=save_path)





class PdfPipeline:
    def __init__(self):
        pass
        
    def get_data(self, text):
        search_text = {}
        data_config = ReplyConfig()
        upi_transaction_id, trust = data_config.main(text)
        print(upi_transaction_id, trust)
        
        if trust == "trust":
            upi_list = []
            path = r'Data\Trust_details.csv' 
            try:
                df = pd.read_csv(path)
                for index, row in df.iterrows():
                    if row['UPI_transaction_id'] == int(upi_transaction_id):
                        upi_list.extend([row['Date'], row['Name'], row['Amount'], 
                                         row['Project'], row['Bank_number'], 
                                         row['UPI_transaction_id'], row['Receipt_No']])
                DATE, Name, Amount, Subscription, Bank_number, UPI_transaction_id, Invoice_No = upi_list
                search_text["RECEIPT"] = Name
                search_text["Date"] = DATE
                search_text["Receipt"] = str(Invoice_No)
                search_text["SUBTOTAL"] = str(Amount)
                search_text["Amount"] = str(Amount)
                search_text["DESCRIPTION"] = Subscription
                search_text["UPI"] = str(UPI_transaction_id)
                return search_text, "trust"
            except FileNotFoundError:
                print("Error: CSV file not found")
                return None
        else:
            upi_list = []
            path = r'Data\club.csv'
            try:
                df = pd.read_csv(path)
                for index, row in df.iterrows():
                    if row['UPI_transaction_id'] == int(upi_transaction_id):
                        upi_list.extend([row['DATE'], row['Name'], row['Amount'], 
                                         row['Subscription'], row['Bank_number'], 
                                         row['UPI_transaction_id'], row['Invoice_No']])
                DATE, Name, Amount, Subscription, Bank_number, UPI_transaction_id, Invoice_No = upi_list
                search_text["RECEIPT"] = Name
                search_text["Date"] = DATE
                search_text["Invoice"] = str(Invoice_No)
                search_text["SUBTOTAL"] = str(Amount)
                search_text["Amount"] = str(Amount)
                search_text["DESCRIPTION"] = Subscription
                search_text["UPI"] = str(UPI_transaction_id)
                return search_text, "Invoice"
            except FileNotFoundError:
                print("Error: CSV file not found")
                return None

class PdfPipelineConfig:
    def __init__(self):
        pass
    
    def main(self, text, save_path):
        pdf = PdfPipeline()
        search_text, type = pdf.get_data(text)
        if type == "trust":
            file_path=r"Data\80G .pdf"
            scannedPdfConverter(file_path,save_path)

            trust_pdf = bill_generation_config()
            pdf_trust = trust_pdf.main(save_path, search_text)
            return pdf_trust
        else:
            file_path=r"Data\invoice.pdf"
            scannedPdfConverter(file_path,save_path)
            invoice = Invoice_generation_config()
            
            invoice_pdf = invoice.main(save_path, search_text)
            return invoice_pdf

text = "yes 440518352387 trust"
save_path = r"output.pdf"
pdf = PdfPipelineConfig()
new_pdf = pdf.main(text, save_path)
print("successful")
