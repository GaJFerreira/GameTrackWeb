from fastapi import APIRouter, Path, HTTPException, BackgroundTasks
from ..services import steam_services

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

@router.post("/sync/{user_id}/{steam_id}")
async def sync_user_steam_library(
    background_tasks: BackgroundTasks,
    user_id: str = Path(..., title="ID do Usuário no Firebase"),
    steam_id: str = Path(..., title="SteamID64 do usuário")
):
    try:

        background_tasks.add_task(steam_services.sync_steam_library, user_id, steam_id)
        
        return {
            "message": "Sincronização iniciada em segundo plano! Seus jogos aparecerão gradualmente.",
            "status": "processing"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao iniciar sincronização: {e}")