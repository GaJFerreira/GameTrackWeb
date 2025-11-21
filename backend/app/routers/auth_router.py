from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from firebase_admin import auth
import requests
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    display_name: str | None = None

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded = auth.verify_id_token(token)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")

@router.post("/register")
def register_user(body: RegisterRequest):
    try:
        user = auth.create_user(
            email=body.email,
            password=body.password,
            display_name=body.display_name
        )
        return {"message": "Usuário criado com sucesso.", "uid": user.uid}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/login")
def login_user(body: LoginRequest):
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={settings.firebase_web_api_key}"
    payload = {
        "email": body.email,
        "password": body.password,
        "returnSecureToken": True
    }
    resp = requests.post(url, json=payload)
    data = resp.json()
    if resp.status_code != 200:
        raise HTTPException(status_code=400, detail=data.get("error", {}).get("message"))
    return {
        "id_token": data["idToken"],
        "refresh_token": data["refreshToken"],
        "expires_in": data["expiresIn"]
    }

@router.get("/me")
def me(current_user=Depends(verify_token)):
    return {"message": "Token válido.", "user": current_user}
