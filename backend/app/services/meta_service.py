from .steam_services import sync_steam_library
from ..models import meta_model
from ..schemas.meta_schema import MetaStatus, MetaTipo

def processar_metas_de_usuario(user_id: str, steam_id: str):
    

    jogos = sync_steam_library(user_id, steam_id)
    metas = meta_model.list_metas(user_id)

    horas = {}
    for g in jogos:
        horas[g.appid] = g.horas_jogadas

    for meta in metas:
        meta_id = meta["id"]
        tipo = meta["tipo"]
        valor = meta["valor_meta"]
        progresso_atual = float(meta.get("progresso_atual", "0"))
        status = meta["status"]

        if status == MetaStatus.concluida.value:
            continue

        if tipo == MetaTipo.tempo.value:
            appid, horas_necessarias = valor.split(":")
            horas_necessarias = float(horas_necessarias)

            jogado = horas.get(int(appid), 0)

            meta_model.atualizar_progresso(user_id, meta_id, str(jogado))

            if jogado >= horas_necessarias:
                meta_model.marcar_meta_concluida(user_id, meta_id)

        elif tipo == MetaTipo.conclusao.value:
            appid = int(valor)
            jogado = horas.get(appid, 0)

            if jogado > 0:  
                meta_model.marcar_meta_concluida(user_id, meta_id)
