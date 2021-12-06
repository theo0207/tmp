

auth = True

def auth_decorator(func):
    def auth_check():
        if auth:
            return func()
        else:
            return None

    return auth_check

def decrypt():
    pass

def check_identification_num():
    pass

def check_session_time():
    pass