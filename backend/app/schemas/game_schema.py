# app/schemas/game_schema.py
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
    img_logo_url: Optional[str] = None

    data_compra: Optional[str] = None
    loja: Optional[str] = None
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    publisher: Optional[str] = None
    descricao: Optional[str] = None
    interesse: Optional[str] = "Médio"
    status: GameStatus = GameStatus.nao_iniciado
    tipo_cadastro: TipoCadastro = TipoCadastro.steam
    nota_pessoal: Optional[int] = None
    horas_jogadas: int = 0
    conquistas_totais: int = 0
    conquistas_obtidas: int = 0

    class Config:
        use_enum_values = True

class GameCreate(GameBase):
    """ Schema para adicionar um novo jogo (via Steam ou Manual) """
    pass

class GameUpdate(BaseModel):
    interesse: Optional[GameStatus] = None
    status: Optional[GameStatus] = None
    nota_pessoal: Optional[int] = None

class Game(GameBase):
    """ Schema para ler um Jogo do banco """
    # O appid será usado como ID do documento, então não precisamos de um 'id' separado

    class Config:
        from_attributes = True
        use_enum_values = True