import json

from checker import check_if_company_code

def handle_twitter(flow):
    print("HANDLE_TWITTER")
    request_text = flow.request.content.decode('utf-8')
    request_data = json.loads(request_text) 
    
    print(request_data)
    if('variables' in request_data):
        vars = request_data['variables']
        tweet_text = vars.get('tweet_text', None)
        if(tweet_text == None):
            return False
        
        if( check_if_company_code(tweet_text) ):
            return True
                
    return False