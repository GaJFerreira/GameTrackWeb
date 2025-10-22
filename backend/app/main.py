import uvicorn
from fastapi import FastAPI
from . import database  # <-- MUDANÇA AQUI

app = FastAPI()
db = database.db

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

# O 'if __name__' não será mais usado para rodar
# Vamos corrigir a forma de rodar no Passo 5