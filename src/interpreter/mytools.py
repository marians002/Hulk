def to_list(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body
    
def get_value(body):
    return_value = None
    for exp in body:
        if isinstance(exp, list):
            return_value = get_value(exp, scope)
        else:
            return_value = self.visit(exp, scope)
    return return_value