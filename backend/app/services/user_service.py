import uuid
from typing import List
from fastapi import HTTPException
from ..schemas.user_schema import UserCreate, User
from ..models import user_model
from .steam_services import fetch_steam_user_profile

def register_user_db(user_data: UserCreate, user_id_firebase: str = None) -> dict:

    if user_id_firebase:
        new_user_id = user_id_firebase
    else:
        new_user_id = str(uuid.uuid4())   
    
    user_dict = user_data.model_dump()
    user_dict['id'] = new_user_id 

    print(f"Buscando perfil Steam básico para {user_data.steam_id}...")
    steam_profile_data = fetch_steam_user_profile(user_data.steam_id)
    
    if steam_profile_data:
        user_dict.update(steam_profile_data)
    
    user_to_save = User(**user_dict)     
    user_created = user_model.create_user(new_user_id, user_to_save)
    
    if not user_created:
        raise HTTPException(status_code=500, detail="Falha ao criar registro no banco.")

    return {
        "user": user_to_save.model_dump(),
        "user_id_gerado": new_user_id,
        "message": "Usuário registrado. A sincronização de jogos começou em segundo plano."
    }

def get_all_users() -> List[User]:
    users_data = user_model.get_all_users()
    return [User(**data) for data in users_data]

def get_user(user_id: str) -> User | None:
    user_data = user_model.get_user(user_id)
    if not user_data:
        return None
    return User(**user_data)