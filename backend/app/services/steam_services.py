import requests
import time
from fastapi import HTTPException
from pydantic import ValidationError

from ..config import settings
from ..schemas import game_schema
from ..models import game_model

STEAM_PLAYER_API_URL = "http://api.steampowered.com"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails"

def fetch_game_details_from_store(appid: int) -> dict:
    params = {
        'appids': appid,
        'cc': 'br',
        'l': 'brazilian'
    }

    try:
        # Delay para não ser bloqueado pela Steam
        time.sleep(0.2)
        response = requests.get(STEAM_STORE_API_URL, params=params, timeout=10)

        if response.status_code != 200:
            return {"error": f"Status code {response.status_code}"}
        
        data = response.json()

        if str(appid) in data and data[str(appid)].get('success') is True:
            return data[str(appid)].get('data', {})
        
        return {"error": "Jogo não encontrado na loja Steam."}

    except requests.exceptions.RequestException as e:
        print(f"Erro de conexão com a loja Steam: {e}")
        return {"error": f"Erro de conexão: {str(e)}"}
    
    except Exception as e:
        print(f"Erro inesperado ao buscar detalhes do jogo: {e}")
        return {"error": f"Erro inesperado: {str(e)}"}

def fetch_total_achievements(appid: int) -> int: 
    API_URL = f"{STEAM_PLAYER_API_URL}/ISteamUserStats/GetSchemaForGame/v2/?key={settings.steam_api_key}&appid={appid}"
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            achievements = data.get('game', {}).get('availableGameStats', {}).get('achievements')
            return len(achievements) if achievements else 0
    except:
        pass
    return 0

def fetch_player_achievements(steam_id: str, appid: int) -> int:
    API_URL = f"{STEAM_PLAYER_API_URL}/ISteamUserStats/GetPlayerAchievements/v1/?key={settings.steam_api_key}&steamid={steam_id}&appid={appid}"
    try:
        response = requests.get(API_URL, timeout=5)
        if response.status_code == 200:
            data = response.json()
            achievements = data.get('playerstats', {}).get('achievements')
            if achievements:
                return sum(1 for a in achievements if a.get('achieved') == 1)
    except:
        pass
    return 0

def sync_steam_library(user_id: str, steam_id: str) -> list:
    print(f"Iniciando sincronização completa para {user_id}...")

    # 1. Verificação de Segurança da Chave
    if not settings.steam_api_key or settings.steam_api_key == "":
        print("ERRO CRÍTICO: Chave da Steam (steam_api_key) não encontrada no .env")
        raise HTTPException(status_code=500, detail="Servidor mal configurado: Chave Steam ausente.")
    
    api_key = settings.steam_api_key
    url = (
        f"{STEAM_PLAYER_API_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={api_key}&steamid={steam_id}&format=json"
        f"&include_appinfo=true&include_played_free_games=true"
    )

    try:
        response = requests.get(url, timeout=15)
        
        if response.status_code == 403:
             raise HTTPException(status_code=500, detail="Chave da Steam inválida (Erro 403). Verifique o .env")
             
        response.raise_for_status()
        data = response.json()
        
        if "response" not in data or "games" not in data["response"]:
            print("Aviso: Biblioteca vazia ou perfil privado.")
            return []
        
        steam_games = data["response"]["games"]
        print(f"Encontrados {len(steam_games)} jogos. Processando os primeiros 20...")

        games_to_sync = []
        ignored_count = 0
        
        for game_dict in steam_games:
            if 'appid' not in game_dict: continue
            
            appid = game_dict['appid']
            
            full_details = fetch_game_details_from_store(appid)
            
            if not full_details.get('error'):
                app_type = full_details.get('type', '').lower()
                if app_type != 'game':
                    ignored_count += 1
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
                games_to_sync.append(game_data)
            except ValidationError as e:
                print(f"Erro validação Pydantic jogo {appid}: {e}")

        if games_to_sync:
            print(f"Salvando {len(games_to_sync)} jogos no banco...")
            count = game_model.sync_steam_games_batch(user_id, games_to_sync)
            return games_to_sync
        
        return []

    except Exception as e:
        print(f"Erro fatal na sincronização: {e}")
        raise HTTPException(status_code=500, detail=f"Falha interna: {str(e)}")

def fetch_steam_user_profile(steam_id: str) -> dict:
    if not settings.steam_api_key:
        return {}

    API_URL = f"{STEAM_PLAYER_API_URL}/ISteamUser/GetPlayerSummaries/v0002/"
    params = {
        'key': settings.steam_api_key,
        'steamids': steam_id
    }

    try:
        response = requests.get(API_URL, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        players = data.get('response', {}).get('players', [])
        
        if players:
            player = players[0]
            return {
                "personaname": player.get('personaname'),
                "realname": player.get('realname'),
                "avatar": player.get('avatarfull'),
                "profileurl": player.get('profileurl'),
                "loccountrycode": player.get('loccountrycode')
            }
            
        return {}

    except Exception as e:
        print(f"Erro ao buscar perfil do usuário Steam {steam_id}: {e}")
        return {}