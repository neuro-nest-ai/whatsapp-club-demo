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

    def get_page_size(self, page_number):
        with open(self.pdf_path, "rb") as file:
            reader = PdfReader(file)
            page = reader.pages[page_number]
            mediabox = page.mediabox

            page_width = float(mediabox[2])
            page_height = float(mediabox[3])

            return page_width, page_height
        
    def convert_text_coordinates(self, page_height, x, y):
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
                            page_height, element["x0"], element["bottom"])
                        x1, y1 = self.convert_text_coordinates(
                            page_height, element["x1"], element["top"]
                        )
                        width = x1 - x0
                        height = y1 - y0

                        return x0 + width, y0, width, height, page_number - 1
                    
                    
    def insert_image(self, x, y, page_number, image_width, image_height, search_text, font_name="Helvetica", font_size=16):
        writer = PdfWriter()
        c = canvas.Canvas("temp.pdf", pagesize=self.get_page_size(page_number))
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
            os.remove("temp.pdf")
            
            
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

    def insert_image_new(self, image_path):
        x = 100
        y = 425
        page_number = 0
        image_width = 399
        image_height = 227
        writer = PdfWriter()
        with open(self.pdf_path, "rb") as file:
            reader = PdfReader(file)
            for i, page in enumerate(reader.pages):
                if i == page_number:
                    c = canvas.Canvas("temp.pdf", pagesize=(page.mediabox[2], page.mediabox[3]))
                    c.drawImage(image_path, x, y, width=image_width, height=image_height)
                    c.save()
                    img_pdf = PdfReader("temp.pdf")
                    img_page = img_pdf.pages[0]
                    page.merge_page(img_page)
                    writer.add_page(page)
        with open(self.pdf_path, "wb") as output_file:
            writer.write(output_file)
        os.remove("temp.pdf")

    def edit_pdf(self, search_texts, text_positions=None):
        if text_positions is None:
            text_positions = {
                "Hours": {"x": 15-5, "y":0, "font_size": 11, "font_name": "Helvetica"},
                "Cost": {"x": 72, "y": 1, "font_size": 11, "font_name": "Helvetica"},
                "Volunteer": {"x": 40, "y": 1, "font_size": 11, "font_name": "Helvetica"},
                "beneficieries": {"x": 10, "y":0, "font_size": 11, "font_name": "Helvetica"},
                "Value": {"x": 82, "y": 1, "font_size": 11, "font_name": "Helvetica"},
                 "Rupees": {"x":10, "y": 0, "font_size": 11, "font_name": "Helvetica"},
                "Members": {"x": 15, "y": 1, "font_size": 11, "font_name": "Helvetica"},
                "Guest": {"x": 50, "y": 0, "font_size": 11, "font_name": "Helvetica"},
                "Rotaractors": {"x": 10, "y": 0, "font_size": 11, "font_name": "Helvetica"},
                "Public": {"x": 10, "y": -2, "font_size": 11, "font_name": "Helvetica"},
                "Family": {"x": 40, "y": -2, "font_size": 11, "font_name": "Helvetica"},
            }
           
        for key in text_positions:
            x1 = text_positions[key]["x"]
            y1 = text_positions[key]["y"]
            font_size = text_positions[key]["font_size"]
            font_name = text_positions[key]["font_name"]
            x, y, width, height, page_number = self.draw_bounding_box(key)
            if width < 20:
                image_width = width
            else:
                image_width = 20  # Reset image_width to default value if width is not less than 20
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

class Report_generation_config:
    def __init__(self):
        pass
    
    def main(self, file_path, search_texts, image_path, text_dicts):
        pdf_editor = PDFEditor(file_path)
        pdf_editor.insert_image_new(image_path)
        pdf_editor.insert_text_at_coordinates(text_dicts)
        pdf_editor.edit_pdf(search_texts)
        return file_path

# search_texts = {
    # "Hours": "007",
    # "Cost": "8861832522",
    # "Volunteer": "004",
    # "beneficieries": "45,000",
    # "Value": "Yes",
    #  "Rupees": "Bangalore",
    # "Members": "xxxx345",
    # "Guest": "Engineer",
    # "Rotaractors": "60",
    # "Public": "WORLD",
    # "Family": "hello"
# }
# 
# text_dicts = [
    # {"x": 50, "y": 800, "text": "New Text", "page_number": 0},
    # {"x": 100, "y": 700, "text": "Heading", "page_number": 0},
    # {"x": 100, "y": 400, "text": "content", "page_number": 0},
    # {"x": 400, "y": 800, "text": "club_details", "page_number": 0}
# ]
# 
# file_path = r"Data\Duplicate.pdf"
# save_path = r"output.pdf"
# scannedPdfConverter(file_path, save_path)
# 
# file_path = r"output.pdf"
# image_path = r"roatryevents\roatryevents\1Members family Function.jpg"
# 
# report = Report_generation_config()
# pdf = report.main(file_path, search_texts, image_path, text_dicts)
