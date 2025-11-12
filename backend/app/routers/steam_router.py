# app/routers/steam_router.py
from fastapi import APIRouter, Path, HTTPException

from ..services import steam_services

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

@router.post("/sync/{user_id}/{steam_id}")
async def sync_user_steam_library(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="O UID do usuário no Firebase Auth."),
    steam_id: str = Path(..., title="SteamID64 do usuário", description="O ID numérico de 64 bits do perfil Steam.")
):
    print(f"Recebida requisição POST para /steam/sync/{user_id}/{steam_id}")
    try:
        synced_games = steam_services.sync_steam_library(user_id, steam_id)

        return {
            "message": "Sincronização concluída com sucesso!",
            "user_id": user_id,
            "game_count": len(synced_games)
        }
    except HTTPException as http_exc:
        print(f"Erro HTTP ao sincronizar {user_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        print(f"Erro inesperado no steam_router para {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao processar a sincronização.")