# app/routers/user_router.py
from fastapi import APIRouter, HTTPException
from ..schemas.user_schema import UserCreate, User  # Importa o Schema corrigido
from ..services import user_service  # Importa o Serviço

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)


# 1. Rota de Registro (POST) - Agora com validação de Schema
# Removemos {user_id} do URL, pois ele é gerado pelo servidor (Service)
@router.post("/register", response_model=User)
def register_user(payload: UserCreate):  # FastAPI usa o Schema para validar o JSON de entrada
    """
    Recebe os dados do usuário, cria o registro e sincroniza a biblioteca Steam.
    O SteamID é obrigatório, conforme definido no UserCreate Schema.
    """
    try:
        # Chama o serviço para orquestrar o registro e a sincronização
        user = user_service.create_user_and_sync_steam(payload)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno no serviço de registro: {e}")


# 2. Rota de Busca (GET) - Chama o Serviço
# Adicione a validação de resposta para garantir que o JSON retornado é um objeto User
@router.get("/{user_id}", response_model=User)
def get_user_data(user_id: str):
    """
    Busca os dados de um usuário pelo ID.
    """
    # O Router chama o Serviço, que chama o Model (a forma correta)
    user = user_service.get_user(user_id)

    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")

    return user