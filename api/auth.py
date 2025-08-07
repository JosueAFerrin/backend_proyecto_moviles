from fastapi import Header, HTTPException
from firebase_admin import auth as admin_auth

def verify_token(authorization: str = Header(...)):
    try:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() != "bearer":
            raise ValueError("Invalid token scheme")
        decoded_token = admin_auth.verify_id_token(token)
        return decoded_token
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
