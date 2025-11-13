# app/services/user_service.py (Versão Final Corrigida)
import uuid
from fastapi import HTTPException
from ..schemas.user_schema import UserCreate, User
from ..models import user_model
from .steam_services import sync_steam_library


def create_user_and_sync_steam(user_data: UserCreate) -> dict:
    """
    Orquestra o registro, cria um UID, salva o usuário completo e dispara a sincronização.
    """

    # 1. SIMULAR AUTENTICAÇÃO E GERAÇÃO DE UID (TESTE)
    new_user_id = str(uuid.uuid4())

    # 2. CONSTRUIR O OBJETO FINAL User
    user_dict = user_data.model_dump()
    user_dict['id'] = new_user_id
    user_to_save = User(**user_dict)

    # 3. SALVAR DADOS DO USUÁRIO NO BANCO
    user_created = user_model.create_user(new_user_id, user_to_save)

    if not user_created:
        raise HTTPException(status_code=500, detail="Falha ao criar o registro do usuário no banco.")

    print(f"Usuário criado com ID: {new_user_id}. Iniciando sincronização Steam...")

    # 4. SINCRONIZAR JOGOS DA STEAM AUTOMATICAMENTE
    sync_status_message = "Sincronização concluída com sucesso."
    synced_games_count = 0
    try:
        # Tenta sincronizar. Retorna a lista de Pydantic Models se for sucesso.
        synced_games_list = sync_steam_library(new_user_id, user_data.steam_id)

        # SUCESSO
        synced_games_count = len(synced_games_list)
        sync_status_message = f"Sincronização concluída com {synced_games_count} jogos."

    except HTTPException as e:
        # FALHA - Captura o erro detalhado (perfil privado, etc.)
        sync_status_message = f"Sincronização falhou: {e.detail}"
        print(f"Alerta: {sync_status_message}")

    # 5. RETORNAR O RESULTADO FINAL
    # Usamos o .model_dump() para garantir que o Pydantic seja serializado corretamente.
    return {
        "user": user_to_save.model_dump(),
        "user_id_gerado": new_user_id,
        "game_count": synced_games_count,
        "sync_status": sync_status_message
    }