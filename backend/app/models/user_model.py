from ..database import db # Nossa conexão com o Firebase
from ..schemas.user_schema import UserCreate

def create_user(user_id: str, user_data: UserCreate):
    """
    Cria um novo documento de usuário no Firestore.
    Isso é separado da Autenticação do Firebase.
    """
    try:
        # Caminho no banco: /users/{user_id}
        user_ref = db.collection("users").document(user_id)
        user_ref.set(user_data.model_dump())
        return user_data
    except Exception as e:
        print(f"Erro ao criar usuário no Firestore: {e}")
        return None

def get_user(user_id: str):
    """
    Busca os dados de um usuário no Firestore.
    """
    try:
        user_ref = db.collection("users").document(user_id)
        user_doc = user_ref.get()
        if user_doc.exists:
            return user_doc.to_dict()
        return None
    except Exception as e:
        print(f"Erro ao buscar usuário {user_id}: {e}")
        return None