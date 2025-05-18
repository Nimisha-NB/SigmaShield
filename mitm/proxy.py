import asyncio
import time
from chatgpt import handle_chatgpt
from checker import check_if_company_code
from models import get_code_in_image, save_image_for_ocr
from mitmproxy import http
import json
import os
from concurrent.futures import ThreadPoolExecutor, TimeoutError

executor = ThreadPoolExecutor(max_workers=2)

def run_async_in_thread(coro):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(coro)
    loop.close()
    return result

class BlockProprietaryRequests:
    def request(self, flow: http.HTTPFlow) -> None:
        # Only check for proprietary code if the URL contains 'chatgpt.com'

        content_type = flow.request.headers.get("Content-Type", "").lower()
        url = flow.request.url.lower()

        # if flow.request.method != 'POST':
        #     return True

        # ----------- HANDLE IMAGE UPLOAD ----------
        if content_type.startswith("image/") or any(ext in url for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]):
            fp = save_image_for_ocr(flow)
            if(fp == None):
                print("SAVE_FAILLLLLL")
                return True
            print("GETTING OCR")
            future = executor.submit(run_async_in_thread, get_code_in_image(fp))
            try:
                ocr_text = future.result(timeout=40)  # Wait up to 10s
                print("OCR RESULT:", ocr_text)

                # Uncomment this when ready to do proper checking
                # if check_if_company_code(ocr_text):
                #     self.block(flow, "COMPANY_CODE_FOUND_IN_IMAGE")
                #     return

                self.block(flow, "COMPANY_CODE_FOUND")  # Always blocking for now
                return

            except TimeoutError:
                print("OCR TIMEOUT")
                self.block(flow, "OCR_TIMEOUT")
                return
            except Exception as e:
                print("OCR ERROR:", e)
                self.block(flow, "OCR_EXCEPTION")
                return
            

            # # ocr_text = get_code_in_image(fp)
            # print("CHECKING OCR")
            # if( check_if_company_code(ocr_text) ):
            #     self.block(flow, "COMPANY_CODE_FOUND_IN_IMAGE")
            #     print("COMPANY_CODE_FOUND_IN_IMAGE")
            #     return True
            # print("NOTHING BUDDY")
            # self.block(flow, "COMPANY_CODE_FOUND")
            # return True
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