# app/main.py
from fastapi import FastAPI
from . import database
from .routers import steam_router, user_router, game_router, meta_router

app = FastAPI(title="GameTrack API")
db = database.db

# Rotas registradas
app.include_router(steam_router.router, prefix="/api")
app.include_router(user_router.router, prefix="/api")
app.include_router(game_router.router, prefix="/api")
app.include_router(meta_router.router, prefix="/api")

# Rota raiz
@app.get("/")
def read_root():
    return {"message": "API do GameTrack (Estruturada) está online!"}

# Teste Firebase
@app.get("/api/test-firebase")
def test_firebase_connection():
    try:
        doc_ref = db.collection("test_collection").document("test_doc")
        doc_ref.set({"message": "Conexão com Firebase bem-sucedida!"})
        return {"status": "success", "message": "Dados escritos no Firebase!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
