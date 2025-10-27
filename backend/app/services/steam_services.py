# app/services/steam_service.py
import requests # Biblioteca para fazer chamadas HTTP
from fastapi import HTTPException # Para retornar erros HTTP padronizados
from ..config import settings # Para pegar nossa chave da API Steam

# URL base da API da Steam que vamos usar
STEAM_API_BASE_URL = "http://api.steampowered.com"

def get_owned_games(steam_id: str):
    """
    Esta função recebe um SteamID64 e busca os jogos da pessoa na API da Steam.
    """
    print(f"Buscando jogos para o SteamID: {steam_id}") # Log para vermos no terminal

    # Pegamos a chave da API que carregamos do .env através do config.py
    api_key = settings.steam_api_key

    # Montamos a URL completa da API da Steam
    # Documentação: https://developer.valvesoftware.com/wiki/Steam_Web_API#GetOwnedGames_.28v0001.29
    url = (
        f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v1/"
        f"?key={api_key}"
        f"&steamid={steam_id}"
        f"&format=json"
        f"&include_appinfo=true" # Pede para incluir nome e ícones dos jogos
        f"&include_played_free_games=true" # Pede para incluir jogos gratuitos
    )

    try:
        # Fazemos a chamada GET para a URL da Steam
        # timeout=15 define um limite de 15 segundos para a resposta
        response = requests.get(url, timeout=15)

        # Verifica se a resposta da Steam foi um erro (ex: 404 Não Encontrado, 500 Erro Interno)
        response.raise_for_status()

        # Se chegou aqui, a chamada deu certo (status 200 OK)
        # Pegamos o conteúdo da resposta em formato JSON (um dicionário Python)
        data = response.json()

        # Verificamos se a estrutura da resposta é a esperada
        # A API da Steam retorna um objeto 'response' que contém a lista 'games'
        if "response" not in data or "games" not in data["response"]:
            # Se não encontrar 'games', pode ser um perfil privado ou ID inválido
            # Usamos HTTPException para mandar um erro 404 de volta para o usuário
            print(f"Resposta da Steam não contém 'games' para {steam_id}. Perfil privado?")
            raise HTTPException(
                status_code=404,
                detail="Não foi possível buscar os jogos. O perfil pode ser privado ou o SteamID inválido."
            )

        # Se tudo deu certo, retornamos APENAS a lista de jogos
        games_list = data["response"]["games"]
        print(f"Encontrados {len(games_list)} jogos para {steam_id}")
        return games_list

    # Tratamento de Erros Específicos do 'requests'
    except requests.exceptions.Timeout:
        print(f"Timeout ao buscar jogos para {steam_id}")
        raise HTTPException(status_code=408, detail="A requisição para a API da Steam demorou muito (timeout).")
    except requests.exceptions.RequestException as e:
        # Erros gerais de conexão ou HTTP que não foram tratados pelo raise_for_status
        print(f"Erro de rede/HTTP ao chamar API da Steam para {steam_id}: {e}")
        raise HTTPException(status_code=503, detail=f"Erro ao comunicar com a API da Steam: {e}")
    except Exception as e:
        # Qualquer outro erro inesperado durante o processo
        print(f"Erro inesperado no steam_service para {steam_id}: {e}")
        raise HTTPException(status_code=500, detail="Ocorreu um erro interno inesperado ao buscar jogos da Steam.")