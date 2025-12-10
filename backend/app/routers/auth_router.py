from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel, EmailStr
from firebase_admin import auth
import requests
from ..config import settings
from ..schemas.user_schema import UserCreate
from ..services import user_service, steam_services

router = APIRouter(prefix="/auth", tags=["Auth"])
security = HTTPBearer()


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    steam_id: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        decoded = auth.verify_id_token(token, clock_skew_seconds=30)
        return decoded
    except Exception:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado")


# ============================================================
# REGISTER COM VALIDAÇÃO DE STEAM ID
# ============================================================
@router.post("/register")
async def register_user(body: RegisterRequest, background_tasks: BackgroundTasks):

    # 1) VALIDA O STEAM ID ANTES DE QUALQUER COISA
    try:
        await steam_services.validate_steam_id(body.steam_id)
    except HTTPException as e:
        raise e
    except Exception:
        raise HTTPException(status_code=400, detail="Steam ID inválido.")

    try:
        # 2) CRIA O USUÁRIO NO FIREBASE
        user_firebase = auth.create_user(
            email=body.email,
            password=body.password,
            display_name=body.steam_id
        )

        # 3) CRIA OBJETO PARA SALVAR NO BANCO LOCAL
        user_data_service = UserCreate(
            email=body.email,
            steam_id=body.steam_id,
            password=body.password,
            personaname=body.steam_id,
        )

        # 4) SALVA NO BANCO VIA SERVICE
        result = user_service.register_user_db(
            user_data_service,
            user_id_firebase=user_firebase.uid
        )

        # 5) AGENDA A SINCRONIZAÇÃO EM BACKGROUND
        print(f"Agendando sincronização em background para {user_firebase.uid}...")
        background_tasks.add_task(
            steam_services.sync_steam_library,
            user_id=user_firebase.uid,
            steam_id=body.steam_id
        )

        return {
            "message": "Conta criada! Seus jogos aparecerão na biblioteca em breve.",
            "uid": user_firebase.uid,
            "background_sync": "Iniciado"
        }

    except HTTPException as e:
        raise e
    except Exception as e:
        print(f"Erro no registro: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================
# LOGIN
# ============================================================
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


# ============================================================
# ME
# ============================================================
@router.get("/me")
def me(current_user=Depends(verify_token)):
    return {"message": "Token válido.", "user": current_user}
