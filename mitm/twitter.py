# import json


# def handle_twitter(flow, call_compare):
#     request_text =  flow.request.content.decode('utf-8')
#     request_data = json.loads(request_text)
    
#     content_type = flow.request.headers.get("Content-Type", "").lower()
#     url = flow.request.url.lower()

#     # Block image upload via multipart/form-data (e.g., Twitter)
#     if "multipart/form-data" in content_type and is_image_data(flow.request.content):
#         self.block(flow, "Image upload via multipart/form-data detected.")
#         return True
    
#     if "upload.twitter.com" in url and "media/upload" in url:
#         self.block(flow, "Twitter image/media upload detected.")
#         return

#     if "upload.twitter.com" in url and "media/upload" in url:
#         self.block(flow, "Twitter image/media upload detected.")
#         return