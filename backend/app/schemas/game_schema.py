from pydantic import BaseModel
from typing import Optional
from enum import Enum

class GameStatus(str, Enum):
    nao_iniciado = "Não Iniciado"
    jogando = "Jogando"
    finalizado = "Finalizado"
    pausado = "Pausado"
    abandonado = "Abandonado"

class TipoCadastro(str, Enum):
    manual = "Manual"
    steam = "Steam"

class GameBase(BaseModel):

    appid: int
    name: str
    playtime_forever: int = 0
    img_icon_url: Optional[str] = None
    data_compra: Optional[str] = None
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    publisher: Optional[str] = None
    descricao: Optional[str] = None
    interesse: Optional[str] = "Médio"
    status: GameStatus = GameStatus.nao_iniciado
    tipo_cadastro: TipoCadastro = TipoCadastro.steam
    nota_pessoal: Optional[int] = 0
    horas_jogadas: int = 0
    conquistas_totais: int = 0
    conquistas_obtidas: int = 0

    class Config:
        use_enum_values = True

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    interesse: Optional[GameStatus] = None
    status: Optional[GameStatus] = None
    nota_pessoal: Optional[int] = None

class Game(GameBase):

    class Config:
        from_attributes = True
        use_enum_values = True