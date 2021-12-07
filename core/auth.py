from fastapi import Header, HTTPException

auth = True

def verify_token(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Token does not exist")
    if authorization != "something":
        raise HTTPException(status_code=403, detail="Token invalid")

def decrypt():
    pass

def check_identification_num():
    pass

def check_expired_time():
    pass