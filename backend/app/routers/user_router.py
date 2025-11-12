from fastapi import APIRouter, HTTPException, Path
from .. import database

router = APIRouter(
    prefix="/users",
    tags=["Usuários"]
)

db = database.db

@router.post("/register/{user_id}")
def register_user(user_id: str, payload: dict):

    try:
        doc_ref = db.collection("users").document(user_id)
        doc_ref.set(payload, merge=True)
        return {"message": "Usuário registrado com sucesso!", "data": payload}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao registrar usuário: {e}")

@router.get("/{user_id}")
def get_user(user_id: str):

    doc = db.collection("users").document(user_id).get()
    if not doc.exists:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return doc.to_dict()
