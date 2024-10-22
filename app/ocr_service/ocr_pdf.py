import pytesseract
from PIL import Image
from pdf2image import convert_from_path


def scan_invoice(filepath):
    # judge files are pdf or image
    text_lines = []
    if filepath.endswith(".pdf"):
        images = convert_from_path(filepath)
        for image in images:
            text_lines.extend(scan_image(image))
    else:
        image = Image.open(filepath)
        text_lines = scan_image(image)
    return text_lines


def scan_image(image):
    # use pytesseract to do OCR on the loaded image
    recognized_text = pytesseract.image_to_string(image, lang="eng+deu")

    # split the recognized text into lines
    # and strip whitespace from each line

    lines = [line.strip() for line in recognized_text.split("\n") if line.strip()]
    return lines
