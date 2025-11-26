from typing import List
from fastapi import APIRouter, HTTPException
from ..schemas.user_schema import UserCreate, User, UserRegisterResponse
from ..services import user_service

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

@router.post("/register", response_model=UserRegisterResponse)
def register_user(payload: UserCreate):
    try:
        user = user_service.create_user_and_sync_steam(payload)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no serviço de registro: {e}")


@router.get("/", response_model=List[User])
def list_users() -> List[User]:
    return user_service.get_all_users()

@router.get("/{user_id}", response_model=User)
def get_user_data(user_id: str):
   
    user = user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user