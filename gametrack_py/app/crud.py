from sqlalchemy.orm import Session
from sqlalchemy import select
from . import models, schemas
from .auth import get_password_hash

# Usuarios
def create_usuario(db: Session, data: schemas.UsuarioCreate) -> models.Usuario:
    user = models.Usuario(
        nome=data.nome,
        email=data.email,
        senha_hash=get_password_hash(data.senha),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_usuario_by_email(db: Session, email: str):
    return db.execute(select(models.Usuario).where(models.Usuario.email == email)).scalar_one_or_none()

# Jogos
def create_jogo(db: Session, owner_id: int, data: schemas.JogoCreate) -> models.Jogo:
    jogo = models.Jogo(
        titulo=data.titulo,
        plataforma=data.plataforma,
        horas_jogadas=data.horas_jogadas,
        status=data.status,
        owner_id=owner_id,
    )
    db.add(jogo)
    db.commit()
    db.refresh(jogo)
    return jogo

def list_jogos(db: Session, owner_id: int):
    return db.query(models.Jogo).filter(models.Jogo.owner_id == owner_id).all()

def get_jogo(db: Session, owner_id: int, jogo_id: int):
    return db.query(models.Jogo).filter(models.Jogo.owner_id == owner_id, models.Jogo.id == jogo_id).first()

def update_jogo(db: Session, owner_id: int, jogo_id: int, data: schemas.JogoUpdate):
    jogo = get_jogo(db, owner_id, jogo_id)
    if not jogo:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(jogo, field, value)
    db.commit()
    db.refresh(jogo)
    return jogo

def delete_jogo(db: Session, owner_id: int, jogo_id: int) -> bool:
    jogo = get_jogo(db, owner_id, jogo_id)
    if not jogo:
        return False
    db.delete(jogo)
    db.commit()
    return True

# Metas
def create_meta(db: Session, owner_id: int, data: schemas.MetaCreate) -> models.Meta:
    meta = models.Meta(
        descricao=data.descricao,
        concluida=data.concluida,
        data_limite=data.data_limite,
        jogo_id=data.jogo_id,
        owner_id=owner_id,
    )
    db.add(meta)
    db.commit()
    db.refresh(meta)
    return meta

def list_metas(db: Session, owner_id: int):
    return db.query(models.Meta).filter(models.Meta.owner_id == owner_id).all()

def get_meta(db: Session, owner_id: int, meta_id: int):
    return db.query(models.Meta).filter(models.Meta.owner_id == owner_id, models.Meta.id == meta_id).first()

def update_meta(db: Session, owner_id: int, meta_id: int, data: schemas.MetaUpdate):
    meta = get_meta(db, owner_id, meta_id)
    if not meta:
        return None
    for field, value in data.dict(exclude_unset=True).items():
        setattr(meta, field, value)
    db.commit()
    db.refresh(meta)
    return meta

def delete_meta(db: Session, owner_id: int, meta_id: int) -> bool:
    meta = get_meta(db, owner_id, meta_id)
    if not meta:
        return False
    db.delete(meta)
    db.commit()
    return True
