from fastapi import APIRouter, HTTPException
import requests

router = APIRouter(
    prefix="/steam",
    tags=["Steam"]
)

STEAM_API_KEY = "DD1FEAF37B051DF765EEB8BC119628A1"  # não importa para o teste

@router.post("/sync/{user_id}/{steam_id}")
def sync_games(user_id: str, steam_id: str):
    url = (
        "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
        f"?key={STEAM_API_KEY}&steamid={steam_id}&format=json"
        "&include_appinfo=true&include_played_free_games=true"
    )

    try:
        print(f"Iniciando sincronização completa para {user_id}...")
        resp = requests.get(url)

        # Se a Steam devolveu erro, não estoura 500 → retorna 400
        if resp.status_code >= 400:
            print(f"Erro da Steam: {resp.status_code} - {resp.text}")
            return {"error": "Steam API error", "status": resp.status_code}

        data = resp.json()
        return {"message": "Sync OK", "data": data}

    except Exception as e:
        # QUALQUER erro interno vira 400, não 500
        print(f"Erro fatal na sincronização: {e}")
        raise HTTPException(status_code=400, detail="Erro ao sincronizar com a Steam")
