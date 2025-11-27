import uuid
from typing import List
from fastapi import HTTPException

from ..schemas.user_schema import UserCreate, User
from ..models import user_model
from .steam_services import SteamService


def create_user_and_sync_steam(user_data: UserCreate) -> dict:
    # gera novo ID do usuário
    new_user_id = str(uuid.uuid4())

    user_dict = user_data.model_dump()
    user_dict["id"] = new_user_id

    # instancia o service correto
    steam = SteamService()

    # busca perfil via API da Steam
    print(f"Buscando dados do perfil Steam para {user_data.steam_id}...")
    steam_profile = steam.fetch_steam_user_profile(user_data.steam_id)

    if steam_profile:
        print(f"Perfil encontrado: {steam_profile.get('personaname')}")
        user_dict.update(steam_profile)
    else:
        print("Aviso: Não foi possível buscar perfil da Steam (ID privado ou inválido).")

    # salva o usuário no banco
    user_to_save = User(**user_dict)
    user_created = user_model.create_user(new_user_id, user_to_save)

    if not user_created:
        raise HTTPException(
            status_code=500,
            detail="Falha ao criar o registro do usuário no banco."
        )

    print(f"Usuário criado com ID: {new_user_id}. Iniciando sincronização de jogos...")

    sync_status_message = "Sincronização iniciada."
    synced_games_count = 0

    # sincronização dos jogos com tratamento de erro
    try:
        synced_games = steam.sync_steam_library(new_user_id, user_data.steam_id)
        synced_games_count = len(synced_games)
        sync_status_message = f"Sincronização concluída com {synced_games_count} jogos."
    except Exception as e:
        sync_status_message = f"Sincronização falhou: {e}"
        print(f"Alerta: {sync_status_message}")

    return {
        "user": user_to_save.model_dump(),
        "user_id_gerado": new_user_id,
        "game_count": synced_games_count,
        "sync_status": sync_status_message
    }


def get_all_users() -> List[User]:
    users_data = user_model.get_all_users()
    return [User(**data) for data in users_data]


def get_user(user_id: int) -> User | None:
    user_data = user_model.get_user(user_id)
    if not user_data:
        return None
    return User(**user_data)
