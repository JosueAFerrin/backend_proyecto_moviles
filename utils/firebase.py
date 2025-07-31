import firebase_admin
from firebase_admin import auth, credentials
from fastapi import HTTPException, Header

cred = credentials.Certificate("secrets/firebase-key.json")
firebase_admin.initialize_app(cred)

async def verify_token(authorization: str = Header(...)):
    try:
        token = authorization.split(" ")[1]
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido o expirado")
