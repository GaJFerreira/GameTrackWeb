# app/models/game_model.py
from ..database import db
from ..schemas.game_schema import GameBase, GameUpdate
from typing import List

def sync_steam_games_batch(user_id: str, games_list: List[GameBase]):
    if not games_list:
        return 0

    try:
        batch = db.batch()
        games_collection_ref = db.collection("users").document(user_id).collection("games")

        # 1. OTIMIZAÇÃO: Busca todos os documentos de uma vez
        doc_refs = [games_collection_ref.document(str(g.appid)) for g in games_list]
        snapshots_list = db.get_all(doc_refs)

        # 2. SEGURANÇA DE ID: Cria um Mapa { "730": snapshot, "123": snapshot }
        # Isso impede que o 'zip' misture a ordem dos jogos.
        snapshots_map = {snap.id: snap for snap in snapshots_list}

        # Campos que JAMAIS devem ser sobrescritos se o jogo já existir
        campos_proibidos_update = {
            "status", 
            "nota_pessoal", 
            "interesse", 
            "data_compra", 
            "tipo_cadastro",
            "review", 
            "tags",
            "notas_pessoais", 
            "categorias_usuario"
        }

        count = 0
        
        # Iteramos sobre a LISTA ORIGINAL (que tem os dados corretos da Steam)
        for game_data in games_list:
            str_id = str(game_data.appid)
            
            # Buscamos o snapshot correspondente no mapa pelo ID
            snapshot = snapshots_map.get(str_id)

            # Define a referência do documento (garantia absoluta de ID correto)
            doc_ref = games_collection_ref.document(str_id)

            # Verifica se o snapshot existe e é válido
            existe_no_banco = snapshot is not None and snapshot.exists

            if existe_no_banco:
                # --- CENÁRIO: UPDATE SEGURO ---
                
                update_payload = game_data.model_dump()
                
                # Removemos chaves proibidas para não zerar dados do usuário
                keys_to_remove = [k for k in update_payload if k in campos_proibidos_update]
                for k in keys_to_remove:
                    del update_payload[k]

                # Debug opcional no primeiro item
                if count == 0:
                    print(f"[UPDATE] Jogo: {game_data.name} | ID: {str_id}")
                    # print(f"   -> Mantendo dados do usuário. Atualizando apenas Steam.")

                # batch.update só altera os campos enviados
                batch.update(doc_ref, update_payload)

            else:
                # --- CENÁRIO: CREATE (JOGO NOVO) ---
                
                full_payload = game_data.model_dump()
                
                # Garante valor padrão se estiver vazio
                if "status" not in full_payload or not full_payload["status"]:
                    full_payload["status"] = "Não Iniciado"
                
                print(f"[NOVO] Criando: {game_data.name} | ID: {str_id}")
                
                # batch.set cria o documento do zero
                batch.set(doc_ref, full_payload)

            count += 1

        batch.commit()
        print(f"Sincronização finalizada. {count} jogos processados.")
        return count

    except Exception as e:
        print(f"Erro CRÍTICO ao salvar jogos em lote: {e}")
        return 0

def get_user_games(user_id: str):
    try:
        games_ref = db.collection("users").document(user_id).collection("games")
        docs = games_ref.stream()

        games_list = []
        for doc in docs:
            # Adicionamos o ID no dicionário para garantir que o frontend tenha acesso fácil
            game_dict = doc.to_dict()
            game_dict['appid'] = doc.id 
            games_list.append(game_dict)

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