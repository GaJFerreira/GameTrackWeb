from fastapi import APIRouter, Path, HTTPException
from ..services import steam_services

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

@router.post("/sync/{user_id}/{steam_id}")
async def sync_user_steam_library(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="ID de Teste."),
    steam_id: str = Path(..., title="SteamID64 do usuário", description="O ID numérico de 64 bits do perfil Steam.")
):
    try:
        synced_games = steam_services.sync_steam_library(user_id, steam_id)
        return {
            "message": "Sincronização concluída com sucesso!",
            "user_id": user_id,
            "game_count": len(synced_games)
        }
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno ao sincronizar: {e}")
