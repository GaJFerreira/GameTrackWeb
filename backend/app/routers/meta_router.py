from fastapi import APIRouter, HTTPException
from .. import database

router = APIRouter(
    prefix="/metas",
    tags=["Metas"]
)

db = database.db

@router.get("/{user_id}")
def list_metas(user_id: str):
    metas = db.collection("users").document(user_id).collection("metas").stream()
    return [m.to_dict() for m in metas]

@router.post("/{user_id}")
def create_meta(user_id: str, meta: dict):
    try:
        ref = db.collection("users").document(user_id).collection("metas").document()
        
        meta['id'] = ref.id 
       
        ref.set(meta)
        return meta 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.put("/{user_id}/{meta_id}")
def update_meta(user_id: str, meta_id: str, meta: dict):
    try:
        ref = db.collection("users").document(user_id).collection("metas").document(meta_id)
        ref.update(meta)
        return {"message": "Meta atualizada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{user_id}/{meta_id}")
def delete_meta(user_id: str, meta_id: str):
    try:
        db.collection("users").document(user_id).collection("metas").document(meta_id).delete()
        return {"message": "Meta deletada com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
