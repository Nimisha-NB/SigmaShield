from mitm.utils import save_image_for_ocr


class Interceptors:
    def handle_chatgpt(self, flow):
        content_type = flow.request.headers.get("Content-Type", "").lower()
        url = flow.request.url.lower()

        # ----------- HANDLE IMAGE UPLOAD ----------
        if('files.oaiusercontent.com' in url):
            if content_type.startswith("image/") or any(ext in url for ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"]):
                fp = save_image_for_ocr(flow)
                # RUN OCR on file @ fp
                return True
    
        if "chatgpt.com" in url and 'conversation' in url:
            request_text = request_body.decode('utf-8')
            request_data = json.loads(request_text) 

            if self.contains_proprietary_code(flow.request.content):
                self.block(flow, "PROPRIETORY_CODE")

        return False
    


class InterceptorComparators:
    @classmethod
    def check_chatgpt_message(cls, request_data, call_compare):
            if('messages' in request_data):
                for m in request_data['messages']:
                    parts =  m.get('content', dict()).get('parts', [])
                    for part in parts:
                        if( call_compare(part) ):
                            return True
            return False