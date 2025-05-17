import json

from checker import check_if_company_code

def handle_chatgpt(flow):
    print("LALALALA")
    content_type = flow.request.headers.get("Content-Type", "").lower()
    url = flow.request.url.lower()

    request_text = flow.request.content.decode('utf-8')
    request_data = json.loads(request_text) 
    
    print(request_data)
    if('messages' in request_data):
        for m in request_data['messages']:
            parts =  m.get('content', dict()).get('parts', [])
            for part in parts:
                print("PART", part)
                if( check_if_company_code(part) ):
                    return True
    return False
    