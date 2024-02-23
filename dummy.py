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
                        max_width = page.mediabox[2] - x  # Maximum width before wrapping
                        lines = self.wrap_text(text, c, max_width)
                        for line in lines:
                            c.drawString(x, y, line.strip())
                            y -= font_size * 1.2  # Adjust line spacing as needed
                c.save()
                img_pdf = PdfReader("temp.pdf")
                img_page = img_pdf.pages[0]
                page.merge_page(img_page)
                writer.add_page(page)
        with open(self.pdf_path, "wb") as output_file:
            writer.write(output_file)
        os.remove("temp.pdf")

    def wrap_text(self, text, canvas_obj, max_width):
        lines = []
        line = ""
        for word in text.split():
            word_width = canvas_obj.stringWidth(word)
            if canvas_obj.stringWidth(line + word) <= max_width:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        return lines

text_dicts = [
    {"x": 50, "y": 800, "text": "New Text", "page_number": 0, "font_name": "Times-Roman", "font_size": 20},
    {"x": 100, "y": 700, "text": "we live india i am indian we are patrotic", "page_number": 0, "font_name": "Helvetica-Bold", "font_size": 18},
    {"x": 60, "y": 400, "text": "We had our AG club assembly meet in heritage in. Discussions about our September month and future project of October month were discussed. Also AG discussed with the plans for DG visit happening on 27 Oct", "page_number": 0, "font_name": "Courier", "font_size": 12},
    {"x": 400, "y": 800, "text": "club_details", "page_number": 0, "font_name": "Times-Italic", "font_size": 16},
]

file_path = "Data\Duplicate.pdf"
save_path = "output.pdf"
scannedPdfConverter(file_path, save_path)
pdf_editor = PDFEditor(save_path)
pdf_editor.insert_text_at_coordinates(text_dicts)