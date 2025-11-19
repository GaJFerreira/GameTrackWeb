# app/schemas/game_schema.py
from pydantic import BaseModel
from typing import Optional, Dict, Any
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
    # --- Dados Básicos (API de Usuário) ---
    appid: int
    name: str
    playtime_forever: int = 0
    img_icon_url: Optional[str] = None
    img_logo_url: Optional[str] = None

    # --- Dados Customizados do Usuário ---
    data_compra: Optional[str] = None
    tipo_cadastro: TipoCadastro = TipoCadastro.steam
    interesse: Optional[str] = "Médio"
    status: GameStatus = GameStatus.nao_iniciado
    nota_pessoal: Optional[int] = 0
    horas_jogadas: int = 0 

    conquistas_totais: int = 0
    conquistas_obtidas: int = 0

    # --- Dados Enriquecidos (Loja Steam - Campos Específicos) ---
    genero: Optional[str] = None
    desenvolvedor: Optional[str] = None
    publisher: Optional[str] = None
    descricao: Optional[str] = None   
    descricao_completa: Optional[str] = None
    sobre: Optional[str] = None
    linguas: Optional[str] = None
    requisitos: Optional[Dict[str, Any]] = None
    preco: Optional[Dict[str, Any]] = None
    
    categorias: Optional[str] = None
    data_lancamento: Optional[str] = None
    metacritic: Optional[int] = None

    # --- CAMPO CORINGA (O "Salva Tudo") ---
    # Aqui guardamos o JSON bruto completo da loja para garantir que nada se perca
    dados_loja: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True
        extra = "ignore" 

class GameCreate(GameBase):
    pass

class GameUpdate(BaseModel):
    
    interesse: Optional[GameStatus] = None
    status: Optional[GameStatus] = None
    nota_pessoal: Optional[int] = None


class Game(GameBase):
    # O appid é usado como ID no banco
    
    class Config:
        from_attributes = True
        use_enum_values = True