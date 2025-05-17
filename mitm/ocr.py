import time
import cv2
import easyocr
from PIL import Image
import numpy as np
import sys
import os

SAVE_DIR = os.path.join(os.getcwd(), 'images')

def save_image_for_ocr(flow):
    os.makedirs(SAVE_DIR, exist_ok=True)
    timestamp = int(time.time())
    binary_data = flow.request.content
    ext = "bin"
    if b"\x89PNG" in binary_data:
        ext = "png"
    elif b"\xFF\xD8" in binary_data:
        ext = "jpg"
    elif b"image/webp" in binary_data:
        ext = "webp"
    filename = f"image_{timestamp}.{ext}"
    filepath = os.path.join(SAVE_DIR, filename)
    try:
        with open(filepath, "wb") as f:
            f.write(binary_data)
        print(f"[+] Saved image to {filepath}")
        return filepath
    except Exception as e:
        print(f"[!] Failed to save image: {e}")
        return None

# ========================== OCR ========================

def preprocess_image(image_path):
    """
    Preprocesses the input image to improve OCR results.
    Steps: grayscale, threshold, resize.
    """
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Could not open image: {image_path}")

    # Threshold to binary
    _, thresh = cv2.threshold(img, 150, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Resize to make text larger
    resized = cv2.resize(thresh, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)

    # Invert back
    final_img = 255 - resized
    return final_img

def run_easyocr_on_image(img_array):
    """
    Runs EasyOCR on a preprocessed image array.
    """
    reader = easyocr.Reader(['en'], gpu=False)  # Set gpu=True if you have GPU
    result = reader.readtext(img_array, detail=0)
    return "\n".join(result)


def save_temp_image(np_img):
    """
    Saves NumPy image array to a temporary PNG file for OCR use.
    """
    temp_filename = "temp_processed.png"
    cv2.imwrite(temp_filename, np_img)
    return temp_filename

def main(image_path):
    print(f"🔍 Processing: {image_path}")
    preprocessed_img = preprocess_image(image_path)

    # EasyOCR expects a file or image array
    extracted_code = run_easyocr_on_image(preprocessed_img)

    print("\n🧾 Extracted Code:\n" + "-"*40)
    print(extracted_code)
    print("-" * 40)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_code_from_image.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    if not os.path.exists(image_path):
        print(f"❌ File not found: {image_path}")
        sys.exit(1)

    main(image_path)