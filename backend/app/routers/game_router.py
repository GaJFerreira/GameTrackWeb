from fastapi import APIRouter, HTTPException
from .. import database

router = APIRouter(
    prefix="/games",
    tags=["Jogos"]
)

db = database.db

@router.get("/{user_id}")
def list_games(user_id: str):

    docs = db.collection("users").document(user_id).collection("games").stream()
    return [doc.to_dict() for doc in docs]

@router.post("/{user_id}")
def add_game(user_id: str, game: dict):

    try:
        ref = db.collection("users").document(user_id).collection("games").document()
        ref.set(game)
        return {"message": "Jogo adicionado com sucesso!", "id": ref.id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}/{game_id}")
def update_game(user_id: str, game_id: str, game: dict):

    try:
        ref = db.collection("users").document(user_id).collection("games").document(game_id)
        ref.update(game)
        return {"message": "Jogo atualizado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}/{game_id}")
def delete_game(user_id: str, game_id: str):

    try:
        db.collection("users").document(user_id).collection("games").document(game_id).delete()
        return {"message": "Jogo deletado com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
