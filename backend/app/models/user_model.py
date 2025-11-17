from typing import List, Dict, Optional

from ..database import db # Nossa conexão com o Firebase
from ..schemas.user_schema import UserCreate

def create_user(user_id: str, user_data: UserCreate):

    try:
        user_ref = db.collection("users").document(user_id)
        user_ref.set(user_data.model_dump())
        return user_data
    except Exception as e:
        print(f"Erro ao criar usuário no Firestore: {e}")
        return None


def get_all_users() -> List[Dict]:

    try:
        docs = db.collection("users").stream()

        users_data = []
        for doc in docs:
            user_dict = doc.to_dict()
            user_dict['id'] = doc.id
            users_data.append(user_dict)

        return users_data

    except Exception as e:
        print(f"Erro ao buscar usuarios no Firestore: {e}")
        return []


def get_user(user_id: str) -> Optional[Dict]:

    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()

        if user_doc.exists:
            user_data = user_doc.to_dict()
            user_data['id'] = user_doc.id
            return user_data

        return None  # Usuário não encontrado

    except Exception as e:
        print(f"Erro ao buscar usuário {user_id}: {e}")
        return None

    except Exception as e:
        print(f"Erro ao buscar usuário {user_id}: {e}")
        return None