# app/services/steam_services.py
import requests
from fastapi import HTTPException
from pydantic import ValidationError # Para capturar erros de validação

# Nossas novas importações
from ..config import settings
from ..models import game_model  # Importa o "trabalhador" do banco
from ..schemas import game_schema # Importa os "moldes"

STEAM_API_BASE_URL = "http://api.steampowered.com"

def sync_steam_library(user_id: str, steam_id: str):
    """
    Busca os jogos na Steam E salva/atualiza no nosso banco de dados.
    """

    # 1. BUSCAR DADOS DA API DA STEAM (igual a antes)
    print(f"Iniciando sincronização para user_id: {user_id} (SteamID: {steam_id})")
    api_key = settings.steam_api_key
    url = (
        f"{STEAM_API_BASE_URL}/IPlayerService/GetOwnedGames/v1/"
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
        print(f"Steam API retornou {len(steam_games_list)} jogos.")

        # 2. FORMATAR DADOS USANDO NOSSO "SCHEMA"
        games_to_sync: list[game_schema.GameBase] = []
        for game_dict in steam_games_list:
            try:
                # A API da Steam às vezes manda campos com nomes errados
                # Vamos garantir que os campos principais existam
                game_dict['name'] = game_dict.get('name', 'Nome Desconhecido')
                game_dict['playtime_forever'] = game_dict.get('playtime_forever', 0)

                # Usamos nosso "molde" GameBase para validar e formatar
                # os dados brutos vindos da Steam.
                # Isso automaticamente adiciona nossos campos padrão
                # (status: "Não Jogado", tipo_cadastro: "Steam", etc.)
                game_data = game_schema.GameBase(**game_dict)
                games_to_sync.append(game_data)

            except ValidationError as e:
                # Se um jogo falhar na validação (ex: appid faltando),
                # registramos o erro e continuamos para os outros.
                print(f"Falha ao validar jogo {game_dict.get('appid', '??')}: {e}")

        # 3. SALVAR DADOS NO FIREBASE (usando nosso "Model")
        if not games_to_sync:
             print("Nenhum jogo válido para sincronizar.")
             return []

        print(f"Enviando {len(games_to_sync)} jogos validados para o banco...")

        # Chamamos nossa nova função do game_model para salvar em lote
        saved_count = game_model.sync_steam_games_batch(user_id, games_to_sync)

        print(f"Sincronização concluída. {saved_count} jogos salvos/atualizados para {user_id}.")
        return games_to_sync # Retorna a lista de jogos que foram sincronizados

    # Tratamento de erros (igual a antes)
    except requests.exceptions.Timeout:
         raise HTTPException(status_code=408, detail="A requisição para a API da Steam demorou muito.")
    except requests.exceptions.RequestException as e:
        print(f"Erro ao chamar API da Steam: {e}")
        raise HTTPException(status_code=503, detail="Erro ao comunicar com a API da Steam.")
    except HTTPException as http_exc:
        raise http_exc # Re-lança a exceção de perfil privado
    except Exception as e:
        print(f"Erro inesperado no serviço Steam: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno no servidor: {e}")