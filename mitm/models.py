import requests
import os
import time
import httpx

BASE = 'https://6dwpp646-4000.inc1.devtunnels.ms'

# def get_code_in_image(image_path):
#     with open(image_path, 'rb') as img:
#         files = {'image': img}
#         try:
#             response = requests.post(f'{BASE}/upload', files=files)
#             response.raise_for_status()
#             resp = response.json()
#             return resp.get('text', False)
#         except requests.exceptions.RequestException as e:
#             print(f"[REQUEST ERROR] {e}")
#         except ValueError:
#             print("[RESPONSE ERROR] Failed to parse JSON.")
#         except Exception as e:
#             print(f"[UNEXPECTED ERROR] {e}")
#     return False

async def get_code_in_image(image_path: str):
    try:
        async with httpx.AsyncClient(timeout=40,verify=False) as client:
            with open(image_path, 'rb') as img_file:
                files = {'image': (image_path, img_file, 'application/octet-stream')}
                response = await client.post(f"{BASE}/upload", files=files)
                response.raise_for_status()
                data = response.json()
                return data.get("text", "")
    except httpx.RequestError as e:
        print(f"[HTTPX ERROR] {e}")
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
    return ""

# def check_if_code_or_not(text):
#     data = {
#         "text": text,
#     }
#     try:
#         response = requests.post(f'{BASE}/predict', json=data, headers={'Content-Type': 'application/json'})
#         resp = response.json()
#         if('Code' in resp):
#             return True 
#     except Exception as e:
#         print("EXCEPTION", e)
#     return False


def save_image_for_ocr(flow):
    SAVE_DIR = os.path.join(os.getcwd(), 'images')
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
    if(ext == "bin"):
        return None
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


# if __name__ == '__main__':
#     print(get_code_in_image("/Users/manashejmadi/Desktop/Screenshot 2025-05-18 at 6.06.04 AM.png"))