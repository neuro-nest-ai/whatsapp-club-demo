from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from reportlab.pdfgen import canvas
import os
import ocrmypdf

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
    
    def split_text(self, text, max_length):
        """
        Split text into lines no longer than max_length.
        """
        words = text.split()
        lines = []
        current_line = ''
        for word in words:
            if len(current_line) + len(word) + 1 <= max_length:
                current_line += ' ' + word if current_line else word
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)
        return lines

    def edit_pdf(self, search_texts, text_positions=None):
        image_width = 20
        if text_positions is None:
            text_positions = {
                "RI": {"x": 30, "y": 3, "font_size": 12, "font_name": "Helvetica"},
                "Ph.No:": {"x":5, "y": 5, "font_size": 12, "font_name": "Helvetica"},
                "Mail": {"x": 30, "y": 3+1, "font_size": 12, "font_name": "Helvetica"},
                "Profession": {"x": 10, "y": 4, "font_size": 12, "font_name": "Helvetica"},
                "Original": {"x":127, "y": 5, "font_size": 12, "font_name": "Helvetica"},
                "Current": {"x":129, "y": 3, "font_size": 12, "font_name": "Helvetica"},
                "Years": {"x":145, "y": 3, "font_size": 14, "font_name": "Helvetica"},
                "ROLES":{"x":10, "y": 5, "font_size": 14, "font_name": "Helvetica"},
                "MEMBER":{"x":-80, "y":-40, "font_size": 14, "font_name": "Helvetica"}
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

            # Split text into multiple lines if it exceeds 60 characters
            if len(search_texts[key]) > 60:
                lines = self.split_text(search_texts[key], 60)
                line_height = font_size * 1.2  # Assuming line spacing
                for i, line in enumerate(lines):
                    self.insert_image(
                        x + x1,
                        y + y1 - i * line_height,
                        page_number,
                        image_width,
                        height,
                        line,
                        font_name,
                        font_size,
                    )
            else:
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

class Profile_generation_config:
    def __init__(self):
        pass
    
    def main(self,file_path,search_texts,postion_dicts):
        pdf_editor=PDFEditor(file_path)
        pdf_editor.insert_text_at_coordinates(postion_dicts)
        pdf_editor.edit_pdf(search_texts)
        return file_path
        
# search_texts = {
#     "RI":"007",
#     "Ph.No:": "8861832522",
#     "Mail": "004",
#     "Profession": "45,000",
#     "Original": "Yes",
#     "Current": "Banglore",
#     "Years": "xxxx345",
#     "ROLES":"Club President (2023-2024),Club Secretary (2018-2019),Member (2017-2023) at Rsesdent Towers",
#     "MEMBER":"Club President (2023-2024),Club Secretary (2018-2019),Member (2017-2023) at Rsesdent Towers hello world my name"
# }       
        
# text_dicts = [
#     {"x": 270, "y": 700, "text": "New Text", "page_number": 0, "font_name": "Times-Roman", "font_size": 20},
#     {"x": 230, "y": 700, "text": "Rtn", "page_number": 0, "font_name": "Times-Roman", "font_size": 20}
# ]

# save_path="output.pdf"
# file_path="Data\Members profile sample.pdf"
# ocrmypdf.ocr(file_path, save_path, skip_text=True)

# pdf_editor = Profile_generation_config()
# file_path=pdf_editor.main(save_path,search_texts,text_dicts)
# print(file_path)
