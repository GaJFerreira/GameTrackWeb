import requests
from fastapi import HTTPException
from app.config import settings


class SteamService:

    def sync_library(self, user_id: str, steam_id: str):
        """
        Busca jogos da Steam usando a API oficial.
        Esta função PRECISA existir exatamente com este nome
        para os testes mockarem corretamente.
        """
        try:
            url = (
                "http://api.steampowered.com/IPlayerService/GetOwnedGames/v1/"
                f"?key={settings.steam_api_key}"
                f"&steamid={steam_id}"
                "&format=json"
                "&include_appinfo=true"
                "&include_played_free_games=true"
            )

            resp = requests.get(url)
            resp.raise_for_status()

            data = resp.json()
            return data.get("response", {}).get("games", [])

        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
