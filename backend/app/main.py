# app/main.py
# (Remova o 'import uvicorn' se ainda estiver lá, não precisamos mais dele aqui)
from fastapi import FastAPI
from . import database
from .routers import steam_router

app = FastAPI(title="GameTrack API") # Adicionando um título para a documentação
db = database.db

# Registramos o router da Steam na nossa aplicação principal.
# O prefix="/api" faz com que todas as rotas definidas no steam_router
# (que já tinham prefixo /steam) fiquem acessíveis em /api/steam/...
app.include_router(steam_router.router, prefix="/api") # <-- Registro do novo router

# ---- Rotas de Teste (podem continuar aqui ou serem movidas para seus próprios routers depois) ----
@app.get("/")
def read_root():
    return {"message": "API do GameTrack (Estruturada) está online!"}

@app.get("/api/test-firebase")
def test_firebase_connection():
    try:
        doc_ref = db.collection("test_collection").document("test_doc")
        doc_ref.set({"message": "Conexão com Firebase bem-sucedida!"})
        return {"status": "success", "message": "Dados escritos no Firebase!"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Não precisamos mais do 'if __name__ == "__main__":' aqui