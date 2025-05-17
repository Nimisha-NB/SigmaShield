from fuzzysearch import global_fuzzy_search

def check_if_company_code(text):
    print("WAAAAA", text)
    # code = True
    
    # if(len(text) < 20):
    #     return False
    
    # # Check Code or No-Code

    # if(not code):
    #     print("RETFALSEEE")
    #     return False
    
    # Implement the Fuzzy Search
    matched = global_fuzzy_search(text)
    print("MATCHEDDDDD", matched)
    if(not matched):
        return False

    return True