# 1) IMPORTS
import requests
import time
from fastapi import HTTPException
from pydantic import ValidationError

from ..config import settings
from ..schemas import game_schema
from ..models import game_model


# 2) CLASSE USADA PELO ROUTER E PELO PYTEST
class SteamService:
    """
    Wrapper apenas para permitir monkeypatch no Pytest.
    """
    def sync_library(self, user_id: str, steam_id: str):
        return sync_steam_library(user_id, steam_id)


# 3) FUNÇÕES COMPLETAS
STEAM_PLAYER_API_URL = "http://api.steampowered.com"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails"


def fetch_game_details_from_store(appid: int) -> dict:
    params = {'appids': appid, 'cc': 'br', 'l': 'brazilian'}
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


def fetch_total_achievements(appid: int) -> int:
    url = f"{STEAM_PLAYER_API_URL}/ISteamUserStats/GetSchemaForGame/v2/?key={settings.steam_api_key}&appid={appid}"
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            data = r.json()
            ach = data.get("game", {}).get("availableGameStats", {}).get("achievements")
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


def sync_steam_library(user_id: str, steam_id: str) -> list:
    """
    Função principal de sincronização.
    GARANTIA: Sempre retorna uma lista (nunca None).
    """
    print(f"[SYNC] Iniciando sincronização Steam do usuário {user_id}")

    api_key = settings.steam_api_key
    if not api_key:
        print("[ERRO] steam_api_key AUSENTE no .env")
        return []  # evita crash no registro

    url = (
        f"{STEAM_PLAYER_API_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={api_key}&steamid={steam_id}&format=json"
        f"&include_appinfo=true&include_played_free_games=true"
    )

    try:
        resp = requests.get(url, timeout=15)

        if resp.status_code == 403:
            print("[ERRO] Steam devolveu 403 – chave inválida ou limitada")
            return []

        resp.raise_for_status()
        data = resp.json()

        steam_games = data.get("response", {}).get("games", [])
        if not steam_games:
            print("[SYNC] Nenhum jogo encontrado (perfil privado?)")
            return []

        games_to_sync = []

        for g in steam_games[:40]:  # limita 40 para performance
            appid = g.get("appid")
            if not appid:
                continue

            details = fetch_game_details_from_store(appid)

            # se der erro, continua, não quebra tudo
            if details.get("error"):
                details = {}

            g["horas_jogadas"] = round(g.get("playtime_forever", 0) / 60)
            g["status"] = "Iniciado" if g["horas_jogadas"] > 0 else "Não Iniciado"

            g["descricao"] = details.get("short_description")
            g["descricao_completa"] = details.get("detailed_description")
            g["sobre"] = details.get("about_the_game")
            g["linguas"] = details.get("supported_languages")

            if "genres" in details:
                g["genero"] = ", ".join([x["description"] for x in details["genres"]])

            g["conquistas_totais"] = fetch_total_achievements(appid)
            if g["conquistas_totais"] > 0:
                g["conquistas_obtidas"] = fetch_player_achievements(steam_id, appid)

            # valida via pydantic
            try:
                validated = game_schema.GameBase(**g)
                games_to_sync.append(validated)
            except ValidationError as e:
                print("[ERRO] Pydantic:", e)

        # salva no Firestore
        if games_to_sync:
            game_model.sync_steam_games_batch(user_id, games_to_sync)

        return games_to_sync  # SEMPRE lista

    except Exception as e:
        print("[ERRO] Falha total na sincronização:", e)
        return []  # nunca retorna None!


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


# 4) EXPORTS
__all__ = [
    "sync_steam_library",
    "fetch_steam_user_profile",
    "SteamService",
]
