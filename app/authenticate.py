from fastapi import HTTPException, Header

STATIC_TOKEN = "static_token_here"


# Dependency to authenticate requests
def token_authenticate(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True
