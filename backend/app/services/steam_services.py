# app/services/steam_services.py
import requests
import time
from fastapi import HTTPException
from pydantic import ValidationError

from ..config import settings
from ..schemas import game_schema
from ..models import game_model

# URLs da API da Steam
STEAM_PLAYER_API_URL = "http://api.steampowered.com"
STEAM_STORE_API_URL = "https://store.steampowered.com/api/appdetails"


def fetch_game_details_from_store(appid: int) -> dict:
    """
    Busca informações ricas (gênero, descrição, desenvolvedor) da API da Loja Steam.
    """
    # Usamos requests para buscar os detalhes
    params = {
        'appids': appid,
        'filters': 'basic,categories,genres,developers,publishers',
        'cc': 'br',  # Código do país (para garantir que a moeda esteja correta, embora busquemos dados)
        'l': 'brazilian'  # Idioma (Português)
    }

    try:
        # Adiciona um pequeno delay de 0.1 segundo para evitar atingir o limite de requisições da Store API
        time.sleep(0.1)

        response = requests.get(STEAM_STORE_API_URL, params=params, timeout=10)
        response.raise_for_status()

        data = response.json()

        # O Store API retorna um dicionário onde a chave é o AppID (string)
        if str(appid) in data and data[str(appid)].get('success') is True:
            return data[str(appid)].get('data', {})

        return {"error": "Detalhes não encontrados."}

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar detalhes da Loja Steam para {appid}: {e}")
        return {"error": f"Erro de conexão com a Loja Steam."}


def sync_steam_library(user_id: str, steam_id: str) -> list[game_schema.GameBase]:
    """
    Busca os jogos na Steam, enriquece os dados, e salva/atualiza no Firestore.
    """
    print(f"Iniciando sincronização (e enriquecimento) para user_id: {user_id} (SteamID: {steam_id})")

    # 1. BUSCAR JOGOS (API DE POSSES)
    api_key = settings.steam_api_key
    url = (
        f"{STEAM_PLAYER_API_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={api_key}&steamid={steam_id}&format=json"
        f"&include_appinfo=true&include_played_free_games=true"
    )

    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        data = response.json()

        if "response" not in data or "games" not in data["response"]:
            raise HTTPException(
                status_code=404,
                detail="Não foi possível buscar os jogos. O perfil pode ser privado ou o SteamID inválido."
            )

        steam_games_list = data["response"]["games"]
        print(f"API de Posses retornou {len(steam_games_list)} jogos. Iniciando Enriquecimento...")

        # 2. ENRIQUECER, FORMATAR E VALIDAR
        games_to_sync: list[game_schema.GameBase] = []
        for game_dict in steam_games_list:

            # Garante que o appid existe para evitar erro
            if 'appid' not in game_dict:
                continue

            try:
                appid = game_dict['appid']

                # A. CHAMADA PARA ENRIQUECER DADOS
                details = fetch_game_details_from_store(appid)

                # B. Mapeamento dos novos campos para o dicionário do jogo
                if details.get('error'):
                    print(f"Alerta: Falha ao enriquecer jogo {appid}. {details.get('error')}")
                else:
                    # Gêneros: transforma a lista de dicionários em uma string separada por vírgula
                    game_dict['genero'] = ', '.join(
                        [g['description'] for g in details.get('genres', [])]) if details.get('genres') else None

                    # Desenvolvedores/Publishers: lista de strings em uma única string
                    game_dict['desenvolvedor'] = ', '.join(details.get('developers', [])) if details.get(
                        'developers') else None
                    game_dict['publisher'] = ', '.join(details.get('publishers', [])) if details.get(
                        'publishers') else None

                    # Descrição: Pega a descrição curta
                    game_dict['descricao'] = details.get('short_description', None)

                # C. Validação e Formatação (uso do Schema)
                # O **game_dict transforma o dicionário em um objeto GameBase
                game_data = game_schema.GameBase(**game_dict)
                games_to_sync.append(game_data)

            except ValidationError as e:
                print(f"Falha ao validar/formatar jogo {appid}: {e}")
            except Exception as e:
                print(f"Erro inesperado durante o loop de enriquecimento para {appid}: {e}")

        # 3. SALVAR DADOS NO FIREBASE (usando o Model em lote)
        if not games_to_sync:
            print("Nenhum jogo válido para sincronizar.")
            return []

        print(f"Enviando {len(games_to_sync)} jogos validados para o banco...")

        # Chamamos a função de model para salvar em lote
        saved_count = game_model.sync_steam_games_batch(user_id, games_to_sync)

        print(f"Sincronização concluída. {saved_count} jogos salvos/atualizados.")
        return games_to_sync

    except requests.exceptions.Timeout:
        raise HTTPException(status_code=408, detail="A requisição para a API da Steam demorou muito.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar API da Steam: {e}")
        raise HTTPException(status_code=503, detail="Erro ao comunicar com a API da Steam.")
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        print(f"Erro inesperado no serviço Steam: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno no servidor: {e}")