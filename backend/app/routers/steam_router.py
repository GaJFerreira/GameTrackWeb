# app/routers/steam_router.py

from fastapi import APIRouter, Path, HTTPException
from ..services import steam_services
# from ..services.auth_service import get_current_user_id # COMENTE OU REMOVA ESTA LINHA POR ENQUANTO

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

# ROTA DE SINCRONIZAÇÃO (TEMPORARIAMENTE SEM SEGURANÇA)
@router.post("/sync/{user_id}/{steam_id}") # user_id DE VOLTA NA ROTA
async def sync_user_steam_library(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="ID de Teste."), # O user_id vem do URL
    steam_id: str = Path(..., title="SteamID64 do usuário", description="O ID numérico de 64 bits do perfil Steam.")
    # user_id: str = Depends(get_current_user_id) # LINHA DE SEGURANÇA REMOVIDA PARA O TESTE
):
    """
    Sincroniza a biblioteca Steam de um usuário no Firebase. (MODO DE TESTE)
    """
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

# ... (você pode deixar as outras rotas GET por enquanto,
# ou podemos adicioná-las no próximo passo)