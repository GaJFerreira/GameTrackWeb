from datetime import date
from pydantic import BaseModel, EmailStr
from typing import Optional, List

class UsuarioCreate(BaseModel):
    nome: str
    email: EmailStr
    senha: str

class UsuarioOut(BaseModel):
    id: int
    nome: str
    email: EmailStr
    class Config:
        from_attributes = True

class JogoBase(BaseModel):
    titulo: str
    plataforma: Optional[str] = None
    horas_jogadas: int = 0
    status: str = "Backlog"

class JogoCreate(JogoBase):
    pass

class JogoUpdate(BaseModel):
    titulo: Optional[str] = None
    plataforma: Optional[str] = None
    horas_jogadas: Optional[int] = None
    status: Optional[str] = None

class JogoOut(JogoBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True

class MetaBase(BaseModel):
    descricao: str
    concluida: bool = False
    data_limite: Optional[date] = None
    jogo_id: Optional[int] = None

class MetaCreate(MetaBase):
    pass

class MetaUpdate(BaseModel):
    descricao: Optional[str] = None
    concluida: Optional[bool] = None
    data_limite: Optional[date] = None
    jogo_id: Optional[int] = None

class MetaOut(MetaBase):
    id: int
    owner_id: int
    class Config:
        from_attributes = True
