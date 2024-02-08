import cv2
from PIL import Image


#checking the Image 
def is_image(image_path):
      try:
        img = cv2.imread(image_path)
        if img:
            return True
      except Exception as e:
            return False