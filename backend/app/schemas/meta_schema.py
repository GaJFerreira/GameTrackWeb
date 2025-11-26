from pydantic import BaseModel
from typing import Optional
from enum import Enum

class MetaTipo(str, Enum):
    tempo = "TEMPO"
    conclusao = "CONCLUSAO"

class MetaStatus(str, Enum):
    em_andamento = "EM_ANDAMENTO"
    concluida = "CONCLUIDA"
    expirada = "EXPIRADA"

class MetaBase(BaseModel):

    tipo: MetaTipo = MetaTipo.conclusao
    valor_meta: Optional[str] = None
    progresso_atual: Optional[str] = "0"
    data_limite: Optional[str] = None
    status: MetaStatus = MetaStatus.em_andamento

class MetaCreate(MetaBase):
    pass

class Meta(MetaBase):
    id: str
    class Config:
        from_attributes = True
        use_enum_values = True