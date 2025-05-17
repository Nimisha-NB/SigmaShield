from mitmproxy import http
import json

class BlockProprietaryRequests:
    def request(self, flow: http.HTTPFlow) -> None:
        # Only check for proprietary code if the URL contains 'chatgpt.com'
        if "chatgpt.com" in flow.request.url and 'conversation' in flow.request.url:
            print(f"Request URL contains 'chatgpt.com'. Checking for proprietary code...")

            if self.contains_proprietary_code(flow.request.content):
                print(f"Proprietary code detected in request to {flow.request.url}. Blocking request...")
                print(f"Blocked request to {flow.request.url}.")
                flow.response = http.Response.make(
                    403,  # Forbidden
                    b"Request blocked due to proprietary code detection.",
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