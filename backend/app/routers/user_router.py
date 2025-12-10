from typing import List
from fastapi import APIRouter, HTTPException, Depends
from ..schemas.user_schema import UserCreate, User, UserRegisterResponse
from ..services import user_service, steam_services

# Import para pegar usuário logado
from ..routers.auth_router import verify_token as get_current_user

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

# ===============================================
# REGISTRO DE USUÁRIO
# ===============================================
@router.post("/register", response_model=UserRegisterResponse)
def register_user(payload: UserCreate):
    try:
        user = user_service.create_user_and_sync_steam(payload)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no serviço de registro: {e}")


# ===============================================
# LISTAR TODOS OS USUÁRIOS
# ===============================================
@router.get("/", response_model=List[User])
def list_users() -> List[User]:
    return user_service.get_all_users()


# ===============================================
# PEGAR DADOS DE UM USUÁRIO ESPECÍFICO
# ===============================================
@router.get("/{user_id}", response_model=User)
def get_user_data(user_id: str):

    user = user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user


# ===============================================
# ATUALIZAR STEAM ID DO USUÁRIO LOGADO
# ===============================================
@router.put("/me/steam-id")
async def update_steam_id(new_steam_id: str, current_user=Depends(get_current_user)):

    # 1. Valida o novo Steam ID
    await steam_services.validate_steam_id(new_steam_id)

    # 2. Atualiza no banco — função síncrona
    updated_user = user_service.update_user(
        current_user["uid"],     # Vem do Firebase Auth
        {"steam_id": new_steam_id}
    )

    if not updated_user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return {
        "message": "Steam ID atualizado com sucesso!",
        "steam_id": new_steam_id
    }
