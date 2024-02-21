from PIL import Image
import requests
from io import BytesIO
 
import ocrmypdf

def scannedPdfConverter_invoice(file_path,save_path):
    ocrmypdf.ocr(file_path, save_path, skip_text=True)
    print('File converted successfully!')
    return save_path
    

def is_image(url, headers=None):
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            image_data = response.content
            image = Image.open(BytesIO(image_data))
            image.verify()  # This checks if the image is valid
            return True
        else:
            print("Failed to fetch image, status code:", response.status_code)
            return False
    except Exception as e:
        print("Exception while checking image:", e)
        return False




   







