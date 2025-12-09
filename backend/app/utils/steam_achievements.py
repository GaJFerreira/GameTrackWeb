import requests
from ..config import settings

STEAM_PLAYER_API_URL = "http://api.steampowered.com"


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
