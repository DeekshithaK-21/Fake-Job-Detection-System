# app/input_handler.py

from ocr.image_ocr import extract_text_from_image
from ocr.pdf_ocr import extract_text_from_pdf

def get_text(input_data, input_type="text"):

    if input_type == "text":
        return input_data

    elif input_type == "image":
        return extract_text_from_image(input_data)

    elif input_type == "image_array":
        return extract_text_from_image(input_data, is_array=True)

    elif input_type == "pdf":
        return extract_text_from_pdf(input_data)

    else:
        raise ValueError("Invalid input type")
