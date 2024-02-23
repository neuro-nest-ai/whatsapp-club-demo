from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from reportlab.pdfgen import canvas
import os


import ocrmypdf
def scannedPdfConverter(file_path, save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')
    




print("you are")

class PDFEditor:
    def __init__(self, pdf_path):
        self.pdf_path = pdf_path

    def get_page_size(self, page_number):
        with open(self.pdf_path, "rb") as file:
            reader = PdfReader(file)
            page = reader.pages[page_number]
            media_box = page.mediabox

            page_width = float(media_box[2])
            page_height = float(media_box[3])

            return page_width, page_height

    def convert_text_coordinates(self, page_height, x, y):
        # Convert y-coordinate to match the coordinate system used by reportlab
        return x, page_height - y

    def draw_bounding_box(self, search_text):
        with pdfplumber.open(self.pdf_path) as pdf:
            for page in pdf.pages:
                page_number = page.page_number
                page_height = page.height
                text_elements = page.extract_words()
                for element in text_elements:
                    if element["text"] == search_text:
                        x0, y0 = self.convert_text_coordinates(
                            page_height, element["x0"], element["bottom"]
                        )
                        x1, y1 = self.convert_text_coordinates(
                            page_height, element["x1"], element["top"]
                        )
                        width = x1 - x0
                        height = y1 - y0

                        return x0 + width, y0, width, height, page_number - 1

    def insert_image(self, x, y, page_number, image_width, image_height, search_text, font_name="Helvetica", font_size=16):
        writer = PdfWriter()

        c = canvas.Canvas("temp.pdf", pagesize=self.get_page_size(page_number))
        # Set font size and font name
        c.setFont(font_name, font_size)
        c.drawString(x, y, search_text)
        c.save()

        img_pdf = PdfReader("temp.pdf")
        img_page = img_pdf.pages[0]

        with open(self.pdf_path, "rb") as file:
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                if i == page_number:
                    page.merge_page(img_page)
                writer.add_page(page)

        with open(self.pdf_path, "wb") as output_file:
            writer.write(output_file)

        # Remove the temporary image PDF file
        os.remove("temp.pdf")

    def edit_pdf(self, search_texts, text_positions=None):
        image_width = 20
        if text_positions is None:
            text_positions = {
                "RECEIPT": {"x": -55, "y": -20, "font_size": 14, "font_name": "Helvetica"},
                "Date": {"x": 45, "y": 3, "font_size": 10, "font_name": "Helvetica"},
                "Receipt": {"x": 30, "y": 3, "font_size": 10, "font_name": "Helvetica"},
                "UPI": {"x": 95, "y": 4, "font_size": 12, "font_name": "Helvetica"},
                "DESCRIPTION": {"x": -80, "y": -45, "font_size": 12, "font_name": "Helvetica"},
                "SUBTOTAL": {"x": -40, "y": -45, "font_size": 12, "font_name": "Helvetica"},
                "Amount": {"x": 40, "y": 5, "font_size": 14, "font_name": "Helvetica"},
            }

        for key in text_positions:
            x1 = text_positions[key]["x"]
            y1 = text_positions[key]["y"]
            font_size = text_positions[key]["font_size"]
            font_name = text_positions[key]["font_name"]
            x, y, width, height, page_number = self.draw_bounding_box(key)
            if width < 20:
                image_width = width
            page_width, page_height = self.get_page_size(page_number)
            self.insert_image(
                x + x1,
                y + y1,
                page_number,
                image_width,
                height,
                search_texts[key],
                font_name,
                font_size,
            )

# Usage:

class bill_generation_config:
    def __init__(self):
        pass
    
    def main(self,file_path,search_text):
        pdf_editor=PDFEditor(file_path)
        pdf_editor.edit_pdf(search_text)
        return file_path
        






        
        

#
#
#
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 