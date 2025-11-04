from datetime import timedelta
from fastapi import FastAPI, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas, crud
from .auth import create_access_token, verify_password, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

app = FastAPI(title="GameTrack API (Python)")

# Cria tabelas
Base.metadata.create_all(bind=engine)

@app.get("/", tags=["root"])
def root():
    return {"ok": True, "name": "GameTrack API (Python/FastAPI)"}

# ---------- AUTH ----------
@app.post("/auth/register", response_model=schemas.UsuarioOut, tags=["auth"])
def register(user: schemas.UsuarioCreate, db: Session = Depends(get_db)):
    if crud.get_usuario_by_email(db, user.email):
        raise HTTPException(status_code=400, detail="Email já cadastrado")
    created = crud.create_usuario(db, user)
    return created

@app.post("/auth/login", tags=["auth"])
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_usuario_by_email(db, form_data.username)
    if not user or not verify_password(form_data.password, user.senha_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Login inválido")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(data={"sub": str(user.id)}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}

# ---------- JOGOS ----------
@app.get("/jogos/", response_model=list[schemas.JogoOut], tags=["jogos"])
def list_jogos(db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    return crud.list_jogos(db, current_user.id)

@app.post("/jogos/", response_model=schemas.JogoOut, tags=["jogos"])
def create_jogo(payload: schemas.JogoCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    return crud.create_jogo(db, current_user.id, payload)

@app.put("/jogos/{jogo_id}", response_model=schemas.JogoOut, tags=["jogos"])
def update_jogo(jogo_id: int, payload: schemas.JogoUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    j = crud.update_jogo(db, current_user.id, jogo_id, payload)
    if not j:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return j

@app.delete("/jogos/{jogo_id}", tags=["jogos"])
def delete_jogo(jogo_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    ok = crud.delete_jogo(db, current_user.id, jogo_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Jogo não encontrado")
    return {"deleted": True}

# ---------- METAS ----------
@app.get("/metas/", response_model=list[schemas.MetaOut], tags=["metas"])
def list_metas(db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    return crud.list_metas(db, current_user.id)

@app.post("/metas/", response_model=schemas.MetaOut, tags=["metas"])
def create_meta(payload: schemas.MetaCreate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    return crud.create_meta(db, current_user.id, payload)

@app.put("/metas/{meta_id}", response_model=schemas.MetaOut, tags=["metas"])
def update_meta(meta_id: int, payload: schemas.MetaUpdate, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    m = crud.update_meta(db, current_user.id, meta_id, payload)
    if not m:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    return m

@app.delete("/metas/{meta_id}", tags=["metas"])
def delete_meta(meta_id: int, db: Session = Depends(get_db), current_user: models.Usuario = Depends(get_current_user)):
    ok = crud.delete_meta(db, current_user.id, meta_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Meta não encontrada")
    return {"deleted": True}

from .auth import get_current_user
from . import models

@app.get("/auth/me", response_model=schemas.UsuarioOut, tags=["auth"])
def me(current_user: models.Usuario = Depends(get_current_user)):
    return current_user
