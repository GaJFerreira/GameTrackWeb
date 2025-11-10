# app/routers/steam_router.py
from fastapi import APIRouter, Path, HTTPException
# O nome do arquivo mudou para 'steam_services' (plural),
# então ajustamos a importação
from ..services import steam_services

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

# 1. MUDAMOS DE 'GET' PARA 'POST'
#    Uma operação de 'sync' modifica dados, então POST é o correto.
# 2. MUDAMOS A ROTA
#    A rota agora precisa saber 'quem' é o usuário (user_id)
#    para salvar os jogos para ele.
@router.post("/sync/{user_id}/{steam_id}")
async def sync_user_steam_library(
    user_id: str = Path(..., title="ID do Usuário no Firebase", description="O UID do usuário no Firebase Auth."),
    steam_id: str = Path(..., title="SteamID64 do usuário", description="O ID numérico de 64 bits do perfil Steam.")
):
    """
    Sincroniza a biblioteca Steam de um usuário:
    Busca os jogos na API da Steam e os salva/atualiza no banco de dados
    do Firebase associados ao user_id.
    """
    print(f"Recebida requisição POST para /steam/sync/{user_id}/{steam_id}")
    try:
        # Chamamos nossa nova função de serviço
        synced_games = steam_services.sync_steam_library(user_id, steam_id)

        return {
            "message": "Sincronização concluída com sucesso!",
            "user_id": user_id,
            "game_count": len(synced_games)
            # Não retornamos a lista inteira para não poluir a resposta
        }
    except HTTPException as http_exc:
        print(f"Erro HTTP ao sincronizar {user_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        print(f"Erro inesperado no steam_router para {user_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao processar a sincronização.")