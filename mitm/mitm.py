import time
from mitmproxy import http
import json
import os


SAVE_DIR = os.path.join(os.getcwd(), 'images')

class BlockProprietaryRequests:
    def request(self, flow: http.HTTPFlow) -> None:
        # Only check for proprietary code if the URL contains 'chatgpt.com'

        content_type = flow.request.headers.get("Content-Type", "").lower()
        url = flow.request.url.lower()

        # Handle Image Uploads (ChatGPT)
        if('files.oaiusercontent.com' in url):
            if content_type.startswith("image/") or any(ext in url for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]):
                fp = self.save_image(flow)
                # RUN OCR on file @ fp
                self.block(flow, "DIRECT_IMAGE_BLOCK")
                return
    
        if "chatgpt.com" in flow.request.url and 'conversation' in flow.request.url:
            print(f"Request URL contains 'chatgpt.com'. Checking for proprietary code...")

            if self.contains_proprietary_code(flow.request.content):
                self.block(flow, "PROPRIETORY_CODE")

    def save_image(self, flow):
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

    def block(self, flow: http.HTTPFlow, reason: str):
        print(f"{reason} Blocking request to {flow.request.url}.")
        flow.response = http.Response.make(
            403,
            b"Request blocked: " + reason.encode(),
            {"Content-Type": "text/plain"}
        )

    def contains_proprietary_code(self, request_body: bytes) -> bool:
        try:
            # Decode bytes into a string (UTF-8) before attempting to parse as JSON
            request_text = request_body.decode('utf-8')
            request_data = json.loads(request_text)  # Parse JSON

            def check(x):
                if 'SECRET_FUNCTION' in x:
                    return True
                return False

            if( self.check_chatgpt(request_data, check) ):
                return True
                    
        except (json.JSONDecodeError) as e:
            print(f"JSONDECCCCCC BUDDDDY: {e}")        
                
        except (UnicodeDecodeError) as e:
            print(f"UNICODEEEEEEE BUDDDDY: {e}")
        
        return False
    

    def check_chatgpt(self, request_data, call_compare):
        if('messages' in request_data):
            for m in request_data['messages']:
                parts =  m.get('content', dict()).get('parts', [])
                for part in parts:
                    if( call_compare(part) ):
                        return True
        return False

# This line initializes the class instance when mitmproxy runs.
addons = [
    BlockProprietaryRequests()
]