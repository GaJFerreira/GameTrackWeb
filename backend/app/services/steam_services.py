import requests
import time
import httpx
from fastapi import HTTPException
from pydantic import ValidationError

from app.services import ai_services
from ..config import settings
from ..schemas import game_schema
from ..models import game_model

# Tentativa de import do MetaModel
try:
    from ..models.meta_model import MetaModel
except ImportError:
    class MetaModel:
        @staticmethod
        def update_goals(user_id):
            print(f"Aviso: MetaModel não encontrado. Ignorando update de metas para {user_id}.")


# -----------------------------
# CONSTANTES
# -----------------------------
STEAM_PLAYER_API_URL = "http://api.steampowered.com"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails"


# ===========================================================
# 1) VALIDAÇÃO DO STEAM ID  (USADO NO CADASTRO E UPDATE)
# ===========================================================
async def validate_steam_id(steam_id: str):
    """
    Verifica se o SteamID existe e se o perfil é público.
    É usado antes de criar conta e quando usuário muda o SteamID.
    """
    url = (
        f"{STEAM_PLAYER_API_URL}/ISteamUser/GetPlayerSummaries/v0002/"
        f"?key={settings.steam_api_key}&steamids={steam_id}"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)

    if response.status_code != 200:
        raise HTTPException(status_code=502, detail="Erro ao comunicar com a Steam")

    data = response.json()
    players = data.get("response", {}).get("players", [])

    if not players:
        raise HTTPException(status_code=400, detail="Steam ID não encontrado.")

    player = players[0]

    # 3 significa perfil público
    if player.get("communityvisibilitystate") != 3:
        raise HTTPException(
            status_code=400,
            detail="O perfil da Steam precisa estar PÚBLICO para importarmos sua biblioteca."
        )

    return player


class SteamService:
    @staticmethod
    def sync_library(user_id: str, steam_id: str):
        return sync_steam_library(user_id, steam_id)


# ===========================================================
# 2) BUSCAR DETALHES DO JOGO NA STEAM STORE
# ===========================================================
def fetch_game_details_from_store(appid: int) -> dict:
    params = {"appids": appid, "cc": "br", "l": "brazilian"}

    try:
        time.sleep(0.1)
        response = requests.get(STEAM_STORE_API_URL, params=params, timeout=10)

        if response.status_code != 200:
            return {"error": f"HTTP {response.status_code}"}

        data = response.json()
        game_data = data.get(str(appid), {})

        if not game_data.get("success"):
            return {"error": "Jogo não encontrado"}

        return game_data.get("data", {})

    except Exception as e:
        return {"error": f"Erro loja: {e}"}


# ===========================================================
# 3) CONQUISTAS
# ===========================================================
def fetch_total_achievements(appid: int) -> int:
    url = (
        f"{STEAM_PLAYER_API_URL}/ISteamUserStats/GetSchemaForGame/v2/"
        f"?key={settings.steam_api_key}&appid={appid}"
    )
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            ach = (
                data.get("game", {})
                .get("availableGameStats", {})
                .get("achievements")
            )
            return len(ach) if ach else 0
    except:
        pass
    return 0


def fetch_player_achievements(steam_id: str, appid: int) -> int:
    url = (
        f"{STEAM_PLAYER_API_URL}/ISteamUserStats/GetPlayerAchievements/v1/"
        f"?key={settings.steam_api_key}&steamid={steam_id}&appid={appid}"
    )
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            ach = data.get("playerstats", {}).get("achievements")
            if ach:
                return sum(1 for a in ach if a.get("achieved") == 1)
    except:
        pass
    return 0


# ===========================================================
# 4) SINCRONIZAÇÃO COMPLETA DA BIBLIOTECA
# ===========================================================
def sync_steam_library(user_id: str, steam_id: str) -> list:
    print(f"Iniciando sincronização completa para {user_id}...")

    if not settings.steam_api_key:
        print("ERRO: steam_api_key não encontrada.")
        return []

    url = (
        f"{STEAM_PLAYER_API_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={settings.steam_api_key}&steamid={steam_id}&format=json"
        f"&include_appinfo=true&include_played_free_games=true"
    )

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 403:
            print("Erro 403: SteamID privado ou chave inválida.")
            return []

        response.raise_for_status()
        data = response.json()

        if "response" not in data or "games" not in data["response"]:
            print("Biblioteca vazia ou perfil privado.")
            return []

        steam_games = data["response"]["games"]
        print(f"{len(steam_games)} jogos encontrados. Processando...")

        batch_buffer = []
        BATCH_SIZE = 10

        for game_dict in steam_games:
            if "appid" not in game_dict:
                continue

            appid = int(game_dict["appid"])
            game_dict["appid"] = appid

            # Detalhes da loja
            full_details = fetch_game_details_from_store(appid)

            if not full_details.get("error"):
                app_type = full_details.get("type", "").lower()
                if app_type != "game":
                    continue

                game_dict["img_logo_url"] = full_details.get("header_image")
                game_dict["dados_loja"] = full_details
                game_dict["descricao"] = full_details.get("short_description")
                game_dict["descricao_completa"] = full_details.get("detailed_description")

                if "genres" in full_details:
                    game_dict["genero"] = ", ".join(g["description"] for g in full_details["genres"])

            # Horas jogadas
            if "playtime_forever" in game_dict:
                game_dict["horas_jogadas"] = round(game_dict["playtime_forever"] / 60)
                game_dict["status"] = (
                    "Iniciado" if game_dict["horas_jogadas"] > 0 else "Não Iniciado"
                )

            # Conquistas
            game_dict["conquistas_totais"] = fetch_total_achievements(appid)
            if game_dict["conquistas_totais"] > 0:
                game_dict["conquistas_obtidas"] = fetch_player_achievements(steam_id, appid)

            # Validação
            try:
                game_data = game_schema.GameBase(**game_dict)
                batch_buffer.append(game_data)
            except ValidationError as e:
                print(f"Erro validação Pydantic jogo {appid}: {e}")

            # Salva em lote
            if len(batch_buffer) >= BATCH_SIZE:
                game_model.sync_steam_games_batch(user_id, batch_buffer)
                batch_buffer = []

        if batch_buffer:
            game_model.sync_steam_games_batch(user_id, batch_buffer)

        MetaModel.update_goals(user_id)
        ai_services.train_and_save_model(user_id)

        print("Sincronização concluída.")
        return []

    except Exception as e:
        print(f"Erro fatal: {e}")
        return []


# ===========================================================
# 5) PERFIL DO USUÁRIO (public data)
# ===========================================================
def fetch_steam_user_profile(steam_id: str) -> dict:
    if not settings.steam_api_key:
        return {}

    url = f"{STEAM_PLAYER_API_URL}/ISteamUser/GetPlayerSummaries/v0002/"
    params = {"key": settings.steam_api_key, "steamids": steam_id}

    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        data = r.json()

        players = data.get("response", {}).get("players", [])
        if not players:
            return {}

        p = players[0]

        return {
            "personaname": p.get("personaname"),
            "realname": p.get("realname"),
            "avatar": p.get("avatarfull"),
            "profileurl": p.get("profileurl"),
            "loccountrycode": p.get("loccountrycode"),
        }

    except Exception:
        return {}


__all__ = [
    "sync_steam_library",
    "fetch_steam_user_profile",
    "validate_steam_id",
    "SteamService"
]
