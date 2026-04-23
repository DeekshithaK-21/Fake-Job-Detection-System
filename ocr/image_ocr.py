import cv2
import os
import pytesseract

if os.name == "nt":  # Windows only
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_image(image_input, is_array=False):
    try:
        if is_array:
            img = image_input
        else:
            img = cv2.imread(image_input)

        if img is None:
            print("❌ Image not loaded")
            return ""

        # 🔥 Speed + clarity
        img = cv2.resize(img, (800, 800))

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, gray = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

        # 🔥 OCR
        text = pytesseract.image_to_string(gray)

        print("OCR TEXT:", text[:200])

        return text

    except Exception as e:
        print("OCR ERROR:", e)
        return ""