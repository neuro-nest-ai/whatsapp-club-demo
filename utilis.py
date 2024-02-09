def is_image(file_path):
    # List of common image file extensions
    image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']

    # Check if the file path ends with any of the image extensions
    if any(file_path.lower().endswith(ext) for ext in image_extensions):
        return True
    else:
        return False

# Example usage:
file_path = 'example_image.jpg'
if is_image(file_path):
    print("The file is an image.")
else:
    print("The file is not an image.")


































