from fastapi import APIRouter, HTTPException
from app.services.steam_services import SteamService

router = APIRouter(prefix="/steam", tags=["Steam"])

steam_service = SteamService()

@router.post("/sync/{user_id}/{steam_id}")
def sync_steam_library(user_id: str, steam_id: str):
    """
    Endpoint esperado pelos testes:
    POST /steam/sync/{user_id}/{steam_id}
    """
    try:
        games = steam_service.sync_library(user_id, steam_id)
        return {
            "message": "Sincronização concluída.",
            "games_synced": len(games)
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
