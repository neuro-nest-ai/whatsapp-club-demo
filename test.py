from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
import os
import ocrmypdf

def scannedPdfConverter(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')

class PDFEditor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def insert_text_at_coordinates(self, text_dicts):
        writer = PdfWriter()
        with open(self.pdf_path, "rb") as file:
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                c = canvas.Canvas("temp.pdf", pagesize=(page.mediabox[2], page.mediabox[3]))
                for text_dict in text_dicts:
                    if i == text_dict["page_number"]:
                        font_name = text_dict.get("font_name", "Helvetica")
                        font_size = text_dict.get("font_size", 16)
                        c.setFont(font_name, font_size)
                        text = text_dict["text"]
                        x = text_dict["x"]
                        y = text_dict["y"]
                        c.drawString(x, y, text)
                c.save()
                img_pdf = PdfReader("temp.pdf")
                img_page = img_pdf.pages[0]
                page.merge_page(img_page)
                writer.add_page(page)
        with open(self.pdf_path, "wb") as output_file:
            writer.write(output_file)
        os.remove("temp.pdf")

text_dicts = [
    {"x": 270, "y": 700, "text": "New Text", "page_number": 0, "font_name": "Times-Roman", "font_size": 20},
    {"x": 230, "y": 700, "text": "Rtn", "page_number": 0, "font_name": "Times-Roman", "font_size": 20}
    
]

file_path = "Data\Members profile sample.pdf"
save_path = "output.pdf"
scannedPdfConverter(file_path, save_path)
pdf_editor = PDFEditor(save_path)
pdf_editor.insert_text_at_coordinates(text_dicts)
