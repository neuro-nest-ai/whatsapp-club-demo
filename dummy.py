from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
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
                for text_dict in text_dicts:
                    if i == text_dict["page_number"]:
                        c = canvas.Canvas("temp.pdf", pagesize=(page.mediabox[2], page.mediabox[3]))
                        font_name = text_dict.get("font_name", "Helvetica")
                        font_size = text_dict.get("font_size", 16)
                        c.setFont(font_name, font_size)
                        c.drawString(text_dict["x"], text_dict["y"], text_dict["text"])
                        c.save()
                        img_pdf = PdfReader("temp.pdf")
                        img_page = img_pdf.pages[0]
                        page.merge_page(img_page)
                writer.add_page(page)
        with open(self.pdf_path, "wb") as output_file:
            writer.write(output_file)
        os.remove("temp.pdf")

text_dicts = [
    {"x": 50, "y": 800, "text": "New Text", "page_number": 0, "font_name": "Times-Roman", "font_size": 20},
    {"x": 100, "y": 700, "text": "Heading", "page_number": 0, "font_name": "Helvetica-Bold", "font_size": 18},
    {"x": 100, "y": 400, "text": "content i am not ", "page_number": 0, "font_name": "Courier", "font_size": 12},
    {"x": 400, "y": 800, "text": "club_details", "page_number": 0, "font_name": "Times-Italic", "font_size": 16},
]

file_path = "output.pdf"
save_path= "Data\Duplicate.pdf"
scannedPdfConverter(save_path,file_path)
pdf_editor = PDFEditor(file_path)
pdf_editor.insert_text_at_coordinates(text_dicts)
