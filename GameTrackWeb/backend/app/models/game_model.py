# app/models/game_model.py
from ..database import db
from ..schemas.game_schema import GameBase, GameUpdate
from typing import List

def sync_steam_games_batch(user_id: str, games_list: List[GameBase]):
    try:
        batch = db.batch()

        games_collection_ref = db.collection("users").document(user_id).collection("games")

        for game_data in games_list:
            game_dict = game_data.model_dump()
            doc_ref = games_collection_ref.document(str(game_data.appid))

            batch.set(doc_ref, game_dict, merge=True)

        batch.commit()
        return len(games_list)

    except Exception as e:
        print(f"Erro ao salvar jogos em lote para {user_id}: {e}")
        return 0

def get_user_games(user_id: str):

    try:
        games_ref = db.collection("users").document(user_id).collection("games")
        docs = games_ref.stream()

        games_list = []
        for doc in docs:
            games_list.append(doc.to_dict())

        return games_list
    except Exception as e:
        print(f"Erro ao buscar jogos para {user_id}: {e}")
        return []

def update_user_game(user_id: str, appid: int, game_update_data: GameUpdate):

    try:
        doc_ref = db.collection("users").document(user_id).collection("games").document(str(appid))

        update_data = game_update_data.model_dump(exclude_unset=True)

        if not update_data:
            return None

        doc_ref.update(update_data)
        return update_data
    except Exception as e:
        print(f"Erro ao atualizar jogo {appid} para {user_id}: {e}")
        return None