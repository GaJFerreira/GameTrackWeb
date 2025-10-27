# app/routers/steam_router.py
from fastapi import APIRouter, Path, HTTPException
# Importamos a função que criamos no passo anterior
from ..services import steam_services

# Criamos um objeto 'Router'. Pense nele como um mini-aplicativo FastAPI
# dedicado apenas às rotas da Steam.
router = APIRouter(
    prefix="/steam", # Todas as rotas aqui começarão com /steam (ex: /steam/games/...)
    tags=["Steam"]   # Agrupa estas rotas sob a tag "Steam" na documentação /docs
)

# Definimos nossa primeira rota/endpoint
# @router.get diz que esta função responderá a requisições GET
# "/games/{steam_id}" define o caminho. {steam_id} é um parâmetro de caminho dinâmico.
@router.get("/games/{steam_id}")
async def fetch_steam_games(
    # Definimos o parâmetro steam_id que vem da URL.
    # Path(...) indica que ele vem do caminho, é obrigatório (...) e damos um título/descrição
    steam_id: str = Path(..., title="SteamID64 do usuário", description="O ID numérico de 64 bits do perfil Steam.")
):
    """
    Endpoint para buscar e retornar a lista de jogos de um usuário da Steam.
    Ele chama a função de serviço correspondente.
    """
    print(f"Recebida requisição GET para /steam/games/{steam_id}")
    try:
        # Chamamos a função do nosso serviço, passando o steam_id recebido
        games = steam_services.get_owned_games(steam_id)
        # Retornamos um JSON com o steam_id e a lista de jogos
        return {"steam_id": steam_id, "game_count": len(games), "games": games}
    except HTTPException as http_exc:
        # Se o serviço levantou um erro HTTP (como 404 ou 503),
        # simplesmente o re-lançamos para o FastAPI retornar a resposta de erro correta.
        print(f"Erro HTTP ao buscar jogos para {steam_id}: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        # Se ocorreu qualquer outro erro inesperado,
        # levantamos um erro 500 genérico.
        print(f"Erro inesperado no steam_router para {steam_id}: {e}")
        raise HTTPException(status_code=500, detail="Erro interno do servidor ao processar a requisição da Steam.")