import os
import time

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