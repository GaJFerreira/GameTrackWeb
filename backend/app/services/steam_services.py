import requests
import time
from fastapi import HTTPException
from pydantic import ValidationError
from app.services import ai_services
from ..config import settings
from ..schemas import game_schema
from ..models import game_model


class SteamService:
    def sync_library(self, user_id: str, steam_id: str):
        return sync_steam_library(user_id, steam_id)


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
    print(f"Iniciando sincronização completa para {user_id}...")

    if not settings.steam_api_key or settings.steam_api_key == "":
        print("ERRO CRÍTICO: Chave da Steam (steam_api_key) não encontrada no .env")
        return []
    
    api_key = settings.steam_api_key
    url = (
        f"{STEAM_PLAYER_API_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={api_key}&steamid={steam_id}&format=json"
        f"&include_appinfo=true&include_played_free_games=true"
    )

    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 403:
             print("Erro 403 Steam: Chave inválida ou perfil privado.")
             return []
             
        response.raise_for_status()
        data = response.json()
        
        if "response" not in data or "games" not in data["response"]:
            print("Aviso: Biblioteca vazia ou perfil privado.")
            return []
        
        steam_games = data["response"]["games"]
        print(f"Encontrados {len(steam_games)} jogos. Iniciando processamento em lotes...")

        batch_buffer = [] 
        BATCH_SIZE = 10   
        
        for idx, game_dict in enumerate(steam_games):

            if 'appid' not in game_dict: continue
            
            raw_id = game_dict['appid']
            try:
                appid_int = int(raw_id)
                game_dict['appid'] = appid_int 
                appid = appid_int
            except ValueError:
                print(f"Pulei um jogo com ID inválido: {raw_id}")
                continue
            
            full_details = fetch_game_details_from_store(appid)
            
            if not full_details.get('error'):
                app_type = full_details.get('type', '').lower()
                if app_type and app_type != 'game':
                    continue
            
                store_image = full_details.get('header_image')
                if store_image:
                    game_dict['img_logo_url'] = store_image

                game_dict['dados_loja'] = full_details
                game_dict['descricao'] = full_details.get('short_description')
                game_dict['descricao_completa'] = full_details.get('detailed_description')
                game_dict['sobre'] = full_details.get('about_the_game')
                game_dict['linguas'] = full_details.get('supported_languages')
                
                if 'genres' in full_details:
                    game_dict['genero'] = ', '.join([g['description'] for g in full_details['genres']])

                if 'developers' in full_details:
                    game_dict['desenvolvedor'] = ', '.join(full_details['developers'])

                if 'publishers' in full_details:
                    game_dict['publisher'] = ', '.join(full_details['publishers'])
               
                if 'metacritic' in full_details:
                    game_dict['metacritic'] = full_details['metacritic'].get('score')
                
                if 'release_date' in full_details:
                    game_dict['data_lancamento'] = full_details['release_date'].get('date')

                game_dict['preco'] = None
                if 'price_overview' in full_details:
                    price_info = full_details['price_overview']
                    game_dict['preco'] = {
                        'moeda': price_info.get('currency'),
                        'preco_original': price_info.get('initial'),
                        'preco_final': price_info.get('final'),
                        'desconto_percentual': price_info.get('discount_percent')
                    }

                game_dict['categorias'] = None
                if 'categories' in full_details:
                    cats = full_details['categories']
                    if isinstance(cats, list):
                        cat_descriptions = [c.get('description', '') for c in cats if isinstance(c, dict) and 'description' in c]
                        if cat_descriptions:
                            game_dict['categorias'] = ', '.join(cat_descriptions) 
                    
                pc_recs = full_details.get('pc_requirements', {})
                if isinstance(pc_recs, list): pc_recs = {}

                game_dict['requisitos_recomendados'] = pc_recs.get('recommended')
                game_dict['requisitos_minimos'] = pc_recs.get('minimum')

            if 'playtime_forever' in game_dict:
                game_dict['horas_jogadas'] = round(game_dict['playtime_forever'] / 60)
                game_dict['status'] = 'Iniciado' if game_dict['horas_jogadas'] > 0 else 'Não Iniciado'
            
            game_dict['conquistas_totais'] = fetch_total_achievements(appid)
            if game_dict['conquistas_totais'] > 0:
                game_dict['conquistas_obtidas'] = fetch_player_achievements(steam_id, appid)

            try:

                game_data = game_schema.GameBase(**game_dict)
                batch_buffer.append(game_data)
            except ValidationError as e:
                print(f"Erro validação Pydantic jogo {appid}: {e}")

            if len(batch_buffer) >= BATCH_SIZE:
                print(f"Salvando lote parcial de {len(batch_buffer)} jogos...")
                game_model.sync_steam_games_batch(user_id, batch_buffer)
                batch_buffer = []


        if batch_buffer:
            print(f"Salvando lote final de {len(batch_buffer)} jogos...")
            game_model.sync_steam_games_batch(user_id, batch_buffer)
        
        print("Sincronização background finalizada com sucesso.")

        ai_services.train_and_save_model(user_id)

        return []

    except Exception as e:
        print(f"Erro fatal na thread de sincronização: {e}")
        return []


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
    "SteamService",
]