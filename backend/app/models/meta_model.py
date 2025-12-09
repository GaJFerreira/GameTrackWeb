from .. import database
from ..utils.steam_achievements import fetch_player_achievements, fetch_total_achievements

db = database.db


class MetaModel:

    @staticmethod
    def create_meta(user_id: str, meta_data: dict) -> str:
        ref = db.collection("users").document(user_id).collection("metas").document()
        ref.set(meta_data)
        return ref.id

    @staticmethod
    def update_meta(user_id: str, meta_id: str, meta_data: dict):
        ref = db.collection("users").document(user_id).collection("metas").document(meta_id)
        ref.update(meta_data)

    @staticmethod
    def delete_meta(user_id: str, meta_id: str):
        db.collection("users").document(user_id).collection("metas").document(meta_id).delete()

    @staticmethod
    def list_metas(user_id: str):
        metas = db.collection("users").document(user_id).collection("metas").stream()
        return [{**m.to_dict(), "id": m.id} for m in metas]

    @staticmethod
    def update_one_meta(user_id: str, meta_id: str, meta_data: dict):
        ref = db.collection("users").document(user_id).collection("metas").document(meta_id)
        ref.update(meta_data)

    @staticmethod
    def update_goals(user_id: str):
        metas = MetaModel.list_metas(user_id)

        for meta in metas:

            meta_id = meta["id"]
            tipo = meta.get("tipo", "").upper()

            # =====================================================
            #                   META DE TEMPO
            # =====================================================
            if tipo == "TEMPO":

                # Agora usa game_name (igual a conclusão)
                game_name = meta.get("game_name")

                if not game_name:
                    print(f"[Meta] Meta '{meta_id}' TEMPO sem game_name.")
                    continue

                # Buscar objetivo (ex.: "Chegar a 150 horas")
                objetivo_raw = meta.get("valor_meta") or ""
                try:
                    objetivo_horas = int("".join(filter(str.isdigit, objetivo_raw)))
                except:
                    print(f"[Meta] Erro ao interpretar objetivo: {objetivo_raw}")
                    continue

                # Buscar jogo pelo nome
                game_ref = (
                    db.collection("users")
                    .document(user_id)
                    .collection("games")
                    .where("name", "==", game_name)
                    .get()
                )

                if not game_ref:
                    print(f"[Meta] Jogo '{game_name}' não encontrado para TEMPO.")
                    continue

                game_data = game_ref[0].to_dict()
                horas_atual = int(game_data.get("horas_jogadas", 0))

                progresso_str = f"{horas_atual}h de {objetivo_horas}h"
                percentual = min(100, round((horas_atual / objetivo_horas) * 100, 2))

                MetaModel.update_one_meta(
                    user_id,
                    meta_id,
                    {
                        "progresso_atual": progresso_str,
                        "percentual": percentual,
                    },
                )

                if horas_atual >= objetivo_horas:
                    MetaModel.update_one_meta(user_id, meta_id, {"status": "CONCLUIDA"})
                    print(f"[Meta] Meta '{meta_id}' concluída!")
                else:
                    MetaModel.update_one_meta(user_id, meta_id, {"status": "EM ANDAMENTO"})

            # =====================================================
            #            META DE CONCLUSÃO / PLATINAR
            # =====================================================
            elif tipo == "CONCLUSAO":

                game_name = meta.get("game_name")

                if not game_name:
                    print(f"[Meta] Meta '{meta_id}' CONCLUSAO sem game_name.")
                    continue

                # Buscar steam_id
                user_doc = db.collection("users").document(user_id).get()
                steam_id = user_doc.to_dict().get("steam_id")

                if not steam_id:
                    print("[Meta] Usuário sem steam_id cadastrado.")
                    continue

                # Buscar jogo pelo nome
                game_ref = (
                    db.collection("users")
                    .document(user_id)
                    .collection("games")
                    .where("name", "==", game_name)
                    .get()
                )

                if not game_ref:
                    print(f"[Meta] Jogo '{game_name}' não encontrado para CONCLUSAO.")
                    continue

                game_data = game_ref[0].to_dict()
                appid = game_data.get("appid")

                if not appid:
                    print(f"[Meta] Jogo '{game_name}' sem appid.")
                    continue

                # Buscar conquistas
                obtidas = fetch_player_achievements(steam_id, appid)
                totais = fetch_total_achievements(appid)

                progresso = f"{obtidas}/{totais}"

                if totais > 0:
                    percentual = min(100, round((obtidas / totais) * 100, 2))
                else:
                    percentual = 0

                MetaModel.update_one_meta(
                    user_id,
                    meta_id,
                    {
                        "progresso_atual": progresso,
                        "percentual": percentual,
                    },
                )

                if totais > 0 and obtidas >= totais:
                    MetaModel.update_one_meta(user_id, meta_id, {"status": "CONCLUIDA"})
                    print(f"[Meta] Meta '{meta_id}' PLATINADA!")
                else:
                    MetaModel.update_one_meta(user_id, meta_id, {"status": "EM_ANDAMENTO"})
                    print(f"[Meta] Meta '{meta_id}' ainda não platinada ({progresso}).")
