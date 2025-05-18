import urllib.parse
from checker import check_if_company_code

def handle_stackoverflow(flow):
    print("HANDLE_STSACKLOVERFLOW")
    
    # Decode request content
    request_text = flow.request.content.decode('utf-8')
    form_data = urllib.parse.parse_qs(request_text)

    # Get 'post-text' field from form data
    post_text_list = form_data.get('post-text', [])
    if not post_text_list:
        return False

    post_text = post_text_list[0]  # take the first value

    if check_if_company_code(post_text):
        return True

    return False