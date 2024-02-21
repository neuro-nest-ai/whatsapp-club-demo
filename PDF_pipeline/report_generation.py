from PyPDF2 import PdfReader, PdfWriter
import pdfplumber
from reportlab.pdfgen import canvas
import os


def get_page_size(pdf_path, page_number):
    with open(pdf_path, "rb") as file:
        reader = PdfReader(file)
        page = reader.pages[page_number]
        media_box = page.mediabox

        page_width = float(media_box[2])
        page_height = float(media_box[3])

        return page_width, page_height


def convert_text_coordinates(page_height, x, y):
    # Convert y-coordinate to match the coordinate system used by reportlab
    return x, page_height - y


def draw_bounding_box(pdf_path, search_text, output_path):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_number = page.page_number
            page_height = page.height
            text_elements = page.extract_words()
            for element in text_elements:
                if element["text"] == search_text:
                    x0, y0 = convert_text_coordinates(
                        page_height, element["x0"], element["bottom"]
                    )
                    x1, y1 = convert_text_coordinates(
                        page_height, element["x1"], element["top"]
                    )
                    width = x1 - x0
                    height = y1 - y0

                    return x0 + width, y0, width, height, page_number - 1


def insert_image(
    pdf_path,
    x,
    y,
    page_number,
    image_width,
    image_height,
    page_width,
    page_height,
    search_text,
    font_name="Helvetica",
    font_size=16,
):
    reader = PdfReader(pdf_path)
    writer = PdfWriter()

    c = canvas.Canvas("temp.pdf", pagesize=(page_width, page_height))
    # Set font size and font name
    c.setFont(font_name, font_size)
    c.drawString(x, y, search_text)
    c.save()

    img_pdf = PdfReader("temp.pdf")
    img_page = img_pdf.pages[0]

    for i, page in enumerate(reader.pages):
        if i == page_number:
            page.merge_page(img_page)
        writer.add_page(page)

    with open(pdf_path, "wb") as output_file:
        writer.write(pdf_path)

    # Remove the temporary image PDF file
    os.remove("temp.pdf")


pdf_path = "output.pdf"
search_text = {
    "RECEIPT": "Kelavan Ganesan",
    "Date": "06/03/2022",
    "Receipt": "143",
    "SUBTOTAL": "45,000",
    "Amount": "45,000",
    "DESCRIPTION": "Club Rotatary Trust",
    "UPI":"xxxx345"
}
image_width = 20
# image_height = 15

a = {
    "TRUST": {
        "RECEIPT": {"x": -55, "y": -30, "font_size": 14, "font_name": "Helvetica"},
        "Date": {"x": 45, "y": 0, "font_size": 10, "font_name": "Helvetica"},
        "Receipt": {"x": 30, "y": 0, "font_size": 10, "font_name": "Helvetica"},
        "UPI": {"x":95, "y":4, "font_size": 12, "font_name": "Helvetica"},
        "DESCRIPTION": {
            "x": -80,
            "y": -45,
            "font_size": 12,
            "font_name": "Helvetica",
        },
        "SUBTOTAL": {"x": -40, "y":-45, "font_size": 12, "font_name": "Helvetica"},
        "Amount": {"x": 40, "y": 5, "font_size": 14, "font_name": "Helvetica"},
    }
}

for key in a["TRUST"]:
    x1 = a["TRUST"][key]["x"]
    y1 = a["TRUST"][key]["y"]
    font_size = a["TRUST"][key]["font_size"]
    font_name = a["TRUST"][key]["font_name"]
    x, y, width, height, page_number = draw_bounding_box(pdf_path, key, pdf_path)
    if width < 20:
        image_width = width
    page_width, page_height = get_page_size(pdf_path, page_number)
    insert_image(
        pdf_path,
        x + x1,
        y + y1,
        page_number,
        image_width,
        height,
        page_width,
        page_height,
        search_text[key],
        font_name,
        font_size,) 