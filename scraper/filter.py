def check_art_type(pub, *art_types):
    if not art_types: return True
    return pub['artType'] in art_types

def _check_all(l1, l2):
    r = True
    for l in l1:
        if l not in l2:
            r = False
    return r

def _check_any(l1, l2):
    if not l1: return True
    r = False
    for h in l1:
        if h in l2:
            r = True
    return r

def _check_not_any(l1, l2):
    if not l1: return True
    r = True
    for h in l1:
        if h in l2:
            r = False
    return r

def check_content(pub, keyword):
    return pub['content'].lower().find(keyword.lower())!=-1

def check_body(pub, keyword):
    return pub['hierarchyStr'].lower().find(keyword.lower())!=-1

def check_hierarchy_list(pub, in_list, not_list, all_list):
    hierarchy_list = pub['hierarchyList']
    in_result = _check_any(in_list, hierarchy_list)
    not_result = _check_not_any(not_list, hierarchy_list)
    all_result = _check_all(all_list, hierarchy_list)
    
    return in_result, not_result, all_result


def find_any(search_on, search_for, case_sensitive=False):
    '''Search on 'search_on' for any occurrencies of 'search_for' '''
    
    if not case_sensitive:
        search_on = search_on.lower() 
        
    if isinstance(search_for, str):
        search_for = [search_for]
        
    for text in search_for:
        t = text
        if not case_sensitive:
            t = t.lower()
        if search_on.find(t) != -1: return True
    
    return False
    

def handle_pre_filters(pre_filters, pub):
    print('handling pre filters')
    print(pre_filters)
    supported_conditions = ('contains_any', 'contains_all')
    conditions_passed = []
    for key, condition, values in pre_filters:
        if condition not in supported_conditions:
            raise ValueError(f"Condition '{condition}' is not valid.\n Should be one of {supported_conditions}")
        conditions_passed.append(find_any(pub[key], values))
    return all(conditions_passed)



