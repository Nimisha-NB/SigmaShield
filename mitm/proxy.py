import time
from chatgpt import handle_chatgpt
from ocr import save_image_for_ocr
from mitmproxy import http
import json
import os

class BlockProprietaryRequests:
    def request(self, flow: http.HTTPFlow) -> None:
        # Only check for proprietary code if the URL contains 'chatgpt.com'

        content_type = flow.request.headers.get("Content-Type", "").lower()
        url = flow.request.url.lower()

        # ----------- HANDLE IMAGE UPLOAD ----------
        if flow.request.method == "POST":
            if content_type.startswith("image/") or any(ext in url for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]):
                fp = save_image_for_ocr(flow)
                # RUN OCR on file @ fp
                return True
        # -----------------------------------------
        
        if "chatgpt.com" in url and 'conversation' in url:
            blocked = handle_chatgpt(flow)        
            print("CHATGPTTTTTT", blocked)  
            if(blocked):
                self.block(flow, "COMPANY_CODE_FOUND")
                return True 
            print("SSAAAAA")

    def block(self, flow: http.HTTPFlow, reason: str):
        print(f"{reason} Blocking request to {flow.request.url}.")
        flow.response = http.Response.make(
            403,
            b"Request blocked: " + reason.encode(),
            {"Content-Type": "text/plain"}
        )


# This line initializes the class instance when mitmproxy runs.
addons = [
    BlockProprietaryRequests()
]